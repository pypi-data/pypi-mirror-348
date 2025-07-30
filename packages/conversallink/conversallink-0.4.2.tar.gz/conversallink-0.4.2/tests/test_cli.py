
import os
import unittest
import subprocess
import tempfile
import shutil
from pathlib import Path


class TestCLI(unittest.TestCase):
    

    def setUp(self):
        
        
        self.temp_dir = tempfile.mkdtemp()
        
        
        self.script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "conversallink.py")
        
        
        self.test_audio_path = os.path.join(self.temp_dir, "test_audio.wav")
        self._create_test_audio_file()

    def tearDown(self):
        
        
        shutil.rmtree(self.temp_dir)

    def _create_test_audio_file(self):
        
        try:
            import numpy as np
            import soundfile as sf
            
            
            data = np.zeros(16000, dtype=np.int16)
            sf.write(self.test_audio_path, data, 16000)
        except ImportError:
            
            with open(self.test_audio_path, 'wb') as f:
                f.write(b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00\x00\x7d\x00\x00\x00\xfa\x00\x00\x02\x00\x10\x00data\x00\x00\x00\x00')

    def test_help_menu(self):
        
        result = subprocess.run(
            ["python", self.script_path, "--help"],
            capture_output=True,
            text=True
        )
        
        
        
        self.assertTrue(len(result.stdout) > 0 or len(result.stderr) > 0)

    def test_version_flag(self):
        
        result = subprocess.run(
            ["python", self.script_path, "--version"],
            capture_output=True,
            text=True
        )
        
        
        self.assertEqual(result.returncode, 0)
        
        
        
        self.assertIn("v", result.stdout.lower())

    @unittest.skip("This test requires the actual transcription model and takes time to run")
    def test_transcribe_file(self):
        
        output_base = os.path.join(self.temp_dir, "output")
        
        result = subprocess.run(
            [
                "python", 
                self.script_path, 
                "--file", self.test_audio_path,
                "--model", "tiny",
                "--device", "cpu",
                "--out", output_base
            ],
            capture_output=True,
            text=True
        )
        
        
        self.assertEqual(result.returncode, 0)
        
        
        self.assertTrue(os.path.exists(f"{output_base}_transcript.txt"))
        self.assertTrue(os.path.exists(f"{output_base}_transcript.md"))
        self.assertTrue(os.path.exists(f"{output_base}_transcript.json"))

    @unittest.skip("This test requires the actual transcription model and takes time to run")
    def test_transcribe_with_vad(self):
        
        output_base = os.path.join(self.temp_dir, "output_vad")
        
        result = subprocess.run(
            [
                "python", 
                self.script_path, 
                "--file", self.test_audio_path,
                "--model", "tiny",
                "--device", "cpu",
                "--segments", "smart",
                "--vad-silence", "1000",
                "--vad-threshold", "0.7",
                "--out", output_base
            ],
            capture_output=True,
            text=True
        )
        
        
        self.assertEqual(result.returncode, 0)
        
        
        self.assertTrue(os.path.exists(f"{output_base}_transcript.txt"))


if __name__ == "__main__":
    unittest.main()
