import os
import subprocess
from pathlib import Path

from dagster import Definitions, asset
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / '.env')


@asset
def run_dbt_models() -> str:
    analytics_dir = os.getenv('ANALYTICS_DIR', '../analytics')
    command = ['dbt', 'run', '--project-dir', analytics_dir, '--profiles-dir', analytics_dir]
    subprocess.run(command, check=True)
    return 'dbt run completed'


@asset(deps=[run_dbt_models])
def run_dbt_tests() -> str:
    analytics_dir = os.getenv('ANALYTICS_DIR', '../analytics')
    command = ['dbt', 'test', '--project-dir', analytics_dir, '--profiles-dir', analytics_dir]
    subprocess.run(command, check=True)
    return 'dbt test completed'


defs = Definitions(assets=[run_dbt_models, run_dbt_tests])
