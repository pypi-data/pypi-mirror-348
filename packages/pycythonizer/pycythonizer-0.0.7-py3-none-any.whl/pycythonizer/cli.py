import click
import logging
from pathlib import Path
from .compiler import compile_project
from .log import setup_logging

setup_logging(logging.DEBUG)


logger = logging.getLogger(__name__)


@click.command()
@click.argument("source_dir", required=False, type=click.Path(exists=True, path_type=Path), default=Path.cwd())
@click.option("--entry-point", "-i", type=click.Path(path_type=Path), default=None)
@click.option("--output-dir", "-o", type=click.Path(path_type=Path), default=None)
def main(source_dir: Path = Path.cwd(), entry_point: Path = None, output_dir: Path= Path.cwd() / "build"):
    """Compile_Python files in source directory into Cython binaries"""
    compile_project(source_dir, entry_point, output_dir)
    logger.info("Compilation complete")

if __name__ == "__main__":
        main()
        

