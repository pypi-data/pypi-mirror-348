
import unittest
from pathlib import Path
from datetime import timedelta

from src.conversallink.utils import secs_to_hms, ensure_suffix


class TestUtils(unittest.TestCase):
    

    def test_secs_to_hms(self):
        
        
        
        self.assertEqual(secs_to_hms(0), str(timedelta(seconds=0)))
        self.assertEqual(secs_to_hms(1), str(timedelta(seconds=1)))
        self.assertEqual(secs_to_hms(60), str(timedelta(seconds=60)))
        self.assertEqual(secs_to_hms(3600), str(timedelta(seconds=3600)))
        self.assertEqual(secs_to_hms(3661), str(timedelta(seconds=3661)))
        self.assertEqual(secs_to_hms(86400), str(timedelta(seconds=86400)))  
        
        
        self.assertEqual(secs_to_hms(60.5), str(timedelta(seconds=int(60.5))))  
        self.assertEqual(secs_to_hms(3599.9), str(timedelta(seconds=int(3599.9))))

    def test_ensure_suffix(self):
        
        
        self.assertEqual(ensure_suffix("test", ".wav"), Path("test.wav"))
        self.assertEqual(ensure_suffix("test.wav", ".wav"), Path("test.wav"))
        self.assertEqual(ensure_suffix("test.mp3", ".wav"), Path("test.mp3"))
        
        
        self.assertEqual(ensure_suffix(Path("test"), ".wav"), Path("test.wav"))
        self.assertEqual(ensure_suffix(Path("test.wav"), ".wav"), Path("test.wav"))
        self.assertEqual(ensure_suffix(Path("test.mp3"), ".wav"), Path("test.mp3"))
        
        
        self.assertEqual(ensure_suffix("test", ".mp3"), Path("test.mp3"))
        self.assertEqual(ensure_suffix("test.txt", ".json"), Path("test.txt"))


if __name__ == "__main__":
    unittest.main()
