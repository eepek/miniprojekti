"""Module for constants"""

MISSING_FIELD_ERROR = "Fields: key, title, author, booktitle and year are mandatory fields"
YEAR_FORMAT_ERROR = "Year must be YYYY"
MONTH_FORMAT_ERROR = "Month is not valid"
VOLUME_FORMAT_ERROR = "Volume needs to be number"
PAGES_FORMAT_ERROR = "Page numbers are not valid"
EXTRA_KEYS_ERROR = "Input contains extra fields"
INPROCEEDINGS_KEYS = ["key", "title", "author", "booktitle", "year",
                      "editor", "volume", "series", "pages", "address",
                      "month", "note"]
