

import os
from pathlib import Path
from typing import List, Dict, Any
import re

from .utils import console, secs_to_hms

def export_modern_html(base: Path, transcript: List[Dict[str, Any]], notes_aligned: List[Dict[str, Any]]):
    
    
    html_path = base.parent / f"{base.stem}_transcript.html"
    audio_path = base.name  
    
    
    from . import cli
    version = getattr(cli, '__version__', '0.4.2')
    
    
    template_path = Path(__file__).parent / "templates" / "transcript_template.html"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
    
    
    notes_content = []
    if notes_aligned:
        for note in notes_aligned:
            time_seconds = note['time_seconds']
            time_hms = note['time_hms']
            note_text = note['note']
            segment_text = note['segment_text']
            
            note_html = f'''
            <div class="note-card" id="note-{int(time_seconds)}">
                <div class="note-header">
                    <div class="note-title">📝 {note_text}</div>
                    <div class="timestamp" data-time="{time_seconds}">
                        <svg class="icon" viewBox="0 0 24 24">
                            <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                        {time_hms}
                    </div>
                </div>
                <div class="note-context">{segment_text}</div>
            </div>
            '''
            notes_content.append(note_html)
    else:
        notes_content.append('<p>No notes available for this recording.</p>')
    
    
    transcript_content = []
    if transcript:
        for segment in transcript:
            start = segment['start']
            end = segment['end']
            text = segment['text']
            hms_start = secs_to_hms(start)
            hms_end = secs_to_hms(end)
            segment_id = f'segment-{int(start)}'
            
            segment_html = f'''
            <div class="transcript-segment" id="{segment_id}" data-start="{start}" data-end="{end}">
                <div class="segment-header">
                    <div class="timestamp" data-time="{start}">
                        <svg class="icon" viewBox="0 0 24 24">
                            <polygon points="5 3 19 12 5 21 5 3"></polygon>
                        </svg>
                        {hms_start}
                    </div>
                    <div class="segment-time">→ {hms_end}</div>
                </div>
                <div class="segment-text">{text}</div>
            </div>
            '''
            transcript_content.append(segment_html)
    else:
        transcript_content.append('<p>No transcript segments available.</p>')
    
    
    html_content = template.replace('{{title}}', f'Transcript for {base.name}')
    html_content = html_content.replace('{{notes_content}}', '\n'.join(notes_content))
    html_content = html_content.replace('{{transcript_content}}', '\n'.join(transcript_content))
    html_content = html_content.replace('{{audio_path}}', audio_path)
    html_content = html_content.replace('{{version}}', version)
    html_content = html_content.replace('{{filename}}', html_path.stem)
    
    
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    console.log(f"🌐 Modern HTML transcript saved to {html_path}")
    return html_path
