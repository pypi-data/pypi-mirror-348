import csv
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from charset_normalizer import detect as charset_detect  # For encoding detection
from satif_core.representers.base import Representer

log = logging.getLogger(__name__)

ENCODING_SAMPLE_SIZE = 1024 * 4  # Reduced sample size for representation context
DELIMITER_SAMPLE_SIZE_LINES = 10  # Number of lines for delimiter sniffing


class CsvRepresenter(Representer):
    """
    Generates representation for CSV files.
    Can be initialized with default encoding and delimiter.
    """

    def __init__(
        self,
        default_delimiter: Optional[str] = None,
        default_encoding: str = "utf-8",
        default_num_rows: int = 10,
    ):
        """
        Initialize CsvRepresenter.

        Args:
            default_delimiter: Default CSV delimiter. Auto-detected if None.
            default_encoding: Default file encoding.
            default_num_rows: Default number of data rows to represent.
        """
        self.default_delimiter = default_delimiter
        self.default_encoding = default_encoding
        self.default_num_rows = default_num_rows

    def _detect_encoding(self, file_path: Path) -> str:
        """
        Detects file encoding using charset_normalizer.
        Returns detected encoding or a default if detection fails.
        """
        try:
            with open(file_path, "rb") as fb:
                data_sample = fb.read(ENCODING_SAMPLE_SIZE)
                if not data_sample:
                    log.debug(
                        f"File {file_path} is empty, cannot detect encoding. Returning instance default: {self.default_encoding}"
                    )
                    return self.default_encoding  # Default for empty file

                detection_result = charset_detect(data_sample)
                detected_encoding = (
                    detection_result.get("encoding") if detection_result else None
                )

                if detected_encoding:
                    log.debug(f"Detected encoding for {file_path}: {detected_encoding}")
                    return detected_encoding
                else:
                    log.warning(
                        f"Encoding detection failed for {file_path}. Using instance default: {self.default_encoding}"
                    )
                    return self.default_encoding
        except Exception as e:
            log.warning(
                f"Error during encoding detection for {file_path}: {e}. Using instance default: {self.default_encoding}"
            )
            return self.default_encoding

    def _detect_delimiter(self, file_path: Path, encoding: str) -> Optional[str]:
        """
        Detects CSV delimiter using csv.Sniffer.
        Returns detected delimiter or None if detection fails.
        """
        try:
            with open(file_path, encoding=encoding, newline="") as f_sniff:
                # Read a sample of lines for sniffing
                sample_lines = [
                    line for _, line in zip(range(DELIMITER_SAMPLE_SIZE_LINES), f_sniff)
                ]
                sample_text = "".join(sample_lines)
                if not sample_text.strip():  # Ensure sample is not just whitespace
                    log.debug(
                        f"File {file_path} sample is empty or whitespace, cannot detect delimiter."
                    )
                    return None

                sniffer = csv.Sniffer()
                # Provide a common set of delimiters to help the sniffer
                dialect = sniffer.sniff(sample_text, delimiters=",;\\t|:")
                if dialect and dialect.delimiter:
                    log.debug(
                        f"Detected delimiter for {file_path}: '{dialect.delimiter}'"
                    )
                    return dialect.delimiter
                log.warning(
                    f"Delimiter detection failed for {file_path} using Sniffer."
                )
                return None
        except (csv.Error, UnicodeDecodeError) as e:
            log.warning(
                f"CSV Sniffer error for {file_path} (encoding: {encoding}): {e}. Delimiter detection failed."
            )
            return None
        except Exception as e:
            log.warning(
                f"Unexpected error during delimiter detection for {file_path}: {e}"
            )
            return None

    def represent(
        self,
        file_path: Union[str, Path],
        num_rows: Optional[int] = None,  # Allow None to use instance default
        **kwargs: Any,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Generates a string representation of a CSV file by showing
        the header and the first N data rows.

        Kwargs Options:
            encoding (str): File encoding. Overrides instance default.
            delimiter (str): CSV delimiter. Overrides instance default.

        Returns:
            Tuple[str, Dict[str, Any]]:
                - The string representation.
                - A dictionary containing used parameters: 'encoding' and 'delimiter'.
        """
        file_path = Path(file_path)
        actual_num_rows = num_rows if num_rows is not None else self.default_num_rows

        used_params: Dict[str, Any] = {}
        representation_lines: List[str] = []

        if not file_path.is_file():
            err_msg = f"File not found: {file_path}"
            log.error(err_msg)
            used_params["error"] = err_msg
            return f"[{err_msg}]", used_params

        # 1. Determine Encoding
        final_encoding: str = kwargs.get("encoding")
        if final_encoding:
            log.debug(f"Using encoding from kwargs: {final_encoding} for {file_path}")
        elif self.default_encoding:  # self.default_encoding is always set in __init__
            final_encoding = self.default_encoding
            log.debug(
                f"Using instance default encoding: {final_encoding} for {file_path}"
            )
        # Fallback to detection only if initial default could be None (which it can't with current __init__)
        # else:
        #     final_encoding = self._detect_encoding(file_path)
        #     log.debug(f"Detected encoding: {final_encoding} for {file_path}")
        used_params["encoding"] = final_encoding

        # 2. Determine Delimiter
        final_delimiter: Optional[str] = kwargs.get("delimiter")
        if final_delimiter:
            log.debug(
                f"Using delimiter from kwargs: '{final_delimiter}' for {file_path}"
            )
        elif self.default_delimiter is not None:
            final_delimiter = self.default_delimiter
            log.debug(
                f"Using instance default delimiter: '{final_delimiter}' for {file_path}"
            )
        else:
            final_delimiter = self._detect_delimiter(file_path, final_encoding)
            if final_delimiter:
                log.debug(f"Detected delimiter: '{final_delimiter}' for {file_path}")
            else:
                log.warning(
                    f"Failed to detect delimiter for {file_path}. Defaulting to ','"
                )
                final_delimiter = ","  # Fallback delimiter
        used_params["delimter"] = final_delimiter

        try:
            with open(
                file_path, newline="", encoding=final_encoding, errors="replace"
            ) as f:
                reader = csv.reader(f, delimiter=final_delimiter)
                try:
                    header = next(reader)
                    representation_lines.append(final_delimiter.join(header))
                    rows_read_count = 0
                    for row in reader:
                        if rows_read_count >= actual_num_rows:
                            break
                        representation_lines.append(final_delimiter.join(map(str, row)))
                        rows_read_count += 1

                    if rows_read_count < actual_num_rows and rows_read_count > -1:
                        log.debug(
                            f"Read {rows_read_count} data rows from {file_path} (less than requested {actual_num_rows})."
                        )
                    if not representation_lines:  # Empty file even before header
                        log.debug(
                            f"CSV file {file_path} appears empty before header read."
                        )
                        return "[CSV file appears empty]", used_params

                except StopIteration:
                    if representation_lines:  # Header was read but no data rows
                        log.debug(f"CSV file {file_path} has header but no data rows.")
                        representation_lines.append("[No data rows found]")
                    else:  # File was completely empty or unreadable by csv.reader
                        log.debug(
                            f"CSV file {file_path} is empty or could not be parsed by CSV reader."
                        )
                        return "[CSV file is empty or unparsable]", used_params
                except csv.Error as e:  # Catch specific CSV parsing errors
                    err_msg = f"CSV parsing error in {file_path}: {e}"
                    log.error(err_msg)
                    used_params["error"] = err_msg
                    return f"[{err_msg}]", used_params
                except Exception as e:  # Catch other unexpected errors during reading
                    err_msg = f"Error reading CSV content from {file_path}: {e}"
                    log.error(err_msg, exc_info=True)
                    used_params["error"] = err_msg
                    return f"[{err_msg}]", used_params

        except FileNotFoundError:  # Should be caught earlier, but defensive
            err_msg = f"File not found: {file_path}"
            log.error(err_msg)
            used_params["error"] = err_msg
            return f"[{err_msg}]", used_params
        except UnicodeDecodeError as e:
            err_msg = f"Encoding error opening {file_path} with encoding '{final_encoding}': {e}"
            log.error(err_msg, exc_info=True)
            used_params["error"] = err_msg
            used_params["encoding_tried"] = final_encoding
            return f"[{err_msg}]", used_params
        except Exception as e:
            err_msg = f"Error opening or processing CSV file {file_path}: {e}"
            log.error(err_msg, exc_info=True)
            used_params["error"] = err_msg
            return f"[{err_msg}]", used_params

        if not representation_lines:  # If somehow it's still empty
            return (
                "[No representation generated, file might be empty or unreadable]",
                used_params,
            )

        return "\\n".join(representation_lines), used_params
