import sys
import os
import itertools

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from datetime import datetime
import json
import logging # Import the logging library
from datetime import datetime
from gitlab import Gitlab
from typing import List, Dict, Optional
from scripts.issue_anomaly_detector import IssueAnomalyDetector
from scripts import fetch_gitlab_events, constants
from dotenv import load_dotenv
import gitlab


# --- Logging Configuration ---
# Configure logging to output to stdout with a specific format and level
logging.basicConfig(
    level=logging.DEBUG,  # Set the logging level (e.g., INFO, DEBUG, WARNING)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout) # Ensure logs go to standard output
    ]
)
# --- End Logging Configuration ---

# Load environment variables from .env file
load_dotenv()

logging.info("Loaded environment variables") # Use logging instead of print

class GitLabIssueFetcher:
    def __init__(self, gitlab_url: str, private_token: str, project_id: str):
        """
        Initialize the GitLab client with authentication details.

        Args:
            gitlab_url: URL of the GitLab instance (e.g., 'https://gitlab.com')
            private_token: Personal access token with API permissions
            project_id: ID or path of the GitLab project
        """
        logging.info(f"Initializing GitLab client for URL: {gitlab_url} and Project ID: {project_id}")
        try:
            # Initialize GitLab client with SSL verification disabled
            self.gitlab = Gitlab(gitlab_url, private_token=private_token, ssl_verify=False)
            self.project = self.gitlab.projects.get(project_id)
            logging.info(f"Successfully connected to GitLab project: {self.project.name_with_namespace}")
        except Exception as e:
            logging.error(f"Failed to initialize GitLab client or get project: {e}", exc_info=True)
            raise # Re-raise exception to halt execution if connection fails

    def fetch_milestones(self, state: str = 'active') -> List[Dict]:
        """
        Fetch milestones from the configured GitLab project.

        Args:
            state: Filter by milestone state ('active', 'closed')

        Returns:
            List of milestone dictionaries with their issues
        """
        logging.info(f"Fetching '{state}' milestones for project {self.project.id}...")
        try:
            milestones = self.project.milestones.list(state=state, per_page=constants.PAGE_SIZE, iterator=True) # Use iterator for pagination
            milestone_data = []
            logging.info(f"Found {len(milestones)} milestones. Fetching issues for each...")

            for i, milestone in enumerate(milestones):
                logging.debug(f"Processing milestone {i+1}/{len(milestones)}: '{milestone.title}' (ID: {milestone.id})")
                # Fetch issues associated with the milestone - handles pagination internally
                issues = milestone.issues()
                logging.debug(f"  Found {len(issues)} issues for milestone '{milestone.title}'")
                milestone_data.append({
                    'id': milestone.id,
                    'iid': milestone.iid,
                    'title': milestone.title,
                    'description': milestone.description,
                    'state': milestone.state,
                    'due_date': milestone.due_date,
                    'start_date': milestone.start_date,
                    'web_url': milestone.web_url,
                    'issues': [{
                        'id': issue.iid,
                        'title': issue.title,
                        'state': issue.state,
                        'web_url': issue.web_url
                    } for issue in issues]
                })

            logging.info(f"Successfully fetched data for {len(milestone_data)} milestones.")
            return milestone_data
        except Exception as e:
            # Use logging.error for errors, exc_info=True includes traceback
            logging.error(f"Error fetching milestones: {e}", exc_info=True)
            return []
    
    def _create_iteration_data(self, iteration, iteration_issues) -> Dict:
        """Helper method to create iteration data dictionary
        
        Creates a standardized dictionary containing iteration data and associated issues.
        
        Args:
            iteration: GitLab iteration object
            iteration_issues: List of issues associated with the iteration
            
        Returns:
            Dictionary containing formatted iteration data with issues
        """
        return {
            'id': iteration.id,
            'iid': iteration.iid,
            'title': iteration.title,
            'description': iteration.description,
            'state': iteration.state,
            'start_date': iteration.start_date,
            'due_date': iteration.due_date,
            'web_url': iteration.web_url,
            'issues': [{
                'id': issue.iid,
                'title': issue.title,
                'state': issue.state,
                'web_url': issue.web_url
            } for issue in iteration_issues]
        }

    def _create_mock_iterations(self) -> List[Dict]:
        """Helper method to create mock iteration data for testing
        
        Creates a list of mock iterations with realistic data structure for testing purposes
        when GitLab Premium features are not available.
        
        Returns:
            List of dictionaries containing mock iteration data
        """
        # Create mock iterations with realistic data structure
        mock_data = []
        mock_data.append({
            'id': 1,
            'iid': 1,
            'title': 'Sprint 1',
            'description': 'First iteration',
            'state': 'closed',  # Using correct GitLab API state value
            'start_date': '2025-04-01',
            'due_date': '2025-04-14',
            'web_url': f"{self.gitlab.url}/{self.project.id}/-/iterations/1",
            'issues': []  # We'll populate this with real issues
        })
        
        mock_data.append({
            'id': 2,
            'iid': 2,
            'title': 'Sprint 2',
            'description': 'Second iteration',
            'state': 'opened',  # Changed from 'active' to 'opened' to match GitLab API
            'start_date': '2025-04-15',
            'due_date': '2025-04-28',
            'web_url': f"{self.gitlab.url}/{self.project.id}/-/iterations/2",
            'issues': []  # We'll populate this with real issues
        })
        return mock_data

    def _populate_mock_issues(self, iterations_data: List[Dict]) -> List[Dict]:
        """Helper method to populate mock iterations with real issues
        
        Takes mock iteration data and populates it with real project issues,
        distributing them evenly across iterations.
        
        Args:
            iterations_data: List of iteration dictionaries to populate with issues
            
        Returns:
            Updated list of iteration dictionaries with populated issues
        """
        # For each iteration, assign some real issues from the project
        # This simulates how issues would be associated with iterations
            # Otherwise fetch issues
        all_issues = self.project.issues.list(per_page=constants.PAGE_SIZE, iterator=True)
            
        # Distribute issues between iterations (for mock data)
        # Take just 100 issues instead of all
        all_issues_list = list(itertools.islice(all_issues, 4))
        for i, issue in enumerate(all_issues_list):
            iteration_index = i % len(iterations_data)
            iterations_data[iteration_index]['issues'].append({
                'id': issue.iid,
                'title': issue.title,
                'state': issue.state,
                'web_url': issue.web_url
            })
        return iterations_data

    def fetch_iterations(self, state: str = 'opened') -> List[Dict]:
        """
        Fetch iterations from the configured GitLab project.
        
        Note: This feature requires GitLab Premium or Ultimate.
        For free-tier GitLab, this will return an empty list with a warning log.

        Args:
            state: Filter by iteration state ('opened', 'closed', 'all')

        Returns:
            List of iteration dictionaries with their issues
        """
        logging.info(f"Fetching '{state}' iterations for project {self.project.id}...")
        iterations_data = []
        
        try:
            # Try to fetch iterations - this will only work with GitLab Premium/Ultimate
            try:
                # Use iterator=True for automatic pagination
                iterations = self.project.iterations.list(state=state, per_page=constants.PAGE_SIZE, iterator=True)
                
                for iteration in iterations:
                    # Fetch issues associated with this iteration
                    # In GitLab API, we need to query issues with iteration_id filter
                    iteration_issues = self.project.issues.list(
                        per_page=constants.PAGE_SIZE, 
                        iterator=True, 
                        iteration_id=iteration.id
                    )
                    
                    iteration_data = self._create_iteration_data(iteration, iteration_issues)
                    iterations_data.append(iteration_data)
                    
                logging.info(f"Successfully fetched data for {len(iterations_data)} iterations.")
                
            except gitlab.exceptions.GitlabListError as e:
                # This might be a free-tier GitLab that doesn't support iterations
                if e.response_code == 403:
                    logging.warning("Iterations API not available. This feature requires GitLab Premium or Ultimate.")
                    
                    # Fall back to mock data for testing purposes
                    if os.getenv('GITLAB_MOCK_ITERATIONS', 'false').lower() == 'true':
                        logging.info("Using mock iteration data for testing purposes.")
                        iterations_data = self._create_mock_iterations()
                        iterations_data = self._populate_mock_issues(iterations_data)
                        logging.info(f"Successfully created mock data for {len(iterations_data)} iterations.")
                else:
                    # Re-raise other GitLab list errors
                    raise
                
        except Exception as e:
            logging.error(f"Error fetching iterations: {e}", exc_info=True)
        
        return iterations_data
    
    def convert_date_format(self, start_date: str, end_date: str) -> str:
        formatted_start_date = "N/A"
        formatted_end_date = "N/A"

        if start_date:
            start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
            formatted_start_date = start_date_obj.strftime('%b %d, %Y')

        if end_date:
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
            formatted_end_date = end_date_obj.strftime('%b %d, %Y')

        return f"{formatted_start_date} - {formatted_end_date}"

    def fetch_issues(self, state: str = 'opened', labels: Optional[List[str]] = None) -> List[Dict]:
        """
        Fetch issues and their iteration change history from the configured GitLab project.
        """
        """
        Fetch issues from the configured GitLab project.

        Args:
            state: Filter by issue state ('opened', 'closed', or 'all')
            labels: List of labels to filter by

        Returns:
            List of issue dictionaries with relevant fields
        """
        # Note: The current implementation fetches *all* issues regardless of the 'state' and 'labels' args
        # due to `get_all=True` without passing filters to the list method.
        # Logging reflects the actual operation.
        logging.info(f"Fetching all issues for project {self.project.id}...")
        try:
            # Construct query parameters based on arguments if they were intended to be used
            # query_params = {'get_all': True}
            # Example of how filters *could* be applied if the logic required it:
            # if state:
            #     query_params['state'] = state
            # if labels:
            #     query_params['labels'] = labels
            # issues = self.project.issues.list(**query_params)
            
            # TODO: Remove test code
            # Current implementation fetches opened issues
            issues = self.project.issues.list(state=state, per_page=constants.PAGE_SIZE, iterator=True)

            # For testing purposes, just fetch the issue with id = 65
            # issues = [self.project.issues.get(65)]

            if not issues:
                logging.warning(f"No issues found for project {self.project.id}") # Use warning for empty results
                return []

            logging.info(f"Successfully fetched {len(issues)} issues. Processing issue data...")
            issue_data = []
            for issue in issues:
                try:
                    logging.debug(f"Processing issue ID: {issue.iid}, Title: {issue.title}")
                    notes_activities = fetch_gitlab_events.get_notes_activities(issue)
                    milestone_activities = fetch_gitlab_events.get_milestone_activities(issue)
                    label_activities = fetch_gitlab_events.get_label_activities(issue)
                    state_activities = fetch_gitlab_events.get_state_activities(issue)
                    iteration_activities = fetch_gitlab_events.get_iteration_activities(issue)

                    current_iteration = "N/A"
                    if getattr(issue, 'iteration', None):
                        current_iteration = self.convert_date_format(
                            issue.iteration.get('start_date'),
                            issue.iteration.get('due_date')
                        )

                    issue_data.append({
                        'id': issue.iid,
                        'title': issue.title,
                        'description': issue.description,
                        'state': issue.state,
                        'created_at': issue.created_at,
                        'updated_at': issue.updated_at,
                        'last_activity_at': getattr(issue, 'last_activity_at', issue.updated_at),
                        'labels': issue.labels,
                        'web_url': issue.web_url,
                        'assignees': [{'name': a.get('name', "N/A"), 
                                    'avatar_url': a.get('avatar_url', "N/A"),
                                    'web_url': a.get('web_url') or f"{self.gitlab.url}/users/{a.get('username', '')}"} 
                                    for a in getattr(issue, 'assignees', [])],
                        'current_iteration': current_iteration,
                        'due_date': getattr(issue, 'due_date', None),
                        'weight': getattr(issue, 'weight', None),
                        'time_estimate': getattr(issue, 'time_estimate', 0),
                        'user_notes_count': getattr(issue, 'user_notes_count', 0),
                        'resolved_at': None,  # Not directly available
                        'last_discussion_at': None,  # Would need discussions API endpoint
                        'notes_activities': notes_activities,
                        'milestone_activities': milestone_activities,
                        'label_activities': label_activities,
                        'state_activities': state_activities,
                        'iteration_activities': iteration_activities,
                    })
                
                except Exception as e:
                    logging.error(f"Error processing issue ID {issue.iid}: {e}", exc_info=True) # Log error with traceback
                
            logging.info(f"Finished processing {len(issue_data)} issues.")
            return issue_data
        except Exception as e:
            logging.error(f"Error fetching issues: {e}", exc_info=True) # Log error with traceback
            return []

