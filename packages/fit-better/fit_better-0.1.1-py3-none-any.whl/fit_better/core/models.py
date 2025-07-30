"""
Author: xlindo
Create Time: 2025-04-29
Description: Model fitting utilities for various regression algorithms and transformers.

Usage:
    from fit_better.core.models import fit_one_model, fit_all_regressors, select_best_model

    # Train all regressors on your data
    results = fit_all_regressors(X_train, y_train, n_jobs=4)

    # Select the best model based on MAE
    best_model = select_best_model(results, metric=Metric.MAE)

    # Train a specific regressor type
    results = fit_all_regressors(X_train, y_train, regressor_type=RegressorType.GRADIENT_BOOSTING)

This module provides utilities for training and evaluating regression models,
with support for parallel processing and diverse model types.
"""

# Standard library imports
import os
import logging
from importlib import import_module
from enum import Enum, auto

# Add import for our new logging utilities
from ..utils.logging_utils import get_logger, setup_worker_logging

# Create a module-level logger
logger = get_logger(__name__)

# Third-party imports
import numpy as np
from joblib import Parallel, delayed

# scikit-learn imports
from sklearn.linear_model import (
    LinearRegression,
    Ridge,
    HuberRegressor,
    Lasso,
    ElasticNet,
)
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    ExtraTreesRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
    BaggingRegressor,
)

# Conditional imports
try:
    from xgboost import XGBRegressor

    HAS_XGB = True
except ImportError:
    HAS_XGB = False

try:
    from lightgbm import LGBMRegressor

    HAS_LGBM = True
except ImportError:
    HAS_LGBM = False


class Metric(Enum):
    """Enum defining the different metrics for model evaluation."""

    MAE = "mae"
    RMSE = "rmse"
    MSE = "mse"
    R2 = "r2"
    PCT_WITHIN_1 = "pct_within_1pct"
    PCT_WITHIN_3 = "pct_within_3pct"
    PCT_WITHIN_5 = "pct_within_5pct"
    PCT_WITHIN_10 = "pct_within_10pct"
    PCT_WITHIN_20 = "pct_within_20pct"

    def __str__(self):
        return self.value


