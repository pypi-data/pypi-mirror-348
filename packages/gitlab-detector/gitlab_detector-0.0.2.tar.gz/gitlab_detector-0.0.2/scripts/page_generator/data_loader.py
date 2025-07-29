import sys
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def _read_data(filepath='public/data.json'):
    """
    Reads the JSON data file or returns default data.

    Args:
        filepath (str): Path to the JSON data file.

    Returns:
        dict: Loaded data or default structure on error.
    """
    logger.debug(f"Attempting to read data from: {filepath}")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            # --- PATCH: Ensure 'iterations' key exists at top-level ---
            if 'iterations' not in data:
                logger.warning("'iterations' key missing in data.json. Adding empty array.")
                data['iterations'] = []
            # Defensive: If 'iterations' is not a list, fix it
            if not isinstance(data['iterations'], list):
                logger.error("'iterations' key in data.json is not a list. Overwriting with empty array.")
                data['iterations'] = []
            return data
    except FileNotFoundError:
        logger.warning(f"Data file not found at {filepath}. Using default empty data structure.")
        return _get_default_data()
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {filepath}: {e}. Using default empty data structure.", exc_info=False)
        return _get_default_data()
    except Exception as e:
        logger.error(f"An unexpected error occurred while reading {filepath}: {e}", exc_info=True)
        return _get_default_data()

def _get_default_data():
    """Returns a default data structure when data.json is missing or invalid."""
    return {
        "generated_at": datetime.now().isoformat(),
        "total_issues": 0,
        "total_anomalies": 0,
        "anomalies_by_severity": {"high": 0, "medium": 0, "low": 0},
        "anomalies": [],
        "milestones": [],
        "iterations": []
    }

def load_environment_variables():
    """Loads and validates environment variables."""
    load_dotenv()
    logger.info("Loaded environment variables (if .env file exists)")
    
    # Access GitLab credentials
    gitlab_url = os.getenv('GITLAB_URL')
    gitlab_token = os.getenv('GITLAB_ACCESS_TOKEN_AGILE')
    gitlab_project_id = os.getenv('GITLAB_PROJECT_ID')
    
    # Log if these crucial variables are loaded
    logger.debug(f"GITLAB_URL: {gitlab_url}")
    logger.debug(f"GITLAB_PROJECT_ID: {gitlab_project_id}")
    
    return {
        'GITLAB_URL': gitlab_url,
        'GITLAB_ACCESS_TOKEN': gitlab_token,
        'GITLAB_PROJECT_ID': gitlab_project_id
    }
