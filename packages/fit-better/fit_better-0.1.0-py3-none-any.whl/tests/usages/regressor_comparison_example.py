#!/usr/bin/env python3
"""
Author: xlindo
Create Time: 2025-05-10
Description: Example script for comparing different regression algorithms on the same dataset.

Usage:
    python regressor_comparison_example.py [options]

This script demonstrates how to compare multiple regression algorithms using the fit-better
package. It generates synthetic data, fits multiple regression models, and compares their
performance using various metrics like MAE, RMSE, R², and percentage-based metrics.

Options:
    --n-samples N          Number of samples to generate (default: 1000)
    --noise-level N        Standard deviation of noise to add (default: 0.5)
    --n-jobs N             Number of parallel jobs (default: 1)
    --output-dir DIR       Directory to save results (default: regressor_comparison_results)
    --function-type STR    Type of function for synthetic data: linear, sine, polynomial, complex (default: sine)
"""
import os
import sys
import argparse
import logging
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent.parent))

# Import from fit_better - handle possible import location changes
from fit_better import (
    RegressorType,
    fit_all_regressors,
    select_best_model,
    generate_train_test_data,
)

# Try to import calc_regression_statistics from different possible locations
try:
    from fit_better import calc_regression_statistics
except ImportError:
    try:
        from fit_better.utils.statistics import calc_regression_statistics
    except ImportError:
        # If all else fails, define a simple version
        def calc_regression_statistics(y_true, y_pred, residual_percentiles=(1, 3, 5, 10)):
            """Simplified calculation of regression statistics."""
            from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
            import numpy as np
            mae = mean_absolute_error(y_true, y_pred)
            mse = mean_squared_error(y_true, y_pred)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_true, y_pred)
            
            # Calculate percentage within thresholds
            rel_errors = np.abs((y_pred - y_true) / (np.abs(y_true) + 1e-10))
            stats = {
                "mae": float(mae),
                "mse": float(mse),
                "rmse": float(rmse),
                "r2": float(r2),
            }
            
            # Add percentile metrics
            for p in [1, 3, 5, 10] + list(residual_percentiles):
                stats[f"pct_within_{p}pct"] = float(np.mean(rel_errors <= (p / 100.0)) * 100.0)
            
            return stats

# Try to import ASCII table utility
try:
    from fit_better.utils.ascii import print_ascii_table
except ImportError:
    # Fallback implementation
    def print_ascii_table(headers, rows, to_log=False):
        """Simple ASCII table printer."""
        # Create row format string based on contents
        col_widths = [max(len(str(row[i])) for row in rows + [headers]) for i in range(len(headers))]
        row_format = "| " + " | ".join("{:<" + str(width) + "}" for width in col_widths) + " |"
        
        # Create header and separator
        header_str = row_format.format(*headers)
        separator = "+" + "+".join("-" * (width + 2) for width in col_widths) + "+"
        
        # Build table as string
        table_str = separator + "\n" + header_str + "\n" + separator + "\n"
        for row in rows:
            table_str += row_format.format(*[str(item) for item in row]) + "\n"
        table_str += separator
        
        # Print or log
        if to_log and logger:
            logger.info("\n" + table_str)
        else:
            print(table_str)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def compare_regressors(
    X_train=None,
    y_train=None,
    X_test=None,
    y_test=None,
    n_jobs=1,
    output_dir=None,
    visualize=True,
    n_partitions=None,
):
    """
    Compare different regression algorithms on the same dataset.

    Args:
        X_train: Training features (if None, will load test data)
        y_train: Training targets
        X_test: Test features
        y_test: Test targets
        n_jobs: Number of parallel jobs
        output_dir: Directory to save results
        visualize: Whether to generate visualizations
        n_partitions: Number of partitions to use (for compatibility with unit tests)

    Returns:
        Tuple of (best_regressor, best_mae) for compatibility with tests
    """
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    # If data not provided, load test data
    if X_train is None or y_train is None or X_test is None or y_test is None:
        X_train, y_train, X_test, y_test = load_test_data()

    # Fit all available regressors
    logger.info("Training all available regression models...")
    model_results = fit_all_regressors(X_train, y_train, n_jobs=n_jobs)

    # Evaluate each model on test data
    results = {}
    for model_dict in model_results:
        regressor_name = model_dict["model_name"]
        model = model_dict["model"]
        scaler = model_dict.get("scaler")
        transformer = model_dict.get("transformer")

        logger.info(f"Evaluating {regressor_name} on test data...")

        # Apply data transformations if needed
        X_test_processed = X_test
        if transformer:
            X_test_processed = transformer.transform(X_test)
        if scaler:
            X_test_processed = scaler.transform(X_test_processed)

        # Make predictions
        y_pred = model.predict(X_test_processed)

        # Calculate metrics
        metrics = calc_regression_statistics(y_test, y_pred)

        # Store results
        results[regressor_name] = {"metrics": metrics, "model": model_dict}

    # Print results table
    print_comparison_table(results)

    # Generate visualizations if requested
    if visualize and output_dir:
        plot_performance_comparison(results, output_dir)
        plot_predictions(X_train, y_train, X_test, y_test, results, output_dir)

    # Find best model by MAE
    best_regressor_name = min(results.items(), key=lambda x: x[1]["metrics"]["mae"])[0]
    best_mae = results[best_regressor_name]["metrics"]["mae"]

    # Convert the regressor name string to a RegressorType enum
    try:
        best_regressor = RegressorType.from_string(best_regressor_name)
    except ValueError:
        # If conversion fails, use SVR_RBF as a fallback
        logger.warning(
            f"Could not convert '{best_regressor_name}' to RegressorType. Using SVR_RBF as fallback."
        )
        best_regressor = RegressorType.SVR_RBF

    return best_regressor, best_mae


