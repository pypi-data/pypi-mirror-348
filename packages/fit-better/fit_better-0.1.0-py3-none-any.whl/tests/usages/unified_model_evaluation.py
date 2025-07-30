#!/usr/bin/env python3
"""
Author: hi@xlindo.com
Create Time: 2025-05-10
Description: Unified script for evaluating models with various partition strategies and regressor types.

Usage:
    python unified_model_evaluation.py [options]

This script combines functionality from partition_and_regressor_example.py and best_partition_and_regressor_example.py
to provide a single entry point for model evaluation, with options to test a specific model configuration
or automatically find the best combination of partition strategy and regressor type.

Options:
    --input-dir DIR        Directory containing input data files (default: data)
    --x-train FILE         Filename for X_train data (default: X_train.npy)
    --y-train FILE         Filename for y_train data (default: y_train.npy)
    --x-test FILE          Filename for X_test data (default: X_test.npy)
    --y-test FILE          Filename for y_test data (default: y_test.npy)
    --delimiter CHAR       Delimiter character for CSV or TXT files (default: ' ' for TXT, ',' for CSV)
    --header OPTION        How to handle headers in CSV/TXT files: 'infer' or 'none' (default: 'infer')
    --evaluation-mode      Evaluation mode: 'single' (one configuration) or 'find_best' (try multiple) (default: single)
    --partition-mode       Partition mode to use (default: KMEANS)
    --n-partitions INT     Number of partitions to create (default: 5)
    --regressor-type       Regressor type to use (default: RANDOM_FOREST)
    --n-jobs N             Number of parallel jobs (default: 1)
    --output-dir DIR       Directory to save results (default: model_results)
    --save-predictions     Save training and evaluation predictions to CSV files
    --use-regression-flow  Use RegressionFlow for a more streamlined workflow
    --test-mode            Run in test mode with fewer combinations for faster testing (only for find_best mode)
"""
import os
import sys
import logging
import numpy as np
from pathlib import Path
from datetime import datetime
from time import time

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

# Import from fit_better
from fit_better import (
    PartitionMode,
    RegressorType,
    setup_logging,
    generate_synthetic_data_by_function,
    save_data,
    load_data_from_files,
)

# Import utilities for argument parsing and model evaluation
from tests.utils.argparse_utils import get_default_parser
from tests.utils.model_evaluation import train_and_evaluate_model, find_best_model

# Logger will be configured in main function using setup_logging
logger = None


def main():
    # Parse command line arguments using the utility function
    parser = get_default_parser(
        description="Unified script for evaluating models with various partition strategies and regressor types"
    )

    # Add evaluation mode argument
    parser.add_argument(
        "--evaluation-mode",
        type=str,
        choices=["single", "find_best"],
        default="single",
        help="Evaluation mode: 'single' (one configuration) or 'find_best' (try multiple)",
    )

    # Add test mode argument
    parser.add_argument(
        "--test-mode",
        action="store_true",
        help="Run in test mode with fewer combinations for faster testing (only for find_best mode)",
    )

    # Add regression flow flag
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

        logger.info(f"Starting unified model evaluation in {args.evaluation_mode} mode")
        logger.info(f"Configuration: {vars(args)}")

        # Ensure output directories exist
        os.makedirs(args.output_dir, exist_ok=True)

        # Check for existing data or generate synthetic data
        input_files = [args.x_train, args.y_train, args.x_test, args.y_test]
        input_paths = [os.path.join(args.input_dir, f) for f in input_files]

        if not all(os.path.exists(p) for p in input_paths):
            logger.info(
                "One or more input files not found, generating synthetic data..."
            )
            os.makedirs(args.input_dir, exist_ok=True)

            # Generate synthetic data
            # Use different functions depending on evaluation mode to provide appropriate test data
            if args.evaluation_mode == "find_best":
                # More complex function for testing different strategies
                X_train, y_train, X_test, y_test = generate_synthetic_data_by_function(
                    function=lambda X: 3.0 * np.sin(2.0 * X[:, 0] + 0.5)
                    + 1.5 * np.cos(X[:, 1]) * X[:, 2] ** 2,
                    n_samples_train=5000,
                    n_samples_test=1000,
                    n_features=3,
                    noise_std=0.7,
                    add_outliers=True,
                    random_state=42,
                )
            else:
                # Simpler function for single model evaluation
                X_train, y_train, X_test, y_test = generate_synthetic_data_by_function(
                    function=lambda X: 3.0 * np.sin(2.0 * X[:, 0] + 0.5)
                    + 1.5 * np.cos(X[:, 1])
                    - X[:, 2],
                    n_samples_train=5000,
                    n_samples_test=1000,
                    n_features=3,
                    noise_std=0.5,
                    add_outliers=True,
                    random_state=42,
                )

            # Save the generated data in both formats
            formats = ["csv", "npy"]
            for fmt in formats:
                save_data(
                    X_train,
                    y_train,
                    X_test,
                    y_test,
                    output_dir=args.input_dir,
                    base_name="data",
                    format=fmt,
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
                        logger.warning(
                            f"Couldn't create file copy from {source_path} to {target_path}: {e}"
                        )

            logger.info(f"Generated and saved synthetic data to {args.input_dir}")
            logger.info(
                f"Data shapes: X_train {X_train.shape}, y_train {y_train.shape}, X_test {X_test.shape}, y_test {y_test.shape}"
            )
        else:
            # Load data from files
            logger.info(f"Loading data from {args.input_dir}...")

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

        # Process based on evaluation mode
        if args.evaluation_mode == "single":
            # Convert partition mode and regressor type strings to enum values
            partition_mode = PartitionMode[args.partition_mode]
            regressor_type = RegressorType[args.regressor_type]

            # Train and evaluate a single model
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

            logger.info(
                f"Evaluation completed for {partition_mode} partitioning with {regressor_type} regressor"
            )
            print(f"\nResults summary:")
            print(f"Partition mode: {partition_mode}")
            print(f"Number of partitions: {results['n_partitions']}")
            print(f"Regressor type: {regressor_type}")
            print(f"Test R²: {results['test_metrics']['r2']:.4f}")

        else:  # find_best mode
            # Find the best partition strategy and regression algorithm
            best_result = find_best_model(
                X_train,
                y_train,
                X_test,
                y_test,
                n_jobs=args.n_jobs,
                output_dir=args.output_dir,
                test_mode=args.test_mode,
            )

            logger.info("Best model evaluation completed")
            print("\nBest combination found:")
            print(f"Partition mode: {best_result['partition_mode']}")
            print(f"Number of partitions: {best_result['n_partitions']}")
            print(f"Regressor type: {best_result['regressor_type']}")
            print(f"Test R²: {best_result['test_r2']:.4f}")

        end_time = time()
        logger.info(f"Total execution time: {end_time - start_time:.2f} seconds")
        logger.info(f"Results saved to {args.output_dir}")
        logger.info(f"Log file: {log_file}")

        print(f"\nExecution completed successfully!")
        print(f"Results saved to {args.output_dir}")
        print(f"Log file: {log_file}")

    except Exception as e:
        if logger:
            logger.error(f"Error occurred: {str(e)}", exc_info=True)
        else:
            print(f"Error occurred before logger was initialized: {str(e)}")
        raise


if __name__ == "__main__":
    main()
