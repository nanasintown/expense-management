from fileManager import *


class User:
    def __init__(self, _file_manager):
        self.file_manager: FileManager = _file_manager

    def get_income(self) -> dict[str, list]:
        return self.file_manager.show_income()

    def get_expenses(self) -> dict[str, list]:
        return self.file_manager.show_expenses()

    def import_file(self, file_path: str) -> tuple[bool, str]:
        return self.file_manager.read_file(file_path)

    def set_importance(self, key_value: str) -> str:
        imp_success = self.file_manager.set_importance(key_value)
        if imp_success:
            return "Importance setting successful."
        else:
            return "Importance setting failed."

    def unset_importance(self, key_value: str) -> str:
        unimp_success = self.file_manager.unset_importance(key_value)
        if unimp_success:
            return "Unimportance setting successful."
        else:
            return "Unimportance setting failed."

    def set_grouping(self, grouping_list: list, group_title: str) -> tuple[str, bool]:
        if len(grouping_list) >= 1 and group_title != "":
            grouping_success = self.file_manager.set_grouping(grouping_list, group_title)
            if grouping_success and len(grouping_list) == 1:
                return "Row renamed successfully.", True
            elif grouping_success and len(grouping_list) != 1:
                return "Grouping successful.", True
            else:
                return "Grouping failed.", False
        elif len(grouping_list) == 0:
            return "No rows checked.", False
        else:
            return "Set group title.", False

    def delete_row(self, delete_list: list) -> str:
        if len(delete_list) == 0:
            return "No rows selected."
        else:
            delete_success = self.file_manager.delete_row(delete_list)

            if delete_success:
                return "Deletion successful."
            else:
                return "Deletion failed."