def generate_issue_anomaly_map(issues: List[Dict], anomalies: List[Dict]) -> Dict[int, List[Dict]]:
    """Create a mapping of issue IDs to their anomalies."""
    issue_anomalies = {}
    for anomaly in anomalies:
        if anomaly['issue_id'] not in issue_anomalies:
            issue_anomalies[anomaly['issue_id']] = []
        issue_anomalies[anomaly['issue_id']].append(anomaly)
    return issue_anomalies

def add_issue_data_to_anomalies(issue_anomaly_map: Dict[int, List[Dict]], issues: List[Dict]) -> None:
    """Add assignees, state, and iteration to anomalies."""
    issue_map = {issue['id']: issue for issue in issues}
    for issue_id, anomalies in issue_anomaly_map.items():
        if issue_id in issue_map:
            issue = issue_map[issue_id]
            for anomaly in anomalies:
                anomaly['assignees'] = issue['assignees']
                anomaly['state'] = issue['state'] # Add the state property
                anomaly['current_iteration'] = issue['current_iteration']
                anomaly['iteration_activities'] = issue['iteration_activities']

def generate_milestone_data(milestones: List[Dict], issue_anomaly_map: Dict[int, List[Dict]]) -> List[Dict]:
    """Add anomaly data to milestones."""
    milestone_data = []
    for milestone in milestones:
        milestone_anomalies = []
        for issue in milestone['issues']:
            if issue['id'] in issue_anomaly_map:
                milestone_anomalies.extend(issue_anomaly_map[issue['id']])
        milestone_data.append({
            **milestone,
            'total_anomalies': len(milestone_anomalies),
            'anomalies': milestone_anomalies,
            'anomalies_by_severity': {
                'high': len([a for a in milestone_anomalies if a['severity'] == 'high']),
                'medium': len([a for a in milestone_anomalies if a['severity'] == 'medium']),
                'low': len([a for a in milestone_anomalies if a['severity'] == 'low'])
            }
        })
    return milestone_data

