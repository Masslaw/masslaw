import unittest

from shared_layer.file_system_utils._file_system_utils import filter_directories_for_types


class TestFunctionFilterDirectoriesForTypes(unittest.TestCase):

    def test_filter_with_valid_file_types(self):
        directories = ["/home/user/music/song.mp3", "/home/user/docs/report.docx", "/home/user/images/wallpaper.png", "/home/user/videos/clip.mp4"]
        file_types = ["mp3", ".docx", "mp4"]
        result = filter_directories_for_types(directories, file_types)
        expected = ["/home/user/music/song.mp3", "/home/user/docs/report.docx", "/home/user/videos/clip.mp4"]
        self.assertEqual(result, expected)

    def test_filter_with_invalid_file_types(self):
        directories = ["/home/user/music/song.mp3", "/home/user/docs/report.docx", "/home/user/images/wallpaper.png", "/home/user/videos/clip.mp4"]
        file_types = ["zip", "tar.gz"]
        result = filter_directories_for_types(directories, file_types)
        self.assertEqual(result, [])

    def test_filter_with_mixed_file_types(self):
        directories = ["/home/user/music/song.mp3", "/home/user/docs/report.docx", "/home/user/images/wallpaper.png", "/home/user/videos/clip.mp4"]
        file_types = ["png", ".docx"]
        result = filter_directories_for_types(directories, file_types)
        expected = ["/home/user/docs/report.docx", "/home/user/images/wallpaper.png"]
        self.assertEqual(result, expected)

    def test_filter_with_no_directories(self):
        directories = []
        file_types = ["mp3", ".docx", "mp4"]
        result = filter_directories_for_types(directories, file_types)
        self.assertEqual(result, [])
