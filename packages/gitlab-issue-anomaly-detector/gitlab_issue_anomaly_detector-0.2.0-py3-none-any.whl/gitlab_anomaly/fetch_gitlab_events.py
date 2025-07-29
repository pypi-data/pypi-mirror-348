import sys
import os
import gitlab
from datetime import datetime, timezone, timedelta
import time
import json
import logging
from dotenv import load_dotenv
from scripts import constants

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


# --- Script Logic ---

def format_datetime(dt_str):
    if not dt_str:
        return "N/A"
    try:
        if '.' in dt_str:
             dt_str = dt_str.split('.')[0] + 'Z'
        dt_obj_utc = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%SZ')
        dt_obj_utc = dt_obj_utc.replace(tzinfo=timezone.utc)
        dt_local = dt_obj_utc.astimezone()
        return dt_local.strftime('%Y-%m-%d %H:%M:%S %Z')
    except (ValueError, TypeError) as e:
        return dt_str

def get_notes_activities(issue):
    """Fetches notes activities (comments and system notes)."""
    activities = []
    try:
        logger.info(f"Fetching notes for issue #{issue.iid}...")
        notes = issue.notes.list(sort='asc', order_by='created_at', per_page=constants.PAGE_SIZE, iterator=True)
        logger.info(f"Found {len(notes)} notes for issue #{issue.iid}")
        for note in notes:
            activity = {
                'type': 'COMMENT' if not note.system else 'NOTE_SYSTEM',
                'timestamp': note.created_at,
                'actor': note.author.get('name', 'N/A') + f" (@{note.author.get('username', 'N/A')})",
                'body': note.body.strip(),
                'raw': note.attributes
            }
            activities.append(activity)
    except Exception as e:
        logger.error(f"Error fetching notes for issue #{issue.iid}: {e}")
    
    activities.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')))
    return activities

def get_milestone_activities(issue):
    """Fetches milestone events."""
    activities = []
    try:
        logger.info(f"Fetching milestone events for issue #{issue.iid}...")
        milestone_events = issue.resourcemilestoneevents.list(sort='asc', per_page=constants.PAGE_SIZE, iterator=True)
        logger.info(f"Found {len(milestone_events)} milestone events for issue #{issue.iid}")
        for event in milestone_events:
            action_text = f"{event.action} milestone"
            milestone_name = event.milestone.get('title', 'N/A') if event.milestone else 'None'
            if event.action == 'add':
                action_text = f"changed milestone to %{milestone_name}"
            elif event.action == 'remove':
                action_text = f"removed milestone %{milestone_name}"

            activity = {
                'type': 'MILESTONE_EVENT',
                'timestamp': event.created_at,
                'actor': event.user.get('name', 'N/A') + f" (@{event.user.get('username', 'N/A')})",
                'body': action_text,
                'raw': event.attributes
            }
            activities.append(activity)
    except gitlab.exceptions.GitlabListError as e:
        logger.warning(f"Error fetching milestone events for issue #{issue.iid} (perhaps none exist?): {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching milestone events for issue #{issue.iid}: {e}")

    activities.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')))
    return activities

def get_label_activities(issue):
    """Fetches label events."""
    activities = []
    try:
        logger.info(f"Fetching label events for issue #{issue.iid}...")
        label_events = issue.resourcelabelevents.list(sort='asc', per_page=constants.PAGE_SIZE, iterator=True)
        logger.info(f"Found {len(label_events)} label events for issue #{issue.iid}")
        for event in label_events:
            action_text = f"{event.action} label"
            label_name = event.label.get('name', 'N/A') if event.label else 'None'
            if event.action == 'add':
                action_text = f"added ~{label_name} label"
            elif event.action == 'remove':
                action_text = f"removed ~{label_name} label"

            activity = {
                'type': 'LABEL_EVENT',
                'timestamp': event.created_at,
                'actor': event.user.get('name', 'N/A') + f" (@{event.user.get('username', 'N/A')})",
                'body': action_text,
                'raw': event.attributes
            }
            activities.append(activity)
    except gitlab.exceptions.GitlabListError as e:
        logger.warning(f"Error fetching label events for issue #{issue.iid} (perhaps none exist?): {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching label events for issue #{issue.iid}: {e}")

    activities.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')))
    return activities

