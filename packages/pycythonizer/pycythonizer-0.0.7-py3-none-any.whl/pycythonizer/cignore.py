# Open cignore file to
from pathlib import Path
from typing import List

def should_ignore(source_dir: Path) -> List:
    cignore_file = Path(source_dir) / ".cignore"
    if cignore_file.exists():
        with open(cignore_file, 'r') as cignore:
            patterns = [line.strip() for line in cignore if not line.startswith("#") and line.strip()]
        return patterns
    else:
        return []
            