def generate_iteration_data(iterations: List[Dict], issue_anomaly_map: Dict[int, List[Dict]]) -> List[Dict]:
    """Add anomaly data to iterations."""
    iteration_data = []
    for iteration in iterations:
        iteration_anomalies = []
        for issue in iteration['issues']:
            if issue['id'] in issue_anomaly_map:
                iteration_anomalies.extend(issue_anomaly_map[issue['id']])
        iteration_data.append({
            **iteration,
            'total_anomalies': len(iteration_anomalies),
            'anomalies': iteration_anomalies,
            'anomalies_by_severity': {
                'high': len([a for a in iteration_anomalies if a['severity'] == 'high']),
                'medium': len([a for a in iteration_anomalies if a['severity'] == 'medium']),
                'low': len([a for a in iteration_anomalies if a['severity'] == 'low'])
            }
        })
    return iteration_data

def generate_report_data(issues: List[Dict], anomalies: List[Dict], milestones: List[Dict], iterations: List[Dict] = None) -> Dict:
    """Generate a report data structure for the web interface."""
    issue_anomaly_map = generate_issue_anomaly_map(issues, anomalies)
    add_issue_data_to_anomalies(issue_anomaly_map, issues)

    milestone_data = generate_milestone_data(milestones, issue_anomaly_map)
    iteration_data = generate_iteration_data(iterations, issue_anomaly_map)

    report = {
        "generated_at": datetime.now().isoformat(),
        "total_issues": len(issues),
        "total_anomalies": len(anomalies),
        "anomalies_by_severity": {
            "high": len([a for a in anomalies if a['severity'] == 'high']),
            "medium": len([a for a in anomalies if a['severity'] == 'medium']),
            "low": len([a for a in anomalies if a['severity'] == 'low'])
        },
        "anomalies_by_category": {
            "hygiene": len([a for a in anomalies if a.get('category') == 'hygiene']),
            "impediment": len([a for a in anomalies if a.get('category') == 'impediment'])
        },
        "anomalies": anomalies,
        "milestones": milestone_data,
        "iterations": iteration_data
    }
    
    logging.info(f"Report data generated successfully.")
    return report