def print_comparison_table(results):
    """
    Print a formatted table comparing regressor performance.

    Args:
        results: Dictionary with results for each regressor
    """
    # Prepare data for table
    table_data = []
    metrics = ["mae", "rmse", "r2", "pct_within_1pct", "pct_within_5pct"]
    headers = ["Regressor", "MAE", "RMSE", "R²", "Within 1%", "Within 5%"]

    # Calculate ranks for each metric
    metric_ranks = {}
    for metric in metrics:
        # For R² and percentage metrics, higher is better
        reverse = metric in ["r2", "pct_within_1pct", "pct_within_5pct"]
        sorted_regressors = sorted(
            results.items(),
            key=lambda x: x[1]["metrics"].get(
                metric, float("-inf" if reverse else "inf")
            ),
            reverse=reverse,
        )
        ranks = {name: i + 1 for i, (name, _) in enumerate(sorted_regressors)}
        metric_ranks[metric] = ranks

    # Build table rows
    for name, data in results.items():
        m = data["metrics"]
        row = [
            name,
            f"{m['mae']:.4f} ({metric_ranks['mae'][name]})",
            f"{m['rmse']:.4f} ({metric_ranks['rmse'][name]})",
            f"{m['r2']:.4f} ({metric_ranks['r2'][name]})",
            f"{m.get('pct_within_1pct', 0):.1f}% ({metric_ranks['pct_within_1pct'].get(name, 'N/A')})",
            f"{m.get('pct_within_5pct', 0):.1f}% ({metric_ranks['pct_within_5pct'].get(name, 'N/A')})",
        ]
        table_data.append(row)

    # Sort by MAE (lowest first)
    table_data.sort(key=lambda x: float(x[1].split()[0]))

    # Print table using our own ASCII table formatter
    logger.info("\nRegressor Performance Comparison (with ranks):")
    print_ascii_table(headers, table_data, to_log=True)

    # Log best model for each metric
    logger.info("\nBest Models:")
    for metric, label in zip(metrics, ["MAE", "RMSE", "R²", "Within 1%", "Within 5%"]):
        best_name = min(
            results.items(),
            key=lambda x: x[1]["metrics"].get(
                metric,
                (
                    float("inf")
                    if metric not in ["r2", "pct_within_1pct", "pct_within_5pct"]
                    else float("-inf")
                ),
            ),
        )[0]
        best_value = results[best_name]["metrics"].get(metric, "N/A")
        logger.info(f"Best by {label}: {best_name} ({best_value:.4f})")


