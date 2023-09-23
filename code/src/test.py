import unittest
import sys
from mainWindow import *
from user import *
from fileManager import *


class Test(unittest.TestCase):
	def test_load_file(self):
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test1.csv"
		boo, msg = self.user.import_file(self.file)
		self.expense = self.user.get_expenses()
		self.income = self.user.get_income()
		self.assertEqual(boo, True, "Not correct")
		self.assertEqual(round(sum([values[0] for values in self.expense.values()]), 2), -691.11, "Not matching expense")
		self.assertEqual(sum([values[0] for values in self.income.values()]), 819.33, "Not matching income")

	def test_load_file2(self):
		"""
		Test file with empty row
		:return:
		"""
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test2.csv"
		boo, msg = self.user.import_file(self.file)
		self.expense = self.user.get_expenses()
		self.income = self.user.get_income()
		self.assertEqual(boo, True, "Not correct")
		self.assertEqual(round(sum([values[0] for values in self.expense.values()]), 2), -237.07, "Not matching expense")
		self.assertEqual(sum([values[0] for values in self.income.values()]), 819.33, "Not matching income")

	def test_load_file_3(self):  # Test that file loads correctly with faulty file
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test_fault.csv"
		boolean, message = self.user.import_file(self.file)
		self.expenses = self.user.get_expenses()
		self.income = self.user.get_income()
		self.assertEqual(boolean, True, "Not correct")
		self.assertEqual(sum([values[0] for values in self.expenses.values()]), 0, "Not correct")
		self.assertEqual(sum([values[0] for values in self.income.values()]), 0, "Not correct")

	def test_load_file_4(self):  # Test that file loads correctly with multiple files
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test1.csv"
		boolean, message = self.user.import_file(self.file)
		self.file = "test2.csv"
		boolean, message = self.user.import_file(self.file)
		self.expenses = self.user.get_expenses()
		self.income = self.user.get_income()
		self.assertEqual(boolean, True, "Not correct")
		self.assertEqual(round(sum([values[0] for values in self.expenses.values()]), 2), -928.18, "Not matching expense")
		self.assertEqual(round(sum([values[0] for values in self.income.values()]), 2), 1638.66, "Not matching income")


	def test_set_important(self):  # Test that setting importance works properly
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test2.csv"
		boolean, message = self.user.import_file(self.file)
		self.user.set_importance("PRISMA ISO OMENA")  # Initially false
		self.expenses = self.user.get_expenses()
		self.assertEqual(self.expenses["PRISMA ISO OMENA"][1], True, "Not correct")

	def test_set_important_2(self):  # Test that unsetting importance works properly
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test1.csv"
		boolean, message = self.user.import_file(self.file)
		self.expenses = self.user.get_expenses()
		self.user.set_importance("UNIQLO GOTEBORG")
		self.user.unset_importance("UNIQLO GOTEBORG")
		self.assertEqual(self.expenses["UNIQLO GOTEBORG"][1], False, "Not correct")

	def test_delete_row(self):  # Test that deleting a row works properly
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test1.csv"
		boolean, message = self.user.import_file(self.file)
		self.user.delete_row(["TOKMANNI OY"])
		self.expenses = self.user.get_expenses()
		self.assertNotIn("TOKMANNI OY", self.expenses.keys(), "Not correct")
		self.assertIn("SAIGON CITY", self.expenses.keys(), "Not correct")

	def test_grouping(self):  # Test that grouping works properly
		self.reader = FileManager()
		self.user = User(self.reader)
		self.file = "test1.csv"
		boolean, message = self.user.import_file(self.file)
		self.user.set_grouping(["PRISMA ISO OMENA", "LIDL ESPOO-ISO-OMENA"], "Grocery")
		self.expenses = self.user.get_expenses()
		self.assertNotIn("PRISMA ISO OMENA", self.expenses.keys(), "Not correct")
		self.assertIn("Grocery", self.expenses.keys(), "Not correct")
		self.assertEqual(self.expenses["Grocery"][0], -14.39, "Not correct")

	def test_clean_window(self):  # Test that clearing window works properly
		app = QApplication(sys.argv)
		self.reader = FileManager()
		self.user = User(self.reader)
		self.mainWind = MainWindow(self.user)
		self.file = "test2.csv"
		boolean, message = self.user.import_file(self.file)
		self.expenses = self.mainWind.expenses
		self.income = self.mainWind.income
		self.mainWind.clear_window()
		self.assertEqual(sum([values[0] for values in self.expenses.values()]), 0, "Not correct")
		self.assertEqual(sum([values[0] for values in self.income.values()]), 0, "Not correct")
		app.quit()

	def test_multiple_functions(self):  # Test multiple operations simultaneously
		app = QApplication(sys.argv)
		self.reader = FileManager()
		self.user = User(self.reader)
		self.mainWind = MainWindow(self.user)
		self.file = "test1.csv"
		boolean, message = self.user.import_file(self.file)
		self.mainWind.file_imported = True
		message, success = self.mainWind.user.set_grouping(["XIN CHAO RESTAURANT", "QUALITEA TRIPLA"], "Food")
		self.expenses = self.mainWind.user.get_expenses()
		self.user.set_importance("UNIQLO GOTEBORG")
		self.user.set_importance("St Christophers")
		self.user.set_importance("RYANAIR     TDG26C0")
		self.user.set_importance("IQUNIX")
		self.user.set_importance("CLAS OHLSON 228 HELSINKI")
		self.user.unset_importance("Food")
		self.assertTrue(boolean)
		self.assertTrue(success)
		self.assertNotIn("XIN CHAO RESTAURANT", self.expenses.keys(), "Not correct")
		self.assertNotIn("QUALITEA TRIPLA", self.expenses.keys(), "Not correct")
		self.assertIn("Food", self.expenses.keys(), "Not correct")
		message, success = self.mainWind.user.set_grouping(["wrongname", "wrongname2"], "Title")
		self.assertFalse(success)
		message, success = self.mainWind.user.set_grouping(["Food"], "")
		self.assertEqual(message, "Set group title.", "Not correct")
		message, success = self.mainWind.user.set_grouping([], "Magazine")
		self.assertEqual(message, "No rows checked.", "Not correct")
		self.user.delete_row(["Food", "RYANAIR     TDG26C0"])
		self.expenses = self.user.get_expenses()
		self.assertNotIn("Food", self.expenses.keys(), "Not correct")
		self.assertNotIn("RYANAIR     TDG26C0", self.expenses.keys(), "Not correct")
		self.file = "/Users/mac/Aalto Courses/Y2/y2project/test_2.csv"
		boolean, message = self.user.import_file(self.file)
		self.mainWind.file_imported = True
		message, success = self.mainWind.user.set_grouping(
			["TOKMANNI OY", "OY GOLDEN CROP", "PRISMA ISO OMENA"], "Stores")
		self.expenses = self.mainWind.user.get_expenses()
		self.assertTrue(boolean)
		self.assertTrue(success)
		self.assertEqual(self.expenses["Stores"][0], -88.72, "Not correct")
		self.mainWind.user.unset_importance("Stores")
		self.user.set_importance("FLIX")
		self.user.set_importance("SAIGON CITY")
		app.quit()
