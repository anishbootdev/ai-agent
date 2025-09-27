# python
import os
import types
from config import MAX_CHARS
import subprocess
from google.genai import types


def get_files_info(working_directory, directory="."):
    try:
        wd_abs = os.path.abspath(working_directory)
        target_abs = os.path.abspath(os.path.join(working_directory, directory))

        if not target_abs.startswith(wd_abs):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_abs):
            return f'Error: "{directory}" is not a directory'

        entries = []
        for name in os.listdir(target_abs):
            path = os.path.join(target_abs, name)
            size = os.path.getsize(path)
            is_dir = os.path.isdir(path)
            entries.append(f"- {name}: file_size={size} bytes, is_dir={is_dir}")

        return "\n".join(entries)
    except Exception as e:
        return f"Error: {e}"
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    function_call_part(**{"working_directory": "./calculator"})
