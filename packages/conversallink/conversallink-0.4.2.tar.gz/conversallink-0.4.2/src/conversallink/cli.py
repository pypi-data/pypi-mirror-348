

__version__ = "0.4.2"

import argparse
import json
import sys
import textwrap
from pathlib import Path
from typing import List, Dict, Any, Optional, Sequence, Union

from rich.table import Table
from rich.console import Console as RichConsole

from .export import export_json, export_markdown, export_txt
from .html_export import export_modern_html
from .recorder import Recorder, capture_notes, list_input_devices, print_input_devices, get_default_input_device
from .transcriber import transcribe, align_notes
from .utils import console, ensure_suffix

class ListDevicesAction(argparse.Action):
    
    
    def __init__(self, option_strings, dest, default=False, help=None):
        super().__init__(option_strings=option_strings, dest=dest, nargs=0, default=default, help=help)
    
    def __call__(self, parser, namespace, values, option_string=None):
        print_input_devices()
        parser.exit()


class ModelHelpAction(argparse.Action):
    
    
    def __init__(self, option_strings, dest, default=False, help=None):
        super().__init__(option_strings=option_strings, dest=dest, nargs=0, default=default, help=help)
    
    def __call__(self, parser, namespace, values, option_string=None):
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        
        console = Console()
        
        
        table = Table(title="Available Whisper Models")
        console.print("Select a model based on your needs for accuracy vs. speed and resource usage.")
        console.print("See https://github.com/gchatzigianniss/ConversalLink?tab=readme-ov-file#-transcription-models for more details.\n")
        table.add_column("Model", style="cyan")
        table.add_column("Disk & RAM Usage")
        table.add_column("Characteristics")
        
        table.add_row("tiny", "~150MB", "Fastest, lowest quality, English-focused")
        table.add_row("base", "~300MB", "Fast, basic quality, improved multilingual")
        table.add_row("small", "~500MB", "Balanced speed/quality, good multilingual")
        table.add_row("medium", "~1.5GB", "Slower, high quality, excellent multilingual")
        table.add_row("large", "~3GB", "Slowest, highest quality, best for complex audio")
        
        
        cuda_info = Panel(
            "If PyTorch with CUDA is installed and a compatible GPU is detected,\n"
            "models will automatically use GPU acceleration for significantly faster processing.\n"
            "CPU-only mode is used as fallback or when explicitly selected with [cyan]--device cpu[/cyan].",
            title="CUDA Acceleration",
            expand=False
        )
        
        
        console.print("\n")
        console.print(table)
        console.print(Panel(
            f"module: conversallink\nversion: {__version__}\nfile: {sys.argv[0]}\npython: {sys.version.split()[0]}",
            title="Environment"
        ))
        console.print(cuda_info)
        console.print("\n")
        
        
        parser.exit()


class VersionAction(argparse.Action):
    
    
    def __init__(self, option_strings, version, dest=argparse.SUPPRESS, default=argparse.SUPPRESS, help="Show program's version number and exit"):
        self.version = version
        super().__init__(option_strings=option_strings, dest=dest, default=default, nargs=0, help=help)
    
    def __call__(self, parser, namespace, values, option_string=None):
        print(f"ConversalLink v{self.version}")
        parser.exit(0)


