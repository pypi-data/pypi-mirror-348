#!/usr/bin/env python
"""
Unit tests for the file_loader module.

This test suite validates:
- Loading data from various file formats
- Loading paired X/y data
- Handling CSV files with headers
- Ensuring correct array shapes
- Using the data cache
"""

import os
import sys
import pytest
import tempfile
import numpy as np
import time
from pathlib import Path

# Add parent directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Import modules to test
from fit_better.data.file_loader import (
    load_file_to_array,
    load_data_from_files,
    match_xy_by_key,
    load_dataset,
    save_data_to_files,
    enable_cache,
    clear_cache,
)


@pytest.fixture
def sample_data():
    """Create sample data for testing file operations."""
    X = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]])
    y = np.array([10, 20, 30, 40])
    return X, y


@pytest.fixture
def sample_csv_files(tmpdir, sample_data):
    """Create sample CSV files for testing file operations."""
    X, y = sample_data

    # Create X data file with header
    x_file = tmpdir.join("x_data.csv")
    with open(x_file, "w") as f:
        f.write("feature1,feature2,feature3\n")
        for row in X:
            f.write(f"{row[0]},{row[1]},{row[2]}\n")

    # Create y data file with header
    y_file = tmpdir.join("y_data.csv")
    with open(y_file, "w") as f:
        f.write("target\n")
        for val in y:
            f.write(f"{val}\n")

    # Create key-based X file
    x_key_file = tmpdir.join("x_key_data.csv")
    with open(x_key_file, "w") as f:
        f.write("id,feature1,feature2\n")
        for i, row in enumerate(X[:, :2]):
            f.write(f"{i+1},{row[0]},{row[1]}\n")

    # Create key-based y file
    y_key_file = tmpdir.join("y_key_data.csv")
    with open(y_key_file, "w") as f:
        f.write("id,target\n")
        for i, val in enumerate(y):
            f.write(f"{i+1},{val}\n")

    # Create a combined data file for dataset loading
    combined_file = tmpdir.join("combined_data.csv")
    with open(combined_file, "w") as f:
        f.write("feature1,feature2,feature3,target\n")
        for i in range(len(X)):
            f.write(f"{X[i][0]},{X[i][1]},{X[i][2]},{y[i]}\n")

    return {
        "x_file": str(x_file),
        "y_file": str(y_file),
        "x_key_file": str(x_key_file),
        "y_key_file": str(y_key_file),
        "combined_file": str(combined_file),
        "dir": str(tmpdir),
    }


