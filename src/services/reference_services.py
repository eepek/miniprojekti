"""Module consisting on Reference Serices class """
import re
from repositories.reference_repository import ReferenceRepository
from entities.reference import Inproceedings
from constants import MISSING_FIELD_ERROR, YEAR_FORMAT_ERROR, MONTH_FORMAT_ERROR, \
    VOLUME_FORMAT_ERROR, PAGES_FORMAT_ERROR, EXTRA_KEYS_ERROR, INPROCEEDINGS_KEYS


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
        Converst Reference Object into dictionary before calling reference_repository.save()

        Args:
          reference (Reference): Refence object
        """

        ref_keys = reference.keys()

        if not all(item in INPROCEEDINGS_KEYS for item in ref_keys):
            raise ValueError(EXTRA_KEYS_ERROR)

        if not reference["key"] or not reference["title"] or not reference["author"] \
                or not reference["booktitle"] or not reference["year"]:
            raise ValueError(MISSING_FIELD_ERROR)

        ref_object = Inproceedings(**reference)
        self._reference_repository.save(ref_object)


    def validate_field(self, field, value):
        """Validate the user input for a specific field.
            Raises ValueError in case of invalid fields
        Args:
            field (str): Field to evaluate
            value (int/str): Value to be evaluated
        Raises:
            ValueError
        """

        if field == "year":
            year_pattern = r"\d{4}"
            if not re.match(year_pattern, str(value)):
                raise ValueError(YEAR_FORMAT_ERROR)
        elif field == "month":
            month_pattern = re.compile(
                r'^(0?[1-9]|1[0-2]|jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?| \
                jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)$',
                re.IGNORECASE)
            if not re.match(month_pattern, str(value)):
                raise ValueError(MONTH_FORMAT_ERROR)
        elif field == "volume":
            regex = r"^\d+$"
            if not re.match(regex, value):
                raise ValueError(VOLUME_FORMAT_ERROR)
        elif field == "pages":
            regex = r"^\d+([-]\d+)?$"
            if not re.match(regex, value):
                raise ValueError(PAGES_FORMAT_ERROR)
