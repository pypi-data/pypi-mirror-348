

import json
from pathlib import Path
from typing import List, Dict, Any

from .utils import console, secs_to_hms

def export_markdown(base: Path, transcript: List[Dict[str, Any]], notes_aligned: List[Dict[str, Any]]):
    
    
    md_path = base.parent / f"{base.stem}_transcript.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# Transcript for {base.name}\n\n")
        f.write("## Notes with Context\n\n")
        for n in notes_aligned:
            f.write(f"### 📝 {n['note']} ({n['time_hms']})\n")
            f.write(f"> {n['segment_text']}\n\n")
        f.write("---\n\n## Full Transcript\n\n")
        for seg in transcript:
            hms_start = secs_to_hms(seg["start"])
            hms_end = secs_to_hms(seg["end"])
            f.write(f"[{hms_start} → {hms_end}] {seg['text']}\n\n")
    console.log(f"📝 Markdown saved to {md_path}")


def export_json(base: Path, transcript: List[Dict[str, Any]], notes: List[Dict[str, Any]], 
                notes_aligned: List[Dict[str, Any]]):
    
    data = {
        "transcript": transcript,
        "notes": notes,
        "notes_aligned": notes_aligned,
    }
    
    json_path = base.parent / f"{base.stem}_transcript.json"
    with open(json_path, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    console.log(f"🗄️  JSON saved to {json_path}")


def export_txt(base: Path, transcript: List[Dict[str, Any]]):
    
    
    txt_path = base.parent / f"{base.stem}_transcript.txt"
    
    
    text_content = '\n'.join(seg['text'] for seg in transcript)
    
    
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(text_content)
    
    console.log(f"📄 Plain text saved to {txt_path}")
