import sys
import os
import logging
import traceback
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('gitlab_anomaly_detector.log')
    ]
)
logger = logging.getLogger(__name__)

# Add project directory to path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from scripts.fetch_gitlab_issues import main as fetch_gitlab_issues_main
from scripts.prepare_pages import main as prepare_pages_main

def main(args: Optional[list] = None) -> int:
    """
    Main entry point for the GitLab anomaly detector package.
    
    Args:
        args: Command line arguments (optional)
        
    Returns:
        int: Exit code (0 for success, non-zero for failure)
    """
    try:
        logger.info("Starting GitLab anomaly detection process")
        
        # Fetch GitLab issues
        logger.info("Fetching GitLab issues")
        fetch_gitlab_issues_main()
        
        # Prepare pages
        logger.info("Preparing pages")
        prepare_pages_main()
        
        logger.info("GitLab anomaly detection process completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error in GitLab anomaly detection process: {str(e)}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))