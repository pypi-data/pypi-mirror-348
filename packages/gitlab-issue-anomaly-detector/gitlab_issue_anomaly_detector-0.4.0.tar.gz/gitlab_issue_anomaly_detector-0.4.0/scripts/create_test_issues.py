import os
import sys
from gitlab import Gitlab
from datetime import datetime, timedelta
from dotenv import load_dotenv
from scripts import constants

# Load environment variables from .env file
load_dotenv()

class GitLabIssueCreator:
    def __init__(self, gitlab_url: str, private_token: str, project_id: str):
        # Initialize GitLab API client with SSL verification disabled
        self.gitlab = Gitlab(gitlab_url, private_token=private_token, ssl_verify=False)
        self.project = self.gitlab.projects.get(project_id)
    
    # def delete_all_issues(self):
    #     """Delete all issues in the project."""
    #     print("\nDeleting all existing issues...")
    #     try:
    #         issues = self.project.issues.list(per_page=constants.PAGE_SIZE, iterator=True)
    #         for issue in issues:
    #             issue.delete()
    #             print(f"Deleted issue #{issue.iid}: {issue.title}")
    #         print(f"Successfully deleted {len(issues)} issues")
    #     except Exception as e:
    #         print(f"Error deleting issues: {e}")

    def issue_exists(self, title: str) -> bool:
        """Check if an issue with the given title already exists."""
        issues = self.project.issues.list(search=title)
        return any(issue.title == title for issue in issues)

    def get_total_issues(self) -> int:
        """Get total count of issues in the project."""
        return len(self.project.issues.list(per_page=constants.PAGE_SIZE, iterator=True))

    def create_issue(self, title: str, description: str, labels: list = None, created_at: str = None):
        try:
            if self.issue_exists(title):
                print(f"Skipping creation: Issue with title '{title}' already exists")
                return None

            data = {
                'title': title,
                'description': description,
                'labels': labels or []
            }
            if created_at:
                data['created_at'] = created_at
            
            issue = self.project.issues.create(data)
            print(f"Created issue: {issue.title} (#{issue.iid})")
            return issue
        except Exception as e:
            print(f"Error creating issue: {e}")
            return None

