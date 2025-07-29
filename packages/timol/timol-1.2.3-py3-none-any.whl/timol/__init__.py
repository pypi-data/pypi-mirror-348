import pathlib

from importlib_metadata import version

__version__ = version("timol")

package_dir = pathlib.Path(__file__).resolve().parent  # src/timol
flag_file = package_dir / ".initialized"
if not flag_file.exists():
    try:
        flag_file.write_text(__version__)
        print(
            "Timol is running for the first time: startup time might be slower due to bytecode compilation and initialization"
        )
    except OSError:
        # Not writeable or smth, so we just don't say anything
        # It is what it is
        pass
else:
    # Keep track of the version it loaded last
    # Potentially useful in the future, why not
    vers = flag_file.read_text()
    if vers != __version__:
        flag_file.write_text(__version__)

from .cli import bmark, cli
