import unittest
import os
import json
import yaml
import sys
import shutil

# Добавляем src в PYTHONPATH
sys.path.append('src')

from conv2docx import cli as conv2docx

TEST_DIR = TEST_DIR = os.path.abspath("test_temp")  # папка для тестов


class TestConv2Docx(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Создаём test_temp/ перед всеми тестами"""
        if os.path.exists(TEST_DIR):
            shutil.rmtree(TEST_DIR)
        os.makedirs(TEST_DIR)

    def setUp(self):
        """Переходим в test_temp/ перед каждым тестом"""
        self.old_cwd = os.getcwd()
        os.chdir(TEST_DIR)

    def tearDown(self):
        """Очищаем содержимое test_temp/, но оставляем папку для анализа"""
        for file in os.listdir():
            path = os.path.join(TEST_DIR, file)
            if os.path.isfile(path):
                os.remove(path)
        os.chdir(self.old_cwd)

    def create_yaml(self, filename, data):
        """Создаём YAML-файл в test_temp/"""
        path = os.path.join(TEST_DIR, filename)
        # print(f"path: {path}")
        # print(f"Current Path: {os.getcwd()}")
        with open(path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f)
        return filename  # имя файла (без пути), т.к. мы внутри test_temp/

    def create_json(self, filename, data):
        """Создаём JSON-файл в test_temp/"""
        path = os.path.join(TEST_DIR, filename)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f)
        return filename

    def test_convert_yaml_to_json(self):
        yaml_path = self.create_yaml("test.yaml", {"key": "value"})
        json_path = conv2docx.convert_yaml_to_json(yaml_path)
        self.assertTrue(os.path.exists(json_path))
        with open(json_path) as f:
            data = json.load(f)
        self.assertEqual(data, {"key": "value"})

    def test_convert_yaml_to_docx(self):
        yaml_path = self.create_yaml("test.yaml", {"key": "value"})
        json_path = conv2docx.convert_yaml_to_json(yaml_path)
        md_path = conv2docx.prepare_markdown_file(json_path)
        result = conv2docx.convert_md_to_docx(md_path)
        self.assertTrue(result)
        self.assertTrue(os.path.exists("test.yaml.json.docx"))

    def test_keep_temp_flag(self):
        yaml_path = self.create_yaml("test.yaml", {"key": "value"})
        conv2docx.sys.argv = ['conv2docx', '--keep-temp', yaml_path]
        conv2docx.main()
        self.assertTrue(os.path.exists("test.yaml"))
        self.assertTrue(os.path.exists("test.yaml.json"))
        self.assertTrue(os.path.exists("test.yaml.json.md"))
        self.assertTrue(os.path.exists("test.yaml.json.docx"))

    def test_main_no_temp_files_on_error(self):
        conv2docx.sys.argv = ['conv2docx', 'nonexistent.yaml']
        with self.assertRaises(SystemExit):
            conv2docx.main()


if __name__ == '__main__':
    unittest.main()