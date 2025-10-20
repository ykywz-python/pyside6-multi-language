import os
import subprocess
from pathlib import Path

# --- Configuration ---
# Set the directory containing your .ts files.
TRANSLATIONS_DIR = Path("../src/translations")
# Define any specific options you want to pass to lrelease (optional)
LRELEASE_OPTIONS = [
    "-compress", 
    # "-nounfinished"
] 
# ---------------------

def batch_compile_translations():
    """
    Finds all .ts files in TRANSLATIONS_DIR and compiles them into .qm files
    using the pyside6-lrelease command-line tool.
    """
    if not TRANSLATIONS_DIR.exists():
        print(f"Error: Translation directory '{TRANSLATIONS_DIR}' not found.")
        return

    ts_files = list(TRANSLATIONS_DIR.glob("*.ts"))
    
    if not ts_files:
        print(f"No .ts files found in '{TRANSLATIONS_DIR}'.")
        return

    print(f"--- Starting batch compilation of {len(ts_files)} translation files ---")
    
    for ts_path in ts_files:
        # Define the output .qm file path
        qm_path = ts_path.with_suffix(".qm")
        
        # Build the command as a list of arguments
        command = [
            "pyside6-lrelease",
            str(ts_path),
            "-qm",
            str(qm_path),
        ]
        
        # Add optional arguments
        command.extend(LRELEASE_OPTIONS)

        print(f"Compiling: {ts_path.name} -> {qm_path.name}")
        
        try:
            # Execute the command
            result = subprocess.run(
                command, 
                check=True,
                capture_output=True, 
                text=True
            )
            # You can uncomment the lines below to see detailed output from lrelease
            # if result.stdout:
            #     print(result.stdout.strip())
            
        except subprocess.CalledProcessError as e:
            print(f"\n--- ERROR compiling {ts_path.name} ---")
            print(f"STDOUT: {e.stdout.strip()}")
            print(f"STDERR: {e.stderr.strip()}")
            print("--------------------------------------\n")
        except FileNotFoundError:
            print(f"\nError: 'pyside6-lrelease' not found. Ensure PySide6 is installed and in your PATH.")
            return

    print("--- Batch compilation finished successfully ---")

if __name__ == "__main__":
    batch_compile_translations()