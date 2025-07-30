"""Unit test for frame_check.ValidationResult"""
import unittest
import pandas as pd
from framecheck.frame_check import ValidationResult


class TestValidationResult(unittest.TestCase):
    """
    Test suite for ValidationResult, verifying result status, summary formatting,
    row indexing, and error/warning serialization behavior.
    """
    def setUp(self):
        """Initialize a default DataFrame for row indexing tests."""
        self.df = pd.DataFrame({
            'a': [1, 2, 3],
            'b': ['x', 'y', 'z']
        })

    def test_is_valid_true(self):
        """Test is_valid returns True when there are no errors."""
        result = ValidationResult(errors=[], warnings=[])
        self.assertTrue(result.is_valid)

    def test_is_valid_false(self):
        """Test is_valid returns False when errors are present."""
        result = ValidationResult(errors=['some error'], warnings=[])
        self.assertFalse(result.is_valid)

    def test_to_dict(self):
        """Test dictionary serialization includes correct values."""
        result = ValidationResult(errors=['err1'], warnings=['warn1'])
        result_dict = result.to_dict()
        self.assertEqual(result_dict['errors'], ['err1'])
        self.assertEqual(result_dict['warnings'], ['warn1'])
        self.assertFalse(result_dict['is_valid'])

    def test_get_invalid_rows_default(self):
        """Test returns DataFrame subset for failing rows by index."""
        failing = {1, 2}
        result = ValidationResult(errors=['err'], warnings=[], failing_row_indices=failing)
        out = result.get_invalid_rows(self.df)
        self.assertEqual(len(out), 2)
        self.assertTrue((out.index == [1, 2]).all())

    def test_get_invalid_rows_errors_only(self):
        """Test includes only rows with errors when include_warnings=False."""
        failing = {0, 1, 2}
        result = ValidationResult(errors=['err'], warnings=['warn'], failing_row_indices=failing)
        result._error_indices = {0, 2}  # simulate error-only rows
        out = result.get_invalid_rows(self.df, include_warnings=False)
        self.assertEqual(set(out.index), {0, 2})

    def test_get_invalid_rows_invalid_index(self):
        """Test raises ValueError when failing index is not in DataFrame."""
        result = ValidationResult(errors=[], warnings=[], failing_row_indices={99})
        with self.assertRaises(ValueError):
            result.get_invalid_rows(self.df)

    def test_get_invalid_rows_duplicate_index(self):
        """Test raises ValueError when DataFrame has duplicate index values."""
        df = pd.DataFrame({'x': [1, 2, 3, 4]}, index=[0, 0, 1, 2])
        result = ValidationResult(errors=['err'], warnings=[], failing_row_indices={0})
        with self.assertRaises(ValueError):
            result.get_invalid_rows(df)

    def test_get_invalid_rows_empty(self):
        """Test returns empty DataFrame when there are no failing indices."""
        result = ValidationResult(errors=[], warnings=[], failing_row_indices=set())
        out = result.get_invalid_rows(self.df)
        self.assertTrue(out.empty)

    def test_get_invalid_rows_errors_only_without_tracking(self):
        """Test raises ValueError when error-only filtering is requested but not tracked."""
        result = ValidationResult(errors=['err'], warnings=['warn'], failing_row_indices={0})
        with self.assertRaises(ValueError):
            result.get_invalid_rows(self.df, include_warnings=False)

    def test_summary_with_warnings_only(self):
        """Test summary output shows success and lists warnings."""
        result = ValidationResult(errors=[], warnings=['warn one', 'warn two'])
        summary = result.summary()
        self.assertIn("Validation PASSED", summary)
        self.assertIn("2 warning(s)", summary)
        self.assertIn("Warnings:", summary)
        self.assertIn("warn one", summary)
        self.assertIn("warn two", summary)

    def test_summary_with_errors_and_warnings(self):
        """Test summary output includes both errors and warnings."""
        result = ValidationResult(errors=['error 1'], warnings=['warn 1'])
        summary = result.summary()
        self.assertIn("Validation FAILED", summary)
        self.assertIn("1 error(s), 1 warning(s)", summary)
        self.assertIn("Errors:", summary)
        self.assertIn("error 1", summary)
        self.assertIn("Warnings:", summary)
        self.assertIn("warn 1", summary)

    def test_to_dict_all_clear(self):
        """Test to_dict returns clean structure when no issues exist."""
        result = ValidationResult(errors=[], warnings=[])
        self.assertEqual(result.to_dict(), {
            'is_valid': True,
            'errors': [],
            'warnings': []
        })



if __name__ == '__main__':
    unittest.main()
