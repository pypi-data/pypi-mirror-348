import os
import subprocess
import json
import pandas as pd
import shutil

from pathlib import Path

def get_executable_path():
    """
    Get the path to the vfp_to_json.exe executable by checking multiple locations.

    Order of search:
    1. Environment variable 'VFP_TO_JSON_PATH'
    2. Package directory's bin folder
    3. Current working directory
    4. System PATH
    """
    # 1. Check environment variable
    env_path = os.getenv('VFP_TO_JSON_PATH')
    if env_path:
        env_exe = Path(env_path)
        if env_exe.exists() and env_exe.is_file():
            return str(env_exe)

    # 2. Check package's bin folder (relative to this file)
    package_dir = Path(__file__).resolve().parent
    bin_path = package_dir / 'bin' / 'vfp_to_json.exe'
    if bin_path.exists() and bin_path.is_file():
        return str(bin_path)

    # 3. Check current working directory
    cwd_exe = Path(os.getcwd()) / 'vfp_to_json.exe'
    if cwd_exe.exists() and cwd_exe.is_file():
        return str(cwd_exe)

    # 4. Check system PATH
    system_exe = shutil.which('vfp_to_json.exe')
    if system_exe:
        return system_exe

    # If all checks fail
    raise FileNotFoundError(
        "vfp_to_json.exe not found in any of the following locations:\n"
        "1. Environment variable 'VFP_TO_JSON_PATH'\n"
        "2. Package directory's bin folder\n"
        "3. Current working directory\n"
        "4. System PATH"
    )

def run_vfp_to_json(connection_string, sql_query):
    """
    Runs the vfp_to_json.exe with the given connection string and SQL query.

    Args:
        connection_string (str): The database connection string.
        sql_query (str): The SQL query to execute.

    Returns:
        dict or list: The JSON output parsed into Python objects.
    """
    exe_path = get_executable_path()

    # Ensure the executable has execute permissions
    if not os.access(exe_path, os.X_OK):
        # Attempt to set execute permissions
        try:
            os.chmod(exe_path, 0o755)
        except Exception as e:
            raise PermissionError(f"Cannot execute {exe_path}: {e}")

    # Prepare the command
    cmd = [
        exe_path,
        connection_string,
        sql_query
    ]

    try:
        # Execute the command and capture stdout and stderr
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False  # Change to False to handle errors manually
        )
    except Exception as e:
        raise RuntimeError(f"Failed to run vfp_to_json.exe: {e}") from e

    if result.returncode != 0:
        raise RuntimeError(f"vfp_to_json.exe failed with return code {result.returncode}:\n{result.stderr}")

    # Parse JSON output
    try:
        json_output = json.loads(result.stdout.replace("\n","").replace("  ", " ").replace("  ", " ").replace("  ", " ").replace("  ", " "))
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON output: {e}") from e

    return json_output

def to_dataframe(connection_string, sql_query):
    """
    Executes the SQL query using vfp_to_json.exe and returns the result as a pandas DataFrame.

    Args:
        connection_string (str): The database connection string.
        sql_query (str): The SQL query to execute.

    Returns:
        pandas.DataFrame: The query result.
    """
    json_data = run_vfp_to_json(connection_string, sql_query)

    if isinstance(json_data, list):
        # Assuming the JSON is a list of records
        df = pd.DataFrame(json_data)
    elif isinstance(json_data, dict):
        # If JSON is a single record
        df = pd.DataFrame([json_data])
    else:
        raise TypeError("Unexpected JSON format")

    return df