def plot_performance_comparison(results, output_dir):
    """
    Plot performance comparison between different regressors.

    Args:
        results: Dictionary with results for each regressor
        output_dir: Directory to save the plots
    """
    # Extract metrics
    regressor_names = list(results.keys())
    metrics = ["mae", "rmse", "r2", "pct_within_1pct", "pct_within_5pct"]
    metric_labels = ["MAE", "RMSE", "R²", "Within 1%", "Within 5%"]

    # Create subplot for each metric
    fig, axes = plt.subplots(len(metrics), 1, figsize=(12, 4 * len(metrics)))

    # Sort regressors by name to ensure consistent colors
    regressor_names.sort()

    # Plot each metric
    for i, (metric, label) in enumerate(zip(metrics, metric_labels)):
        # Regressors sorted by performance (better first)
        reverse = metric in ["r2", "pct_within_1pct", "pct_within_5pct"]
        sorted_data = sorted(
            [
                (name, results[name]["metrics"].get(metric, 0))
                for name in regressor_names
            ],
            key=lambda x: x[1],
            reverse=reverse,
        )
        names, values = zip(*sorted_data)

        # Create bar chart
        axes[i].barh(names, values)
        axes[i].set_title(f"{label} Comparison")
        axes[i].set_xlabel(label)

        # Add value labels
        for j, v in enumerate(values):
            axes[i].text(v, j, f"{v:.4f}", va="center")

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "regressor_performance_comparison.png"))
    plt.close()


def plot_predictions(X_train, y_train, X_test, y_test, results, output_dir):
    """
    Plot predictions from each regressor against ground truth.

    Args:
        X_train: Training features
        y_train: Training targets
        X_test: Test features
        y_test: Test targets
        results: Dictionary with results for each regressor
        output_dir: Directory to save the plots
    """
    # Flatten arrays for plotting
    X_test_flat = X_test.flatten()

    # Get sorted indices for plotting
    sort_idx = np.argsort(X_test_flat)
    X_sorted = X_test_flat[sort_idx]
    y_sorted = y_test[sort_idx]

    # Get top 5 models by MAE
    top_models = sorted(results.items(), key=lambda x: x[1]["metrics"]["mae"])[:5]

    # Create a plot
    plt.figure(figsize=(12, 8))

    # Plot training data points
    plt.scatter(X_train, y_train, s=10, alpha=0.3, label="Training Data", color="gray")

    # Plot test data points
    plt.scatter(X_test, y_test, s=20, alpha=0.5, label="Test Data", color="black")

    # Plot predictions for each regressor
    colors = ["red", "blue", "green", "purple", "orange"]
    for i, (name, data) in enumerate(top_models):
        # Get model and make predictions
        model_dict = data["model"]
        model = model_dict["model"]
        scaler = model_dict.get("scaler")
        transformer = model_dict.get("transformer")

        # Apply data transformations if needed
        X_test_processed = X_test.copy()
        if transformer:
            X_test_processed = transformer.transform(X_test_processed)
        if scaler:
            X_test_processed = scaler.transform(X_test_processed)

        # Make predictions
        y_pred = model.predict(X_test_processed)
        y_pred_sorted = y_pred[sort_idx]

        # Plot predictions
        plt.plot(
            X_sorted,
            y_pred_sorted,
            label=f"{name} (MAE={data['metrics']['mae']:.4f})",
            color=colors[i % len(colors)],
            linewidth=2,
        )

    plt.title("Top 5 Regressor Predictions")
    plt.xlabel("X")
    plt.ylabel("y")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(output_dir, "top_regressor_predictions.png"))
    plt.close()

    # Create individual plots for each model
    for name, data in results.items():
        plot_single_model_prediction(
            X_train, y_train, X_test, y_test, name, data, output_dir
        )