def get_state_activities(issue):
    """Fetches state events (open/close)."""
    activities = []
    try:
        logger.info(f"Fetching state events for issue #{issue.iid}...")
        state_events = issue.resourcestateevents.list(sort='asc', per_page=constants.PAGE_SIZE, iterator=True)
        logger.info(f"Found {len(state_events)} state events for issue #{issue.iid}")
        for event in state_events:
            state_action = event.state
            if state_action == 'reopened':
                action_text = "reopened issue"
            elif state_action == 'closed':
                action_text = "closed issue"
            else:
                action_text = f"{state_action} issue"

            activity = {
                'type': 'STATE_EVENT',
                'timestamp': event.created_at,
                'actor': event.user.get('name', 'N/A') + f" (@{event.user.get('username', 'N/A')})",
                'body': action_text,
                'raw': event.attributes
            }
            activities.append(activity)
    except gitlab.exceptions.GitlabListError as e:
        logger.warning(f"Error fetching state events for issue #{issue.iid} (perhaps none exist?): {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching state events for issue #{issue.iid}: {e}")
    
    activities.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')))
    return activities

def get_iteration_activities(issue):
    """Fetches iteration events."""
    activities = []
    try:
        logger.info(f"Fetching iteration events for issue #{issue.iid}...")
        if hasattr(issue, 'resource_iteration_events'):
            iteration_events = issue.resource_iteration_events.list(sort='asc', per_page=constants.PAGE_SIZE, iterator=True)
            logger.info(f"Found {len(iteration_events)} iteration events for issue #{issue.iid}")
            for event in iteration_events:
                iteration_title = event.iteration.get('title', 'N/A') if event.iteration else 'None'
                if event.action == 'add':
                    action_text = f"changed iteration to %{iteration_title}"
                elif event.action == 'remove':
                    action_text = f"removed iteration %{iteration_title}"
                else:
                    action_text = f"{event.action} iteration %{iteration_title}"

                activity = {
                    'type': 'ITERATION_EVENT',
                    'timestamp': event.created_at,
                    'actor': event.user.get('name', 'N/A') + f" (@{event.user.get('username', 'N/A')})",
                    'body': action_text,
                    'raw': event.attributes
                }
                activities.append(activity)
        else:
            logger.info("Skipping iteration events: 'resourceiterationevents' attribute not found on issue object.")
    except gitlab.exceptions.GitlabListError as e:
        logger.warning(f"Error fetching iteration events (perhaps none exist or feature unavailable?): {e}")
    except Exception as e:
        logger.error(f"Unexpected error fetching iteration events: {e}")

    activities.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')))
    return activities

def get_combined_activities(issue):
    """Fetches notes and specific resource events, then combines and sorts them."""
    logger.info(f"--- Fetching activities for Issue #{issue.iid} ---")
    
    # Collect all activities from different sources
    all_activities = []
    all_activities.extend(get_notes_activities(issue))
    all_activities.extend(get_milestone_activities(issue))
    all_activities.extend(get_label_activities(issue))
    all_activities.extend(get_state_activities(issue))
    all_activities.extend(get_iteration_activities(issue))

    # Sort all collected activities by timestamp
    logger.info("--- Sorting all collected activities ---")
    all_activities.sort(key=lambda x: datetime.fromisoformat(x['timestamp'].replace('Z', '+00:00')))

    return all_activities

