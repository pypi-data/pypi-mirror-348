#!/usr/bin/env python3
"""
Author: xlindo
Create Time: 2025-05-10
Description: Simplified script for model evaluation using utility modules.

Usage:
    python simplified_model_evaluation.py --evaluation-mode single --partition-mode KMEANS --regressor-type RANDOM_FOREST
    python simplified_model_evaluation.py --evaluation-mode best --test-mode
    python simplified_model_evaluation.py --evaluation-mode multiple --n-jobs 4

This script demonstrates how to use the utility modules to simplify model evaluation.
It leverages the model_evaluation module to reduce code duplication and provide a standardized
interface for training and evaluating regression models with different partitioning strategies.
"""
import os
import sys
import logging
from datetime import datetime
from time import time
from pathlib import Path
import numpy as np
import argparse

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Import from fit_better
from fit_better import PartitionMode, RegressorType, setup_logging, load_data_from_files, generate_synthetic_data_by_function, save_data

# Import utilities
from tests.utils.argparse_utils import get_default_parser
from tests.utils.model_evaluation import train_and_evaluate_model, find_best_model

# Logger will be configured in main function
logger = None


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Simplified model evaluation script for fit-better"
    )
    # Get the tests directory for proper path resolution
    tests_dir = Path(__file__).resolve().parent.parent
    
    parser.add_argument(
        "--input-dir", default=str(tests_dir / "data_gen" / "data"), help="Directory containing input data files"
    )
    parser.add_argument(
        "--x-train", default="X_train.npy", help="Filename for X_train data"
    )
    parser.add_argument(
        "--y-train", default="y_train.npy", help="Filename for y_train data"
    )
    parser.add_argument(
        "--x-test", default="X_test.npy", help="Filename for X_test data"
    )
    parser.add_argument(
        "--y-test", default="y_test.npy", help="Filename for y_test data"
    )
    parser.add_argument(
        "--delimiter", default=None, help="Delimiter for CSV/TXT files"
    )
    parser.add_argument(
        "--header", default="infer", help="How to handle headers in CSV/TXT files"
    )
    parser.add_argument(
        "--partition-mode",
        default="KMEANS",
        choices=[mode.name for mode in PartitionMode],
        help="Partition mode to use",
    )
    parser.add_argument(
        "--n-partitions", type=int, default=5, help="Number of partitions to create"
    )
    parser.add_argument(
        "--regressor-type",
        default="RANDOM_FOREST",
        choices=[reg.name for reg in RegressorType],
        help="Regressor type to use",
    )
    parser.add_argument(
        "--n-jobs", type=int, default=1, help="Number of parallel jobs"
    )
    # Get the tests directory
    tests_dir = Path(__file__).resolve().parent.parent
    
    parser.add_argument(
        "--output-dir",
        default=str(tests_dir / "data_gen" / "model_eval_results"),
        help="Directory to save results",
    )
    parser.add_argument(
        "--log-dir",
        default=str(tests_dir / "data_gen" / "logs"),
        help="Directory to save log files",
    )
    parser.add_argument(
        "--save-predictions",
        action="store_true",
        help="Save training and evaluation predictions",
    )
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode with reduced configurations",
    )
    parser.add_argument(
        "--impute-strategy",
        default="mean",
        choices=["mean", "median", "most_frequent", "constant"],
        help="Strategy for imputing missing values",
    )
    parser.add_argument(
        "--impute-value", type=float, default=0, help="Value for constant imputation"
    )
    parser.add_argument(
        "--drop-na",
        action="store_true",
        help="Drop rows with NaN values instead of imputing",
    )
    parser.add_argument(
        "--evaluation-mode",
        choices=["single", "multiple", "best"],
        default="single",
        help="Evaluation mode: single (one configuration), multiple (test several), best (find optimal)",
    )
    parser.add_argument(
        "--use-regression-flow",
        action="store_true",
        help="Use RegressionFlow for a more streamlined workflow",
    )

    args = parser.parse_args()

    try:
        # Set up logging
        global logger
        os.makedirs(args.log_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = os.path.join(args.log_dir, f"model_evaluation_{timestamp}.log")
        logger = setup_logging(log_file)

        logger.info(f"Starting simplified model evaluation")
        logger.info(f"Configuration: {vars(args)}")

        # Ensure output directory exists
        os.makedirs(args.output_dir, exist_ok=True)

        # Check for existing data or generate synthetic data
        input_files = [args.x_train, args.y_train, args.x_test, args.y_test]
        input_paths = [os.path.join(args.input_dir, f) for f in input_files]

        if not all(os.path.exists(p) for p in input_paths):
            logger.info("One or more input files not found, generating synthetic data...")
            os.makedirs(args.input_dir, exist_ok=True)

            # Generate synthetic sine data separately for train and test
            X_train, y_train = generate_synthetic_data_by_function(
                function=lambda X: 3.0 * np.sin(2.0 * X[:, 0] + 0.5) + 1.5 * np.cos(X[:, 1]) - X[:, 2],
                n_samples=5000,
                n_features=3,
                noise_std=0.5,
                add_outliers=True,
                random_state=42,
            )
            
            X_test, y_test = generate_synthetic_data_by_function(
                function=lambda X: 3.0 * np.sin(2.0 * X[:, 0] + 0.5) + 1.5 * np.cos(X[:, 1]) - X[:, 2],
                n_samples=1000,
                n_features=3,
                noise_std=0.5,
                add_outliers=True,
                random_state=43,  # Different seed for test data
            )

            # Save the generated data
            save_data(
                X_train,
                y_train,
                X_test,
                y_test,
                output_dir=args.input_dir,
                base_name="data",
                format="npy",
            )

            # Create symlinks/copies for backward compatibility
            for target, source in zip(
                input_files,
                [
                    f"data_X_train.npy",
                    f"data_y_train.npy",
                    f"data_X_test.npy",
                    f"data_y_test.npy",
                ],
            ):
                target_path = os.path.join(args.input_dir, target)
                source_path = os.path.join(args.input_dir, source)
                if os.path.exists(source_path) and not os.path.exists(target_path):
                    try:
                        import shutil
                        shutil.copy2(source_path, target_path)
                    except Exception as e:
                        logger.warning(f"Couldn't create file copy from {source_path} to {target_path}: {e}")

            logger.info(f"Generated and saved synthetic data to {args.input_dir}")
        else:
            # Load data
            logger.info("Loading data...")
            # Set default delimiter based on file type if not specified
            if args.delimiter is None:
                if args.x_train.endswith(".txt"):
                    args.delimiter = " "
                else:
                    args.delimiter = ","
                logger.info(
                    f"Using default delimiter: '{args.delimiter}' based on file type"
                )

            X_train, y_train, X_test, y_test = load_data_from_files(
                args.input_dir,
                args.x_train,
                args.y_train,
                args.x_test,
                args.y_test,
                delimiter=args.delimiter,
                header=args.header,
            )

        start_time = time()

        # Determine which evaluation mode to use
        if args.evaluation_mode == "single":
            # Evaluate a single model configuration
            logger.info(
                f"Evaluating single model configuration: {args.partition_mode}, {args.n_partitions} partitions, {args.regressor_type}"
            )

            # Convert partition mode and regressor type strings to enum values
            partition_mode = PartitionMode[args.partition_mode]
            regressor_type = RegressorType[args.regressor_type]

            # Evaluate model using our new unified function
            results = train_and_evaluate_model(
                X_train,
                y_train,
                X_test,
                y_test,
                partition_mode=partition_mode,
                n_partitions=args.n_partitions,
                regressor_type=regressor_type,
                n_jobs=args.n_jobs,
                output_dir=args.output_dir,
                save_predictions=args.save_predictions,
                use_regression_flow=args.use_regression_flow,
                impute_strategy=args.impute_strategy,
                impute_value=args.impute_value,
                drop_na=args.drop_na,
            )

        elif args.evaluation_mode == "best":
            # Find the best model
            logger.info("Finding best model configuration...")

            # Find best model using our new unified function
            results = find_best_model(
                X_train,
                y_train,
                X_test,
                y_test,
                n_jobs=args.n_jobs,
                output_dir=args.output_dir,
                test_mode=args.test_mode,
            )

        else:  # multiple mode
            # Define configurations to evaluate
            if args.test_mode:
                partition_modes = [PartitionMode.RANGE, PartitionMode.KMEANS]
                regressor_types = [
                    RegressorType.LINEAR,
                    RegressorType.RIDGE,
                    RegressorType.RANDOM_FOREST,
                ]
                partition_counts = [2, 5]
            else:
                partition_modes = [
                    PartitionMode.RANGE,
                    PartitionMode.PERCENTILE,
                    PartitionMode.EQUAL_WIDTH,
                    PartitionMode.KMEANS,
                ]
                regressor_types = [
                    RegressorType.LINEAR,
                    RegressorType.POLYNOMIAL_2,
                    RegressorType.RIDGE,
                    RegressorType.HUBER,
                    RegressorType.RANDOM_FOREST,
                    RegressorType.GRADIENT_BOOSTING,
                    RegressorType.XGBOOST,
                ]
                partition_counts = [2, 3, 5, 8]

            # Find best model with customized parameters
            results = find_best_model(
                X_train,
                y_train,
                X_test,
                y_test,
                partition_modes=partition_modes,
                regressor_types=regressor_types,
                partition_counts=partition_counts,
                n_jobs=args.n_jobs,
                output_dir=args.output_dir,
                test_mode=args.test_mode,
            )

        end_time = time()
        logger.info(f"Total execution time: {end_time - start_time:.2f} seconds")
        logger.info(f"Results saved to {args.output_dir}")
        logger.info(f"Log file: {log_file}")

        print(f"\nExecution completed successfully!")
        print(f"Results saved to {args.output_dir}")
        print(f"Log file: {log_file}")

    except Exception as e:
        if logger:
            logger.exception(f"Error during execution: {e}")
        else:
            print(f"Error during execution (before logger was initialized): {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
