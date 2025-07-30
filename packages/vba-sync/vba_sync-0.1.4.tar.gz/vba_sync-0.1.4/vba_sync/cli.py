"""
VBA Sync Tool — Export or import VBA macros from Word (.docm) or Excel (.xlsm) files.

This script allows you to:
    - Export all VBA modules from a document into a folder.
    - Import previously exported modules back into the document.

Usage:
    python vba_sync.py export <document>
    python vba_sync.py import <document>

Requirements:
    - Python 3.x
    - pywin32 (install via pip install pywin32)
    - Microsoft Office with enabled "Trust access to the VBA project object model"
"""

import os
import sys
import win32com.client
import pywintypes
from datetime import datetime
import argparse
from importlib.metadata import version

def check_dependencies():
    try:
        import win32com.client
        import pywintypes
        return True
    except ImportError as e:
        print(f"""
Error: Required module not found: {e.name}

This script requires the 'pywin32' package to interact with VBA in Word and Excel.

Please install it using:
    pip install pywin32

After installation, you may need to run:
    python -c "import pywin32; pywin32.post_install()"
""")
        return False


def main():
    print(version('vba-sync'))  # выведем версию модуля
    parser = argparse.ArgumentParser(description="Export or import VBA macros from Word/Excel documents.")
    parser.add_argument("action", choices=["export", "import"], help="Action to perform")
    parser.add_argument("document", help="Name of the document file (e.g., mydoc.docm)")
    args = parser.parse_args()

    # Check pywin32 installed
    if not check_dependencies():
        sys.exit(1)

    if args.action == "export":
        export_macros(args.document)
    elif args.action == "import":
        import_macros(args.document)


def get_app_and_doc(doc_path):
    """
    Launches appropriate COM application and opens the document.

    Args:
        doc_path (str): Path to the document file.

    Returns:
        tuple: (application, document, VBProject)
    """
    ext = os.path.splitext(doc_path)[1].lower()

    try:
        if ext in ('.docm', '.dotm'):
            app = win32com.client.Dispatch("Word.Application")
            doc = app.Documents.Open(doc_path)
        elif ext in ('.xlsm', '.xlam'):
            app = win32com.client.Dispatch("Excel.Application")
            doc = app.Workbooks.Open(doc_path)
        else:
            raise ValueError(f"Unsupported file type: {ext}. Supported: .docm, .dotm, .xlsm, .xlam")
        vba_project = doc.VBProject
        return app, doc, vba_project

    except pywintypes.com_error as e:
        if hasattr(e, 'strerror') and "access is disabled" in e.strerror.lower():
            print("""
Error: Access to the VBA Project Object Model is disabled.

To fix this:
  In Word:
    File -> Options -> Trust Center -> Macros -> 
    Enable checkbox: "Trust access to the VBA project object model"

  In Excel:
    File -> Options -> Trust Center -> Macros -> 
    Enable checkbox: "Trust access to the VBA project object model"
""")
            sys.exit(1)
        else:
            print(f"COM error occurred: {e}")
            sys.exit(1)
    except Exception as e:
        print(f"Error opening document: {e}")
        sys.exit(1)


def make_backup(doc_path, doc_filename):
    """
    Creates a backup copy of the document before importing macros.

    Args:
        doc_path (str): Full path to the document.
        doc_filename (str): Name of the document file.
    """
    backup_folder = os.path.join(os.path.dirname(doc_path), "backup")
    if not os.path.exists(backup_folder):
        os.makedirs(backup_folder)

    ext = os.path.splitext(doc_filename)[1]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    backup_name = f"{os.path.splitext(doc_filename)[0]}_{timestamp}{ext}"
    backup_path = os.path.join(backup_folder, backup_name)

    try:
        import shutil
        shutil.copy2(doc_path, backup_path)
        print(f"Backup created: {backup_name}")
    except Exception as e:
        print(f"Failed to create backup: {e}")


