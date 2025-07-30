# Foldora - File & Directory Manager CLI Tool

[![PyPI version](https://img.shields.io/pypi/v/foldora)](https://pypi.org/project/foldora/)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](code_of_conduct.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Downloads](https://img.shields.io/pypi/dm/foldora)](https://pypi.org/project/foldora/)

**Foldora** is a Python command-line interface (CLI) tool designed to help you efficiently manage files and directories.

## 🚀 Features

Foldora provides essential file and directory operations, including:

- 📝 Displaying file contents
- 🧹 Purging files and directories
- 📁 Listing files and directories  
- 📂 Creating directories and files  
- ✏️ Replacing spaces in file and directory names with underscores  

## 🛠️ Installation

To install Foldora, clone the repository and navigate to the project directory:

- PS: Make sure python is installed in case you're new to Python.

```sh
pip install foldora
```

## 📦 Usage

Run Foldora using the `fd` command followed by the desired operation.


### 📁 List Files and Directories

Lists all files and directories in the current or specified paths.


**Command:**

```sh
fd la [optional_paths]
```


**Notes:**

- Hidden files and directories may also be included depending on the system settings.
- If a specified path is a file, an error will be raised.
- Multiple paths can be specified to list contents from different directories at once.


**Examples:**

- List files/dirs of the current directory

```sh
fd la
```

- List files/dirs of specific directories

```sh
fd la /path/to/dir1 /path/to/dir2  
```

### 📂 Create Directories

Creates one or more directories.


**Command:**

```sh
fd cd [paths]
```


**Notes:**

- Creates all necessary parent directories if they do not exist.
- Does not modify existing directories.
- Supports creating multiple directories in a single command.


**Example:**

```sh
fd cd /path/to/dir1 /path/to/dir2 ...
```


### 📄 Create Files

Creates one or more files in the current directory or a specified path.


**Command:**

```sh
fd cf '[-p path]' [file_paths]
```


**Notes:**

- Existing files with the same names will not be overwritten.
- If the specified directory (or path) does not exist, it will be created.
- Supports creating multiple files in a single command.


**Examples:**

- Create files in the current directory

```sh
fd cf file1.txt file2.txt  
```

- Create files in a specified directory

```sh
fd cf -p /path/to/dir file1.txt file2.txt  
```


### 🧹 Purge Files and Directories

Deletes specified files and directories with user confirmation.


**Command:**

```sh
fd pa [file_paths] [dir_paths]
```


**Notes:**

- Use with caution, as this action cannot be undone.
- Directories will be deleted recursively, including all their contents.
- Ensure you have the necessary permissions to delete the specified paths.


**Example:**

```sh
fd pa /path/to/dir1 /path/to/file1 ...
```

### 📝 Display File Contents

Shows the content of one or more files.


**Command:**

```sh
fd sc [file_paths]
```

**Notes:**

- Files must be readable, or an error will be raised.
- Supports multiple files, displaying each file's content in sequence.


**Example:**

```sh
fd sc /path/to/file1 /path/to/file2 ...
```


### ✏️ Fill Blanks in File/Directory Names

Replace spaces in file and folder names with underscores.

This command renames files and folders by replacing any spaces in their names with underscores. It operates on the specified directory (or the current directory if none is provided). All files and directories in that location will have their names updated to remove spaces.


**Command:**

```sh
fd rs [path]
```

**Notes:**

- By default, only top-level files and folders are renamed.
- When prompted, entering 'y' activates Deep Folder Traversal mode, which processes all nested directories.
- Deep Folder Traversal mode allows recursive renaming for all files and folders within the specified path.


**Example:**

- Current directory

```sh
fd rs
```

- Specific directory

```sh
fd rs /path/to/dir
```


## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to help improve Foldora.

## 📄 License

This project is licensed under the MIT License.
