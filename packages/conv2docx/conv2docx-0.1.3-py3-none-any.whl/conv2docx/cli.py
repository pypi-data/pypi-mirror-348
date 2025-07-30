import sys
import os
import pypandoc
from importlib.metadata import version


def prepare_markdown_file(input_file):
    """
    Создаёт временный .md файл на основе переданного JSON-файла.
    Добавляет маркеры ```json в начало и конец файла.

    :param input_file: Путь к исходному JSON-файлу.
    :return: Путь к созданному .md файлу или None, если произошла ошибка.
    """
    # Проверяем, существует ли исходный файл
    if not os.path.isfile(input_file):
        print(f"Файл {input_file} не найден.")
        return None

    # Формируем имя нового .md файла
    md_file = input_file + ".md"

    try:
        # Читаем содержимое оригинального файла
        with open(input_file, 'r', encoding='utf-8') as src:
            content = src.read()

        # Добавляем маркеры JSON в начало и конец
        new_content = "```json\n" + content + "\n```"

        # Записываем в новый .md файл
        with open(md_file, 'w', encoding='utf-8') as dst:
            dst.write(new_content)

        print(f"Создан временный файл: {md_file}")
        return md_file

    except Exception as e:
        print(f"Ошибка при подготовке файла: {e}")
        return None


def convert_md_to_docx(input_file):
    """
    Конвертирует указанный Markdown (.md) файл в формат .docx с помощью pypandoc.

    :param input_file: Путь к .md файлу.
    :return: True, если конвертация прошла успешно, иначе False.
    """

    base_name = os.path.splitext(os.path.basename(input_file))[0]
    output_file = f"{base_name}.docx"

    try:
        output = pypandoc.convert_file(input_file, 'docx', outputfile=output_file)
        print(f"Файл успешно сохранён как {output_file}")
        return True  # Успешно завершено
    except Exception as e:
        print(f"Ошибка при конвертации: {e}")
        return False  # Ошибка


def main():
    """
    Основное тело программы:
    
    - Если указан аргумент командной строки — обрабатывается один файл.
    - Если аргументов нет — обрабатываются все .json файлы в текущей директории.
    - Для каждого JSON-файла создаётся временный .md файл, выполняется конвертация,
      после чего временный файл удаляется.
    """
    print(version('conv2docx'))  # выведем версию модуля

    # Получаем список файлов для обработки
    if len(sys.argv) >= 2:
        input_files = [sys.argv[1]]
    else:
        # Берём все .json файлы из текущей директории
        input_files = [f for f in os.listdir() if f.lower().endswith('.json')]

    if not input_files:
        print("Нет подходящих .json файлов для обработки.")
        sys.exit(1)

    for json_file in input_files:
        print(f"\nОбработка файла: {json_file}")

        # Шаг 1: Подготовить .md файл
        md_file = prepare_markdown_file(json_file)
        if not md_file:
            print(f"Не удалось подготовить файл {json_file}, пропускаем.")
            continue

        # Шаг 2: Конвертировать .md в .docx
        success = convert_md_to_docx(md_file)

        # Шаг 3: Удалить временный .md файл
        if os.path.exists(md_file):
            try:
                os.remove(md_file)
                print(f"Временный файл {md_file} удалён.")
            except Exception as e:
                print(f"Не удалось удалить временный файл: {e}")

        if not success:
            print(f"Ошибка при обработке файла {json_file}")


if __name__ == "__main__":
    print(version('conv2docx'))  # выведем версию модуля
    main()
 