

import sys
from pathlib import Path
from typing import List, Dict, Any, Optional

from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn


try:
    from faster_whisper import WhisperModel  
except ImportError:  
    WhisperModel = None  

from .utils import console

def transcribe(audio_path: Path, model_size: str, device: str = "auto", 
           segment_mode: str = "default", vad_silence_ms: int = 2000, vad_threshold: float = 0.5,
           batch_size: int = 8) -> List[Dict[str, Any]]:
    
    if WhisperModel is None:
        console.print("[red]You must install faster-whisper: `pip install faster-whisper`.")
        sys.exit(1)
        
    
    if not audio_path.exists():
        console.print(f"[red]Error: Audio file not found: {audio_path}")
        console.print("[yellow]Tip: For recording, always use .wav extension. For importing, make sure the file exists.")
        sys.exit(1)
    
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        TaskProgressColumn(),
        TimeRemainingColumn(),
        console=console
    ) as progress:
        
        model_task = progress.add_task("[yellow]Loading model...", total=100)
        
        
        has_cuda = False
        if device == "auto" or device == "cuda":
            try:
                progress.update(model_task, description="[yellow]Checking CUDA availability...", completed=10)
                import torch
                has_cuda = torch.cuda.is_available()
            except ImportError:
                has_cuda = False
        
        
        actual_device = "cuda" if has_cuda and device != "cpu" else "cpu"
        compute_type = "float16" if has_cuda and device != "cpu" else "int8"
        
        
        device_status = f"[green]GPU (CUDA)" if actual_device == "cuda" else "[yellow]CPU"
        progress.update(model_task, description=f"[yellow]Loading {model_size} model on {device_status}...", completed=20)
        
        
        model = WhisperModel(model_size, device=actual_device, compute_type=compute_type)
        progress.update(model_task, description="[green]Model loaded successfully!", completed=100)
        
        
        transcribe_task = progress.add_task("[yellow]Transcribing audio...", total=100)
        progress.update(transcribe_task, completed=5)
        
        
        try:
            import soundfile as sf
            with sf.SoundFile(audio_path) as audio_file:
                duration = len(audio_file) / audio_file.samplerate
                progress.update(transcribe_task, description=f"[yellow]Transcribing {duration:.1f}s of audio...", completed=10)
        except Exception:
            
            pass
        
        
        
        progress.update(transcribe_task, description="[yellow]Transcribing audio...", completed=20)
        
        
        progress.update(transcribe_task, description="[yellow]Running transcription model...", completed=30)
        
        
        use_vad = segment_mode == "smart"
        if use_vad:
            progress.update(transcribe_task, description="[yellow]Running transcription with Voice Activity Detection...", completed=30)
            
            
            vad_params = {
                "threshold": vad_threshold,              
                "min_silence_duration_ms": vad_silence_ms,  
            }
            console.log(f"[blue]ℹ Using Voice Activity Detection (silence: {vad_silence_ms}ms, threshold: {vad_threshold})")
        
        
        transcribe_params = {
            "beam_size": 5,
            "vad_filter": use_vad,
        }
        
        
        if use_vad and vad_params:
            transcribe_params["vad_parameters"] = vad_params
            
        
        try:
            
            segments, info = model.transcribe(
                str(audio_path),
                **transcribe_params,
                batch_size=batch_size
            )
        except TypeError:
            
            console.log("[yellow]⚠️ batch_size parameter not supported in this version, ignoring it")
            segments, info = model.transcribe(
                str(audio_path),
                **transcribe_params
            )
        
        
        segment_list = []
        progress.update(transcribe_task, description="[yellow]Processing segments...", completed=60)
        
        
        for i, segment in enumerate(segments):
            segment_list.append(segment)
            
            if i % 3 == 0 or i == 0:
                
                current_progress = 60 + min(30, (i / max(1, len(segment_list) + 10) * 30))
                progress.update(transcribe_task, 
                               description=f"[yellow]Processing segments: {len(segment_list)} found so far...", 
                               completed=current_progress)
        
        
        progress.update(transcribe_task, description="[yellow]Processing results...", completed=95)
        transcript = [
            {
                "start": s.start,
                "end": s.end,
                "text": s.text.strip(),
            }
            for s in segment_list
        ]
        progress.update(transcribe_task, description=f"[green]Transcription complete! {len(transcript)} segments", completed=100)
        
    console.log(f"[green]📜 Transcribed {len(transcript)} segments")
    return transcript


def align_notes(notes: List[Dict[str, Any]], transcript: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    
    if not notes:
        return []
    aligned = []
    for n in notes:
        target = min(transcript, key=lambda s: abs(s["start"] - n["time_seconds"]))
        aligned.append({
            **n,
            "segment_start": target["start"],
            "segment_end": target["end"],
            "segment_text": target["text"],
        })
    return aligned
