"""
byte_sleuth.py
A utility for scanning text streams, files, and directories for suspicious ASCII control and Unicode characters, with optional sanitization and backup features.

This module provides the ByteSleuth class, which can be used as a library, via CLI, or as a filter in shell pipelines to detect and optionally remove control characters from text. It is designed for international use and follows Python packaging best practices.
"""
import os
import unicodedata
import argparse
import logging
import json
import sys
import hashlib
from concurrent.futures import ProcessPoolExecutor

class ByteSleuth:
    """
    Scans text streams, files, and directories for suspicious ASCII control and Unicode characters.
    Optionally sanitizes files or streams by removing these characters.
    Supports concurrent scanning of files in directories for improved performance.
    """

    # Default log file name
    # This can be overridden by the user when initializing the class or via CLI
    # or by setting the environment variable BYTE_SLEUTH_LOG_FILE
    log_file = "scanner.log"

    # ASCII control characters (0-31, 127)
    # and their names for logging
    ASCII_CONTROL_NAMES = {i: unicodedata.name(chr(i), f"ASCII {i}") for i in range(32)}
    ASCII_CONTROL_NAMES[127] = "DEL (Delete)"

    # List of suspicious/invisible Unicode codepoints (expandable)
    UNICODE_SUSPICIOUS_CODEPOINTS = set([
        0x00A0,  # NO-BREAK SPACE (invisível, comum em problemas de JSON)
        0x00AD,  # SOFT HYPHEN
        0x034F,  # COMBINING GRAPHEME JOINER
        0x061C,  # ARABIC LETTER MARK
        0x115F, 0x1160,  # HANGUL FILLER
        0x17B4, 0x17B5,  # KHMER VOWEL INHERENT
        0x180B, 0x180C, 0x180D, 0x180E,  # MONGOLIAN FREE VARIATION SELECTOR
        0x200B, 0x200C, 0x200D, 0x200E, 0x200F,  # ZERO WIDTH, LRM, RLM
        0x202A, 0x202B, 0x202C, 0x202D, 0x202E,  # BIDI overrides
        0x2060, 0x2061, 0x2062, 0x2063, 0x2064, 0x2066, 0x2067, 0x2068, 0x2069, 0x206A, 0x206B, 0x206C, 0x206D, 0x206E, 0x206F,  # INVISIBLE CONTROLS
        0xFE00, 0xFE01, 0xFE02, 0xFE03, 0xFE04, 0xFE05, 0xFE06, 0xFE07,  # VARIATION SELECTORS
        0xFE10, 0xFE11, 0xFE12, 0xFE13, 0xFE14, 0xFE15, 0xFE16, 0xFE17,  # PRESENTATION FORM
        0xFE18, 0xFE19, 0xFE1A, 0xFE1B,  # PRESENTATION FORM
        0xFE20, 0xFE21, 0xFE22, 0xFE23,  # COMBINING MARKS
        0xFE24, 0xFE25, 0xFE26, 0xFE27, 0xFE28, 0xFE29, 0xFE2A, 0xFE2B,  # COMBINING MARKS
        0xFEFF,  # ZERO WIDTH NO-BREAK SPACE
        0xFFF9, 0xFFFA, 0xFFFB,  # INTERLINEAR ANNOTATION
        0x1D173, 0x1D174, 0x1D175, 0x1D176, 0x1D177, 0x1D178, 0x1D179, 0x1D17A,  # MUSICAL INVISIBLE
        0x1D1AA, 0x1D1AB, 0x1D1AC, 0x1D1AD, 0x1D1AE, 0x1D1AF,  # MUSICAL INVISIBLE
    ])

    # Constructor
    # This method initializes the ByteSleuth class with optional parameters for sanitization, backup, logging, and verbosity.
    # It sets up logging configuration and prepares the class for scanning files or directories.
    # The constructor also defines the default log file name and initializes the list of suspicious characters.
    def __init__(self, sanitize=False, backup=True, log_file="scanner.log", verbose=False, debug=False, quiet=False, sanitize_only=False):
        """
        Initialize the scanner with optional sanitization and backup.
        Args:
            sanitize (bool): If True, automatically remove suspicious characters.
            backup (bool): If True, create a backup before modifying files (not used in PIPE mode).
            log_file (str): Path to the log file.
        """
        self.sanitize = sanitize
        self.backup = backup
        self.verbose = verbose
        self.debug = debug
        self.quiet = quiet
        self.sanitize_only = sanitize_only
        logging.basicConfig(
            filename=log_file, filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s',
            level=logging.DEBUG if debug else logging.INFO
        )

    # Representation method for the class
    # This method provides a detailed representation of the ByteSleuth class,
    # including the current settings for sanitization, backup, logging, and verbosity.
    # This is useful for debugging and logging purposes.
    # It returns a string that includes the class name and its attributes.
    def __repr__(self):
        return f"ByteSleuth(sanitize={self.sanitize}, backup={self.backup}, log_file='{self.log_file}', verbose={self.verbose}, debug={self.debug}, quiet={self.quiet})"

    # String representation of the class
    # This method provides a string representation of the ByteSleuth class,
    # including the current settings for sanitization, backup, logging, and verbosity.
    # This is useful for debugging and logging purposes.
    def __str__(self):
        """
        String representation of the ByteSleuth class.
        Returns:
            str: String representation of the class.
        """
        return f"ByteSleuth(sanitize={self.sanitize}, backup={self.backup}, log_file='{self.log_file}', verbose={self.verbose}, debug={self.debug}, quiet={self.quiet})"

    # Enter method for the context manager
    # This method allows the ByteSleuth class to be used as a context manager.
    # It returns the instance of the class when entering the context.
    # This is useful for resource management and cleanup.
    # It allows the class to be used in a with statement, ensuring proper cleanup.
    def __enter__(self):
        """
        Enter the runtime context related to this object.
        Returns:
            ByteSleuth: The ByteSleuth instance.
        """
        return self
    
    # Exit method for the context manager
    # This method handles cleanup when exiting the context manager.
    # It can also log any exceptions that occurred during the context.
    # It is called when the context manager exits, either normally or due to an exception.
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exit the runtime context related to this object.
        Args:
            exc_type (type): The exception type.
            exc_val (Exception): The exception value.
            exc_tb (Traceback): The exception traceback.
        """
        if exc_type is not None:
            logging.error(f"Error occurred: {exc_val}")
        return False

    # Destructor
    # This method is called when the ByteSleuth instance is deleted.
    # It cleans up resources and logs the exit.
    # It is called when the instance is about to be destroyed.
    # This is useful for resource management and cleanup.
    # It ensures that any resources are properly released and logs the exit.
    def __del__(self):
        """
        Destructor for the ByteSleuth class.
        Cleans up resources and logs the exit.
        """
        logging.info("ByteSleuth instance is being deleted.")
        if hasattr(self, 'suspicious_codepoints'):
            logging.info(f"Suspicious codepoints: {self.UNICODE_SUSPICIOUS_CODEPOINTS}")
        if hasattr(self, 'ASCII_CONTROL_NAMES'):
            logging.info(f"ASCII control names: {self.ASCII_CONTROL_NAMES}")
        if hasattr(self, 'backup'):
            logging.info(f"Backup enabled: {self.backup}")
        if hasattr(self, 'sanitize'):
            logging.info(f"Sanitize enabled: {self.sanitize}")
        if hasattr(self, 'verbose'):
            logging.info(f"Verbose mode: {self.verbose}")
        if hasattr(self, 'debug'):
            logging.info(f"Debug mode: {self.debug}")
        if hasattr(self, 'quiet'):
            logging.info(f"Quiet mode: {self.quiet}")
        if hasattr(self, 'sanitize_only'):
            logging.info(f"Sanitize only mode: {self.sanitize_only}")

        del self.UNICODE_SUSPICIOUS_CODEPOINTS
        del self.ASCII_CONTROL_NAMES
        del self.backup
        del self.sanitize
        del self.verbose
        del self.debug
        del self.quiet
        del self.sanitize_only
        logging.info("ByteSleuth instance cleaned up.")

        del self

    def show_suspicious_codepoints(self, text):
        """
        Show suspicious codepoints found in the text.
        Args:
            text (str): The text to scan.
        """
        findings = self.detect_suspicious_chars(text)
        if not findings:
            logging.info("No suspicious characters found.")
            return
        for cp, name, char, pos in findings:
            logging.info(f"Suspicious character found: {char} (U+{cp:04X}, {name}) at position {pos}")
        if not self.quiet:
            print("\n=== Suspicious Character Report ===")
            for cp, name, char, pos in findings:
                print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {pos}")
            print("===================================")
        logging.info("Suspicious characters detected.")
        if not self.quiet:
            print("Suspicious characters detected.")

    def has_suspicious_chars(self, text):
        """
        Check if the text contains any suspicious characters.
        Args:
            text (str): The text to scan.
        Returns:
            bool: True if suspicious characters are found, False otherwise.
        """
        findings = self.detect_suspicious_chars(text)
        return len(findings) > 0

    def detect_suspicious_chars(self, text):
        """
        Detect ASCII control and suspicious Unicode characters in the text.
        Args:
            text (str): The text to scan.
        Returns:
            list: List of tuples (codepoint, name, character, position) for each suspicious character found.
        """
        findings = []
        for idx, char in enumerate(text):
            cp = ord(char)
            # ASCII control (0-31, 127)
            if (0 <= cp < 32) or cp == 127:
                name = self.ASCII_CONTROL_NAMES.get(cp, chr(cp))
                findings.append((cp, name, char, idx))
            # Unicode suspicious/invisible
            elif cp in self.UNICODE_SUSPICIOUS_CODEPOINTS:
                import unicodedata
                name = unicodedata.name(char, "UNKNOWN")
                findings.append((cp, name, char, idx))
        return findings

    def sanitize_text(self, text):
        """
        Remove suspicious characters while preserving formatting.
        Args:
            text (str): The text to sanitize.
        Returns:
            str: Sanitized text.
        """
        return ''.join(
            char if not (
                (0 <= ord(char) < 32) or ord(char) == 127 or ord(char) in self.UNICODE_SUSPICIOUS_CODEPOINTS
            ) else ''
            for char in text
        )

    def process_stdin(self, log_removed_chars=False, log_file_path=None):
        """
        Sanitize input from PIPE in real-time, line by line.
        Reads from sys.stdin and writes sanitized output to stdout.
        Optionally logs removed characters for audit purposes.
        Returns True if any suspicious characters were detected, else False.
        Args:
            log_removed_chars (bool): If True, logs removed characters.
            log_file_path (str or None): Path to log file (if None, uses self.log_file).
        """
        removed_log = []
        suspicious_found = False
        for line in sys.stdin:
            findings = self.detect_suspicious_chars(line)
            sanitized_line = self.sanitize_text(line)
            if findings:
                suspicious_found = True
            if log_removed_chars and findings:
                for cp, name, char, idx in findings:
                    removed_log.append({
                        "codepoint": cp,
                        "name": name,
                        "char": repr(char),
                        "position": idx,
                        "line": line.rstrip('\n')
                    })
            print(sanitized_line, end="")
        if log_removed_chars and removed_log:
            log_path = log_file_path or getattr(self, 'log_file', 'scanner.log')
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write("\n=== ByteSleuth PIPE Removed Characters Audit ===\n")
                for entry in removed_log:
                    f.write(f"Removed: U+{entry['codepoint']:04X} {entry['name']} {entry['char']} at pos {entry['position']} | line: {entry['line']}\n")
                f.write("=== End of Audit ===\n")
        return suspicious_found

    def file_hash(self, file_path):
        """
        Calculate the SHA256 hash of a file.
        Args:
            file_path (str): Path to the file.
        Returns:
            str: SHA256 hex digest, or None if file not found.
        """
        try:
            with open(file_path, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            if self.debug:
                print(f"[DEBUG] Could not hash {file_path}: {e}")
            return None

    def scan_file(self, file_path):
        """
        Scan a file and optionally sanitize it. Handles backup and sanitize-only modes.
        Args:
            file_path (str): Path to the file to scan.
        Returns:
            list: List of suspicious characters found.
        """
        pre_hash = self.file_hash(file_path)
        if self.verbose:
            print(f"[INFO] Pre-scan hash for {file_path}: {pre_hash}")
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            if not self.quiet:
                print(f"Error reading {file_path}: {e}")
            return []

        if self.sanitize_only:
            if self.backup:
                self.backup_file(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.sanitize_text(content))
            post_hash = self.file_hash(file_path)
            if self.verbose:
                print(f"[INFO] Post-sanitize hash for {file_path}: {post_hash}")
            if not self.quiet:
                print(f"Sanitization complete for {file_path} (sanitize-only mode).")
            return []

        findings = self.detect_suspicious_chars(content)

        if not findings:
            logging.info(f"No suspicious characters found in {file_path}. ✅")
            if not self.quiet:
                print(f"✅ {file_path} is clean!")
            return []

        if self.sanitize:
            if self.backup:
                self.backup_file(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(self.sanitize_text(content))
            post_hash = self.file_hash(file_path)
            if self.verbose:
                print(f"[INFO] Post-sanitize hash for {file_path}: {post_hash}")
            if not self.quiet:
                print(f"Sanitization complete for {file_path}.")

        if self.verbose or self.debug:
            for cp, name, char, idx in findings:
                print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {idx}")
        return findings

    def scan_directory(self, directory_path):
        """
        Scan all files in a directory using parallel processing for performance.
        Args:
            directory_path (str): Path to the directory to scan.
        Returns:
            dict: Mapping of file names to findings (for reporting).
        """
        if not os.path.isdir(directory_path):
            logging.error(f"Invalid directory: {directory_path}")
            if not self.quiet:
                print(f"Invalid directory: {directory_path}")
            return {}

        files = [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]
        if not self.quiet:
            print(f"🔍 Scanning {len(files)} files in parallel...")

        cpu_count = os.cpu_count() or 1
        max_workers = min(4, max(1, cpu_count // 2))
        results = {}
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            scan_results = list(executor.map(self.scan_file, files))
        for file_path, findings in zip(files, scan_results):
            if findings:
                results[file_path] = findings
        return results

    def report(self, results, output_path=None):
        """
        Print or save a JSON report of suspicious character findings.
        Args:
            results (dict): Mapping of file paths to findings.
            output_path (str or None): If given, write report to this file; else print to stdout.
        """
        report_data = {}
        for file_path, findings in results.items():
            report_data[file_path] = [
                {"codepoint": cp, "name": name, "char": repr(char)} for cp, name, char in findings
            ]
        report_json = json.dumps(report_data, indent=4, ensure_ascii=False)
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_json)
            print(f"\n📄 Report written to {output_path}")
        else:
            print("\n=== Suspicious Character Report ===")
            print(report_json)
            print("===================================")
        logging.info("Report generated.")
        if not self.quiet:
            print("Report generated.")

    def sanitize_text_from_stream(self, text):
        """
        Sanitize text from a stream (e.g., stdin) and return the sanitized text.
        Args:
            text (str): The text to sanitize.
        Returns:
            str: Sanitized text.
        """
        return self.sanitize_text(text)
    
    def set_custom_hunted_chars(self, hunted_chars):
        """
        Set custom characters to hunt for during scanning.
        Args:
            hunted_chars (list): List of characters to hunt for.
        """
        self.UNICODE_SUSPICIOUS_CODEPOINTS = set(hunted_chars)
        logging.info(f"Custom hunted characters set: {self.UNICODE_SUSPICIOUS_CODEPOINTS}")
        if not self.quiet:
            print(f"Custom hunted characters set: {self.UNICODE_SUSPICIOUS_CODEPOINTS}")

    def set_custom_ascii_control_names(self, custom_names):
        """
        Set custom names for ASCII control characters.
        Args:
            custom_names (dict): Dictionary mapping codepoints to custom names.
        """
        self.ASCII_CONTROL_NAMES.update(custom_names)
        logging.info(f"Custom ASCII control names set: {self.ASCII_CONTROL_NAMES}")
        if not self.quiet:
            print(f"Custom ASCII control names set: {self.ASCII_CONTROL_NAMES}")

    def set_log_file(self, log_file):
        """
        Set a custom log file for logging.
        Args:
            log_file (str): Path to the log file.
        """
        self.log_file = log_file
        logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG if self.debug else logging.INFO)
        logging.info(f"Log file set to: {self.log_file}")
        if not self.quiet:
            print(f"Log file set to: {self.log_file}")
        # Set the log file for the class
        self.__class__.log_file = log_file
        # Update the logger's file handler
        for handler in logging.getLogger().handlers:
            if isinstance(handler, logging.FileHandler):
                handler.baseFilename = log_file
                handler.stream = open(log_file, 'a', encoding='utf-8')
                break
        logging.info(f"Log file updated to: {self.log_file}")
        if not self.quiet:
            print(f"Log file updated to: {self.log_file}")

    def backup_file(self, file_path):
        """
        Create a backup of the file before sanitization. If a backup already exists, only create a new one if the content hash is different.
        Args:
            file_path (str): Path to the file to back up.
        """
        import shutil
        import datetime
        if self.backup:
            backup_path = f"{file_path}.bak"
            current_hash = self.file_hash(file_path)
            # Find all existing backups
            import glob
            backup_candidates = sorted(glob.glob(f"{file_path}.bak*"))
            # Check if any backup has the same hash
            for candidate in backup_candidates:
                with open(candidate, 'rb') as f:
                    backup_hash = hashlib.sha256(f.read()).hexdigest()
                if current_hash == backup_hash:
                    logging.info(f"Backup already exists and is identical: {candidate}")
                    print(f"Backup already exists and is identical: {candidate}")
                    return
            # If no identical backup, create a new one (timestamp if needed)
            if os.path.exists(backup_path):
                timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                backup_path = f"{file_path}.bak.{timestamp}"
            shutil.copy2(file_path, backup_path)
            logging.info(f"Backup created: {backup_path}")
            print(f"Backup created: {backup_path}")
        else:
            logging.warning("Backup feature is disabled. No backup created.")
            print("Backup feature is disabled. No backup created.")

    def restore_file(self, file_path):
        """
        Restore the original file from the backup. If multiple backups exist, restores from the oldest .bak file.
        Args:
            file_path (str): Path to the file to restore.
        """
        import glob
        backup_candidates = sorted(glob.glob(f"{file_path}.bak*"))
        if not backup_candidates:
            logging.warning("No backup found. Cannot restore.")
            print("No backup found. Cannot restore.")
            return False
        # Always restore from the first backup (oldest)
        backup_path = backup_candidates[0]
        with open(backup_path, 'r', encoding='utf-8') as backup_file:
            original_content = backup_file.read()
        with open(file_path, 'w', encoding='utf-8') as original_file:
            original_file.write(original_content)
        logging.info(f"File restored from backup: {file_path}")
        print(f"File restored from backup: {file_path}")
        # Do NOT remove the backup file (keep for audit)
        return True
    
    def sanitize_file(self, file_path):
        """
        Sanitize a file in-place, removing suspicious characters. Creates a backup unless backup is False.
        Args:
            file_path (str): Path to the file to sanitize.
        Returns:
            bool: True if sanitized, False if file was already clean or error occurred.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            logging.error(f"Error reading {file_path}: {e}")
            if not self.quiet:
                print(f"Error reading {file_path}: {e}")
            return False
        findings = self.detect_suspicious_chars(content)
        if not findings:
            if not self.quiet:
                print(f"No suspicious characters found in {file_path}. No changes made.")
            return False
        if self.backup:
            self.backup_file(file_path)
        sanitized = self.sanitize_text(content)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(sanitized)
        if not self.quiet:
            print(f"Sanitization complete for {file_path}.")
        return True

    def sanitize_directory(self, directory_path):
        """
        Sanitize all files in a directory, creating backups unless backup is False.
        Args:
            directory_path (str): Path to the directory to sanitize.
        Returns:
            dict: Mapping of file names to True (sanitized) or False (already clean or error).
        """
        if not os.path.isdir(directory_path):
            logging.error(f"Invalid directory: {directory_path}")
            if not self.quiet:
                print(f"Invalid directory: {directory_path}")
            return {}
        files = [
            os.path.join(directory_path, f)
            for f in os.listdir(directory_path)
            if os.path.isfile(os.path.join(directory_path, f))
        ]
        results = {}
        for file_path in files:
            results[file_path] = self.sanitize_file(file_path)
        return results