def plot_single_model_prediction(
    X_train, y_train, X_test, y_test, name, data, output_dir
):
    """
    Plot detailed prediction results for a single model.

    Args:
        X_train: Training features
        y_train: Training targets
        X_test: Test features
        y_test: Test targets
        name: Name of the regressor
        data: Results data for this regressor
        output_dir: Directory to save the plots
    """
    # Create model-specific directory
    model_dir = os.path.join(output_dir, "model_plots")
    os.makedirs(model_dir, exist_ok=True)

    # Flatten arrays for plotting
    X_test_flat = X_test.flatten()
    X_train_flat = X_train.flatten()

    # Get model and metrics
    model_dict = data["model"]
    model = model_dict["model"]
    scaler = model_dict.get("scaler")
    transformer = model_dict.get("transformer")
    metrics = data["metrics"]

    # Apply transformations and make predictions
    X_test_processed = X_test.copy()
    if transformer:
        X_test_processed = transformer.transform(X_test_processed)
    if scaler:
        X_test_processed = scaler.transform(X_test_processed)

    y_pred = model.predict(X_test_processed)

    # Get sorted indices for plotting
    sort_idx = np.argsort(X_test_flat)
    X_sorted = X_test_flat[sort_idx]
    y_sorted = y_test[sort_idx]
    y_pred_sorted = y_pred[sort_idx]

    # Calculate residuals
    residuals = y_test - y_pred

    # Create plot with two subplots: predictions and residuals
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # Plot 1: Predictions
    ax1.scatter(
        X_train_flat, y_train, s=10, alpha=0.3, label="Training Data", color="gray"
    )
    ax1.scatter(X_test_flat, y_test, s=20, alpha=0.5, label="Test Data", color="black")
    ax1.plot(X_sorted, y_pred_sorted, label="Predictions", color="red", linewidth=2)

    ax1.set_title(
        f"{name} Predictions\nMAE={metrics['mae']:.4f}, RMSE={metrics['rmse']:.4f}, R²={metrics['r2']:.4f}"
    )
    ax1.set_xlabel("X")
    ax1.set_ylabel("y")
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Plot 2: Residuals
    ax2.scatter(X_test_flat, residuals, alpha=0.7, color="blue")
    ax2.axhline(y=0, color="red", linestyle="--")
    ax2.set_title("Residuals (Test Data - Predictions)")
    ax2.set_xlabel("X")
    ax2.set_ylabel("Residual")
    ax2.grid(True, alpha=0.3)

    # Add histogram of residuals as an inset
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    inset_ax = inset_axes(ax2, width="30%", height="30%", loc="upper right")
    inset_ax.hist(residuals, bins=30, alpha=0.7, color="blue")
    inset_ax.set_title("Residual Distribution")
    inset_ax.axvline(x=0, color="red", linestyle="--")

    plt.tight_layout()

    # Clean filename
    filename = name.replace(" ", "_").replace("(", "").replace(")", "").lower()
    plt.savefig(os.path.join(model_dir, f"{filename}_analysis.png"))
    plt.close()


def load_test_data(
    data_dir=None,
    function_type="sine",
    n_samples=1000,
    noise_level=0.5,
    random_state=42,
):
    """
    Helper function to load test data for other test modules.

    Args:
        data_dir: Directory containing test data files (can be None)
        function_type: Type of function to generate
        n_samples: Number of samples
        noise_level: Noise level
        random_state: Random seed

    Returns:
        X_train, y_train, X_test, y_test
    """
    # If a directory is provided and it's a string, try to load from files
    if data_dir is not None and isinstance(data_dir, str):
        return load_test_data_from_dir(data_dir)

    # Otherwise generate synthetic data
    n_train = int(n_samples * 0.8)
    n_test = n_samples - n_train

    return generate_train_test_data(
        function_type=function_type,
        n_samples_train=n_train,
        n_samples_test=n_test,
        noise_std=noise_level,
        random_state=random_state,
    )


