import io
from typing import List
from .utils import Output, convert_to_json, convert_to_jsonV2


class MaybankPdf2Json:
    """
    Extracts transaction data from a Maybank PDF statement and converts it to JSON.

    Attributes:
        buffer (io.BufferedReader): The PDF file buffer.
        pwd (str): The password for the PDF file.
    """

    def __init__(self, buffer: io.BufferedReader, pwd: str) -> None:
        """
        Initializes the MaybankPdf2Json extractor.

        Args:
            buffer (io.BufferedReader): The PDF file buffer.
            pwd (str): The password for the PDF file.
        """
        self.buffer: io.BufferedReader = buffer
        self.pwd: str = pwd

    def json(self) -> List[Output]:
        """
        Extracts and returns the transaction data as a list of dictionaries.

        Returns:
            List[Dict[str, Any]]: List of transaction records with keys 'date', 'desc', 'bal', and 'trans'.
        """
        return convert_to_json(self)

    def jsonV2(self) -> dict:
        """
        Extracts and returns the transaction data as a dictionary.

        Returns:
            dict: Dictionary containing the account number, date, and transaction records.
        """
        return convert_to_jsonV2(self)
