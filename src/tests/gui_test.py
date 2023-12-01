""" Unit tests for the GUI module. """
from unittest.mock import MagicMock
from gui import GUI
from unittest import IsolatedAsyncioTestCase
from entities.reference import Reference
from repositories.reference_repository import ReferenceRepository, ReferenceType
from services.reference_services import ReferenceServices


class TestGUI(IsolatedAsyncioTestCase):
    def setUp(self):
        self.ref_repository = ReferenceRepository()
        self.ref_repository.empty_all_tables()
        self.ref_services = ReferenceServices(self.ref_repository)
        file_dialog = MagicMock()
        self.gui = GUI(self.ref_repository, self.ref_services, file_dialog)
        self.inpro_all = Reference(ReferenceType.INPROCEEDINGS, "Key123", {
            "title": "Inproceeding name",
            "author": "Mikki Hiiri",
            "booktitle": "Proceedings of the Conference",
            "year": 2023,
            "volume": 1,
            "pages": "123-145",
            "address": "Helsinki",
            "month": "June",
            "note": "test"
        })


    async def test_shutting_down(self):
        """Test shutting down, app return code is 0 when exiting with no errors"""
        async with self.gui.run_test() as gui:
            self.assertEqual(self.gui.return_code, None)
            await gui.press("q")
            await gui.press("n")
            await gui.press("q")
            await gui.press("y")
            self.assertEqual(self.gui.return_code, 0)
    
    async def test_shutting_down_with_button(self):
        """Test shutting down, app return code is 0 when exiting with no errors"""
        async with self.gui.run_test() as gui:
            self.assertEqual(self.gui.return_code, None)
            await gui.press("q")
            await gui.click("#no")
            await gui.press("q")
            await gui.click("#yes")
            self.assertEqual(self.gui.return_code, 0)
    
    async def test_shutting_down_with_tab_and_enter(self):
        """Test shutting down, app return code is 0 when exiting with no errors"""
        async with self.gui.run_test() as gui:
            self.assertEqual(self.gui.return_code, None)
            await gui.press("q")
            await gui.press("tab")
            await gui.press("enter")
            await gui.press("q")
            await gui.press("enter")
            self.assertEqual(self.gui.return_code, 0)

    
    async def test_adding_reference_screen_and_backtracking_to_default_view(self):
        """Test for accessing add_reference screen"""
        async with self.gui.run_test() as gui:
            await gui.press("a")
            self.assertEqual(str(self.gui.screen), "AddReference()")
            await gui.press("o")
            self.assertEqual(str(self.gui.screen), "ReferenceForm()")
            await gui.press("escape")
            self.assertEqual(str(self.gui.screen), "Screen(id='_default')")
    
    async def test_add_reference(self):
        """Test for adding a reference"""
        self.ref_services.create_reference = MagicMock()
        async with self.gui.run_test() as gui:
            await gui.press("a")
            await gui.press("o")
            await gui.press("T", "i", "t", "l", "e")
            await gui.press("tab")
            await gui.press("D", "o", "e", ",", " ", "J", "o", "h", "n")
            await gui.press("tab")
            await gui.press("M", "I", "T") 
            await gui.press("tab")
            await gui.press("1", "9", "9", "9")
            await gui.press("tab")
            await gui.press("tab")  
            await gui.press("10")
            await gui.press("tab")
            await gui.press("H", "e", "l", "s", "i", "n", "k", "i")
            await gui.press("tab")
            await gui.press("tab")
            await gui.press("tab")
            await gui.press("tab")
            await gui.press("tab")
            await gui.press("ctrl+j") 
            self.ref_services.create_reference.assert_called()

    async def test_add_reference_cancelled_does_not_call_reff_rep(self):
        """test for cancelling add reference"""
        self.ref_services.create_reference = MagicMock()
        async with self.gui.run_test() as gui:
            await gui.press("a")
            await gui.press("o")
            for _ in range(12):
                await gui.press("tab")
            await gui.click("#cancel")
            await gui.press("o")
            for _ in range(12):
                await gui.press("tab")
            await gui.press("enter")
            self.ref_services.create_reference.assert_not_called()


    async def test_viewing_single_reference_and_backtracking_to_default_view(self):
        """Test for accessing view_reference screen"""
        self.ref_repository.save(self.inpro_all)
        async with self.gui.run_test() as gui:
            await gui.press("l")
            self.assertEqual(str(self.gui.screen), "ListKeys()")
            await gui.press("ctrl+j")
            self.assertEqual(str(self.gui.screen), "SingleReference()")
            await gui.press("escape")
            self.assertEqual(str(self.gui.screen), "Screen(id='_default')")

    async def test_deleting_reference(self):
        """Test for deleting a reference"""
        self.ref_repository.save(self.inpro_all)
        self.ref_services.delete_reference = MagicMock()
        async with self.gui.run_test() as gui:
            await gui.press("l")
            await gui.press("ctrl+j")
            await gui.press("d")
            await gui.press("n")
            await gui.press("d")
            await gui.press("y")
            await gui.press("enter")
            self.ref_services.delete_reference.assert_called()
    
    async def test_deleting_reference_cancelled(self):
        """Test for deleting a reference"""
        self.ref_repository.save(self.inpro_all)
        self.ref_services.delete_reference = MagicMock()
        async with self.gui.run_test() as gui:
            await gui.press("l")
            await gui.press("ctrl+j")
            await gui.press("d")
            await gui.click("#no")
            self.ref_services.delete_reference.assert_not_called()

    async def test_show_all_references_in_bibtex(self):
        """Test for showing all references"""
        self.ref_repository.save(self.inpro_all)
        async with self.gui.run_test() as gui:
            await gui.press("s")
            self.assertEqual(str(self.gui.screen), "ShowAll()")
            await gui.press("escape")
            self.assertEqual(str(self.gui.screen), "Screen(id='_default')")