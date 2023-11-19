"""Unittests for reference_services module"""
import unittest
import pytest
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from constants import MISSING_FIELD_ERROR, YEAR_FORMAT_ERROR, \
    MONTH_FORMAT_ERROR, VOLUME_FORMAT_ERROR, PAGES_FORMAT_ERROR, EXTRA_KEYS_ERROR


class TestReferenceServices(unittest.TestCase):
    """Unittests for reference_services module"""

    def setUp(self):
        """Creates ReferenceRepository and ReferenceServices objects

        Create dictionary with all valid fields corresponding to 
        Reference class object
        """
        self.repository = ReferenceRepository()
        self.ref_services = ReferenceServices(self.repository)

        self.inpro = {
            "key": "dockey12",
            "title": "Title",
            "author": "Ghost Writer",
            "booktitle": "Proceedings of the Conference",
            "year": 2023,
            "editor": "Super Editor",
            "volume": "1",
            "series": "Proceedings in Science",
            "pages": "123-145",
            "address": "Helsinki",
            "month": "June",
            "note": "test"
        }

    def test_all_valid_fields_does_not_raise_error(self):
        """No ValueError with all valid fields"""
        self.ref_services.create_reference(self.inpro)

    def test_alternative_month_format_does_not_raise_error(self):
        """No Value error when month is standard English abbreviation"""
        self.inpro["month"] = "jun"
        self.ref_services.create_reference(self.inpro)

    def test_alternative_numerical_month_format_does_not_raise_error(self):
        """No Value error when month is in numerical format"""
        self.inpro["month"] = 6
        self.ref_services.create_reference(self.inpro)

    def test_single_page_does_not_raise_error(self):
        """Tests with single page article, no ValueError"""
        self.inpro["pages"] = "44"
        self.ref_services.create_reference(self.inpro)

    def test_missing_key_raises_error(self):
        """Test Value error with missing field key"""
        self.inpro["key"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_missing_title_raises_error(self):
        """Test Value error with missing field title"""
        self.inpro["title"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_missing_author_raises_error(self):
        """Test Value error with missing field author"""
        self.inpro["author"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_missing_booktitle_raises_error(self):
        """Test Value error with missing field booktitletitle"""
        self.inpro["booktitle"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_missing_year_raises_error(self):
        """Test Value error with missing field year"""
        self.inpro["year"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_invalid_month_raises_error(self):
        """Test Value error with invalid month format"""
        self.inpro["month"] = "Tammikuu"
        with pytest.raises(ValueError, match=MONTH_FORMAT_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_invalid_year_raises_error(self):
        """Test Value error with invalid year format"""
        self.inpro["year"] = 21
        with pytest.raises(ValueError, match=YEAR_FORMAT_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_invalid_volume_raises_error(self):
        """Test Value error with invalid volume format"""
        self.inpro["volume"] = "volumeX"
        with pytest.raises(ValueError, match=VOLUME_FORMAT_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_invalid_pages_raises_error(self):
        """Test Value error with invalid pages format"""
        self.inpro["pages"] = "from 2 to 32"
        with pytest.raises(ValueError, match=PAGES_FORMAT_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_extra_keys_raises_error(self):
        """Test Value error with invalid pages format"""
        self.inpro["extrafiled"] = "foo"
        with pytest.raises(ValueError, match=EXTRA_KEYS_ERROR):
            self.ref_services.create_reference(self.inpro)

    def test_only_mandatory_fields_passes(self):
        inpro = {
            "key": "dockey12",
            "title": "Title",
            "author": "Ghost Writer",
            "booktitle": "Proceedings of the Conference",
            "year": 2023,
            "editor": "",
            "volume": "",
            "series": "",
            "pages": "",
            "address": "",
            "month": "",
            "note": ""
        }
        self.ref_services.create_reference(inpro)
