"""Unittests for reference_services module"""
import unittest
import pytest
from repositories.reference_repository import ReferenceRepository
from services.reference_services import ReferenceServices
from entities.reference import ReferenceType
from constants import MISSING_FIELD_ERROR, YEAR_FORMAT_ERROR, \
    MONTH_FORMAT_ERROR, VOLUME_FORMAT_ERROR, PAGES_FORMAT_ERROR, \
    EXTRA_KEYS_ERROR, ROOT_DIR, KEY_ALREADY_EXISTS_ERROR
from tests.testcases import INPRO_VALID1


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
            "title": "On theory of relativity",
            "author": "Smith, John",
            "booktitle": "Proceedings of the Conference",
            "year": 2023,
            "editor": "Doe, Jane",
            "volume": 1,
            "series": "Proceedings in Science",
            "pages": "123--145",
            "address": "Helsinki",
            "month": "June",
            "note": "test"
        }

    def test_all_valid_fields_does_not_raise_error(self):
        """No ValueError with all valid fields"""
        self.ref_services.create_reference(
            ReferenceType.INPROCEEDINGS, self.inpro)

    def test_all_valid_fields_with_manual_key_does_not_raise_error(self):
        """No ValueError with all valid fields"""
        self.ref_services.create_reference(
            ReferenceType.INPROCEEDINGS, self.inpro, manual_key="Unique25")

    def test_alternative_month_format_does_not_raise_error(self):
        """No Value error when month is standard English abbreviation"""
        self.inpro["month"] = "jun"
        self.ref_services.create_reference(
            ReferenceType.INPROCEEDINGS, self.inpro)

    def test_alternative_numerical_month_format_does_not_raise_error(self):
        """No Value error when month is in numerical format"""
        self.inpro["month"] = 6
        self.ref_services.create_reference(
            ReferenceType.INPROCEEDINGS, self.inpro)

    def test_single_page_does_not_raise_error(self):
        """Tests with single page article, no ValueError"""
        self.inpro["pages"] = "44"
        self.ref_services.create_reference(
            ReferenceType.INPROCEEDINGS, self.inpro)

    def test_missing_title_raises_error(self):
        """Test Value error with missing field title"""
        self.inpro["title"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(
                ReferenceType.INPROCEEDINGS, self.inpro)

    def test_missing_booktitle_raises_error(self):
        """Test Value error with missing field booktitletitle"""
        self.inpro["booktitle"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(
                ReferenceType.INPROCEEDINGS, self.inpro)

    def test_missing_year_raises_error(self):
        """Test Value error with missing field year"""
        self.inpro["year"] = None
        with pytest.raises(ValueError,
                           match=MISSING_FIELD_ERROR):
            self.ref_services.create_reference(
                ReferenceType.INPROCEEDINGS, self.inpro)

    def test_valid_month_does_not_raise_error(self):
        self.ref_services.validate_field("month", "january")

    def test_invalid_month_raises_error(self):
        """Test Value error with invalid month format"""
        with pytest.raises(ValueError, match=MONTH_FORMAT_ERROR):
            self.ref_services.validate_field("month", "tammikuu")

    def test_invalid_year_raises_error(self):
        """Test Value error with invalid year format"""
        with pytest.raises(ValueError, match=YEAR_FORMAT_ERROR):
            self.ref_services.validate_field("year", 21)

    def test_valid_volume_does_not_raise_error(self):
        self.ref_services.validate_field("volume", str(1))

    def test_invalid_volume_raises_error(self):
        """Test Value error with invalid volume format"""
        with pytest.raises(ValueError, match=VOLUME_FORMAT_ERROR):
            self.ref_services.validate_field("volume", "VolumeX")

    def test_valid_pages_does_not_raise_error(self):
        self.ref_services.validate_field("pages", str(11))

    def test_invalid_pages_raises_error(self):
        """Test Value error with invalid pages format"""
        with pytest.raises(ValueError, match=PAGES_FORMAT_ERROR):
            self.ref_services.validate_field("pages", "from 2 to 32")

    def test_extra_keys_raises_error(self):
        """Test Value error with invalid pages format"""
        self.inpro["extrafiled"] = "foo"
        with pytest.raises(ValueError, match=EXTRA_KEYS_ERROR):
            self.ref_services.create_reference(
                ReferenceType.INPROCEEDINGS, self.inpro)

    def test_only_mandatory_fields_passes(self):
        """Tests that reference with only mandatory fields doesn't cause Value Error"""
        inpro = {
            "title": "Title",
            "author": "Ghost, Writer",
            "booktitle": "Proceedings of the Conference",
            "year": 2023
        }
        self.ref_services.create_reference(ReferenceType.INPROCEEDINGS, inpro)

    def test_bibtex_key_generator(self):
        """ Test for bibtex key constructing"""
        inpro = {
            "title": "How to Google",
            "author": "Alphabet Inc.",
            "booktitle": "Proceedings of the Conference",
            "year": 2023
        }
        self.ref_services.create_reference(ReferenceType.INPROCEEDINGS, inpro)
        key1 = self.ref_services.construct_bibtex_key("Powers", 2023)
        key2 = self.ref_services.construct_bibtex_key("Powersson", 1995)
        key3 = self.ref_services.construct_bibtex_key("Alphabet Inc.", 2023)
        self.assertEqual(key1, "powers23")
        self.assertEqual(key2, "powerss95")
        self.assertEqual(key3, "alphabe23_1")

    def test_filtering_references(self):
        """Test for filtering references"""
        self.inpro["author"] = "Reed, Lou"
        self.inpro["title"] = "Walk on the Wild Side"
        self.inpro["year"] = 1972
        self.ref_services.create_reference(
            ReferenceType.INPROCEEDINGS, self.inpro)
        refs = self.repository.load_all()
        print(refs)
        res = self.ref_services.filter_references(refs, 0, "Reed, Lou")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 0, "lou")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 0, "rEed")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 0, "Mankell")
        self.assertEqual(len(res), 0)
        res = self.ref_services.filter_references(refs, 2, "Walk")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 2, "alk")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 2, "wild")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 2, "ON THE WILD")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 2, "Perfect day")
        self.assertEqual(len(res), 0)
        res = self.ref_services.filter_references(refs, 1, "1972")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 1, "72")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 1, "197")
        self.assertEqual(len(res), 1)
        res = self.ref_services.filter_references(refs, 1, "1973")
        self.assertEqual(len(res), 0)

    def test_add_valid_from_file_no_errors(self):
        """Tests that adding valid references from file does not cause errors
        and unsupported types are just passed"""
        res = self.ref_services.add_from_file("data/test_build.bib")
        self.assertEqual(len(res), 0)

    def test_add_extra_fields_type_returns_error(self):
        """Tests that adding valid references from file does not cause errors"""
        res = self.ref_services.add_from_file("data/errors.bib")
        self.assertEqual(len(res), 2)
        self.assertEqual(
            str(res[0][1]), EXTRA_KEYS_ERROR)
        self.assertEqual(
            str(res[1][1]), KEY_ALREADY_EXISTS_ERROR)

    def test_delete_reference_works(self):
        """Tests that delete_reference reduces reference count by one"""
        self.repository.empty_all_tables()
        self.ref_services.add_from_file("data/test_build.bib")
        orig_refs = self.repository.load_all()
        orig_length = len(orig_refs)
        self.ref_services.delete_reference(orig_refs[0].key)
        new_length = len(self.repository.load_all())
        self.assertEqual(orig_length, new_length+1)
