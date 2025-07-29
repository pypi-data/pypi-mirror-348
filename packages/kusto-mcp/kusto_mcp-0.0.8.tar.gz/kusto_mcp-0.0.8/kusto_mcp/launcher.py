import os
import platform
import sys
from pathlib import Path


def get_executable_path() -> str:
    """Get the path to the platform-specific executable."""
    system = platform.system().lower()

    # Get the package directory path
    package_dir = Path(__file__).parent
    bin_dir = package_dir / "bin"

    if system == "windows":
        executable = "kusto-mcp.exe"
    elif system == "darwin":
        executable = "kusto-mcp-macos"
    else:
        executable = "kusto-mcp-linux"

    executable_path = bin_dir / executable

    if not executable_path.exists():
        raise RuntimeError(
            f"Could not find executable for your platform ({system}). Expected at: {executable_path}"
        )

    # Ensure the executable has the right permissions on Unix-like systems
    if system != "windows" and not os.access(executable_path, os.X_OK):
        os.chmod(executable_path, 0o755)

    return str(executable_path)


def run() -> None:
    """Run the platform-specific executable."""
    try:
        executable_path = get_executable_path()
        os.execv(executable_path, [executable_path] + sys.argv[1:])
    except Exception as e:
        print(f"Error launching kusto-mcp: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    run()
