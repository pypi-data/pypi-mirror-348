import gitlab
import logging
from dotenv import load_dotenv
import sys
import os

# --- Logging Configuration ---
# Configure logging to output to stdout with a specific format and level
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
# --- End Logging Configuration ---

logger = logging.getLogger(__name__)

load_dotenv()

# --- Configuration ---
GITLAB_URL = os.getenv('GITLAB_URL')
PRIVATE_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN_AGILE')
# --- End Configuration ---

def get_all_project_ids_python_gitlab():
    """
    Fetches all accessible project IDs from GitLab using the python-gitlab library.
    """
    project_ids = []
    
    print(f"Connecting to {GITLAB_URL}...")
    try:
        # Initialize GitLab connection
        # For self-hosted GitLab with self-signed certs, you might need:
        # gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN, ssl_verify=False)
        gl = gitlab.Gitlab(GITLAB_URL, private_token=PRIVATE_TOKEN, timeout=30)
        
        # Authenticate (optional, but good for checking credentials early)
        gl.auth()
        print(f"Successfully authenticated as: {gl.user.username}")

        # Get all projects the authenticated user has access to
        # The library handles pagination automatically with `all=True`
        # `simple=True` makes the query faster by fetching less data per project
        projects = gl.projects.list(all=True, simple=True, owned=None, membership=True) 
        # `owned=None` (default) considers all projects.
        # Set `owned=True` for only projects owned by the token's user.
        # Set `membership=True` (default) to include projects where user is a member.

        for project in projects:
            project_ids.append({
                'id': project.id,
                'name': f"{project.name} ({project.web_url})"
            })
        
        print(f"Fetched {len(project_ids)} project IDs.")

    except gitlab.exceptions.GitlabAuthenticationError:
        print("Authentication failed. Check your GITLAB_URL and PRIVATE_TOKEN, and token scopes.")
    except gitlab.exceptions.GitlabHttpError as e:
        print(f"GitLab HTTP Error: {e.error_message} (Status code: {e.response_code})")
    except gitlab.exceptions.GitlabError as e:
        print(f"An error occurred with the GitLab API: {e}")
    except requests.exceptions.ConnectionError as e:
        print(f"Connection Error: Could not connect to {GITLAB_URL}. Details: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
    return project_ids

if __name__ == "__main__":
    if PRIVATE_TOKEN == "YOUR_PRIVATE_ACCESS_TOKEN":
        print("ERROR: Please set your GITLAB_URL and PRIVATE_TOKEN in the script.")
    else:
        all_ids = get_all_project_ids_python_gitlab()
        if all_ids:
            print(f"\nFound {len(all_ids)} project IDs in total:")
            # for pid in all_ids:
            #     print(pid)
            print(all_ids) # Print the list directly
        else:
            print("\nNo project IDs found or an error occurred.")