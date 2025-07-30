import os
import sys
import shutil
import platform
import atexit
import tempfile
import logging
from setuptools import setup, Extension
from Cython.Build import cythonize
from pathlib import Path
from .cignore import should_ignore


logger = logging.getLogger(__name__)


def compile_project(source_dir: Path, entry_point: Path = None, output_dir: Path = None, clean_temp: bool = True):
    """Compiles python files in the source dir to Cython binaries except for the entry_point
       If the entry point doesn't exist it compiles everything. None python files are copied
       to the output dir.
       Args:
            source_dir: Path to you python source code / project
            ouput_dir: Path to save the compiled files default = CWD
            entry_point: The entry point to your code. Will not be compiled
            clean_temp: Whether or not to clean the temp folder afterwards
    """
    logger.info("Starting Compilation")
    source_dir = source_dir or Path(__file__).resolve().parent
    output_dir: Path = output_dir or source_dir / "build"
    build_temp: Path = Path(tempfile.gettempdir()) / "cython_temp"
    if entry_point:
        entry_point: Path = Path(entry_point).resolve()
        print(entry_point)
    else:
        entry_point = None

    # Build extensions list
    extensions: list = []
    for root, dirs, files in os.walk(source_dir):
        ignored_dirs = []
        for pattern in should_ignore(source_dir):
            ignored_dirs.extend(Path(root).glob(pattern))
            
        ignored_dirs = {p.resolve() for p in ignored_dirs}
        dirs[:] = [d for d in dirs if (Path(root) / d ).resolve() not in ignored_dirs]
        for file in files:
            if file.endswith((".pyc", ".pyo")):
                continue

            abs_path: Path = Path(root) / file
            rel_path: Path = abs_path.relative_to(source_dir)

            if file.endswith(".py") and not file.startswith("__init__"):
                # Copy the entry point to the output dir
                if entry_point:
                    if abs_path.resolve() == entry_point.resolve():
                        target_entry_point = output_dir / rel_path
                        target_entry_point.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copyfile(abs_path, target_entry_point)
                        continue
                
                # Convert .py to .pyx and prepare for compilation
                target_pyx = build_temp / rel_path.with_suffix(".pyx")
                target_pyx.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(abs_path, target_pyx)
                extensions.append(Extension(
                    name=".".join(rel_path.with_suffix("").parts),
                    sources=[str(target_pyx)]
                ))
            else:
                # Copy non-Python files directly
                target = output_dir / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(abs_path, target)
        
        # Compile
        setup(
            script_args=[
                "build_ext",
                "--build-lib", str(output_dir),
                "--build-temp", str(build_temp),
            ],
            ext_modules=cythonize(
                extensions,
                compiler_directives={
                    "language_level": "3",
                    "embedsignature": True,
                },
                build_dir=str(build_temp / "cython_build"),
                nthreads=4
            )
        )

        if clean_temp:
            atexit.register(lambda: shutil.rmtree(build_temp, ignore_errors=True))
            atexit.register(lambda: shutil.rmtree(
                output_dir / f"{platform.system().lower()[:3]}-{platform.machine().lower()}-cpython-{sys.version_info.major}{sys.version_info.minor}",
                ignore_errors=True
            ))
        