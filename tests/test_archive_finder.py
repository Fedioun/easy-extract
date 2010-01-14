"""Unit tests for ArchiveCollector object"""
import unittest

from easy_extract.archive import Archive
from easy_extract.archive_finder import ArchiveFinder

TEST_DIRPATH  = './tests/'
TEST_PATH_ARCHIVES = {'path_1': ['archive_1', 'archive_2'],
                      'path_2': ['archive_3',],}

class AllIsArchive(Archive):
    """Test Archive allowing all files for archive"""

    @classmethod
    def is_archive_file(self, filename):
        return True

class ArchiveFinderTestCase(unittest.TestCase):

    def test_init(self):
        af = ArchiveFinder()

        self.assertEquals(af.root_path, '.')
        self.assertEquals(af.recursive, True)
        self.assertEquals(af.archive_classes, [])

        af = ArchiveFinder(TEST_DIRPATH, False, [AllIsArchive,])

        self.assertEquals(af.root_path, TEST_DIRPATH)
        self.assertEquals(af.recursive, False)
        self.assertEquals(af.archive_classes, [AllIsArchive,])

    def test_find_archives_recursivity(self):
        af = ArchiveFinder()
        
        self.assertEquals(len(af.find_archives(TEST_DIRPATH, False)), 1)
        self.assertNotEquals(len(af.find_archives(TEST_DIRPATH, True)), 1)

    def test_get_path_archives(self):
        af = ArchiveFinder()
        filenames = ['archive_1.1', 'archive_1.2', 'archive_1.3',
                     'archive_2.1', 'archive_2.2', 'archive_2.3',]
        
        result = af.get_path_archives('path', filenames)
        self.assertEquals(result, [])
        result = af.get_path_archives('path', filenames, [AllIsArchive,])
        self.assertEquals(len(result), 2)
        self.assertTrue(isinstance(result[0], AllIsArchive))

    def test_is_archive_file(self):
        af = ArchiveFinder()
        
        self.assertFalse(af.is_archive_file('toto.avi'))
        self.assertEquals(af.is_archive_file('toto.avi', [AllIsArchive,]), AllIsArchive)

    def test_archives(self):
        af = ArchiveFinder()
        af.path_archives_found = TEST_PATH_ARCHIVES
        
        self.assertEquals(len(af.archives), 3)


suite = unittest.TestLoader().loadTestsFromTestCase(ArchiveFinderTestCase)
