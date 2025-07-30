
import os
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile
import shutil

from src.conversallink.transcriber import transcribe, align_notes
from src.conversallink.export import export_markdown, export_json, export_txt


class TestIntegration(unittest.TestCase):
    

    def setUp(self):
        
        
        self.temp_dir = tempfile.mkdtemp()
        
        
        self.audio_path = Path(os.path.join(self.temp_dir, "test_audio.wav"))
        
        
        self.transcript = [
            {"start": 0.0, "end": 5.0, "text": "This is the first segment."},
            {"start": 5.0, "end": 10.0, "text": "This is the second segment."}
        ]
        
        
        self.notes = [
            {"time_seconds": 2.0, "time_hms": "0:00:02", "note": "Important point"},
            {"time_seconds": 7.0, "time_hms": "0:00:07", "note": "Another note"}
        ]

    def tearDown(self):
        
        
        shutil.rmtree(self.temp_dir)

    @patch('src.conversallink.transcriber.WhisperModel')
    def test_transcribe_and_export_flow(self, mock_whisper_model_class):
        
        
        mock_whisper_model = mock_whisper_model_class.return_value
        
        
        mock_segment1 = MagicMock()
        mock_segment1.start = 0.0
        mock_segment1.end = 5.0
        mock_segment1.text = " This is the first segment."
        
        mock_segment2 = MagicMock()
        mock_segment2.start = 5.0
        mock_segment2.end = 10.0
        mock_segment2.text = " This is the second segment."
        
        mock_segments = [mock_segment1, mock_segment2]
        mock_whisper_model.transcribe.return_value = (mock_segments, {})
        
        
        torch_module_mock = MagicMock()
        cuda_mock = MagicMock()
        cuda_mock.is_available.return_value = False
        torch_module_mock.cuda = cuda_mock
        
        
        sf_module_mock = MagicMock()
        mock_audio_file = MagicMock()
        mock_audio_file.__enter__.return_value.samplerate = 16000
        mock_audio_file.__enter__.return_value.__len__.return_value = 160000
        sf_module_mock.SoundFile.return_value = mock_audio_file
        
        
        with patch.object(Path, 'exists', return_value=True), \
             patch.dict('sys.modules', {
                 'torch': torch_module_mock,
                 'soundfile': sf_module_mock
             }), \
             patch('src.conversallink.transcriber.Progress'):
            
            
            transcript = transcribe(self.audio_path, "tiny", device="cpu")
            
            
            self.assertEqual(len(transcript), 2)
            self.assertEqual(transcript[0]["start"], 0.0)
            self.assertEqual(transcript[0]["end"], 5.0)
            self.assertEqual(transcript[0]["text"], "This is the first segment.")
            
            
            aligned_notes = align_notes(self.notes, transcript)
            
            
            self.assertEqual(len(aligned_notes), 2)
            self.assertEqual(aligned_notes[0]["segment_text"], "This is the first segment.")
            self.assertEqual(aligned_notes[1]["segment_text"], "This is the second segment.")
            
            
            with patch('builtins.open', create=True), \
                 patch('src.conversallink.export.console'):
                
                
                export_markdown(self.audio_path, transcript, aligned_notes)
                
                
                export_json(self.audio_path, transcript, self.notes, aligned_notes)
                
                
                export_txt(self.audio_path, transcript)
                
                
                self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
