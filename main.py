import json
import os
import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QFrame, QMessageBox


class Window(QFrame):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi("ZenScriptGen.ui", self)
        self.show()
        self.ui.saveButton.clicked.connect(self.click_saveButton)
        self.ui.clearButton.clicked.connect(self.click_clearButton)
        self.ui.saveRemoveButton.clicked.connect(self.click_saveRemoveButton)

        # Список для полей ввода и SpinBox
        self.text_fields = [
            self.ui.assemblerLine1,
            self.ui.assemblerLine2,
            self.ui.assemblerLine3,
            self.ui.assemblerLine4,
            self.ui.assemblerLine5,
            self.ui.assemblerLine6,
            self.ui.assemblerLine7,
            self.ui.assemblerLine8,
            self.ui.assemblerLine9,
            self.ui.assemblerLine10,
            self.ui.assemblerLine11,
            self.ui.assemblerLine12
        ]
        self.spinbox_values = [
            self.ui.assemblerSpinBox1,
            self.ui.assemblerSpinBox2,
            self.ui.assemblerSpinBox3,
            self.ui.assemblerSpinBox4,
            self.ui.assemblerSpinBox5,
            self.ui.assemblerSpinBox6,
            self.ui.assemblerSpinBox7,
            self.ui.assemblerSpinBox8,
            self.ui.assemblerSpinBox9,
            self.ui.assemblerSpinBox10,
            self.ui.assemblerSpinBox11,
            self.ui.assemblerSpinBox12
        ]

    def _get_config(self):
        config_file_path = "config.json"
        if not os.path.exists(config_file_path):
            QMessageBox.critical(self, "Ошибка", f"Файл конфигурации '{config_file_path}' не найден.")
            return None

        with open(config_file_path, "r") as configFile:
            return json.load(configFile)

    def _write_to_file(self, content):
        config = self._get_config()
        if config is None:
            return

        folder_path = config.get("folder_path")
        if not folder_path:
            QMessageBox.critical(self, "Ошибка", "Конфигурация не содержит путь к папке.")
            return

        if not os.path.exists(folder_path):
            try:
                os.makedirs(folder_path)
            except OSError as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось создать папку: {str(e)}")
                return

        file_path = os.path.join(folder_path, "GenerateScript.zs")
        try:
            if os.path.exists(file_path):
                with open(file_path, "r") as file:
                    existing_content = file.read()
                new_content = existing_content + "\n" + content
            else:
                new_content = content

            with open(file_path, "w") as file:
                file.write(new_content)

            QMessageBox.information(self, "Успех", f"Скрипт сохранен в {file_path}")
        except IOError as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка при записи файла: {str(e)}")

    def click_saveButton(self):
        try:
            # Получение данных из полей ввода и SpinBox
            input_items = [
                f"{text_field.text().strip()}*{spinbox.value()}" if spinbox.value() > 0 else text_field.text().strip()
                for text_field, spinbox in zip(self.text_fields, self.spinbox_values)
                if text_field.text().strip()
            ]

            inputs_string = ', '.join(input_items) if input_items else "[]"
            output_item = self.ui.assemblerLineOutput.text().strip()
            if not output_item:
                QMessageBox.critical(self, "Ошибка", "Выходной предмет не указан.")
                return

            int_duration = self.ui.intDurationSpinBox.value()
            new_recipe = f"mods.ntm.Assembler.addRecipe({output_item}, [{inputs_string}], {int_duration});"
            self._write_to_file(new_recipe)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def click_saveRemoveButton(self):
        try:
            output_item = self.ui.removeLine.text().strip()
            if not output_item:
                QMessageBox.critical(self, "Ошибка", "Предмет на удаление не указан.")
                return

            new_remove_recipe = f"mods.ntm.Assembler.removeRecipe({output_item});"
            self._write_to_file(new_remove_recipe)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")

    def click_clearButton(self):
        # Очистка всех полей ввода
        for field in self.text_fields:
            field.clear()

        # Сброс значений SpinBox
        for spinbox in self.spinbox_values:
            spinbox.setValue(0)

        # Очистка дополнительных данных
        self.ui.assemblerLineOutput.clear()
        self.ui.intDurationSpinBox.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())
