"""Unittests for reference module"""
import unittest
import pytest
from entities.reference import Reference, ReferenceType
from constants import INPROCEEDINGS_KEYS, INPROCEEDINGS_MANDATORY_KEYS, TECHREPORT_KEYS, \
    TECHREPORT_MANDATORY_KEYS, ARTICLE_KEYS, ARTICLE_MANDATORY_KEYS, PHD_KEYS, \
    PHD_MANDATORY_KEYS
from tests.testcases import INPRO_SOME_FIELDS


class TestReference(unittest.TestCase):
    """Unittests for reference module"""

    def setUp(self):
        """Creating couple of Inproceedings class objects
        - One with all the optional parameters
        - One with only optional parameter "test"
        """
        self.ref = Reference(ReferenceType.INPROCEEDINGS,
                             "key1", {"title": "Test title"})
        self.inpro_some = INPRO_SOME_FIELDS

    def test_creating_object(self):
        """Testing for the correct instances"""
        self.assertIsInstance(self.ref, Reference)

    def test_set_inproceedings_parameters(self):
        """ Testing if optional parameters are set correctly
        - address and pages were not given as parameters to the consturctor
        - year should be found
        """
        self.assertNotIn("address", self.inpro_some.fields)
        self.assertNotIn("pages", self.inpro_some.fields)
        self.assertEqual(self.inpro_some.fields["year"], 1992)

    def test_none_fields_not_in_inproceedings_str(self):
        """ Testing for correct __str__ method output
        paramaters not set in the constructor should not be found
        in the return of str(self.inpro_some).
        Title and note should be in the string.
        """
        self.assertNotIn("volume", str(self.inpro_some))
        self.assertNotIn("pages", str(self.inpro_some))
        self.assertNotIn("address", str(self.inpro_some))
        self.assertNotIn("month", str(self.inpro_some))
        self.assertIn("title", str(self.inpro_some))
        self.assertIn("note", str(self.inpro_some))

        self.inpro_some.fields["note"] = None
        self.assertNotIn("note", str(self.inpro_some))

    def test_inproceedings_get_keys(self):
        inproceedings = ReferenceType("inproceedings")
        self.assertListEqual(inproceedings.get_keys(), INPROCEEDINGS_KEYS)
        self.assertSetEqual(inproceedings.get_mandatory_keys(),
                            INPROCEEDINGS_MANDATORY_KEYS)

    def test_techreport_get_keys(self):
        techreport = ReferenceType("techreport")
        self.assertListEqual(techreport.get_keys(), TECHREPORT_KEYS)
        self.assertSetEqual(techreport.get_mandatory_keys(),
                            TECHREPORT_MANDATORY_KEYS)

    def test_article_get_keys(self):
        techreport = ReferenceType("article")
        self.assertListEqual(techreport.get_keys(), ARTICLE_KEYS)
        self.assertSetEqual(techreport.get_mandatory_keys(),
                            ARTICLE_MANDATORY_KEYS)

    def test_phd_get_keys(self):
        techreport = ReferenceType("phd")
        self.assertListEqual(techreport.get_keys(), PHD_KEYS)
        self.assertSetEqual(techreport.get_mandatory_keys(),
                            PHD_MANDATORY_KEYS)

    def test_non_supported_raises_error(self):
        with pytest.raises(ValueError):
            techreport = ReferenceType("non-supported")
