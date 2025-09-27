# python
import os
import sys
import types
from config import MAX_CHARS
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        wd_abs = os.path.abspath(working_directory)
        file_abs = os.path.abspath(os.path.join(working_directory, file_path))
        if not file_abs.startswith(wd_abs):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_abs):
            return f'Error: File "{file_path}" not found.'
        if file_path[-3:] != ".py":
            return f'Error: File "{file_path}" is not a Python file.'
        result = subprocess.run(
            [sys.executable, file_abs] + (args or []),
            timeout=30,
            capture_output=True,
            text=True,
        )
        stdout = result.stdout or ""
        stderr = result.stderr or ""
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}\nSTDOUT:\n{stdout}\nSTDERR:\n{stderr}"
        if not stdout.strip() and not stderr.strip():
            return "No output produced"
        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(type=types.Type.STRING),
                description="Optional list of string arguments to pass to the Python file.",
            ),
        },
        required=["file_path"],
    ),
)