def extract_vba_code(text):
    """
    Removes header information from a VBA module.

    Args:
        text (str): Raw text from a .bas/.cls file.

    Returns:
        str: Cleaned VBA code without header lines.
    """
    lines = text.splitlines()
    start_index = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith(("VERSION", "BEGIN", "END", "MultiUse", "Attribute")):
            start_index = i + 1
        else:
            break

    return "\n".join(lines[start_index:])


def export_macros(doc_filename):
    """
    Exports all VBA modules from a document into a folder.

    Args:
        doc_filename (str): Name of the document file.
    """
    current_dir = os.getcwd()
    doc_path = os.path.join(current_dir, doc_filename)
    output_folder = os.path.join(current_dir, f"_modules_{doc_filename}")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    app, doc, vba_project = None, None, None

    try:
        app, doc, vba_project = get_app_and_doc(doc_path)
        app.Visible = False
        print(f"Document opened: {doc_filename}")

        # Export all modules
        for component in vba_project.VBComponents:
            module_name = component.Name
            output_path = os.path.join(output_folder, f"{module_name}.bas")
            component.Export(output_path)
            print(f"Exported module: {module_name} -> {output_path}")

        doc.Save()
        doc.Close()
    except Exception as e:
        print(f"Export error: {e}")
    finally:
        if app:
            app.Quit()


def import_macros(doc_filename):
    """
    Imports VBA modules from a folder into a document.

    Args:
        doc_filename (str): Name of the document file.
    """
    current_dir = os.getcwd()
    doc_path = os.path.join(current_dir, doc_filename)
    input_folder = os.path.join(current_dir, f"_modules_{doc_filename}")

    if not os.path.exists(input_folder):
        print(f"Folder '{input_folder}' not found. Nothing to import.")
        return

    print("\nCreating document backup before import...")
    make_backup(doc_path, doc_filename)

    app, doc, vba_project = None, None, None

    try:
        app, doc, vba_project = get_app_and_doc(doc_path)
        app.Visible = False
        print(f"Document opened: {doc_filename}")

        # Process all valid files
        for filename in os.listdir(input_folder):
            if not filename.endswith((".bas", ".cls", ".frm")):
                continue

            file_path = os.path.join(input_folder, filename)
            module_name = filename[:-4]  # Remove extension

            print(f"\nProcessing module: {module_name} ({filename})")

            # Look for existing module
            existing_component = None
            for component in list(vba_project.VBComponents):
                if component.Name == module_name:
                    existing_component = component
                    break

            if existing_component:
                print(f"Found existing module: {module_name}")

                # Skip system modules like ThisDocument / Sheet1
                if existing_component.Type == 100:
                    print(f"This is a system module: {module_name}. Updating code in-place.")

                    # Read content
                    with open(file_path, 'r', encoding='cp1251') as f:
                        new_code = f.read()

                    # Clean up header
                    new_code = extract_vba_code(new_code)

                    # Update code directly
                    code_module = existing_component.CodeModule
                    count = code_module.CountOfLines
                    if count > 0:
                        code_module.DeleteLines(1, count)

                    code_module.InsertLines(1, new_code)
                    print(f"Code in system module {module_name} updated.")
                    continue
                else:
                    # Remove old module
                    try:
                        print(f"Removing old module: {module_name}")
                        vba_project.VBComponents.Remove(existing_component)
                    except Exception as e:
                        print(f"Error removing module {module_name}: {e}")
                        continue
            else:
                print(f"Old module {module_name} not found — will be created.")

            # Import new module
            try:
                print(f"Importing module: {module_name} <- {file_path}")
                vba_project.VBComponents.Import(file_path)
                print(f"Module {module_name} successfully imported")
            except Exception as e:
                print(f"Import error for {module_name}: {e}")

        doc.Save()
        doc.Close()
    except Exception as e:
        print(f"Import failed: {e}")
    finally:
        if app:
            app.Quit()


if __name__ == "__main__":
    main()