class RegressorType(Enum):
    """\n    Enum defining the types of regression algorithms available in `fit_better`.\n\n    Each member represents a specific regression model, primarily from scikit-learn,\n    XGBoost, or LightGBM. This enum provides a standardized way to specify and\n    instantiate regressors throughout the package.\n\n    The `create_regressor(regressor_type)` function can be used to get an instance\n    of the specified model with default parameters suitable for general use.\n    Users can further customize these models using scikit-learn's `set_params` method\n    or by directly instantiating them with desired parameters.\n\n    Attributes:\n        ALL: A special value used to indicate that all available regressors should be considered.\n             Not a specific model type itself.\n        LINEAR: Standard Ordinary Least Squares Linear Regression.\n            - Theory: Fits a linear model \(y = X\beta + c\) by minimizing the residual sum of squares\n              between the observed targets and the targets predicted by the linear approximation.\n            - Formula: \(\min_{\beta} ||X\beta - y||_2^2\)
    - Pros: Simple, interpretable, fast to train, no hyperparameters to tune.\n            - Cons: Assumes a linear relationship, sensitive to outliers, may underfit complex data.\n        POLYNOMIAL_2, POLYNOMIAL_3, POLYNOMIAL_4: Polynomial Regression of specified degree.\n            - Theory: Extends linear regression by adding polynomial terms of the features.\n              Transforms features \(x\) into \([x, x^2, ..., x^d]\) and then fits a linear model.\n            - Formula: \(y = \beta_0 + \beta_1 x + \beta_2 x^2 + ... + \beta_d x^d + \epsilon\)
    - Pros: Can model non-linear relationships, still relatively interpretable for low degrees.\n            - Cons: Prone to overfitting with high degrees, feature scaling is important, can be computationally intensive.\n        RIDGE: Ridge Regression (Linear Regression with L2 regularization).\n            - Theory: Adds a penalty equal to the square of the magnitude of coefficients to the loss function.\n              Shrinks coefficients and helps reduce model complexity and multicollinearity.\n            - Formula: \(\min_{\beta} ||X\beta - y||_2^2 + \alpha||eta||_2^2\)
    - Pros: Reduces overfitting, improves stability when features are correlated.\n            - Cons: Introduces bias, \(\alpha\) (regularization strength) needs tuning.\n        HUBER: Huber Regressor, robust to outliers.\n            - Theory: Combines aspects of MSE (for small errors) and MAE (for large errors) by using a quadratic loss for errors smaller\n              than a threshold \(\epsilon\) and linear loss for errors larger than \(\epsilon\).\n            - Pros: Less sensitive to outliers than OLS, provides a good balance between MSE and MAE.\n            - Cons: Requires tuning of \(\epsilon\), can be slower than OLS.\n        RANDOM_FOREST: Random Forest Regressor.\n            - Theory: An ensemble learning method that fits a number of decision tree regressors on various sub-samples of the dataset\n              and uses averaging to improve predictive accuracy and control overfitting.\n            - Pros: Powerful, handles non-linearities and interactions well, robust to outliers, requires less feature scaling.\n            - Cons: Less interpretable than linear models, can be computationally expensive, prone to overfitting on noisy data if not tuned.\n        LASSO: Lasso Regression (Linear Regression with L1 regularization).\n            - Theory: Adds a penalty equal to the absolute value of the magnitude of coefficients.\n              Can lead to sparse models where some feature coefficients become exactly zero.\n            - Formula: \(\min_{\beta} ||X\beta - y||_2^2 + \alpha||eta||_1\)
    - Pros: Performs feature selection by shrinking some coefficients to zero, helps with high-dimensional data.\n            - Cons: \(\alpha\) needs tuning, can be unstable with highly correlated features (may arbitrarily pick one).\n        ELASTIC_NET: ElasticNet Regression (Linear Regression with combined L1 and L2 regularization).\n            - Theory: Combines penalties from Lasso and Ridge regression.\n            - Formula: \(\min_{\beta} ||X\beta - y||_2^2 + \alpha \rho ||eta||_1 + \frac{\alpha(1-\rho)}{2} ||eta||_2^2\)
    - Pros: Combines benefits of Lasso (sparsity) and Ridge (stability with correlated features).\n            - Cons: Two hyperparameters (\(\alpha\) and \(\rho\)) to tune.\n        SVR_RBF: Support Vector Regression with Radial Basis Function (RBF) kernel.\n            - Theory: Finds a function that deviates from \(y\) by a value no greater than \(\epsilon\) for each training point,\n              and at the same time is as flat as possible. The RBF kernel allows modeling non-linear relationships.\n            - Pros: Effective in high-dimensional spaces, can model complex non-linearities.\n            - Cons: Computationally intensive, sensitive to hyperparameter choices (C, gamma, epsilon), less interpretable.\n        KNEIGHBORS: K-Neighbors Regressor.\n            - Theory: Predicts the target for a new data point based on the average target values of its k nearest neighbors in the feature space.\n            - Pros: Simple, non-parametric, can capture complex local relationships.\n            - Cons: Computationally expensive for large datasets, performance depends on distance metric and k, sensitive to irrelevant features (curse of dimensionality).\n        DECISION_TREE: Decision Tree Regressor.\n            - Theory: Builds a tree-like model of decisions. Each internal node represents a test on a feature, each branch represents an outcome, and each leaf node represents a target value (mean of samples in the leaf).\n            - Pros: Interpretable, handles non-linear data, requires little data preparation.\n            - Cons: Prone to overfitting (can be mitigated by pruning or ensemble methods), can be unstable (small changes in data can lead to different trees).\n        EXTRA_TREES: Extremely Randomized Trees Regressor.\n            - Theory: Similar to Random Forest, but randomness goes one step further in the way splits are computed. Thresholds are drawn at random for each candidate feature and the best of these randomly-generated thresholds is picked as the splitting rule.\n            - Pros: Generally faster to train than Random Forest, can reduce variance.\n            - Cons: May sometimes lead to slightly higher bias.\n        GRADIENT_BOOSTING: Gradient Boosting Regressor.\n            - Theory: An ensemble technique that builds models sequentially. Each new model attempts to correct the errors made by the previous ones.\n            - Pros: Highly accurate, can optimize various loss functions, handles complex data well.\n            - Cons: Prone to overfitting if not carefully tuned, can be slow to train due to sequential nature.\n        ADABOOST: AdaBoost Regressor.\n            - Theory: A boosting algorithm that fits a sequence of weak learners (e.g., decision trees) on repeatedly modified versions of the data. Predictions are combined through a weighted majority vote (or sum).\n            - Pros: Simple to implement, often performs well.\n            - Cons: Sensitive to noisy data and outliers.\n        BAGGING: Bagging Regressor.\n            - Theory: An ensemble method that fits base regressors each on random subsets of the original dataset (with replacement) and then aggregates their individual predictions (by averaging) to form a final prediction.\n            - Pros: Reduces variance, helps prevent overfitting.\n            - Cons: May not improve performance significantly if the base learner is already stable.\n        XGBOOST: XGBoost Regressor (Extreme Gradient Boosting).\n            - Theory: An optimized distributed gradient boosting library designed for speed and performance. Implements regularization and other advanced features.\n            - Pros: Highly efficient, state-of-the-art performance in many cases, handles missing values, built-in cross-validation.\n            - Cons: More hyperparameters to tune, can be complex.\n        LIGHTGBM: LightGBM Regressor (Light Gradient Boosting Machine).\n            - Theory: A gradient boosting framework that uses tree-based learning algorithms. It is designed to be distributed and efficient with faster training speed and lower memory usage.\n            - Pros: Very fast training, lower memory usage than XGBoost, good accuracy, supports categorical features directly.\n            - Cons: Can overfit on small datasets, sensitive to parameters.\n
    """

    ALL = "All Regressors"  # Special value to try all available regressors
    LINEAR = "Linear Regression"
    POLYNOMIAL_2 = "Polynomial Regression (deg=2)"
    POLYNOMIAL_3 = "Polynomial Regression (deg=3)"
    POLYNOMIAL_4 = "Polynomial Regression (deg=4)"
    RIDGE = "Ridge Regression"
    HUBER = "Huber Regressor"
    RANDOM_FOREST = "Random Forest Regression"
    LASSO = "Lasso Regression"
    ELASTIC_NET = "ElasticNet Regression"
    SVR_RBF = "SVR (RBF)"
    KNEIGHBORS = "KNeighbors Regressor"
    DECISION_TREE = "Decision Tree Regressor"
    EXTRA_TREES = "Extra Trees Regressor"
    GRADIENT_BOOSTING = "Gradient Boosting Regressor"
    ADABOOST = "AdaBoost Regressor"
    BAGGING = "Bagging Regressor"
    XGBOOST = "XGBoost Regressor"
    LIGHTGBM = "LightGBM Regressor"

    def __str__(self):
        return self.value

    @classmethod
    def from_string(cls, string_value):
        """Convert a string to the corresponding RegressorType enum.

        Args:
            string_value: String value to convert

        Returns:
            RegressorType enum value

        Raises:
            ValueError: If the string doesn't match any enum value
        """
        try:
            return cls(string_value)
        except ValueError:
            # Try a case-insensitive match on the enum names
            for enum_value in cls:
                if enum_value.name.lower().replace("_", " ") == string_value.lower():
                    return enum_value
            # If no match found, raise ValueError with available options
            valid_values = [f"{rt.name} ('{rt.value}')" for rt in cls]
            raise ValueError(
                f"Invalid regressor type: {string_value}. Valid values are: {valid_values}"
            )

    @classmethod
    def available_types(cls):
        """Return list of available regressor types, filtering out unavailable ones."""
        available = list(cls)
        # Always filter out the ALL type since it's a special case
        available = [r for r in available if r != cls.ALL]
        if not HAS_XGB:
            available = [r for r in available if r != cls.XGBOOST]
        if not HAS_LGBM:
            available = [r for r in available if r != cls.LIGHTGBM]
        return available


