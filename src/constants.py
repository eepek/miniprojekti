"""Module for constants"""
import os

MISSING_FIELD_ERROR = "Fields: key, title, author, booktitle and year are mandatory fields"
YEAR_FORMAT_ERROR = "Year must be YYYY"
MONTH_FORMAT_ERROR = "Month is not valid"
VOLUME_FORMAT_ERROR = "Volume needs to be number"
PAGES_FORMAT_ERROR = "Page numbers are not valid"
EXTRA_KEYS_ERROR = "Input contains extra fields"
FIELD_MANDATORY_ERROR = "Field is mandatory"
UNSUITABLE_COMMAND_ERROR = "Unsuitable command"

INPROCEEDINGS_KEYS = ["key", "title", "author", "booktitle", "year",
                      "editor", "volume", "series", "pages", "address",
                      "month", "note"]
INPROCEEDINGS_MANDATORY_KEYS = set(["key", "author", "title", "booktitle", "year"])
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
