"""Module for the library class for the Robot framework."""
from repositories.reference_repository import ReferenceRepository


class AppLibrary:
    """Library class for the Robot framework."""
    def __init__(self):
        self._ref_repository = ReferenceRepository()

    def empty_all_tables(self):
        """embty db"""
        self._ref_repository.empty_all_tables()
