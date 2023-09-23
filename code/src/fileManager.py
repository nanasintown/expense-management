class FileManager:
	_income: dict[str, list] = {}
	_expenses: dict[str, list] = {}
	_info: list = []

	def __init__(self):
		self._file: list = []
		self._rdy_file: list = []
		self._words: list = []
		self._titles: list = []
		self.important = False
		FileManager._expenses = {}
		FileManager._income = {}
		FileManager._info = []
		self._expense = FileManager._expenses
		self._income = FileManager._income
		self._info = FileManager._info

	def read_file(self, filepath: str) -> tuple[bool, str]:
		counter = 0  # if 0 then titles of the csv-files
		self._file.append(filepath)
		try:
			with open(filepath, 'r', encoding='utf-8') as csv:
				self._rdy_file = csv.readline()
				while self._rdy_file != "":
					if counter == 0:
						self._titles = self._rdy_file.split(";")
						counter += 1
						self._rdy_file = csv.readline()
					else:
						self._words.append(self._rdy_file.split(";"))
						self.organize_rows(self._words[-1])  # always organize the latest row
						self._rdy_file = csv.readline()
		except IOError:
			return False, "Error in loading a file"
		except Exception as err:
			return False, "Error in loading a file"
		else:
			return True, "Loading a file successfull!"

	def organize_rows(self, row):
		check_receiver = False
		check_amount = False
		receiver_index = 0
		amount_index = 0
		for i, info in enumerate(self._titles):
			if ("Saaja" in info and (not check_receiver)) or ("Otsikko" in info and (not check_receiver)) or (
					"Title" in info and (not check_receiver)) or ("Receiver" in info and (not check_receiver)):
				receiver_index = i
				check_receiver = True

			if ("Määrä" in info and (not check_amount)) or ("Amount" in info and (not check_amount)):
				amount_index = i
				check_amount = True
		if row != [""]:
			try:
				amount = float(row[amount_index].replace(",", "."))
			except ValueError:
				print("row {} wasn't added".format(row[receiver_index]))
			else:
				temp_holder: list[str] = row[receiver_index].split(" ")  # remove redundant spaces
				temp_holder = [receiver for receiver in temp_holder if receiver != ""]
				row[receiver_index] = " ".join(temp_holder)
				if amount >= 0:
					if row[receiver_index] not in self._income:
						self._income[row[receiver_index]] = [amount, self.important, 1]
						if self._income[row[receiver_index]][0] >= 500:  # Importance algorithm
							self._income[row[receiver_index]][1] = True
					else:
						self._income[row[receiver_index]][0] += amount
						self._income[row[receiver_index]][2] += 1
						if self._income[row[receiver_index]][2] >= 3:  # Importance algorithm
							self._income[row[receiver_index]][1] = True
				else:
					if row[receiver_index] not in self._expenses:
						self._expenses[row[receiver_index]] = [amount, self.important, 1]
						if abs(self._expenses[row[receiver_index]][0]) >= 100:
							self._expenses[row[receiver_index]][1] = True
					else:
						self._expenses[row[receiver_index]][0] += amount
						self._expenses[row[receiver_index]][2] += 1
						if self._expenses[row[receiver_index]][2] >= 5:
							self._expenses[row[receiver_index]][1] = True

	def show_income(self) -> dict[str, list]:
		return self._income

	def show_expenses(self) -> dict[str, list]:
		return self._expenses

	def set_grouping(self, grouping_list: list, group_title: str) -> bool:
		temp_holder: dict[str, list] = {group_title: [0, False, 1]}

		try:
			for row in grouping_list:
				amount, importance, occurrence = self._expenses[row]
				temp_holder[group_title][0] += amount

			if abs(temp_holder[group_title][0]) >= 100:
				temp_holder[group_title][1] = True

			for row in grouping_list:
				self._expenses.pop(row)

			if group_title not in self._expenses:
				self._expenses.update(temp_holder)
			else:
				self._expenses[group_title][0] += temp_holder[group_title][0]
				self._expenses[group_title][2] += 1

		except ValueError:
			return False
		except Exception:
			return False
		else:
			return True

	def set_importance(self, key_value: str) -> bool:
		try:
			self._expenses[key_value][1] = True
		except Exception:
			return False
		else:
			return True

	def unset_importance(self, key_value):
		try:
			self._expenses[key_value][1] = False
		except Exception:
			return False
		else:
			return True

	def delete_row(self, del_list):
		try:
			for row in del_list:
				self._expenses.pop(row)
		except Exception:
			return False
		else:
			return True
