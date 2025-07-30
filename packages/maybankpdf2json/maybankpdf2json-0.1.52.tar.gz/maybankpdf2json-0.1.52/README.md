# Maybank PDF Account Statement to JSON

This package provides functionality to extract and process data from Maybank account statement PDFs. It allows users to read PDF files and extract json data from them.

## Installation

To install the package, clone the repository and run the following command:

```
pip install maybankpdf2json
```

## Usage

Here is a simple example of how to use the package to extract data from a Maybank PDF statement:

```python
import os
from maybankpdf2json import MaybankPdf2Json

# Path to your PDF file and its password
example_path = os.path.join(os.path.dirname(__file__), "test.pdf")
example_password = "12345"  # Replace with your actual PDF password

with open(example_path, "rb") as f:
    extractor = MaybankPdf2Json(f, example_password)
    data = extractor.json()
    print(data)

    # Output example:
    # [
    #   {
    #     "date": "01/01/2024",
    #     "desc": "Deposit from client",
    #     "trans": 50.0,
    #     "bal": 1050.0
    #   },
    #   {
    #     "date": "02/01/2024",
    #     "desc": "Purchase - Office Supplies",
    #     "trans": -20.0,
    #     "bal": 1030.0
    #   }
    # ]
```

## Testing

To run the tests, navigate to the project directory and execute:

```
pytest tests/
```

## Makefile Usage

This project includes a `Makefile` with helpful commands:

- To run tests:
  ```sh
  make test
  ```
- To build and release the package (requires proper credentials):
  ```sh
  make release
  ```

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
