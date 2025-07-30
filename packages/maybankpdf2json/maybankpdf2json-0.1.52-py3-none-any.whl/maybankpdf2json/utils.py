from datetime import datetime
import io
from typing import TypedDict, List, Optional, Any
import numpy as np
import pdfplumber
import re

START_ENTRY = "BEGINNING BALANCE"
END_ENTRY = "TOTAL DEBIT"
NOTE_START_ENTRY = "Perhation / Note"
NOTE_END_ENTRY = (
    "ENTRY DATE TRANSACTION DESCRIPTION TRANSACTION AMOUNT STATEMENT BALANCE"
)
EXCLUDE_ITEMS = ["TOTAL CREDIT", "TOTAL DEBIT", "ENDING BALANCE"]


class Output(TypedDict):
    date: str
    desc: str
    bal: float
    trans: float


def parse_acc_value(value: str) -> float:
    """
    Parses a string representing an account value and returns it as a float.
    Handles trailing '-' for negative and '+' for positive values.

    Args:
        value (str): The string value to parse.
    Returns:
        float: The parsed float value.
    """
    value = value.replace(",", "")
    if value.endswith("-"):
        return -float(value[:-1])
    elif value.endswith("+"):
        return float(value[:-1])
    else:
        return float(value)


def is_valid_date(date_str: str) -> bool:
    """
    Checks if a string is a valid date in the format 'dd/mm/yy'.

    Args:
        date_str (str): The date string to validate.
    Returns:
        bool: True if valid, False otherwise.
    """
    try:
        datetime.strptime(date_str, "%d/%m/%y")
        return True
    except ValueError:
        return False


def get_mapped_data(arr: List[str]) -> List[Output]:
    """
    Maps raw text lines to structured Output dictionaries.

    Args:
        arr (List[str]): List of text lines from the PDF.
    Returns:
        List[Output]: List of structured transaction records.
    """
    narr: List[Output] = []
    i = 0
    while i < len(arr):
        current = arr[i]
        splitted = current.split()
        obj: Output = {"desc": "", "bal": 0, "trans": 0, "date": ""}
        if i != 0 and (not (is_valid_date(splitted[0]))):
            i += 1
            continue
        elif i == 0:
            obj["desc"] = " ".join(splitted[0:2])
            obj["bal"] = parse_acc_value(splitted[2])
            narr.append(obj)
        elif is_valid_date(splitted[0]):
            obj["date"] = splitted[0]
            obj["trans"] = parse_acc_value(splitted[-2])
            obj["bal"] = parse_acc_value(splitted[-1])
            obj["desc"] = " ".join(splitted[1:-2])
            i += 1
            while i < len(arr) and not is_valid_date(arr[i].split()[0]):
                obj["desc"] = obj["desc"] + " " + " ".join(arr[i].split())
                i += 1
            narr.append(obj)
            continue
        i += 1
    narr[0]["date"] = datetime.strptime(narr[2]["date"], "%d/%m/%y").strftime(
        "01/%m/%y"
    )
    return narr


def expand_ranges(arr: List[int]) -> List[int]:
    """
    Expands a list of index pairs into a flat list of indices.

    Args:
        arr (List[int]): List of indices (start, end, ...).
    Returns:
        List[int]: Expanded list of indices.
    """
    expanded: List[int] = []
    for ar in range(0, len(arr), 2):
        f = arr[ar]
        s = arr[ar + 1]
        for i in range(f, s + 1):
            expanded.append(i)
    return expanded


def get_filtered_data(arr: List[str]) -> List[str]:
    """
    Filters out non-transaction lines and note sections from the PDF text lines.

    Args:
        arr (List[str]): List of text lines from the PDF.
    Returns:
        List[str]: Filtered list of transaction lines.
    """
    indexes = [0, len(arr)]
    for i, x in enumerate(arr):
        if x.startswith(START_ENTRY):
            indexes[0] = i
        elif x.startswith(END_ENTRY):
            indexes[1] = i + 1
            break
    filtered = arr[indexes[0] : indexes[1]]
    temp = np.array(filtered)
    notes_indices = np.where(
        np.char.startswith(temp, NOTE_START_ENTRY)
        | np.char.startswith(temp, NOTE_END_ENTRY)
    )[0].tolist()
    expanded = expand_ranges(notes_indices)
    narr: List[str] = []
    for i, v in enumerate(temp):
        if i not in expanded and (
            not any(v.startswith(item) for item in EXCLUDE_ITEMS)
        ):
            narr.append(v)
    return narr


def read(buf: io.BufferedReader, pwd: Optional[str] = None) -> List[str]:
    """
    Reads text lines from a PDF file buffer using pdfplumber.

    Args:
        buf (io.BufferedReader): The PDF file buffer.
        pwd (Optional[str]): The password for the PDF file.
    Returns:
        List[str]: List of text lines from all pages.
    """
    buf.seek(0)
    with pdfplumber.open(buf, password=pwd) as pdf:
        return [
            txt
            for pg, page in enumerate(pdf.pages)
            for txt in page.extract_text().split("\n")
        ]


def convert_to_json(s: Any) -> List[Output]:
    """
    Converts a PDF statement to a list of transaction records in JSON format.

    Args:
        s (MaybankPdf2Json): An object with a 'buffer' attribute and optional 'pwd' attribute.
    Returns:
        List[Output]: List of transaction records.
    """
    all_lines = read(s.buffer, pwd=getattr(s, "pwd", None))
    d = get_filtered_data(all_lines)
    return get_mapped_data(d)


def extract_account_and_date(lines) -> dict:
    """
    Extracts the account number and statement date from the provided lines.
    Returns a dict with string or None values.
    """
    account_number = None
    statement_date = None

    for line in lines:
        # Look for account number pattern (e.g., 162021-851156)
        account_match = re.search(r"\b\d{6}-\d{6}\b", line)
        if account_match:
            account_number = account_match.group()

        # Look for date pattern (e.g., 30/09/24)
        date_match = re.search(r"\b\d{2}/\d{2}/\d{2}\b", line)
        if date_match:
            raw_date = date_match.group()
            try:
                # Always return as string in 'dd/mm/yy' format
                dt = datetime.strptime(raw_date, "%d/%m/%y")
                statement_date = dt.strftime("%d/%m/%y")
            except ValueError:
                pass

    return {"account_number": account_number, "statement_date": statement_date}


def convert_to_jsonV2(s: Any) -> dict:
    """
    Converts a PDF statement

    Args:
        s (MaybankPdf2Json): An object with a 'buffer' attribute and optional 'pwd' attribute.
    Returns:
        {
            "account_number": str,
            "statement_date": str,
            "transactions": List[Output]
        }
    """
    all_lines = read(s.buffer, pwd=getattr(s, "pwd", None))
    d = get_filtered_data(all_lines)
    t = get_mapped_data(d)
    o = extract_account_and_date(all_lines)
    return {
        "account_number": o["account_number"],
        "statement_date": o["statement_date"],
        "transactions": t,
    }
