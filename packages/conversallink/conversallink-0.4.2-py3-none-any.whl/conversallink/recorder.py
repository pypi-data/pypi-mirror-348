

import threading
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple, Union

import numpy as np
import sounddevice as sd
import soundfile as sf

from .utils import console, secs_to_hms

def list_input_devices() -> List[Dict[str, Any]]:
    
    devices = sd.query_devices()
    input_devices = []
    
    for i, device in enumerate(devices):
        
        if device['max_input_channels'] > 0:
            input_devices.append({
                'id': i,
                'name': device['name'],
                'channels': device['max_input_channels'],
                'default': device.get('default_input', False)
            })
    
    return input_devices


def print_input_devices() -> None:
    
    devices = list_input_devices()
    
    if not devices:
        console.print("[yellow]No input devices found![/]")  
        return
    
    console.print("[bold cyan]Available input devices:[/]")  
    for device in devices:
        default_mark = "[green]* (default)[/]" if device['default'] else ""
        console.print(f"  [cyan]{device['id']}[/]: {device['name']} ({device['channels']} channels) {default_mark}")  


def get_default_input_device() -> Optional[int]:
    
    try:
        return sd.default.device[0]  
    except:
        
        devices = list_input_devices()
        for device in devices:
            if device.get('default', False):
                return device['id']
        
        if devices:
            return devices[0]['id']
    return None


class Recorder(threading.Thread):
    

    def __init__(self, outfile: Path, samplerate: int = 16_000, channels: int = 1, device: Optional[Union[int, str]] = None):
        super().__init__(daemon=True)
        self.outfile = outfile
        self.samplerate = samplerate
        self.channels = channels
        self.device = device
        self._stop_event = threading.Event()
        self._start_time: Optional[float] = None
        self._frames: List[Any] = []

    @property
    def elapsed(self) -> float:
        
        return 0.0 if self._start_time is None else time.time() - self._start_time

    def run(self) -> bool:
        
        self._start_time = time.time()
        with sd.InputStream(samplerate=self.samplerate,
                             channels=self.channels,
                             device=self.device,
                             dtype="int16",
                             blocksize=1024,
                             callback=self._callback):
            console.log("🎙️  Recording...  (type /stop + ⏎ to finish)")
            while not self._stop_event.is_set():
                time.sleep(0.1)
        
        if self._frames:
            try:
                
                data = np.frombuffer(b"".join(self._frames), dtype=np.int16)
                
                if self.channels > 1:
                    data = data.reshape(-1, self.channels)
                sf.write(self.outfile, data, self.samplerate, subtype="PCM_16")
                console.log(f"💾 Saved audio to {self.outfile}")
                return True
            except Exception as e:
                console.print(f"[red]Error saving audio: {e}")
                return False
        else:
            console.print("[yellow]⚠️ No audio data recorded")
            return False

    def _callback(self, indata, frames, time_info, status):
        
        if status:
            console.print(f"[red]⚠️ {status}")
        self._frames.append(indata.copy())

    def stop(self):
        
        self._stop_event.set()

def capture_notes(rec: Recorder) -> Tuple[List[Dict[str, Any]], bool]:
    
    notes: List[Dict[str, Any]] = []
    while True:
        try:
            line = input()
        except EOFError:  
            line = "/stop"
        if line.strip().lower() == "/stop":
            rec.stop()
            break
        timestamp = rec.elapsed
        note_entry = {
            "time_seconds": timestamp,
            "time_hms": secs_to_hms(timestamp),
            "note": line.strip(),
        }
        notes.append(note_entry)
        console.print(f"[green]✔ Added note @ {note_entry['time_hms']}")
    
    
    rec.join()
    
    
    process_now = False
    if rec.outfile.exists() and rec.outfile.stat().st_size > 0:
        console.print("\n[bold cyan]Recording completed successfully.[/]")
        while True:
            response = input("Do you want to process this recording now? (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                process_now = True
                break
            elif response in ['n', 'no']:
                process_now = False
                break
            else:
                console.print("[yellow]Please enter 'y' or 'n'[/]")
    else:
        console.print("\n[red]Recording failed or no audio was captured.[/]")
        process_now = False
    
    return notes, process_now
