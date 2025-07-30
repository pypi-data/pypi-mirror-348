# VBA-Sync

A command-line tool for exporting and importing VBA macros from Microsoft Word (.docm .dotm) and Excel (.xlsm .xlam) files.

This script allows you to:
- Export all VBA modules from a document into a folder.
- Import previously exported modules back into the document.

Create a backup copy of the document before importing macros.


## Installation

```bash
pip install vba-sync
```

# Requirements

Python >= 3.7

Microsoft Word or Excel installed

Trust access to the VBA project object model enabled in Office settings

# Usage

## Export macros
vba-sync export your_file.docm

## Import macros
vba-sync import your_file.docm

[![License](https://img.shields.io/github/license/AndyTakker/VBA-Sync)](https://github.com/AndyTakker/VBA-Sync)
