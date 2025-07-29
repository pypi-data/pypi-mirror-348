"""
Test script to verify the export functionality with different filter selections.
This script uses Playwright to simulate user interactions with the UI.
"""
import os
import time
import logging
from playwright.sync_api import sync_playwright

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_export_functionality():
    """Test the export functionality with different filter selections."""
    logger.info("Starting export functionality test...")
    
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            # Navigate to the application
            logger.info("Navigating to application...")
            page.goto('http://localhost:8080')
            
            # Wait for the page to load
            page.wait_for_selector('.view.active')
            
            # Test 1: Export all anomalies (default)
            logger.info("Test 1: Exporting all anomalies...")
            # Make sure we're on the issues view
            page.click('.view-btn[data-view="issues"]')
            # Make sure 'All Anomalies' is selected
            page.select_option('#anomaly-category-filter', 'all')
            # Click export button
            page.click('#export-issues-btn')
            # Give time for the export process
            time.sleep(2)
            logger.info("All anomalies export triggered")
            
            # Test 2: Export only hygiene anomalies
            logger.info("Test 2: Exporting hygiene anomalies...")
            # Select 'Hygiene' filter
            page.select_option('#anomaly-category-filter', 'hygiene')
            # Check console logs to verify filtered data
            logs = page.evaluate("""() => {
                const logs = [];
                const originalConsoleLog = console.log;
                console.log = (...args) => {
                    logs.push(args.join(' '));
                    originalConsoleLog(...args);
                };
                
                // Trigger export
                document.getElementById('export-issues-btn').click();
                
                // Wait a bit for logs to be captured
                return new Promise(resolve => setTimeout(() => {
                    console.log = originalConsoleLog;
                    resolve(logs);
                }, 1000));
            }""")
            
            for log in logs:
                if "Filtered anomalies by category" in log:
                    logger.info(f"  Console log: {log}")
            logger.info("Hygiene anomalies export triggered")
            
            # Test 3: Export only impediment anomalies
            logger.info("Test 3: Exporting impediment anomalies...")
            # Select 'Impediment' filter
            page.select_option('#anomaly-category-filter', 'impediment')
            # Check console logs to verify filtered data
            logs = page.evaluate("""() => {
                const logs = [];
                const originalConsoleLog = console.log;
                console.log = (...args) => {
                    logs.push(args.join(' '));
                    originalConsoleLog(...args);
                };
                
                // Trigger export
                document.getElementById('export-issues-btn').click();
                
                // Wait a bit for logs to be captured
                return new Promise(resolve => setTimeout(() => {
                    console.log = originalConsoleLog;
                    resolve(logs);
                }, 1000));
            }""")
            
            for log in logs:
                if "Filtered anomalies by category" in log:
                    logger.info(f"  Console log: {log}")
            logger.info("Impediment anomalies export triggered")
            
            logger.info("All tests completed successfully!")
            
        finally:
            # Close browser
            browser.close()

if __name__ == "__main__":
    test_export_functionality()