def _setup_subprocess_logging():
    """
    Configure logging for subprocesses by reading settings from environment variables.
    This ensures consistent logging across the main process and all worker processes.
    """
    # Use our centralized worker logging setup
    setup_worker_logging()


def _setup_worker_environment():
    """
    Set up environment variables that will be passed to worker processes.
    These variables allow worker processes to configure their logging correctly.
    """
    # Find the log file path from any existing file handler
    log_path = None
    for handler in logging.getLogger().handlers:
        if hasattr(handler, "baseFilename"):
            log_path = handler.baseFilename
            break

    # Set environment variables for worker processes
    if log_path:
        os.environ["LOG_PATH"] = log_path

    # Pass the current log level to worker processes
    current_level = logging.getLogger().level
    os.environ["LOG_LEVEL"] = str(current_level)


# Helper function to create regressor instances with appropriate parameters
def create_regressor(regressor_type):
    """
    Create and return a regressor instance with appropriate parameters based on type.

    Args:
        regressor_type: The RegressorType enum value

    Returns:
        An instance of the specified regressor with appropriate parameters
    """
    if regressor_type == RegressorType.LINEAR:
        return LinearRegression()
    elif regressor_type == RegressorType.RIDGE:
        return Ridge(alpha=1.0, random_state=42)
    elif regressor_type == RegressorType.HUBER:
        return HuberRegressor(epsilon=1.35)
    elif regressor_type == RegressorType.RANDOM_FOREST:
        return RandomForestRegressor(n_estimators=100, random_state=42)
    elif regressor_type == RegressorType.LASSO:
        return Lasso(alpha=0.1, random_state=42)
    elif regressor_type == RegressorType.ELASTIC_NET:
        return ElasticNet(alpha=0.1, l1_ratio=0.5, random_state=42)
    elif regressor_type == RegressorType.SVR_RBF:
        return SVR(kernel="rbf", C=100, gamma=0.1, epsilon=0.1)
    elif regressor_type == RegressorType.KNEIGHBORS:
        return KNeighborsRegressor(n_neighbors=5)
    elif regressor_type == RegressorType.DECISION_TREE:
        return DecisionTreeRegressor(random_state=42)
    elif regressor_type == RegressorType.EXTRA_TREES:
        return ExtraTreesRegressor(n_estimators=100, random_state=42)
    elif regressor_type == RegressorType.GRADIENT_BOOSTING:
        return GradientBoostingRegressor(n_estimators=100, random_state=42)
    elif regressor_type == RegressorType.ADABOOST:
        return AdaBoostRegressor(n_estimators=100, random_state=42)
    elif regressor_type == RegressorType.BAGGING:
        return BaggingRegressor(n_estimators=10, random_state=42)
    elif regressor_type == RegressorType.XGBOOST and HAS_XGB:
        return XGBRegressor(n_estimators=100, random_state=42)
    elif regressor_type == RegressorType.LIGHTGBM and HAS_LGBM:
        # Configure LightGBM with parameters to reduce warnings and improve small partition handling
        return LGBMRegressor(
            n_estimators=100,
            min_child_samples=5,  # Reduce minimum samples in leaf nodes
            min_split_gain=0,  # Allow splits with minimal gain
            subsample=0.8,  # Use subsampling to reduce overfitting
            verbosity=-1,  # Reduce verbosity of output
            random_state=42,
            force_row_wise=True,  # Avoid auto-selection warnings
            feature_name="auto",  # Automatically handle feature names
        )
    else:
        # Default to LinearRegression if the type is not recognized
        logger.warning(
            f"Unknown regressor type: {regressor_type}, using LinearRegression"
        )
        return LinearRegression()