def print_combined_activities(issue):
    """Fetches, combines, and prints activities including specific resource events."""
    logger.info(f"\n=== Combined Activities Log for Issue #{issue.iid}: {issue.title} ===")
    logger.info(f"    URL: {issue.web_url}")

    activities = get_combined_activities(issue)
    setattr(issue, 'activities', activities)


    if not activities:
        logger.info("\n    --- Chronological Activity Log ---")
        logger.info("    - No activities found.")
        logger.info("=" * (len(f"=== Combined Activities Log for Issue #{issue.iid}: {issue.title} ===") + 5))
        return

    logger.info("\n    --- Chronological Activity Log ---")
    for activity in activities:
        timestamp_str = format_datetime(activity['timestamp'])
        actor = activity['actor']
        body = activity['body']
        type = activity['type']

        # Improve comment display slightly
        if type == 'COMMENT':
             logger.info(f"    - [{timestamp_str}] ({type}) {actor} commented:")
             for line in body.splitlines():
                 logger.info(f"        {line}")
        else:
             logger.info(f"    - [{timestamp_str}] ({type}) {actor}: {body}")

    logger.info("=" * (len(f"=== Combined Activities Log for Issue #{issue.iid}: {issue.title} ===") + 5))

def main():
    if not GITLAB_PRIVATE_TOKEN:
        logger.error("Error: GitLab Personal Access Token not found.")
        logger.error("Please set the GITLAB_PRIVATE_TOKEN environment variable.")
        return

    logger.info(f"Connecting to GitLab at {GITLAB_URL}...")
    try:
        gl = gitlab.Gitlab(GITLAB_URL, private_token=GITLAB_PRIVATE_TOKEN)
        gl.auth()
        logger.info("Authentication successful.")
    except gitlab.GitlabAuthenticationError:
        logger.error("Authentication failed. Please check your GITLAB_PRIVATE_TOKEN.")
        return
    except Exception as e:
        logger.error(f"Error connecting to GitLab or authenticating: {e}")
        return

    try:
        logger.info(f"Fetching project '{PROJECT_ID}'...")
        project = gl.projects.get(PROJECT_ID)
        logger.info(f"Found project: {project.name_with_namespace}")
    except gitlab.exceptions.GitlabGetError:
        logger.error(f"Error: Project '{PROJECT_ID}' not found or access denied.")
        return
    except Exception as e:
        logger.error(f"An error occurred while fetching the project: {e}")
        return

    if SPECIFIC_ISSUE_IID:
        logger.info(f"\nFetching specific issue #{SPECIFIC_ISSUE_IID}...")
        try:
            issue = project.issues.get(SPECIFIC_ISSUE_IID)
            print_combined_activities(issue)
        except gitlab.exceptions.GitlabGetError:
            logger.error(f"Error: Issue #{SPECIFIC_ISSUE_IID} not found in project '{PROJECT_ID}'.")
        except Exception as e:
            logger.error(f"An error occurred fetching issue #{SPECIFIC_ISSUE_IID}: {e}")
    else:
        logger.info("\nFetching multiple issues is currently disabled in this example. Set SPECIFIC_ISSUE_IID.")

if __name__ == "__main__":
    # --- Configuration ---
    GITLAB_URL = os.getenv('GITLAB_URL')
    GITLAB_PRIVATE_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN_AGILE')
    # --- !! Less Secure Alternative !! ---
    # GITLAB_PRIVATE_TOKEN = 'YOUR_TOKEN_HERE'
    # -----------------------------------
    PROJECT_ID = os.getenv('GITLAB_PROJECT_ID')
    ISSUE_STATE = 'opened'
    # --- !! Set to the IID from your screenshot !! ---
    SPECIFIC_ISSUE_IID = 65 # <--- CHANGE THIS if needed, otherwise it will check issue #65

    MAX_ISSUES_TO_CHECK = 1 # Focus on one issue when using SPECIFIC_ISSUE_IID
    SORT_ISSUES_BY = 'updated_at'
    SORT_ISSUES_ORDER = 'desc'

    main()
    logger.info("\nScript finished.")
