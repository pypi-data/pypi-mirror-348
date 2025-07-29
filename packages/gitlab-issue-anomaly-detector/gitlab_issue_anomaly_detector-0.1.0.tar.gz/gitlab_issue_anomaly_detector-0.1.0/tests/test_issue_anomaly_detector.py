import unittest
from datetime import datetime, timezone
from typing import Dict
from unittest.mock import MagicMock
from scripts.issue_anomaly_detector import IssueAnomalyDetector

class TestIssueAnomalyDetector(unittest.TestCase):
    def setUp(self):
        self.detector = IssueAnomalyDetector()
        self.detector.logger = MagicMock()

    def test_check_assignee_changes_no_activities(self):
        """Test when issue has no assignee activities"""
        issue = {
            'id': 1,
            'title': 'Test Issue',
            'web_url': 'http://example.com/1',
            'assignee_activities': [],
            'assignees': []
        }
        result = self.detector.check_assignee_changes(issue)
        self.assertIsNone(result)

    def test_check_assignee_changes_below_threshold(self):
        """Test when assignee changes are below threshold"""
        issue = {
            'id': 1,
            'title': 'Test Issue',
            'web_url': 'http://example.com/1',
            'assignee_activities': [
                {'timestamp': '2025-05-01T10:00:00Z'},
                {'timestamp': '2025-05-02T10:00:00Z'}
            ],
            'assignees': [{'username': 'user1'}]
        }
        result = self.detector.check_assignee_changes(issue)
        self.assertIsNone(result)

    def test_check_assignee_changes_above_threshold(self):
        """Test when assignee changes exceed threshold"""
        issue = {
            'id': 1,
            'title': 'Test Issue',
            'web_url': 'http://example.com/1',
            'assignee_activities': [
                {'timestamp': '2025-05-01T10:00:00Z'},
                {'timestamp': '2025-05-02T10:00:00Z'},
                {'timestamp': '2025-05-03T10:00:00Z'},
                {'timestamp': '2025-05-04T10:00:00Z'}
            ],
            'assignees': [{'username': 'user1'}, {'username': 'user2'}]
        }
        result = self.detector.check_assignee_changes(issue)
        self.assertIsNotNone(result)
        self.assertEqual(result['type'], 'frequent_assignee_changes')
        self.assertEqual(result['issue_id'], 1)
        self.assertEqual(result['details']['assignee_change_count'], 4)
        self.assertEqual(result['details']['current_assignee_count'], 2)
        self.assertEqual(result['details']['current_assignees'], ['user1', 'user2'])
        self.assertEqual(result['details']['latest_change'], '2025-05-04T10:00:00Z')

    def test_check_assignee_changes_invalid_activities(self):
        """Test when assignee_activities has invalid type"""
        issue = {
            'id': 1,
            'title': 'Test Issue',
            'web_url': 'http://example.com/1',
            'assignee_activities': 'invalid',
            'assignees': []
        }
        result = self.detector.check_assignee_changes(issue)
        self.assertIsNone(result)
        self.detector.logger.warning.assert_called_once()

    def test_check_assignee_changes_custom_threshold(self):
        """Test with custom threshold value"""
        issue = {
            'id': 1,
            'title': 'Test Issue',
            'web_url': 'http://example.com/1',
            'assignee_activities': [
                {'timestamp': '2025-05-01T10:00:00Z'},
                {'timestamp': '2025-05-02T10:00:00Z'}
            ],
            'assignees': [{'username': 'user1'}]
        }
        result = self.detector.check_assignee_changes(issue, change_threshold=1)
        self.assertIsNotNone(result)
        self.assertEqual(result['details']['threshold'], 1)
        self.assertEqual(result['details']['assignee_change_count'], 2)

if __name__ == '__main__':
    unittest.main()
