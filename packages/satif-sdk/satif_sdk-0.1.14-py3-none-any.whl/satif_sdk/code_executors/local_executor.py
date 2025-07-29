import csv
import inspect
import io
import json
import logging
import os
import re
import sqlite3
import unicodedata
import uuid
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, Optional

import numpy as np
import pandas as pd
from satif_core import CodeExecutor, SDIFDatabase
from satif_core.exceptions import CodeExecutionError
from sdif_db import cleanup_db_connection, create_db_connection

logger = logging.getLogger(__name__)


class LocalCodeExecutor(CodeExecutor):
    """
    Executes user-provided Python code strings locally using Python's built-in `exec`.

    This executor is responsible for:
    1. Setting up an SQLite database environment based on provided SDIF source file paths.
       This includes creating an in-memory database (if multiple sources) or connecting
       to a single source, and then ATTACHing all specified SDIF files as schemas.
    2. Executing a given `code` string in an environment where this database connection
       is accessible, along with other standard libraries and provided `extra_context`.
    3. Identifying a specific function within the executed `code` by its `function_name`.
    4. Calling this identified function, passing it the live SQLite connection and context.
    5. Returning the result produced by the called function.
    6. Ensuring the database connection is properly closed and resources are cleaned up.

    **Security Warning:**
    This executor runs arbitrary Python code directly on the host machine where it is instantiated.
    It provides **NO SANDBOXING OR SECURITY ISOLATION**. Therefore, it should **ONLY** be used
    in trusted environments and with code from trusted sources.
    """

    _DEFAULT_INITIAL_CONTEXT: Dict[str, Any] = {
        "pd": pd,
        "json": json,
        "Path": Path,
        "sqlite3": sqlite3,
        "datetime": datetime,
        "timedelta": timedelta,
        "re": re,
        "uuid": uuid,
        "os": os,
        "io": io,
        "BytesIO": BytesIO,
        "csv": csv,
        "np": np,
        "unicodedata": unicodedata,
        "SDIFDatabase": SDIFDatabase,
    }

    def __init__(self, initial_context: Optional[Dict[str, Any]] = None):
        """
        Initializes the LocalCodeExecutor.

        Args:
            initial_context:
                An optional dictionary of global variables to make available
                during code execution. These will be merged with (and can
                override) the default set of globals provided by the executor.
        """
        self._resolved_initial_globals = self._DEFAULT_INITIAL_CONTEXT.copy()
        if initial_context:
            self._resolved_initial_globals.update(initial_context)

    def execute(
        self,
        code: str,
        function_name: str,
        sdif_sources: Dict[str, Path],
        extra_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Sets up a database from SDIF sources, executes the code string to define a function,
        then calls that function with the database connection and context.

        Args:
            code:
                A string containing the Python script to be executed. This script
                is expected to define the function identified by `function_name`.
                It can include imports, helper functions, and class definitions
                as needed for the main transformation function.
            function_name:
                The name of the function (defined in `code`) to be invoked.
            sdif_sources:
                A dictionary mapping schema names (str) to resolved `Path` objects
                of the SDIF database files. This executor will create/connect to
                an SQLite database and ATTACH these sources.
            extra_context:
                A dictionary of additional objects and data to be made available
                to the transformation logic.
                - The entire `extra_context` dictionary is passed as the `context`
                  argument to the transformation function if its signature includes it.
                - Additionally, all key-value pairs in `extra_context` are injected
                  as global variables into the environment where the `code` string
                  is initially executed. If `extra_context` contains keys that
                  match standard globals (e.g., 'pd', 'json') or the explicitly
                  provided 'conn' or 'context' globals, they will be overwritten
                  in that global scope.

        Returns:
            A dictionary, which is the result of calling the user-defined
            transformation function (`function_name`). The keys are typically
            output filenames, and values are the data to be written.

        Raises:
            CodeExecutionError: If any error occurs during the process, including:
                - Database setup errors from `db_utils`.
                - Syntax errors in the `code` string.
                - The specified `function_name` not being found after executing `code`.
                - The identified `function_name` not being a callable function.
                - The function having an incompatible signature (e.g., not accepting `conn`).
                - The function not returning a dictionary.
                - Any exception raised during the execution of the user's transformation function.
        """
        db_conn: Optional[sqlite3.Connection] = None
        attached_schemas: Dict[str, Path] = {}

        try:
            db_conn, attached_schemas = create_db_connection(sdif_sources)

            execution_globals = {
                **self._resolved_initial_globals,
                "conn": db_conn,
                "context": extra_context,
                "__builtins__": __builtins__,
                **extra_context,  # extra_context can override defaults or even conn/context in globals
            }
            execution_locals = {}

            logger.warning(
                f"Executing user-provided code locally to define and run function '{function_name}'. "
                "This is insecure and should only be used in trusted environments."
            )

            compiled_code = compile(code, "<code_string>", "exec")
            exec(compiled_code, execution_globals, execution_locals)

            if function_name not in execution_locals:
                raise CodeExecutionError(
                    f"Function '{function_name}' not found after executing code string."
                )

            transform_func = execution_locals[function_name]
            if not callable(transform_func):
                raise CodeExecutionError(
                    f"'{function_name}' defined in code is not a callable function."
                )

            sig = inspect.signature(transform_func)
            param_names = list(sig.parameters.keys())
            func_result: Any

            if "conn" in param_names and "context" in param_names:
                func_result = transform_func(conn=db_conn, context=extra_context)
            elif "conn" in param_names:
                func_result = transform_func(conn=db_conn)
            else:
                raise CodeExecutionError(
                    f"Transformation function '{function_name}' must accept 'conn' parameter. Signature: {param_names}"
                )

            if not isinstance(func_result, dict):
                raise CodeExecutionError(
                    f"Function '{function_name}' must return a Dict. Got {type(func_result)}."
                )

            return {str(k): v for k, v in func_result.items()}

        except (
            CodeExecutionError
        ):  # Re-raise CodeExecutionErrors directly (e.g., from db_utils or logic above)
            raise
        except Exception as e:
            logger.exception(
                f"Error during local execution for function '{function_name}':"
            )
            # Wrap other unexpected exceptions in CodeExecutionError
            raise CodeExecutionError(
                f"An error occurred in LocalCodeExecutor for function '{function_name}': {e}"
            ) from e
        finally:
            # Use the new db_utils function for cleanup
            # It handles db_conn being None and logs errors during detach/close internally
            cleanup_db_connection(db_conn, attached_schemas, should_close=True)
