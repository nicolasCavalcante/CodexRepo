import subprocess
import sys
from pathlib import Path

from dagster import Definitions, asset

from app.core.settings import get_env

API_PACKAGE_DIR = Path(__file__).resolve().parents[1] / "api"
if str(API_PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(API_PACKAGE_DIR))


@asset
def run_dbt_models() -> str:
    analytics_dir = get_env("ANALYTICS_DIR", required=True)
    command = [
        "dbt",
        "run",
        "--project-dir",
        analytics_dir,
        "--profiles-dir",
        analytics_dir,
    ]
    subprocess.run(command, check=True)
    return "dbt run completed"


@asset(deps=[run_dbt_models])
def run_dbt_tests() -> str:
    analytics_dir = get_env("ANALYTICS_DIR", required=True)
    command = [
        "dbt",
        "test",
        "--project-dir",
        analytics_dir,
        "--profiles-dir",
        analytics_dir,
    ]
    subprocess.run(command, check=True)
    return "dbt test completed"


defs = Definitions(assets=[run_dbt_models, run_dbt_tests])
