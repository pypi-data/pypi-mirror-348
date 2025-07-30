
import unittest
from unittest.mock import patch, MagicMock, call, PropertyMock
import numpy as np
from pathlib import Path
import threading

from src.conversallink.recorder import (
    list_input_devices,
    get_default_input_device,
    Recorder
)


class TestRecorderFunctions(unittest.TestCase):
    

    @patch('src.conversallink.recorder.sd.query_devices')
    def test_list_input_devices(self, mock_query_devices):
        
        
        mock_query_devices.return_value = [
            {'name': 'Device 1', 'max_input_channels': 2, 'default_input': True},
            {'name': 'Device 2', 'max_input_channels': 0},  
            {'name': 'Device 3', 'max_input_channels': 1}
        ]
        
        devices = list_input_devices()
        
        
        self.assertEqual(len(devices), 2)
        self.assertEqual(devices[0]['name'], 'Device 1')
        self.assertEqual(devices[0]['channels'], 2)
        self.assertTrue(devices[0]['default'])
        self.assertEqual(devices[1]['name'], 'Device 3')
        self.assertEqual(devices[1]['channels'], 1)
        self.assertFalse(devices[1].get('default', False))

    def test_get_default_input_device_from_sd(self):
        
        with patch('src.conversallink.recorder.sd.default.device', create=True, new=[3, 5]):
            device_id = get_default_input_device()
            self.assertEqual(device_id, 3)

    def test_get_default_input_device_fallback_with_default_device(self):
        
        with patch('src.conversallink.recorder.sd') as mock_sd, \
             patch('src.conversallink.recorder.list_input_devices') as mock_list_devices:
            
            mock_sd.default.device = PropertyMock(side_effect=Exception("No default device"))
            
            
            mock_list_devices.return_value = [
                {'id': 1, 'name': 'Device 1', 'default': False},
                {'id': 2, 'name': 'Device 2', 'default': True}
            ]
            
            
            result = get_default_input_device()
            
            
            self.assertEqual(result, 2)
    
    def test_get_default_input_device_fallback_no_default(self):
        
        with patch('src.conversallink.recorder.sd') as mock_sd, \
             patch('src.conversallink.recorder.list_input_devices') as mock_list_devices:
            
            mock_sd.default.device = PropertyMock(side_effect=Exception("No default device"))
            
            
            mock_list_devices.return_value = [
                {'id': 1, 'name': 'Device 1'},
                {'id': 2, 'name': 'Device 2'}
            ]
            
            
            result = get_default_input_device()
            
            
            self.assertEqual(result, 1)
    
    def test_get_default_input_device_fallback_no_devices(self):
        
        with patch('src.conversallink.recorder.sd') as mock_sd, \
             patch('src.conversallink.recorder.list_input_devices') as mock_list_devices:
            
            mock_sd.default.device = PropertyMock(side_effect=Exception("No default device"))
            
            
            mock_list_devices.return_value = []
            
            
            result = get_default_input_device()
            
            
            self.assertIsNone(result)


class TestRecorderClass(unittest.TestCase):
    

    def setUp(self):
        
        self.outfile = Path("test_output.wav")
        
        
        self.input_stream_patcher = patch('src.conversallink.recorder.sd.InputStream')
        self.mock_input_stream = self.input_stream_patcher.start()
        
        
        self.mock_stream = MagicMock()
        self.mock_input_stream.return_value.__enter__.return_value = self.mock_stream
        
        
        self.sf_write_patcher = patch('src.conversallink.recorder.sf.write')
        self.mock_sf_write = self.sf_write_patcher.start()
        
        
        self.sleep_patcher = patch('src.conversallink.recorder.time.sleep')
        self.mock_sleep = self.sleep_patcher.start()

    def tearDown(self):
        
        self.input_stream_patcher.stop()
        self.sf_write_patcher.stop()
        self.sleep_patcher.stop()

    def test_recorder_init(self):
        
        recorder = Recorder(self.outfile, samplerate=44100, channels=2, device=1)
        self.assertEqual(recorder.outfile, self.outfile)
        self.assertEqual(recorder.samplerate, 44100)
        self.assertEqual(recorder.channels, 2)
        self.assertEqual(recorder.device, 1)
        self.assertIsNone(recorder._start_time)
        self.assertEqual(recorder._frames, [])

    @patch('src.conversallink.recorder.time.time', return_value=1000.0)
    def test_recorder_elapsed(self, mock_time):
        
        recorder = Recorder(self.outfile)
        self.assertEqual(recorder.elapsed, 0.0)  
        
        
        recorder._start_time = 900.0
        mock_time.return_value = 1000.0
        self.assertEqual(recorder.elapsed, 100.0)

    def test_recorder_run_and_stop(self):
        
        
        recorder = Recorder(self.outfile)
        
        
        recorder._frames = [np.array([1, 2, 3], dtype=np.int16), np.array([4, 5, 6], dtype=np.int16)]
        recorder._start_time = 1000.0
        
        
        with patch('src.conversallink.recorder.np.frombuffer') as mock_frombuffer:
            mock_frombuffer.return_value = np.array([1, 2, 3, 4, 5, 6], dtype=np.int16)
            
            
            recorder._stop_event.set()
            
            
            
            result = recorder.run()
        
        
        self.assertTrue(result)
        self.mock_sf_write.assert_called_once()
        self.assertEqual(self.mock_sf_write.call_args[0][0], self.outfile)
        
    def test_callback(self):
        
        recorder = Recorder(self.outfile)
        test_data = np.array([[1, 2], [3, 4]], dtype=np.int16)
        
        
        recorder._callback(test_data, 2, None, None)
        
        
        self.assertEqual(len(recorder._frames), 1)
        np.testing.assert_array_equal(recorder._frames[0], test_data)


if __name__ == "__main__":
    unittest.main()