def main():
    logging.info("Starting GitLab issue analysis script.")
    start_time = datetime.now()

    # Configuration
    GITLAB_URL = os.getenv('GITLAB_URL')
    PRIVATE_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN_AGILE')
    PROJECT_ID = os.getenv('GITLAB_PROJECT_ID')

    if not PRIVATE_TOKEN or not PROJECT_ID:
        # Use logging.critical for fatal errors leading to exit
        logging.critical("Error: Missing required environment variables GITLAB_ACCESS_TOKEN_AGILE and GITLAB_PROJECT_ID")
        sys.exit(1)

    try:
        # Initialize Fetcher
        fetcher = GitLabIssueFetcher(GITLAB_URL, PRIVATE_TOKEN, PROJECT_ID)

        # Fetch issues and milestones
        issues = fetcher.fetch_issues()
        # Check if fetching issues failed (returned empty list due to error)
        # Note: This check assumes an error returns [] and success with no issues also returns [].
        # A more robust check might involve inspecting logs or modifying fetcher to signal errors differently.
        # if not issues and some_error_flag_was_set_in_fetcher:
        #    logging.critical("Exiting due to failure fetching issues.")
        #    sys.exit(1)

        milestones = fetcher.fetch_milestones()
        # Similarly check for milestone fetching errors if needed

        # Analyze issues for anomalies
        logging.info("Initializing anomaly detector...")
        detector = IssueAnomalyDetector()
        logging.info("Starting issue anomaly analysis...")
        anomalies = detector.analyze_issues(issues)
        logging.info(f"Anomaly detection complete. Found {len(anomalies)} anomalies.")

        # Generate report data
        iterations = fetcher.fetch_iterations()
        report_data = generate_report_data(issues, anomalies, milestones, iterations)

        # Save report data
        output_dir = 'public'
        output_file = os.path.join(output_dir, 'data.json')
        logging.info(f"Ensuring output directory '{output_dir}' exists...")
        os.makedirs(output_dir, exist_ok=True)

        logging.info(f"Saving report data to {output_file}...")
        try:
            with open(output_file, 'w') as f:
                json.dump(report_data, f, indent=2)
            logging.info(f"Report data successfully saved to {output_file}")
        except IOError as e:
            logging.error(f"Failed to write report data to {output_file}: {e}", exc_info=True)
            sys.exit(1) # Exit if we cannot save the report

        end_time = datetime.now()
        # Use logging for final summary instead of print
        logging.info(f"Script finished. Found {len(issues)} issues and {len(anomalies)} anomalies.")
        logging.info(f"Total execution time: {(end_time - start_time).total_seconds():.2f} seconds.")

    except Exception as e:
        logging.critical(f"An unhandled error occurred during script execution: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