def fit_one_model(args):
    """
    Fit a single regression model.

    Args:
        args: Tuple containing (regressor_type, model_class, X, y, transformer)
             where regressor_type is a RegressorType enum

    Returns:
        Dictionary with model info, stats, and transformer
    """
    # Set up logging for this subprocess
    _setup_subprocess_logging()

    regressor_type, model_class, X, y, transformer = args

    # Input validation
    if np.any(np.isnan(X)) or np.any(np.isinf(X)):
        raise ValueError("Input X contains NaN or inf values")
    if np.any(np.isnan(y)) or np.any(np.isinf(y)):
        raise ValueError("Input y contains NaN or inf values")

    # Ensure X is 2D
    if X.ndim == 1:
        X = X.reshape(-1, 1)

    # Add data preprocessing
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Create model instance with optimized parameters
    if model_class == "CREATE_WITH_PARAMS":
        # Use our helper function to create regressor with appropriate params
        model = create_regressor(regressor_type)
    else:
        # Use the provided model_class
        model = model_class()

    # Ensure we don't divide by zero when calculating percentage metrics
    nonzero_y = np.abs(y) > 1e-10

    # Fit the model
    try:
        # Handle LightGBM specially to avoid feature_name warnings
        if regressor_type == RegressorType.LIGHTGBM and HAS_LGBM:
            # For LightGBM, explicitly set feature names to avoid warnings
            feature_names = [f"feature_{i}" for i in range(X_scaled.shape[1])]
            model.fit(X_scaled, y, feature_name=feature_names)
        else:
            # For all other models, use standard fit
            model.fit(X_scaled, y)

        # Make predictions with error handling for numerical stability
        try:
            with np.errstate(all="ignore"):  # Suppress numpy warnings
                y_pred = model.predict(X_scaled)
        except Exception as pred_error:
            logger.warning(
                f"Error in prediction for {regressor_type}: {str(pred_error)}"
            )
            return None

        # Calculate statistics
        stats = {
            "mae": np.mean(np.abs(y - y_pred)),
            "mse": np.mean((y - y_pred) ** 2),
            "rmse": np.sqrt(np.mean((y - y_pred) ** 2)),
            "r2": model.score(X_scaled, y),
            "n_samples": len(y),
        }

        # Calculate percentage metrics only on non-zero y values to avoid division by zero
        if np.any(nonzero_y):
            y_subset = y[nonzero_y]
            y_pred_subset = y_pred[nonzero_y]
            rel_errors = np.abs((y_subset - y_pred_subset) / y_subset)

            stats.update(
                {
                    "pct_within_1pct": 100 * np.mean(rel_errors <= 0.01),
                    "pct_within_3pct": 100 * np.mean(rel_errors <= 0.03),
                    "pct_within_5pct": 100 * np.mean(rel_errors <= 0.05),
                    "pct_within_10pct": 100 * np.mean(rel_errors <= 0.10),
                    "pct_within_20pct": 100 * np.mean(rel_errors <= 0.20),
                }
            )

        logger.debug(
            f"Successfully fitted {regressor_type} model with {len(y)} samples"
        )

        return {
            "model": model,
            "model_name": str(regressor_type),
            "stats": stats,
            "transformer": transformer,
            "scaler": scaler,  # Store the scaler for later use
        }
    except Exception as e:
        logger.warning(f"Error fitting {regressor_type} model: {str(e)}")
        return None