# CLI usage
# This section allows the script to be run from the command line with arguments.
# It uses argparse to handle command-line arguments and options.
# It provides options for sanitization, logging, and reporting.
# The script can scan files or directories, and it can also read from standard input (PIPE).
# This is a simple command-line interface (CLI) for the ByteSleuth class.
# It allows users to scan files or directories for suspicious characters, with options for sanitization and logging.
# The script can be run directly from the command line, and it supports both file and directory scanning.
# It also provides options for sanitization and logging, and can read from standard input (PIPE).
# This section is executed when the script is run directly.

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Suspicious character scanner (Unicode & ASCII)")
    parser.add_argument("target", nargs="?", help="File or directory to scan (or use PIPE input)")
    parser.add_argument("-s", "--sanitize", action="store_true", help="Enable automatic sanitization")
    parser.add_argument("-l", "--log", default="scanner.log", help="Log file path")
    parser.add_argument("-r", "--report", nargs="?", default="", help="Print JSON report to stdout or save to file if a path is provided.")
    parser.add_argument("-f", "--no-backup", action="store_true", default=False, help="Disable backup creation")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug output")
    parser.add_argument("-q", "--quiet", action="store_true", help="Suppress all output except errors")
    parser.add_argument("-S", "--sanitize-only", action="store_true", help="Only sanitize the input, do not scan")
    parser.add_argument("-F", "--fail-on-detect", action="store_true", help="Exit with code 1 if suspicious characters are found")
    parser.add_argument("-V", "--version", action="version", version="%(prog)s 1.0", help="Show version and exit")
    args = parser.parse_args()

    backup = not args.no_backup
    scanner = ByteSleuth(
        sanitize=args.sanitize,
        backup=backup,
        log_file=args.log,
        verbose=args.verbose,
        debug=args.debug,
        quiet=args.quiet,
        sanitize_only=args.sanitize_only
    )

    suspicious_found = False
    if args.target:
        if os.path.isdir(args.target):
            results = scanner.scan_directory(args.target)
            if args.report:
                output_path = args.report if isinstance(args.report, str) and args.report else None
                scanner.report(results, output_path=output_path)
            # Always print findings summary for VSCode/CLI
            if results:
                print("\n=== Suspicious Character Report ===")
                for file_path, findings in results.items():
                    print(f"\nFile: {file_path}")
                    for cp, name, char, idx in findings:
                        print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {idx}")
                suspicious_found = True
            else:
                print("\n✅ All files in the directory are clean!")
        elif os.path.isfile(args.target):
            findings = scanner.scan_file(args.target)
            if args.report:
                output_path = args.report if isinstance(args.report, str) and args.report else None
                scanner.report({args.target: findings}, output_path=output_path)
            # Always print findings summary for VSCode/CLI
            if findings:
                print("\n=== Suspicious Character Report ===")
                print(f"File: {args.target}")
                for cp, name, char, idx in findings:
                    print(f"  - U+{cp:04X} {name} ({repr(char)}) at position {idx}")
                suspicious_found = True
            else:
                print(f"\n✅ {args.target} is clean!")
        else:
            if not args.quiet:
                print("Error: Invalid path. Provide an existing file or directory.")
            exit(1)
    else:
        if not args.quiet:
            print("⏳ Reading from PIPE...")
        suspicious_found = scanner.process_stdin()

    if not args.quiet:
        print("\n✅ Scan finished! Check the log for details.")
    logging.info("✅ Scan finished! Check the log for details.")
    if args.fail_on_detect and suspicious_found:
        exit(1)
    exit(0)


# Note: The script can be run from the command line with various options.
# Usage examples:
# python byte_sleuth.py /path/to/file.txt -s -l my_log.log
# python byte_sleuth.py /path/to/directory
# cat file.txt | python byte_sleuth.py -s > sanitized.txt