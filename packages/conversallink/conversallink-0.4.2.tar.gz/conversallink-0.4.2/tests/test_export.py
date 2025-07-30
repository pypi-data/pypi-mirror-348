
import unittest
from unittest.mock import patch, mock_open, MagicMock
import json
from pathlib import Path

from src.conversallink.export import export_markdown, export_json, export_txt


class TestExport(unittest.TestCase):
    

    def setUp(self):
        
        
        self.transcript = [
            {"start": 0.0, "end": 5.0, "text": "This is the first segment."},
            {"start": 5.0, "end": 10.0, "text": "This is the second segment."}
        ]
        
        
        self.notes = [
            {"time_seconds": 2.0, "time_hms": "0:00:02", "note": "Important point"},
            {"time_seconds": 7.0, "time_hms": "0:00:07", "note": "Another note"}
        ]
        
        
        self.notes_aligned = [
            {
                "time_seconds": 2.0,
                "time_hms": "0:00:02",
                "note": "Important point",
                "segment_start": 0.0,
                "segment_end": 5.0,
                "segment_text": "This is the first segment."
            },
            {
                "time_seconds": 7.0,
                "time_hms": "0:00:07",
                "note": "Another note",
                "segment_start": 5.0,
                "segment_end": 10.0,
                "segment_text": "This is the second segment."
            }
        ]
        
        
        self.base_path = Path("test_audio.wav")

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.conversallink.export.console')
    def test_export_markdown(self, mock_console, mock_file):
        
        export_markdown(self.base_path, self.transcript, self.notes_aligned)
        
        
        expected_path = Path("test_audio_transcript.md")
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        
        
        written_content = ''.join(call.args[0] for call in mock_file().write.call_args_list)
        
        
        self.assertIn("# Transcript for test_audio.wav", written_content)
        self.assertIn("## Notes with Context", written_content)
        self.assertIn("### 📝 Important point (0:00:02)", written_content)
        self.assertIn("> This is the first segment.", written_content)
        self.assertIn("### 📝 Another note (0:00:07)", written_content)
        self.assertIn("> This is the second segment.", written_content)
        self.assertIn("## Full Transcript", written_content)
        self.assertIn("[0:00:00 → 0:00:05] This is the first segment.", written_content)
        self.assertIn("[0:00:05 → 0:00:10] This is the second segment.", written_content)
        
        
        mock_console.log.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('src.conversallink.export.console')
    def test_export_json(self, mock_console, mock_json_dump, mock_file):
        
        export_json(self.base_path, self.transcript, self.notes, self.notes_aligned)
        
        
        expected_path = Path("test_audio_transcript.json")
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        
        
        mock_json_dump.assert_called_once()
        args, kwargs = mock_json_dump.call_args
        data = args[0]
        
        self.assertEqual(data["transcript"], self.transcript)
        self.assertEqual(data["notes"], self.notes)
        self.assertEqual(data["notes_aligned"], self.notes_aligned)
        
        
        self.assertEqual(kwargs["ensure_ascii"], False)
        self.assertEqual(kwargs["indent"], 2)
        
        
        mock_console.log.assert_called_once()

    @patch('builtins.open', new_callable=mock_open)
    @patch('src.conversallink.export.console')
    def test_export_txt(self, mock_console, mock_file):
        
        export_txt(self.base_path, self.transcript)
        
        
        expected_path = Path("test_audio_transcript.txt")
        mock_file.assert_called_once_with(expected_path, "w", encoding="utf-8")
        
        
        expected_content = "This is the first segment.\nThis is the second segment."
        mock_file().write.assert_called_once_with(expected_content)
        
        
        mock_console.log.assert_called_once()


if __name__ == "__main__":
    unittest.main()
