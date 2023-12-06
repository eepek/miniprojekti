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
KEY_DOES_NOT_EXIST_ERROR = "Key does not exist"
INVALID_REFERENCE_TYPE_ERROR = "Invalid reference type"
KEY_ALREADY_EXISTS_ERROR = "Key already exists"

INPROCEEDINGS_KEYS = ["title", "author", "booktitle", "year",
                      "editor", "volume", "series", "pages", "address",
                      "month", "note"]
INPROCEEDINGS_MANDATORY_KEYS = set(["author", "title", "booktitle", "year"])

TECHREPORT_KEYS = ["title", "author", "institution", "year", "type", "number",
                   "address", "month", "note", "annote"]
TECHREPORT_MANDATORY_KEYS = set(["title", "author", "institution", "year"])

ARTICLE_KEYS = ["title", "author", "journal", "year", "volume", "number", "pages", "month", "note"]
ARTICLE_MANDATORY_KEYS = set(["title", "author", "journal", "year"])

PHD_KEYS = [ "author", "title", "school", "year", "type", "address", "month", "note"]
PHD_MANDATORY_KEYS = set([ "author", "title", "school", "year"])

NUMBER_KEYS = set(["year", "volume"])
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
