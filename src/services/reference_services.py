"""Module consisting on Reference Serices class """
import re
from repositories.reference_repository import ReferenceRepository
from entities.reference import Reference, ReferenceType
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

    def create_reference(self, reference_type: ReferenceType, reference: dict):
        """Validates reference dictionary fields
        generates Reference object and
        and calls reference_repository save method
        Text type fields are only validated for existence not for contents

        Args:
          reference (Reference): Refence object
        """
        ref_keys = reference.keys()
        key = self.construct_bibtex_key(reference["author"], reference["year"])

        ref_type_keys = reference_type.get_keys()
        ref_type_mandatory_keys = reference_type.get_mandatory_keys()

        if not all(item in ref_type_keys for item in ref_keys):
            raise ValueError(EXTRA_KEYS_ERROR)

        if not all((m in reference and reference[m] is not None) for m in ref_type_mandatory_keys):
            raise ValueError(MISSING_FIELD_ERROR)

        ref_object = Reference(reference_type, key, reference)
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

    def construct_bibtex_key(self, author: str, year: int) -> str:
        """Algorithm for constucting bibtex -key.
        if author: Powers and year: 2023 -> powers23
        Expected author notation: {Lastname, Firstname}
        In case for company name etc. notation does not matter.
        Args:
            author (String): Reference author
            year (Int): Reference year
        """
        author = author.lower()
        if "," in author:
            author = author.split(",")[0]
        if " " in author:
            author = author.replace(" ", "")
        if len(author) >= 8:
            author = author[:7]
        year = str(year)[2:]
        bibtex_key = author + year
        previous = self._reference_repository.get_similar_key_count(bibtex_key)
        if previous > 0:
            bibtex_key = bibtex_key + "_" + str(previous)
        return bibtex_key

    def delete_reference(self, reference_key):
        """Calls for repository method to delete
        wanted reference from DB

        Args:
            reference_key (str): Key value of reference
            to be deleted
        """
        pass
