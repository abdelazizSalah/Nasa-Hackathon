"""Checks that the proof rejects bad data and does not alter installed startup files."""
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from gmat_smoke import prepare_startup, validate_report
from common import gmat_executable


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'report.txt'

    def test_rejects_truncated_report(self):
        self.path.write_text('0 31359 6993 0 0 0 6.6 3.6\n')
        with self.assertRaisesRegex(ValueError, '11 samples'):
            validate_report(self.path)

    def test_rejects_nonfinite_samples(self):
        self.path.write_text('0 31359 nan 0 0 0 6.6 3.6\n')
        with self.assertRaisesRegex(ValueError, 'finite'):
            validate_report(self.path)

    def test_startup_is_local_and_preserves_source(self):
        root = Path(self.temp.name)
        bin_dir = root / 'install' / 'bin'
        bin_dir.mkdir(parents=True)
        source = bin_dir / 'gmat_startup_file.txt'
        original = 'ROOT_PATH = ../\nOUTPUT_PATH = ../output/\nPLUGIN = ../plugins/libPythonInterface_py312\nPLUGIN = ../plugins/libStation\n'
        source.write_text(original)
        output = root / 'project-output'
        output.mkdir()
        destination = prepare_startup(bin_dir / 'GmatConsole.exe', output)
        self.assertEqual(source.read_text(), original)
        self.assertEqual(destination.parent, output)
        self.assertIn(output.as_posix(), destination.read_text())
        self.assertIn('# Standalone proof', destination.read_text())

    def test_configured_missing_console_is_actionable(self):
        with self.assertRaisesRegex(FileNotFoundError, 'configured path'):
            gmat_executable(str(Path(self.temp.name) / 'does-not-exist'))


if __name__ == '__main__':
    unittest.main()
