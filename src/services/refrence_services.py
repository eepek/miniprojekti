"""Module consisting on Reference Serices class """
import re
from repositories.reference_repository import ReferenceRepository
from entities.reference import Inproceedings
from constants import MISSING_FIELD_ERROR, YEAR_FORMAT_ERROR, MONTH_FORMAT_ERROR, \
    VOLUME_FORMAT_ERROR, PAGES_FORMAT_ERROR, EXTRA_KEYS_ERROR


class ReferenceServices:
    """Services for references
    Attributes:
      _refence_repository: Reference repository object

    """

    def __init__(self, reference_repository: ReferenceRepository) -> None:
        """Constructor initialises self._reference repository 
        from reference repository object given as parameter
        """
        self._reference_repository = reference_repository

    def create_reference(self, reference):
        """Validates reference dictionary fields
        generates Reference object and
        and calls reference_repository save method
        Text type fields are only validated for existence not for contents
        Raises ValueError in case of invalid fields
        Converst Reference Object into dictionary before calling reference_repository.save()

        Args:
          reference (Reference): Refence object
        """

        ref_keys = reference.keys()
        allowed_keys = ["key", "title", "author", "booktitle", "year",
                        "editor", "volume", "series", "pages", "address",
                        "month", "note"]

        if not all(item in allowed_keys for item in ref_keys):
            raise ValueError(EXTRA_KEYS_ERROR)

        if not reference["key"] or not reference["title"] or not reference["author"] \
                or not reference["booktitle"] or not reference["year"]:
            raise ValueError(MISSING_FIELD_ERROR)

        year_pattern = r"\d{4}"
        if not re.match(year_pattern, str(reference["year"])):
            raise ValueError(YEAR_FORMAT_ERROR)

        month_pattern = re.compile(
            r'^(0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?| \
      jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)$',
            re.IGNORECASE)
        if not re.match(month_pattern, str(reference["month"])):
            raise ValueError(MONTH_FORMAT_ERROR)

        regex = r"^\d+$"
        if not re.match(regex, reference["volume"]):
            raise ValueError(VOLUME_FORMAT_ERROR)

        regex = r"^\d+([-]\d+)?$"
        if not re.match(regex, reference["pages"]):
            raise ValueError(PAGES_FORMAT_ERROR)

        ref_object = Inproceedings(**reference)
        reference_dict = vars(ref_object)
        self._reference_repository.save(reference_dict)
