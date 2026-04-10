import logging
import os
import sys
from pathlib import Path
from urllib.parse import urlparse

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from mlflow.models.signature import infer_signature
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
DATA_PATH = SCRIPT_DIR / "winequality-red.csv"
DEFAULT_REMOTE_TRACKING_URI = "https://dagshub.com/shovo896/ML-Ops-.mlflow"

load_dotenv(PROJECT_ROOT / ".env")
load_dotenv(SCRIPT_DIR / ".env")


def configure_tracking():
    tracking_uri = os.getenv("MLFLOW_TRACKING_URI")
    dagshub_token = os.getenv("DAGSHUB_USER_TOKEN") or os.getenv("DAGSHUB_TOKEN")

    if tracking_uri:
        mlflow.set_tracking_uri(tracking_uri)
        return mlflow.get_tracking_uri()

    if dagshub_token:
        try:
            import dagshub
        except ImportError as exc:
            raise RuntimeError(
                "DagsHub logging was requested, but the 'dagshub' package is not installed "
                "in the active Python environment."
            ) from exc
        os.environ.setdefault("DAGSHUB_USER_TOKEN", dagshub_token)
        dagshub.init(repo_owner="shovo896", repo_name="ML-Ops-", mlflow=True)
        mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", DEFAULT_REMOTE_TRACKING_URI))
        return mlflow.get_tracking_uri()

    local_tracking_dir = SCRIPT_DIR / "mlruns"
    mlflow.set_tracking_uri(local_tracking_dir.as_uri())
    logger.warning(
        "DAGSHUB_USER_TOKEN is not set. Logging to the local MLflow store at %s",
        local_tracking_dir,
    )
    return mlflow.get_tracking_uri()


def eval_metrics(actual, pred):
    rmse = np.sqrt(mean_squared_error(actual, pred))
    mae = mean_absolute_error(actual, pred)
    r2 = r2_score(actual, pred)
    return rmse, mae, r2


def main():
    tracking_uri = configure_tracking()
    tracking_url_type = urlparse(tracking_uri).scheme

    data = pd.read_csv(DATA_PATH, sep=None, engine="python")

    train, test = train_test_split(data, random_state=42)
    train_x = train.drop(["quality"], axis=1)
    test_x = test.drop(["quality"], axis=1)
    train_y = train["quality"]
    test_y = test["quality"]

    alpha = float(sys.argv[1]) if len(sys.argv) > 1 else 0.5
    l1_ratio = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5

    with mlflow.start_run():
        lr = ElasticNet(alpha=alpha, l1_ratio=l1_ratio, random_state=42)
        lr.fit(train_x, train_y)

        predicted_qualities = lr.predict(test_x)
        rmse, mae, r2 = eval_metrics(test_y, predicted_qualities)
        signature = infer_signature(train_x, predicted_qualities)

        print(f"ElasticNet model (alpha={alpha:.6f}, l1_ratio={l1_ratio:.6f}):")
        print(f"  RMSE: {rmse}")
        print(f"  MAE: {mae}")
        print(f"  R2: {r2}")

        mlflow.log_param("alpha", alpha)
        mlflow.log_param("l1_ratio", l1_ratio)
        mlflow.log_metric("rmse", rmse)
        mlflow.log_metric("r2", r2)
        mlflow.log_metric("mae", mae)

        if tracking_url_type != "file":
            mlflow.sklearn.log_model(
                lr,
                "model",
                signature=signature,
                registered_model_name="ElasticnetWineModel",
            )
        else:
            mlflow.sklearn.log_model(lr, "model", signature=signature)


if __name__ == "__main__":
    main()
    