def create_test_issues():
    # Configuration
    GITLAB_URL = os.getenv('GITLAB_URL')
    PRIVATE_TOKEN = os.getenv('GITLAB_ACCESS_TOKEN_AGILE')
    PROJECT_ID = os.getenv('GITLAB_PROJECT_ID')
    
    if not PRIVATE_TOKEN or not PROJECT_ID:
        print("Error: Missing required environment variables GITLAB_ACCESS_TOKEN and GITLAB_PROJECT_ID")
        sys.exit(1)
    
    creator = GitLabIssueCreator(GITLAB_URL, PRIVATE_TOKEN, PROJECT_ID)
    
    # Delete all existing issues first
    # creator.delete_all_issues()
    
    created_count = 0
    print("\nCreating new test issues...")
    print("=" * 50)

    # 1. Well-formed issue (control case - no anomalies)
    creator.create_issue(
        title="Implement user authentication",
        description="""## Description
        Add OAuth2-based authentication system for user login.

        ## Acceptance Criteria
        - [ ] Implement OAuth2 flow
        - [ ] Add login/logout endpoints
        - [ ] Handle token refresh
        - [ ] Add user session management""",
        labels=["type::feature", "priority::medium", "status::open"]
    )
    created_count += 1

    # 2. Stale high-priority issue (long_open_high_priority)
    old_date = (datetime.now() - timedelta(days=10)).isoformat()
    creator.create_issue(
        title="Fix critical security vulnerability",
        description="""## Description
        Security patch needed for dependency vulnerability.

        ## Acceptance Criteria
        - [ ] Update vulnerable package
        - [ ] Run security scan
        - [ ] Deploy hotfix""",
        labels=["type::bug", "priority::high", "status::open", "security"],
        created_at=old_date
    )
    created_count += 1

    # 3. Blocked issue without blocker info and stale
    old_date = (datetime.now() - timedelta(days=35)).isoformat()
    creator.create_issue(
        title="Design UX",
        description="Need to implement new database schema for the messaging system.",
        labels=["type::task", "priority::medium", "status::blocked"],
        created_at=old_date
    )
    created_count += 1

    # 4. Issue with very long title
    creator.create_issue(
        title="[Backend][Database][API] Implement comprehensive distributed caching system with Redis cluster integration and fallback mechanism for handling cache misses and network partitions",
        description="""## Description
        Set up caching infrastructure.

        ## Acceptance Criteria
        - [ ] Set up Redis cluster
        - [ ] Implement cache logic""",
        labels=["type::feature", "priority::medium", "status::open"]
    )
    created_count += 1

    # 5. Issue with conflicting labels
    creator.create_issue(
        title="Review UI Components",
        description="Review and update component library",
        labels=["type::task", "priority::high", "priority::low", "status::open"]
    )
    created_count += 1

    # 6. Issue with multiple assignees
    creator.create_issue(
        title="Team planning session",
        description="Quarterly planning meeting with all team members",
        labels=["type::task", "priority::medium", "status::open", "team::all"]
    )
    created_count += 1

    # 7. Large checklist and multiple priorities in description
    checklist = "\n".join([f"- [ ] Task {i+1}" for i in range(20)])
    creator.create_issue(
        title="Complex feature implementation",
        description=f"""## Description
This high-priority task requires careful implementation.
Urgent: Need to complete this ASAP.
Critical for next release.
P1: Customer facing feature.

## Checklist
{checklist}""",
        labels=["type::feature", "priority::high", "status::open"]
    )
    created_count += 1

    # 8. Bug report missing version/environment info
    creator.create_issue(
        title="Fix login error",
        description="Users are unable to log in using SSO.",
        labels=["type::bug", "priority::high", "status::open"]
    )
    created_count += 1

    # 9. Inconsistent labels with title keywords
    creator.create_issue(
        title="Fix API endpoint security vulnerability",
        description="""## Description
Need to patch a security hole in the API authentication.

## Acceptance Criteria
- [ ] Audit authentication flow
- [ ] Implement fix
- [ ] Add tests""",
        labels=["type::task", "status::open"]  # Missing security and bug labels
    )
    created_count += 1

    # 10. Issue with large comment thread and cyclic state changes
    creator.create_issue(
        title="Cyclic bug investigation",
        description="""## Description
Bug keeps reappearing after fixes.

## Notes
Fixed in PR #123
Issue reappeared
Fixed again in PR #124
Issue reappeared again
Need thorough investigation""",
        labels=["type::bug", "status::open", "priority::high"]
    )
    created_count += 1

    # 11. Issue with unusual weight and many dependencies
    creator.create_issue(
        title="Overhaul database schema",
        description="""## Description
Major database restructuring needed.

Dependencies:
- Depends on: #1
- Blocked by: #2
- Related to: #3, #4, #5, #6
- After: #7, #8

## Acceptance Criteria
- [ ] Design new schema
- [ ] Plan migration
- [ ] Test data integrity""",
        labels=["type::task", "status::open", "priority::high"]
    )
    created_count += 1

    # 12. Issue with empty description
    creator.create_issue(
        title="Update documentation",
        description="",
        labels=["type::doc", "priority::low", "status::open"]
    )
    created_count += 1

    # 13. Issue with duplicate descriptions
    creator.create_issue(
        title="Refactor authentication module",
        description="""## Description
Need to improve code organization.

## Tasks
- Improve code organization
- Need to improve code organization
- Must improve code organization structure
- Organization of code needs improvement""",
        labels=["type::refactor", "priority::medium", "status::open"]
    )
    created_count += 1

    # 14. Issue with mixed priority indicators
    creator.create_issue(
        title="Low priority: Update npm packages",
        description="""## URGENT: Security Updates Required
        
Need to update all npm packages to latest versions.

Priority: HIGH
Impact: Critical""",
        labels=["type::maintenance", "priority::low", "status::open"]
    )
    created_count += 1

    # 15. Issue with excessive formatting
    creator.create_issue(
        title="Optimize database queries",
        description="""# Database Optimization
        
## **CRITICAL PERFORMANCE ISSUE**
### _Needs immediate attention_
#### `Query optimization required`
        
* **Bold item 1**
* *Italic item 2*
* ***Both bold and italic***
* ~~Strikethrough~~
* __Underline__
* **_Bold italic_**""",
        labels=["type::performance", "priority::medium", "status::open"]
    )
    created_count += 1

    # 16. Issue with unicode characters and emojis
    creator.create_issue(
        title="🐛 Fix internationalization issues 🌍",
        description="""## 国际化问题修复
        
🔍 Need to fix the following:
• UTF-8 encoding issues
• RTL layout problems
• £€¥ currency symbols
• مشكلة في العرض
• проблема с отображением""",
        labels=["type::bug", "priority::medium", "status::open", "i18n"]
    )
    created_count += 1

    # 17. Issue with HTML in markdown
    creator.create_issue(
        title="Clean up HTML injection",
        description="""## Description
<style>
body { color: red; }
</style>
<script>
alert('test');
</script>
<div class="custom">
    <h1>Important Task</h1>
    <p>Need to sanitize HTML inputs</p>
</div>""",
        labels=["type::security", "priority::high", "status::open"]
    )
    created_count += 1

    # 18. Issue with extremely short title
    creator.create_issue(
        title="Fix",
        description="The system is experiencing performance degradation under heavy load.",
        labels=["type::bug", "priority::high", "status::open"]
    )
    created_count += 1

    # 19. Issue with code blocks and syntax highlighting
    creator.create_issue(
        title="Debug memory leak in production",
        description="""## Code Analysis Required

```python
def memory_leak():
    large_list = []
    while True:
        large_list.append('*' * 1000000)
```

```javascript
function memoryLeak() {
    let arr = [];
    setInterval(() => {
        arr.push(new Array(1000000));
    }, 100);
}
```

```sql
SELECT * FROM large_table WHERE column IN (SELECT * FROM another_large_table);
```""",
        labels=["type::bug", "priority::critical", "status::open"]
    )
    created_count += 1

    # 20. Issue with nested lists and deep indentation
    creator.create_issue(
        title="Restructure project architecture",
        description="""## Current Structure
1. Frontend
   - React Components
     - UI Elements
       - Buttons
         - Primary
           - Large
           - Small
         - Secondary
           - Large
           - Small
     - Forms
       - Validation
         - Client-side
           - JavaScript
             - RegExp
             - Custom Rules
         - Server-side
           - API
             - Endpoints
               - POST
               - PUT
   - Redux Store
     - Actions
       - Types
         - Constants
2. Backend
   - API
     - Routes
       - Controllers
         - Services
           - Models
             - Schema
               - Validation""",
        labels=["type::task", "priority::medium", "status::planning"]
    )
    created_count += 1

    # 21. Issue with table formatting
    creator.create_issue(
        title="Performance metrics analysis",
        description="""## Performance Data

| Endpoint | Response Time | Error Rate | Load |
|----------|--------------|------------|------|
| /api/v1/users | 1200ms | 0.5% | High |
| /api/v1/products | 800ms | 1.2% | Medium |
| /api/v1/orders | 1500ms | 2.1% | Critical |
| /api/v1/auth | 300ms | 0.1% | Low |

| Time Period | Users | Sessions | Errors |
|-------------|-------|----------|---------|
| Morning | 5000 | 15000 | 75 |
| Afternoon | 7500 | 22500 | 125 |
| Evening | 10000 | 30000 | 250 |""",
        labels=["type::analysis", "priority::high", "status::open"]
    )
    created_count += 1

    # 22. Issue with mixed line endings
    creator.create_issue(
        title="Standardize line endings",
        description="This line ends with CRLF\r\nThis line ends with LF\nThis line ends with CR\rThis line ends with CRLF again\r\n",
        labels=["type::maintenance", "priority::low", "status::open"]
    )
    created_count += 1

    # 23. Issue with version numbers and environment specifications
    creator.create_issue(
        title="Version compatibility issues",
        description="""## Environment Matrix

Node.js versions:
- v14.17.0 ✓
- v16.13.0 ✗
- v18.0.0 ?
- v20.0.0 !

Browser Support:
- Chrome 89+ ✓
- Firefox 85+ ✗
- Safari 14+ ?
- Edge 90+ ✓

OS Compatibility:
- Windows 10 21H2 ✓
- Ubuntu 20.04 LTS ✗
- macOS Big Sur ✓
- Debian 11 ?""",
        labels=["type::compatibility", "priority::high", "status::investigating"]
    )
    created_count += 1

    # 24. Issue with URL and email patterns
    creator.create_issue(
        title="Fix malformed URLs in config",
        description="""## Invalid Patterns Found

URLs:
- https:/example.com (missing slash)
- http://internal-server (no TLD)
- https://api.service.com:8080:3000 (double port)
- http://[invalid-ip]:8080
- https://username:password@api.internal (exposed credentials)

Emails:
- user@domain (no TLD)
- @domain.com (no user)
- user@.com (no domain)
- user.@domain.com (trailing dot)
- .user@domain.com (leading dot)""",
        labels=["type::bug", "priority::medium", "status::open"]
    )
    created_count += 1

    # 25. Issue with binary data representation
    creator.create_issue(
        title="Debug binary file corruption",
        description="""## Binary Data Sample
[Binary data 0x89PNG...]
[Truncated binary content]
[Base64: /9j/4AAQSkZJRg...]
[Hex dump: 89 50 4E 47...]

## File Info
- Size: 1048576 bytes
- MD5: d41d8cd98f00b204e9800998ecf8427e
- SHA1: da39a3ee5e6b4b0d3255bfef95601890afd80709""",
        labels=["type::bug", "priority::urgent", "status::open"]
    )
    created_count += 1

    final_count = creator.get_total_issues()
    # ADDING CUSTOM TEST CASES FOR EACH ANOMALY CATEGORY
    print("\n" + "=" * 50)
    print("Creating specific test cases for anomaly categories...")
    print("=" * 50)

    # HYGIENE ANOMALIES
    print("\nCreating test cases for HYGIENE anomalies:")

    # Test for missing_labels
    creator.create_issue(
        title="Issue with missing essential labels",
        description="This issue has no priority label, which should trigger a hygiene anomaly.",
        labels=["type::task", "status::open"]
    )
    created_count += 1
    print("✓ Created test for missing_labels anomaly")

    # Test for poor_description
    creator.create_issue(
        title="Issue with poor quality description",
        description="Too short.",
        labels=["type::feature", "priority::medium", "status::open"]
    )
    created_count += 1
    print("✓ Created test for poor_description anomaly")

    # Test for missing_template_sections
    creator.create_issue(
        title="Bug missing required sections",
        description="This is a bug report that doesn't follow the template structure.",
        labels=["type::bug", "priority::high", "status::open"]
    )
    created_count += 1
    print("✓ Created test for missing_template_sections anomaly")

    # Test for missing_time_estimate
    creator.create_issue(
        title="Feature without time estimate",
        description="""## Description
        Add new dashboard functionality.
        
        ## Acceptance Criteria
        - Must have charts
        - Must have filters""",
        labels=["type::feature", "priority::medium", "status::open"]
    )
    created_count += 1
    print("✓ Created test for missing_time_estimate anomaly")

    # Test for missing_version_info
    creator.create_issue(
        title="Bug without version information",
        description="""## Description
        The login button doesn't work.
        
        ## Steps to Reproduce
        1. Go to login page
        2. Click login
        3. Nothing happens""",
        labels=["type::bug", "priority::medium", "status::open"]
    )
    created_count += 1
    print("✓ Created test for missing_version_info anomaly")

    # Test for missing_assignee
    creator.create_issue(
        title="Task without assignee",
        description="""## Description
        Update documentation for API endpoints.
        
        ## Tasks
        - Update endpoint descriptions
        - Add code examples
        - Update authentication section""",
        labels=["type::documentation", "priority::low", "status::open"]
    )
    created_count += 1
    print("✓ Created test for missing_assignee anomaly")

    # Test for missing_milestone
    creator.create_issue(
        title="Feature without milestone",
        description="""## Description
        Implement dark mode for the application.
        
        ## Acceptance Criteria
        - Add color scheme
        - Add toggle in settings
        - Save user preference""",
        labels=["type::feature", "priority::medium", "status::open"]
    )
    created_count += 1
    print("✓ Created test for missing_milestone anomaly")

    # Test for missing_iteration
    creator.create_issue(
        title="Task without iteration",
        description="""## Description
        Refactor authentication code.
        
        ## Tasks
        - Extract authentication logic
        - Add unit tests
        - Update documentation""",
        labels=["type::task", "priority::medium", "status::open"]
    )
    created_count += 1
    print("✓ Created test for missing_iteration anomaly")

    # Test for label_state_mismatch
    creator.create_issue(
        title="Issue with state-label mismatch",
        description="This issue is closed but has an 'in progress' label.",
        labels=["type::bug", "priority::medium", "status::in progress"]
    )
    # Close the issue to create the mismatch
    created_count += 1
    print("✓ Created test for label_state_mismatch anomaly")

    # IMPEDIMENT ANOMALIES
    print("\nCreating test cases for IMPEDIMENT anomalies:")

    # Test for stale_issue
    old_date = (datetime.now() - timedelta(days=35)).isoformat()
    creator.create_issue(
        title="Stale issue not updated in 35 days",
        description="""## Description
        This issue has not been updated for over 30 days.
        
        ## Acceptance Criteria
        - Criteria 1
        - Criteria 2""",
        labels=["type::task", "priority::medium", "status::open"],
        created_at=old_date
    )
    created_count += 1
    print("✓ Created test for stale_issue anomaly")

    # Test for blocked_without_details
    creator.create_issue(
        title="Blocked issue without explanation",
        description="""## Description
        This feature is currently blocked.
        
        ## Acceptance Criteria
        - Criteria 1
        - Criteria 2""",
        labels=["type::feature", "priority::high", "status::blocked"]
    )
    created_count += 1
    print("✓ Created test for blocked_without_details anomaly")

    # Test for long_open_high_priority
    old_date = (datetime.now() - timedelta(days=10)).isoformat()
    creator.create_issue(
        title="High priority issue open for too long",
        description="""## Description
        This high priority issue has been open for more than 7 days.
        
        ## Impact
        Critical functionality is affected.""",
        labels=["type::bug", "priority::high", "status::open"],
        created_at=old_date
    )
    created_count += 1
    print("✓ Created test for long_open_high_priority anomaly")

    # Test for potential_scope_creep
    creator.create_issue(
        title="Issue with potential scope creep",
        description="""## Description
        This issue keeps growing in scope.
        
        ## Original Scope
        - Feature A
        
        ## Added Later
        - Feature B
        - Feature C
        - Feature D
        - Feature E
        - Feature F""",
        labels=["type::feature", "priority::medium", "status::open"]
    )
    created_count += 1
    print("✓ Created test for potential_scope_creep anomaly")

    # Test for improper_lifecycle
    creator.create_issue(
        title="Closed issue without comments",
        description="""## Description
        This issue was closed without any explanation or comments.
        
        ## Acceptance Criteria
        - Something was supposed to be done""",
        labels=["type::bug", "priority::medium", "status::closed"]
    )
    created_count += 1
    print("✓ Created test for improper_lifecycle anomaly")

    # Test for inactive_high_priority
    last_activity_date = (datetime.now() - timedelta(days=5)).isoformat()
    creator.create_issue(
        title="Inactive high priority issue",
        description="""## Description
        This high priority issue has been inactive for more than 3 days.
        
        ## Impact
        User experience is severely degraded.""",
        labels=["type::bug", "priority::high", "status::open"],
        created_at=last_activity_date
    )
    created_count += 1
    print("✓ Created test for inactive_high_priority anomaly")

    print("\n" + "=" * 50)
    print(f"Creation Summary:")
    print(f"- Total issues created: {created_count}")
    print(f"- Total issues in project: {final_count}")
    print("=" * 50)

if __name__ == "__main__":
    create_test_issues()
