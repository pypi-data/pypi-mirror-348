#!/usr/bin/env python3
"""
PyPI Publishing Script

This script handles the process of building and publishing the package to PyPI
with proper error handling and logging.
"""

import os
import sys
import logging
import subprocess
import argparse
import traceback
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('pypi_publish.log')
    ]
)
logger = logging.getLogger(__name__)

def run_command(command, cwd=None):
    """
    Run a shell command and log its output.
    
    Args:
        command (list): Command to run as a list of strings
        cwd (str, optional): Working directory
        
    Returns:
        bool: True if command succeeded, False otherwise
    """
    try:
        logger.info(f"Running command: {' '.join(command)}")
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            text=True,
            capture_output=True
        )
        logger.info(f"Command output: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed with exit code {e.returncode}")
        logger.error(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Exception running command: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def clean_previous_builds(project_dir):
    """
    Clean previous build artifacts.
    
    Args:
        project_dir (Path): Project directory
        
    Returns:
        bool: True if cleaning succeeded, False otherwise
    """
    try:
        logger.info("Cleaning previous build artifacts")
        dist_dir = project_dir / "dist"
        build_dir = project_dir / "build"
        egg_info_dir = project_dir.glob("*.egg-info")
        
        # Remove dist directory
        if dist_dir.exists():
            logger.info(f"Removing {dist_dir}")
            for file in dist_dir.glob("*"):
                file.unlink()
            dist_dir.rmdir()
            
        # Remove build directory
        if build_dir.exists():
            logger.info(f"Removing {build_dir}")
            import shutil
            shutil.rmtree(build_dir)
            
        # Remove egg-info directories
        for egg_dir in egg_info_dir:
            logger.info(f"Removing {egg_dir}")
            import shutil
            shutil.rmtree(egg_dir)
            
        return True
    except Exception as e:
        logger.error(f"Error cleaning build artifacts: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def build_package(project_dir):
    """
    Build the Python package.
    
    Args:
        project_dir (Path): Project directory
        
    Returns:
        bool: True if build succeeded, False otherwise
    """
    logger.info("Building package")
    return run_command(
        ["python3", "-m", "build"],
        cwd=str(project_dir)
    )

def upload_to_pypi(project_dir, repository="pypi"):
    """
    Upload the package to PyPI.
    
    Args:
        project_dir (Path): Project directory
        repository (str): Repository to upload to (pypi or testpypi)
        
    Returns:
        bool: True if upload succeeded, False otherwise
    """
    logger.info(f"Uploading package to {repository}")
    
    # Check if TWINE_USERNAME and TWINE_PASSWORD environment variables are set
    if "TWINE_USERNAME" not in os.environ or "TWINE_PASSWORD" not in os.environ:
        logger.warning("TWINE_USERNAME and/or TWINE_PASSWORD environment variables not set")
        logger.info("You will be prompted for credentials during upload")
    
    command = ["python3", "-m", "twine", "upload"]
    
    if repository == "testpypi":
        command.extend(["--repository", "testpypi"])
    
    command.append("dist/*")
    
    # Use subprocess.Popen for interactive prompt
    try:
        logger.info(f"Running command: {' '.join(command)}")
        process = subprocess.Popen(
            " ".join(command),
            cwd=str(project_dir),
            shell=True
        )
        process.communicate()
        
        if process.returncode == 0:
            logger.info("Package uploaded successfully")
            return True
        else:
            logger.error(f"Upload failed with exit code {process.returncode}")
            return False
    except Exception as e:
        logger.error(f"Exception during upload: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def main():
    """
    Main function to handle the PyPI publishing process.
    """
    parser = argparse.ArgumentParser(description="Publish package to PyPI")
    parser.add_argument(
        "--repository", 
        choices=["pypi", "testpypi"],
        default="pypi",
        help="Repository to upload to (default: pypi)"
    )
    parser.add_argument(
        "--skip-clean",
        action="store_true",
        help="Skip cleaning previous build artifacts"
    )
    args = parser.parse_args()
    
    try:
        logger.info("Starting PyPI publishing process")
        
        # Get project directory
        project_dir = Path(__file__).parent.parent.absolute()
        logger.info(f"Project directory: {project_dir}")
        
        # Clean previous builds
        if not args.skip_clean:
            if not clean_previous_builds(project_dir):
                logger.error("Failed to clean previous builds")
                return 1
        
        # Build package
        if not build_package(project_dir):
            logger.error("Failed to build package")
            return 1
        
        # Upload to PyPI
        if not upload_to_pypi(project_dir, args.repository):
            logger.error("Failed to upload package to PyPI")
            return 1
        
        logger.info("PyPI publishing process completed successfully")
        return 0
    except Exception as e:
        logger.error(f"Error in PyPI publishing process: {str(e)}")
        logger.error(traceback.format_exc())
        return 1

if __name__ == "__main__":
    sys.exit(main())