def fit_all_regressors(X, y, n_jobs=1, regressor_type=None):
    """
    Fit all available regression models to the data, or a specific one if specified.

    Args:
        X: Feature matrix
        y: Target vector
        n_jobs: Number of parallel jobs to run
        regressor_type: Optional RegressorType enum or string to fit only one specific model

    Returns:
        List of dictionaries containing fitted models and stats
    """
    # Create polynomial features for polynomial regression models
    poly2 = PolynomialFeatures(degree=2)
    X_poly2 = poly2.fit_transform(X)
    poly3 = PolynomialFeatures(degree=3)
    X_poly3 = poly3.fit_transform(X)
    poly4 = PolynomialFeatures(degree=4)
    X_poly4 = poly4.fit_transform(X)

    # Use "CREATE_WITH_PARAMS" as a marker to use our helper function
    # that creates regressors with optimized parameters
    model_configs = [
        (RegressorType.LINEAR, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.POLYNOMIAL_2, LinearRegression, X_poly2, y, poly2),
        (RegressorType.POLYNOMIAL_3, LinearRegression, X_poly3, y, poly3),
        (RegressorType.POLYNOMIAL_4, LinearRegression, X_poly4, y, poly4),
        (RegressorType.RIDGE, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.HUBER, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.RANDOM_FOREST, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.LASSO, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.ELASTIC_NET, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.SVR_RBF, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.KNEIGHBORS, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.DECISION_TREE, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.EXTRA_TREES, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.GRADIENT_BOOSTING, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.ADABOOST, "CREATE_WITH_PARAMS", X, y, None),
        (RegressorType.BAGGING, "CREATE_WITH_PARAMS", X, y, None),
    ]

    # Add optional models if available
    if HAS_XGB:
        model_configs.append((RegressorType.XGBOOST, "CREATE_WITH_PARAMS", X, y, None))

    if HAS_LGBM:
        model_configs.append((RegressorType.LIGHTGBM, "CREATE_WITH_PARAMS", X, y, None))

    # If a specific regressor type is requested, filter the list
    if regressor_type is not None and regressor_type != RegressorType.ALL:
        model_configs = [cfg for cfg in model_configs if cfg[0] == regressor_type]
        if not model_configs:
            raise ValueError(f"Regressor type {regressor_type} not available")

        # Only log "Fitting only model" when we're actually fitting just one model type
        logger.debug(
            f"[fit_all_regressors] Using specific model: {model_configs[0][0]}"
        )
    else:
        logger.debug(
            f"[fit_all_regressors] Trying all available regressors ({len(model_configs)} models)"
        )
    # Set up environment variables for worker processes
    _setup_worker_environment()

    logger.debug(f"[fit_all_regressors] Using n_jobs={n_jobs}")

    # Safety check - if we have too few samples, don't use parallelization
    if len(y) < 50 and n_jobs != 1:
        old_n_jobs = n_jobs
        n_jobs = 1
        logger.warning(
            f"[fit_all_regressors] Small sample size ({len(y)} < 50), "
            f"reducing n_jobs from {old_n_jobs} to {n_jobs} to avoid multiprocessing overhead"
        )

    # If input is small and there are many models to fit, sequential might be faster
    if len(y) < 200 and len(model_configs) <= 3 and n_jobs != 1:
        old_n_jobs = n_jobs
        n_jobs = 1
        logger.debug(
            f"[fit_all_regressors] Small problem size with few models, "
            f"using sequential processing (n_jobs={n_jobs})"
        )

    try:
        if n_jobs != 1:
            # Run model fitting in parallel with error handling
            logger.debug(
                f"[fit_all_regressors] Running in parallel with n_jobs={n_jobs}"
            )
            results = Parallel(n_jobs=n_jobs, backend="loky", verbose=0)(
                delayed(fit_one_model)(cfg) for cfg in model_configs
            )

            # Filter out any None results (from failed model fits)
            results = [r for r in results if r is not None]

            if not results:
                logger.warning(
                    "[fit_all_regressors] All parallel model fits failed! Falling back to sequential execution"
                )
                raise RuntimeError("Parallel execution failed")
        else:
            # Force sequential execution
            raise ValueError("Force sequential execution")

    except Exception as e:
        logger.debug(f"[fit_all_regressors] Using sequential processing: {str(e)}")
        # Fall back to sequential processing
        results = []
        for cfg in model_configs:
            try:
                result = fit_one_model(cfg)
                if result is not None:
                    results.append(result)
            except Exception as e:
                logger.error(
                    f"[fit_all_regressors] Error fitting model {cfg[0]}: {str(e)}"
                )

    # Report results
    if results:
        logger.debug(f"[fit_all_regressors] Successfully fitted {len(results)} models")
    else:
        logger.warning("[fit_all_regressors] No models were successfully fitted!")

    return results


