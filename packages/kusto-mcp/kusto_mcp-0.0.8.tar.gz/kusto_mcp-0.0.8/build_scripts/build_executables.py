import os
import platform
import shutil
import sys
from pathlib import Path


def get_executable_name() -> str:
    system = platform.system().lower()
    if system == "windows":
        return "kusto-mcp.exe"
    elif system == "darwin":
        return "kusto-mcp-macos"
    else:
        return "kusto-mcp-linux"


def build_executable() -> None:
    # Ensure PyInstaller is installed
    try:
        import PyInstaller.__main__
    except ImportError:
        print("Installing PyInstaller...")
        os.system(f"{sys.executable} -m pip install pyinstaller")
        import PyInstaller.__main__

    executable_name = get_executable_name()

    # Create bin directory if it doesn't exist
    bin_dir = Path("kusto_mcp/bin")
    bin_dir.mkdir(exist_ok=True, parents=True)

    # Build executable
    venv_path = os.environ.get("VIRTUAL_ENV", ".venv")
    site_packages = os.path.join(venv_path, "Lib", "site-packages")
    kusto_data_path = os.path.join(site_packages, "azure", "kusto", "data")

    print(f"Looking for JSON files in: {kusto_data_path}")
    if not os.path.exists(kusto_data_path):
        raise FileNotFoundError(f"Could not find path: {kusto_data_path}")
    json_files = [f for f in os.listdir(kusto_data_path) if f.endswith(".json")]
    print(f"Found JSON files: {json_files}")

    PyInstaller.__main__.run(
        [
            "kusto_mcp/server.py",
            "--onefile",
            "--name",
            executable_name,
            "--distpath",
            str(bin_dir),
            "--clean",
            "--add-data",
            f"{kusto_data_path}/*.json{os.pathsep}azure/kusto/data",
        ]
    )

    # Clean up build artifacts
    if os.path.exists("build"):
        shutil.rmtree("build")
    if os.path.exists(f"{executable_name}.spec"):
        os.remove(f"{executable_name}.spec")


if __name__ == "__main__":
    build_executable()