class TestFileLoader:
    """Tests for the file_loader module."""

    def test_load_file_to_array(self, sample_csv_files):
        """Test loading a single file into a numpy array."""
        # Load X data with header
        X_loaded = load_file_to_array(
            sample_csv_files["x_file"], delimiter=",", header="infer"
        )

        assert isinstance(X_loaded, np.ndarray)
        assert X_loaded.shape[1] == 3  # 3 features
        assert X_loaded.shape[0] == 4  # 4 samples

        # Load y data with header
        y_loaded = load_file_to_array(
            sample_csv_files["y_file"], delimiter=",", header="infer"
        )

        assert isinstance(y_loaded, np.ndarray)
        assert y_loaded.shape[0] == 4  # 4 samples

        # Load specific column by index
        feature2 = load_file_to_array(
            sample_csv_files["x_file"], delimiter=",", header="infer", target_column=1
        )

        assert feature2.shape == (4,)

        # Load specific column by name
        feature1 = load_file_to_array(
            sample_csv_files["x_file"],
            delimiter=",",
            header="infer",
            target_column="feature1",
        )

        assert feature1.shape == (4,)

    def test_load_data_from_files(self, sample_csv_files):
        """Test loading X and y data from separate files."""
        X_train, y_train, X_test, y_test = load_data_from_files(
            input_dir=sample_csv_files["dir"],
            x_train_file="x_data.csv",
            y_train_file="y_data.csv",
            x_test_file="x_data.csv",  # Using same file for test data in this example
            y_test_file="y_data.csv",
            delimiter=",",
        )

        assert X_train.shape == (4, 3)
        assert y_train.shape == (4,)
        assert X_test.shape == (4, 3)
        assert y_test.shape == (4,)

    def test_match_xy_by_key(self, sample_csv_files):
        """Test matching X and y based on key columns."""
        X, y = match_xy_by_key(
            X_path=sample_csv_files["x_key_file"],
            y_path=sample_csv_files["y_key_file"],
            x_key_column="id",
            y_key_column="id",
            x_value_columns=["feature1", "feature2"],
            y_value_column="target",
            delimiter=",",
        )

        assert X.shape == (4, 2)  # 4 samples, 2 features (excluding key)
        assert y.shape == (4,)

        # Test with different key ordering by creating files with shuffled keys
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create shuffled key files
            x_shuffled = os.path.join(tmpdir, "x_shuffled.csv")
            with open(x_shuffled, "w") as f:
                f.write("id,feature1,feature2\n")
                f.write("3,7,8\n")
                f.write("1,1,2\n")
                f.write("4,10,11\n")
                f.write("2,4,5\n")

            y_shuffled = os.path.join(tmpdir, "y_shuffled.csv")
            with open(y_shuffled, "w") as f:
                f.write("id,target\n")
                f.write("2,20\n")
                f.write("4,40\n")
                f.write("1,10\n")
                f.write("3,30\n")

            X_matched, y_matched = match_xy_by_key(
                X_path=x_shuffled,
                y_path=y_shuffled,
                x_key_column="id",
                y_key_column="id",
                delimiter=",",
            )

            assert X_matched.shape[0] == 4
            assert y_matched.shape[0] == 4

            # First row should be id=1
            assert X_matched[0][0] == 1  # feature1 value for id=1

    def test_load_dataset(self, sample_csv_files):
        """Test loading a dataset from a single file with automatic splitting."""
        # Test with default test split
        X_train, X_test, y_train, y_test = load_dataset(
            file_path=sample_csv_files["combined_file"],
            target_column="target",
            test_size=0.5,  # Use 50% split for predictable results with small test data
            random_state=42,
        )

        assert X_train.shape[1] == 3  # 3 features
        assert X_test.shape[1] == 3
        assert X_train.shape[0] + X_test.shape[0] == 4  # 4 total samples
        assert len(y_train) + len(y_test) == 4

        # Test with validation split
        X_train, X_val, X_test, y_train, y_val, y_test = load_dataset(
            file_path=sample_csv_files["combined_file"],
            target_column="target",
            test_size=0.25,
            val_size=0.25,
            random_state=42,
        )

        assert X_train.shape[0] + X_val.shape[0] + X_test.shape[0] == 4

    def test_save_data_to_files(self, sample_data, tmpdir):
        """Test saving data to files in different formats."""
        X, y = sample_data
        output_dir = str(tmpdir.join("output"))

        # Test saving in numpy format
        save_data_to_files(
            output_dir=output_dir,
            X_train=X,
            y_train=y,
            X_test=X,
            y_test=y,
            format="npy",
        )

        assert os.path.exists(os.path.join(output_dir, "X_train.npy"))
        assert os.path.exists(os.path.join(output_dir, "y_train.npy"))
        assert os.path.exists(os.path.join(output_dir, "X_test.npy"))
        assert os.path.exists(os.path.join(output_dir, "y_test.npy"))

        # Test saving in CSV format
        save_data_to_files(
            output_dir=output_dir,
            X_train=X,
            y_train=y,
            X_test=X,
            y_test=y,
            format="csv",
            x_train_name="X_train_csv",
            y_train_name="y_train_csv",
        )

        assert os.path.exists(os.path.join(output_dir, "X_train_csv.csv"))
        assert os.path.exists(os.path.join(output_dir, "y_train_csv.csv"))

    def test_cache_functionality(self, sample_csv_files):
        """Test the data caching functionality."""
        # Enable caching
        enable_cache(True)

        # First load should cache the data
        start_time = time.time()
        X1 = load_file_to_array(sample_csv_files["x_file"], delimiter=",")
        first_load_time = time.time() - start_time

        # Second load should be faster due to cache
        start_time = time.time()
        X2 = load_file_to_array(sample_csv_files["x_file"], delimiter=",")
        second_load_time = time.time() - start_time

        # Test cache correctness
        np.testing.assert_array_equal(X1, X2)

        # Clear cache
        clear_cache()

        # Load again after clearing cache
        start_time = time.time()
        X3 = load_file_to_array(sample_csv_files["x_file"], delimiter=",")
        third_load_time = time.time() - start_time

        # Disable cache
        enable_cache(False)

        # Load with cache disabled
        X4 = load_file_to_array(sample_csv_files["x_file"], delimiter=",")

        # Verify data correctness
        np.testing.assert_array_equal(X1, X3)
        np.testing.assert_array_equal(X1, X4)


if __name__ == "__main__":
    pytest.main(["-v", __file__])