def build_arg_parser() -> argparse.ArgumentParser:
    
    p = argparse.ArgumentParser(
        description="Conversation Recorder + Faster‑Whisper‑powered transcriber")
    p.add_argument("--version", action=VersionAction, version=__version__)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--record", metavar="WAV", help="Record from mic and save to this WAV file")
    g.add_argument("--file", metavar="AUDIO", help="Use an existing audio file (WAV/MP3/FLAC…)")
    g.add_argument("--list-devices", action=ListDevicesAction, help="List available audio input devices and exit")

    p.add_argument("--notes", metavar="JSON", help="(optional) JSON notes file to merge")
    p.add_argument("--input-device", metavar="ID", type=int, help="Audio input device ID to use for recording (use --list-devices to see available devices)")
    p.add_argument("--model", default="small", 
                   help="Whisper model size (tiny|base|small|medium|large)")
    p.add_argument("--model-info", action=ModelHelpAction, 
                   help="Show detailed information about available Whisper models and exit")
    p.add_argument("--device", default="auto", help="Device: cpu, cuda, auto")
    p.add_argument("--out", choices=["markdown", "json", "html", "txt", "all"], default="all",
                   help="Which output files to generate (markdown, json, html, txt, or all)")
    p.add_argument("--segments", choices=["default", "smart"], default="default",
                   help="Segmentation mode: default or smart (VAD-based)")
    p.add_argument("--vad-silence", type=int, default=2000,
                   help="Minimum silence duration in ms to split segments (default: 2000ms)")
    p.add_argument("--vad-threshold", type=float, default=0.5,
                   help="VAD threshold (0.0-1.0) for voice detection, higher values are more conservative (default: 0.5)")
    p.add_argument("--batch-size", type=int, default=8,
                   help="Batch size for processing audio chunks (higher values may increase speed on powerful GPUs)")
    return p


def main():
    
    args = build_arg_parser().parse_args()
    
    
    return_code = 0

    base: Path
    notes: List[Dict[str, Any]] = []

    
    if args.record:
        
        
        
        input_path = Path(args.record)
        out_wav = input_path.with_suffix(".wav")
        
        
        if input_path.suffix.lower() not in ["", ".wav"]:
            console.print(f"[yellow]⚠️ Note: Recording must use WAV format. Changed output to: {out_wav}")
        else:
            console.log(f"Recording to file: {out_wav}")
        
        
        input_device = args.input_device if args.input_device is not None else get_default_input_device()
        if input_device is not None:
            console.log(f"Using input device: {input_device}")
        else:
            console.log("Using system default input device")
            
        rec = Recorder(out_wav, device=input_device)
        rec.start()
        notes, process_now = capture_notes(rec)
        
        
        if not out_wav.exists() or out_wav.stat().st_size == 0:
            console.print(f"[red]Error: Failed to create valid audio file {out_wav}")
            sys.exit(1)
            
        if notes:
            notes_path = out_wav.parent / f"{out_wav.stem}_notes.json"
            with open(notes_path, "w", encoding="utf-8") as fp:
                json.dump(notes, fp, ensure_ascii=False, indent=2)
            console.log(f"📎️  Notes saved to {notes_path}")
        base = out_wav
        
        
        if not process_now:
            console.print("[cyan]Recording saved. Run the program with --file option to process it later.[/]")
            sys.exit(0)
    
    else:
        base = Path(args.file)
        
        if not base.exists():
            console.print(f"[red]Error: Audio file not found: {base}")
            console.print("[yellow]Tip: For recording, always use .wav extension. For importing, make sure the file exists.")
            sys.exit(1)
            
        if args.notes:
            notes_path = Path(args.notes)
            if notes_path.exists():
                notes = json.loads(Path(notes_path).read_text(encoding="utf-8"))
                console.log(f"📥 Loaded {len(notes)} notes from {notes_path}")
            else:
                console.print(f"[yellow]⚠ Notes file not found: {notes_path}")

    
    transcript = transcribe(
        base, 
        args.model, 
        device=args.device, 
        segment_mode=args.segments,
        vad_silence_ms=args.vad_silence,
        vad_threshold=args.vad_threshold,
        batch_size=args.batch_size
    )
    notes_aligned = align_notes(notes, transcript)

    
    if args.out in {"markdown", "all"}:
        export_markdown(base, transcript, notes_aligned)
    if args.out in {"json", "all"}:
        export_json(base, transcript, notes, notes_aligned)
    if args.out in {"html", "all"}:
        export_modern_html(base, transcript, notes_aligned)
    if args.out in {"txt", "all"}:
        export_txt(base, transcript)

    
    tbl = Table(title=f"ConversalLink v{__version__} - Done!", show_lines=False)
    tbl.add_column("Statistic")
    tbl.add_column("Count")
    tbl.add_row("Transcript segments", str(len(transcript)))
    tbl.add_row("Notes", str(len(notes)))
    tbl.add_row("Export formats", args.out if args.out != "all" else "markdown, json, html")
    console.print(tbl)
    
    return return_code


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("[red]\nInterrupted by user")
