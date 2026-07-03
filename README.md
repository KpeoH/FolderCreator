**[🇷🇺 Русская версия](#-foldercreator-1)** | **[🇬🇧 English version](#-foldercreator)**

---

# 🇷🇺 FolderCreator

Простой и удобный инструмент для автоматической сортировки файлов по расширениям в выбранной папке.

### Описание

FolderCreator — это десктопное приложение на Python, которое помогает быстро навести порядок в рабочих директориях. Оно перемещает файлы в соответствующие подпапки согласно заданным правилам (например, все .obj и .fbx в папку Export). 

Поддерживает отмену последней операции сортировки и удобную настройку правил через интерфейс.

## Возможности

- Автоматическая сортировка файлов по расширениям
- Настраиваемая конфигурация (JSON)
- Функция отмены (возврат файлов обратно)
- Поддержка drag & drop папок
- Красивый современный интерфейс с тёмной темой
- Прогресс-бар и подробный журнал операций
- Автоматическое создание подпапок
- Обработка конфликтов имён файлов

## Как использовать

1. Запустите приложение (`FolderCreator.exe` для Windows).
2. Укажите путь к папке (можно перетащить папку в окно).
3. Нажмите «Сортировать».
4. При необходимости отмените действие кнопкой «Отменить».

### Настройка правил

Перейдите во вкладку «Настройки»:
- Добавляйте новые правила: укажите имя папки и список расширений через запятую.
- Сохраняйте изменения.
- Или сбросьте на значения по умолчанию.

По умолчанию используются следующие папки:
- **Export**: `.obj`, `.fbx`
- **Max**: `.max`, `.3ds`
- **Textures**: `.jpg`, `.png`, `.mtl`

## Сборка из исходников (для разработчиков)

Требования:
- Python 3.9+
- PySide6

```bash
pip install PySide6
python FolderCreator.py
```
## Для создания EXE-файла (Windows):
```Bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.png --add-data "icon.png;." FolderCreator.py
```
Готовый `.exe` файл появится в папке `dist`.

## Конфигурация
Все настройки хранятся в файле `config.json` рядом с программой. Вы можете редактировать его вручную, если нужно.

## Лицензия
Проект распространяется как есть. Используйте на свой страх и риск.


# 🇬🇧 FolderCreator

A simple and convenient tool for automatic file sorting by extensions in the selected folder.

### Description

FolderCreator is a desktop application written in Python that helps you quickly organize files in your working directories. It moves files into corresponding subfolders according to predefined rules (for example, all `.obj` and `.fbx` files go to the Export folder).

It supports undoing the last sorting operation and provides easy rule management through a user-friendly interface.

## Features

- Automatic sorting of files by their extensions
- Customizable configuration via JSON
- Undo functionality — easily restore files to their original location
- Drag & drop support for folders
- Modern dark-themed interface
- Progress bar and detailed operation log
- Automatic creation of target subfolders
- Smart handling of duplicate filenames

## How to Use

1. Launch the application (`FolderCreator.exe` for Windows).
2. Specify the target folder path (or simply drag & drop a folder into the window).
3. Click **Сортировать** (Sort).
4. If needed, use the **Отменить** (Undo) button to revert the changes.

### Managing Rules

Switch to the **Настройки** (Settings) tab:
- Add new rules by entering a folder name and a comma-separated list of extensions.
- Save your changes.
- Or reset everything to default values with one click.

**Default folders:**
- **Export**: `.obj`, `.fbx`
- **Max**: `.max`, `.3ds`
- **Textures**: `.jpg`, `.png`, `.mtl`

## Building from Source

**Requirements:**
- Python 3.9+
- PySide6

```bash
pip install PySide6
python FolderCreator.py
```

## To create a standalone Windows executable:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.png --add-data "icon.png;." FolderCreator.py
```
The `.exe` file will appear in the `dist` folder.

## Configuration
All settings are stored in the `config.json` file located next to the program. You can edit it manually if you prefer.

## License
This project is provided "as is". Use at your own risk.
