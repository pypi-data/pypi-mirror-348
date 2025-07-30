
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path
import sys

from src.conversallink.transcriber import transcribe, align_notes


class TestTranscriber(unittest.TestCase):
    

    def setUp(self):
        
        
        self.audio_path = Path("test_audio.wav")
        
        
        mock_segment1 = MagicMock()
        mock_segment1.start = 0.0
        mock_segment1.end = 5.0
        mock_segment1.text = " This is the first segment."
        
        mock_segment2 = MagicMock()
        mock_segment2.start = 5.0
        mock_segment2.end = 10.0
        mock_segment2.text = " This is the second segment."
        
        
        self.mock_segments = [mock_segment1, mock_segment2]

    def tearDown(self):
        pass
        

    def test_transcribe_basic(self):
        
        
        expected_result = [
            {"start": 0.0, "end": 5.0, "text": "This is the first segment."},
            {"start": 5.0, "end": 10.0, "text": "This is the second segment."}
        ]
        
        
        with patch('src.conversallink.transcriber.sys.exit') as mock_exit, \
             patch.object(Path, 'exists', return_value=True), \
             patch('src.conversallink.transcriber.WhisperModel') as mock_whisper_model_class:
            
            
            mock_whisper_model = mock_whisper_model_class.return_value
            mock_whisper_model.transcribe.return_value = (self.mock_segments, {})
            
            
            torch_module_mock = MagicMock()
            cuda_mock = MagicMock()
            cuda_mock.is_available.return_value = False
            torch_module_mock.cuda = cuda_mock
            
            
            sf_module_mock = MagicMock()
            mock_audio_file = MagicMock()
            mock_audio_file.__enter__.return_value.samplerate = 16000
            mock_audio_file.__enter__.return_value.__len__.return_value = 160000
            sf_module_mock.SoundFile.return_value = mock_audio_file
            
            
            with patch.dict('sys.modules', {
                'torch': torch_module_mock,
                'soundfile': sf_module_mock
            }), patch('src.conversallink.transcriber.Progress') as mock_progress_class:
                
                
                mock_progress = MagicMock()
                mock_progress_class.return_value.__enter__.return_value = mock_progress
                mock_task = MagicMock()
                mock_progress.add_task.return_value = mock_task
                
                
                result = transcribe(self.audio_path, "base", device="cpu")
                
                
                mock_whisper_model_class.assert_called_once_with("base", device="cpu", compute_type="int8")
                
                
                self.assertEqual(len(result), 2)
                self.assertEqual(result[0]["start"], 0.0)
                self.assertEqual(result[0]["end"], 5.0)
                self.assertEqual(result[0]["text"], "This is the first segment.")
                self.assertEqual(result[1]["start"], 5.0)
                self.assertEqual(result[1]["end"], 10.0)
                self.assertEqual(result[1]["text"], "This is the second segment.")
                
                
                mock_exit.assert_not_called()

    def test_transcribe_with_cuda(self):
        
        
        with patch('src.conversallink.transcriber.sys.exit') as mock_exit, \
             patch.object(Path, 'exists', return_value=True), \
             patch('src.conversallink.transcriber.WhisperModel') as mock_whisper_model_class:
            
            
            mock_whisper_model = mock_whisper_model_class.return_value
            mock_whisper_model.transcribe.return_value = (self.mock_segments, {})
            
            
            torch_module_mock = MagicMock()
            cuda_mock = MagicMock()
            cuda_mock.is_available.return_value = True  
            torch_module_mock.cuda = cuda_mock
            
            
            sf_module_mock = MagicMock()
            mock_audio_file = MagicMock()
            mock_audio_file.__enter__.return_value.samplerate = 16000
            mock_audio_file.__enter__.return_value.__len__.return_value = 160000
            sf_module_mock.SoundFile.return_value = mock_audio_file
            
            
            with patch.dict('sys.modules', {
                'torch': torch_module_mock,
                'soundfile': sf_module_mock
            }), patch('src.conversallink.transcriber.Progress') as mock_progress_class:
                
                
                mock_progress = MagicMock()
                mock_progress_class.return_value.__enter__.return_value = mock_progress
                mock_task = MagicMock()
                mock_progress.add_task.return_value = mock_task
                
                
                result = transcribe(self.audio_path, "medium", device="auto")
                
                
                mock_whisper_model_class.assert_called_once_with("medium", device="cuda", compute_type="float16")
                
                
                mock_exit.assert_not_called()

    def test_transcribe_with_vad(self):
        
        
        with patch('src.conversallink.transcriber.sys.exit') as mock_exit, \
             patch.object(Path, 'exists', return_value=True), \
             patch('src.conversallink.transcriber.WhisperModel') as mock_whisper_model_class:
            
            
            mock_whisper_model = mock_whisper_model_class.return_value
            mock_transcribe = mock_whisper_model.transcribe
            mock_transcribe.return_value = (self.mock_segments, {})
            
            
            torch_module_mock = MagicMock()
            cuda_mock = MagicMock()
            cuda_mock.is_available.return_value = False
            torch_module_mock.cuda = cuda_mock
            
            
            sf_module_mock = MagicMock()
            mock_audio_file = MagicMock()
            mock_audio_file.__enter__.return_value.samplerate = 16000
            mock_audio_file.__enter__.return_value.__len__.return_value = 160000
            sf_module_mock.SoundFile.return_value = mock_audio_file
            
            
            with patch.dict('sys.modules', {
                'torch': torch_module_mock,
                'soundfile': sf_module_mock
            }), patch('src.conversallink.transcriber.Progress') as mock_progress_class:
                
                
                mock_progress = MagicMock()
                mock_progress_class.return_value.__enter__.return_value = mock_progress
                mock_task = MagicMock()
                mock_progress.add_task.return_value = mock_task
                
                
                result = transcribe(
                    self.audio_path, 
                    "small", 
                    device="cpu",
                    segment_mode="smart",
                    vad_silence_ms=1500,
                    vad_threshold=0.6
                )
                
                
                call_kwargs = mock_transcribe.call_args[1]
                self.assertTrue(call_kwargs["vad_filter"])
                self.assertEqual(call_kwargs["vad_parameters"]["min_silence_duration_ms"], 1500)
                self.assertEqual(call_kwargs["vad_parameters"]["threshold"], 0.6)
                
                
                mock_exit.assert_not_called()

    def test_transcribe_file_not_found(self):
        
        
        with patch('src.conversallink.transcriber.console.print') as mock_console_print, \
             patch('src.conversallink.transcriber.sys.exit') as mock_sys_exit, \
             patch.object(Path, 'exists', return_value=False):
            
            
            
            dummy_path = Path('dummy.wav')
            
            
            try:
                transcribe(dummy_path, "base")
            except Exception:
                
                pass
            
            
            mock_console_print.assert_any_call(f"[red]Error: Audio file not found: {dummy_path}")
            
            
            mock_sys_exit.assert_called_once_with(1)

    def test_align_notes(self):
        
        
        notes = [
            {"time_seconds": 1.0, "time_hms": "0:00:01", "note": "Note at 1 second"},
            {"time_seconds": 7.0, "time_hms": "0:00:07", "note": "Note at 7 seconds"},
            {"time_seconds": 12.0, "time_hms": "0:00:12", "note": "Note at 12 seconds"}
        ]
        
        transcript = [
            {"start": 0.0, "end": 5.0, "text": "This is the first segment."},
            {"start": 5.0, "end": 10.0, "text": "This is the second segment."},
            {"start": 10.0, "end": 15.0, "text": "This is the third segment."}
        ]
        
        aligned = align_notes(notes, transcript)
        
        
        self.assertEqual(len(aligned), 3)
        
        
        self.assertEqual(aligned[0]["segment_start"], 0.0)
        self.assertEqual(aligned[0]["segment_end"], 5.0)
        self.assertEqual(aligned[0]["segment_text"], "This is the first segment.")
        
        
        self.assertEqual(aligned[1]["segment_start"], 5.0)
        self.assertEqual(aligned[1]["segment_end"], 10.0)
        self.assertEqual(aligned[1]["segment_text"], "This is the second segment.")
        
        
        self.assertEqual(aligned[2]["segment_start"], 10.0)
        self.assertEqual(aligned[2]["segment_end"], 15.0)
        self.assertEqual(aligned[2]["segment_text"], "This is the third segment.")

    def test_align_notes_empty(self):
        
        transcript = [
            {"start": 0.0, "end": 5.0, "text": "This is a segment."}
        ]
        
        aligned = align_notes([], transcript)
        self.assertEqual(aligned, [])


if __name__ == "__main__":
    unittest.main()
