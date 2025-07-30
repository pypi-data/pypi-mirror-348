

import sys
from datetime import timedelta
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.console import Console


console = Console()

def secs_to_hms(seconds: float) -> str:
    
    return str(timedelta(seconds=int(seconds)))

def ensure_suffix(path: str | Path, suffix: str) -> Path:
    
    p = Path(path)
    return p if p.suffix else p.with_suffix(suffix)