def load_test_data_from_dir(data_dir):
    """
    Load test data from files in a directory.

    Args:
        data_dir: Directory containing test data files

    Returns:
        X_train, y_train, X_test, y_test
    """
    import os
    import numpy as np

    # Define possible file patterns to look for
    patterns = [
        # Pattern 1: sine_X_train.txt, sine_y_train.txt, etc.
        {
            "X_train": "sine_X_train.txt",
            "y_train": "sine_y_train.txt",
            "X_test": "sine_X_test.txt",
            "y_test": "sine_y_test.txt",
        },
        # Pattern 2: X_train.txt, y_train.txt, etc.
        {
            "X_train": "X_train.txt",
            "y_train": "y_train.txt",
            "X_test": "X_test.txt",
            "y_test": "y_test.txt",
        },
        # Pattern 3: X_train.npy, y_train.npy, etc.
        {
            "X_train": "X_train.npy",
            "y_train": "y_train.npy",
            "X_test": "X_test.npy",
            "y_test": "y_test.npy",
        },
        # Pattern 4: sine_X_train.npy, sine_y_train.npy, etc.
        {
            "X_train": "sine_X_train.npy",
            "y_train": "sine_y_train.npy",
            "X_test": "sine_X_test.npy",
            "y_test": "sine_y_test.npy",
        },
    ]

    # Try each pattern until data is found
    for pattern in patterns:
        try:
            X_train_path = os.path.join(data_dir, pattern["X_train"])
            y_train_path = os.path.join(data_dir, pattern["y_train"])
            X_test_path = os.path.join(data_dir, pattern["X_test"])
            y_test_path = os.path.join(data_dir, pattern["y_test"])

            # Check if all files exist
            if (
                os.path.exists(X_train_path)
                and os.path.exists(y_train_path)
                and os.path.exists(X_test_path)
                and os.path.exists(y_test_path)
            ):

                # Load the data based on file extension
                if X_train_path.endswith(".npy"):
                    X_train = np.load(X_train_path)
                    y_train = np.load(y_train_path)
                    X_test = np.load(X_test_path)
                    y_test = np.load(y_test_path)
                else:
                    X_train = np.loadtxt(X_train_path)
                    y_train = np.loadtxt(y_train_path)
                    X_test = np.loadtxt(X_test_path)
                    y_test = np.loadtxt(y_test_path)

                # Ensure correct shapes
                if X_train.ndim == 1:
                    X_train = X_train.reshape(-1, 1)
                if X_test.ndim == 1:
                    X_test = X_test.reshape(-1, 1)

                return X_train, y_train, X_test, y_test
        except Exception as e:
            # If there's an error, try the next pattern
            continue

    # If no data found using any pattern, generate synthetic data as fallback
    logger.warning(
        f"Could not load data from {data_dir}. Generating synthetic data instead."
    )
    return load_test_data(None)


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Compare regression algorithms")

    parser.add_argument(
        "--n-samples", type=int, default=1000, help="Number of samples to generate"
    )
    parser.add_argument(
        "--noise-level", type=float, default=0.5, help="Standard deviation of noise"
    )
    parser.add_argument("--n-jobs", type=int, default=1, help="Number of parallel jobs")
    parser.add_argument(
        "--function-type",
        type=str,
        default="sine",
        choices=["linear", "sine", "polynomial", "complex"],
        help="Type of function for synthetic data",
    )

    # Output directory - default to a subdirectory in tests/data_gen
    tests_dir = Path(__file__).resolve().parent.parent
    default_output_dir = str(tests_dir / "data_gen" / "regressor_comparison_results")

    parser.add_argument(
        "--output-dir",
        type=str,
        default=default_output_dir,
        help="Directory to save results",
    )

    args = parser.parse_args()

    # Generate synthetic data
    logger.info(
        f"Generating {args.function_type} data with {args.n_samples} samples..."
    )

    # Calculate train and test samples based on a 80/20 split
    n_train = int(args.n_samples * 0.8)
    n_test = args.n_samples - n_train

    X_train, y_train, X_test, y_test = generate_train_test_data(
        function_type=args.function_type,
        n_samples_train=n_train,
        n_samples_test=n_test,
        noise_std=args.noise_level,
        random_state=42,
    )

    # Compare regressors
    logger.info("Comparing regression algorithms...")
    results = compare_regressors(
        X_train, y_train, X_test, y_test, n_jobs=args.n_jobs, output_dir=args.output_dir
    )

    # Print final message
    logger.info(f"Results and visualizations saved to {args.output_dir}")


if __name__ == "__main__":
    main()
