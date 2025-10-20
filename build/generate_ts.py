import subprocess
import sys
import glob
from pathlib import Path

# --- Configuration ---

# 1. Directory containing your Python source code files to scan (e.g., 'src', 'app').
SOURCE_ROOT_DIR = Path("../src") 

# 2. Directory where the generated/updated .ts files should be saved.
TRANSLATIONS_DIR = Path("../src/translations")

# 3. List of language codes to generate/update translation files for.
# (ISO 639-1 code + optional country code, e.g., 'fr', 'en_US', 'pt_BR')
LANGUAGES = [
    # "en",    # English (Base language, often not needed, but good for standardization)
    # "fr",    # French
    # "de",    # German
    # "es",    # Spanish
    # "pt_BR", # Brazilian Portuguese
    # "zh_CN", # Simplified Chinese
    # "ja",    # Japanese
    # "it",    # Italian
    # "ru",    # Russian
    "id",    # Indonesian (Example from your previous request)
]

# 4. Optional: Extra flags for pyside6-lupdate (recommended to skip obsolete strings)
EXTRA_OPTIONS = ["-no-obsolete"]
# ---------------------

def run_pyside_lupdate_batch():
    """
    Scans the SOURCE_ROOT_DIR for all .py files, including subdirectories,
    and executes the pyside6-lupdate command.
    """
    
    # --- Path Setup and Validation ---
    
    # 1. Resolve the source directory to an absolute path for safety
    resolved_source_dir = SOURCE_ROOT_DIR.resolve()
    TRANSLATIONS_DIR.mkdir(parents=True, exist_ok=True)
    
    print(f"Scanning resolved source directory: '{resolved_source_dir}'")
    
    # --- Source File Detection (Includes Subfolders) ---
    
    # 2. Automatically find all .py source files using rglob (recursive glob)
    # The **/*.py pattern finds all .py files in resolved_source_dir and all its subdirectories.
    source_files = [
        str(p) 
        for p in resolved_source_dir.rglob('*.py') 
        if p.is_file() and p.name != Path(__file__).name # Exclude this compilation script itself
    ]
    
    if not source_files:
        print(f"Error: No Python (.py) source files found in '{resolved_source_dir}'.", file=sys.stderr)
        return

    print(f"Found {len(source_files)} source files for scanning.")
    
    # --- Target TS File Generation ---
    
    # 3. Build the list of target .ts files
    ts_targets = []
    for lang_code in LANGUAGES:
        ts_filename = f"app_{lang_code}.ts"
        ts_path = TRANSLATIONS_DIR / ts_filename
        ts_targets.append(str(ts_path))

    print(f"Preparing to update {len(ts_targets)} translation files.")
    
    # --- Command Execution ---
    
    command = ["pyside6-lupdate"]
    command.extend(source_files)
    
    # Add all -ts arguments
    for ts_file in ts_targets:
        command.extend(["-ts", ts_file])
    
    # Add extra options
    command.extend(EXTRA_OPTIONS)

    print(f"\nCommand: {' '.join(command[:10])} ... and {len(command) - 10} more arguments")

    try:
        result = subprocess.run(
            command, 
            check=True,
            capture_output=True, 
            text=True
        )

        print("\n--- pyside6-lupdate completed successfully. ---")
        if result.stdout:
            print(result.stdout.strip())
        print(f"Output files are in: {TRANSLATIONS_DIR.resolve()}")

    except subprocess.CalledProcessError as e:
        print(f"\n--- ERROR running pyside6-lupdate (Exit Code {e.returncode}) ---", file=sys.stderr)
        print(f"STDOUT: {e.stdout}", file=sys.stderr)
        print(f"STDERR: {e.stderr}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: 'pyside6-lupdate' not found. Ensure PySide6 is installed and in your PATH.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    run_pyside_lupdate_batch()