def select_best_model(results, exclude_types=None, metric=Metric.MAE):
    """
    Select the best model based on a given metric.

    Args:
        results: List of model result dictionaries from fit_all_regressors
        exclude_types: List/tuple of RegressorType enums to exclude from consideration
                      (default: exclude LINEAR)
        metric: The Metric enum to use for model selection (e.g., Metric.MAE, Metric.R2)

    Returns:
        The best model result dictionary
    """
    # Default to excluding Linear Regression if nothing specified
    if exclude_types is None:
        exclude_types = (RegressorType.LINEAR,)

    # Get the string names of the excluded regressor types
    exclude_names = [str(ex_type) for ex_type in exclude_types]

    # Filter out excluded models
    filtered = [r for r in results if r["model_name"] not in exclude_names]

    if not filtered:
        logger.warning("No models left after filtering. Using all models.")
        filtered = results

    # Get metric name as string
    metric_name = str(metric)

    # Select best model (higher is better for percentage metrics, lower is better for error metrics)
    if metric in (
        Metric.PCT_WITHIN_1,
        Metric.PCT_WITHIN_3,
        Metric.PCT_WITHIN_5,
        Metric.PCT_WITHIN_10,
        Metric.PCT_WITHIN_20,
    ):
        best = max(filtered, key=lambda r: r["stats"].get(metric_name, float("-inf")))
        logger.debug(
            f"Selected best model '{best['model_name']}' with {metric_name}={best['stats'].get(metric_name, 'N/A')}"
        )
    else:
        best = min(filtered, key=lambda r: r["stats"].get(metric_name, float("inf")))
        logger.debug(
            f"Selected best model '{best['model_name']}' with {metric_name}={best['stats'].get(metric_name, 'N/A')}"
        )

    return best
