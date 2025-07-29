import logging

logger = logging.getLogger(__name__)

def _css_root_variables():
    """Generates CSS :root variables."""
    return """
    :root {
        --gl-primary: #6666c4;
        --gl-secondary: #2e2e2e;
        --gl-gray-100: #fafafa;
        --gl-gray-200: #dfdfdf;
        --gl-gray-300: #e3e3e3;
        --gl-text: #333;
        --gl-high: #dd2b0e;
        --gl-medium: #ef8e50;
        --gl-low: #1f75cb;
    }
    """

def _css_global_styles():
    """Generates global HTML, body, and wildcard styles."""
    return """
    html {
        scroll-behavior: smooth;
        scroll-padding-top: 4rem; /* Adjust based on navbar height */
    }
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    body {
        font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        line-height: 1.6;
        color: var(--gl-text);
        background-color: var(--gl-gray-100);
    }
    """

def _css_navbar():
    """Generates CSS for the navigation bar."""
    return """
    .navbar {
        background: #fff;
        border-bottom: 1px solid var(--gl-gray-200);
        padding: 0.5rem 2rem;
        display: flex;
        align-items: center;
        height: 48px;
        position: sticky;
        top: 0;
        z-index: 1000;
        gap: 1rem;
    }
    .navbar img {
        height: 30px;
        flex-shrink: 0;
    }
    .navbar-title {
        font-size: 1.125rem;
        font-weight: 600;
        color: var(--gl-secondary);
    }
    """

def _css_view_switcher_base():
    """Generates base CSS for the view switcher container and buttons."""
    return """
    .view-switcher {
        margin-left: auto;
        display: flex;
        gap: 0.5rem;
        position: relative; /* Needed for dropdown positioning */
        align-items: center;
    }
    .view-btn {
        padding: 0.5rem 1rem;
        border: 1px solid var(--gl-gray-200);
        background: white;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.875rem;
        color: var(--gl-text);
        position: relative;
        transition: background-color 0.3s ease, color 0.3s ease, border-color 0.3s ease;
        height: 36px;
        display: flex;
        align-items: center;
        white-space: nowrap;
    }
    .view-btn.active {
        background: var(--gl-primary);
        color: white;
        border-color: var(--gl-primary);
    }
    .view-btn[data-view="milestones"],
    .view-btn[data-view="iterations"] {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        padding-right: 2rem;
        position: relative;
    }
    .view-btn[data-view="milestones"]::after,
    .view-btn[data-view="iterations"]::after {
        content: "▼";
        font-size: 0.675rem;
        opacity: 0.75;
        transition: transform 0.2s ease;
        position: absolute;
        right: 0.75rem;
        top: 50%;
        transform: translateY(-50%);
    }
    .view-btn[data-view="milestones"].active::after,
    .view-btn[data-view="iterations"].active::after {
        transform: translateY(-50%) rotate(180deg);
    }
    """

def _css_milestone_dropdown():
    """Generates CSS specifically for the milestone dropdown menu."""
    return """
    .milestone-dropdown,
    .iteration-dropdown {
        display: none;
        position: absolute;
        top: calc(100% + 0.5rem); /* Position below the button */
        width: 280px;
        background: white;
        border: 1px solid var(--gl-gray-200);
        border-radius: 0.5rem;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        z-index: 1000;
        opacity: 0;
        transform: translateY(-12px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        max-height: 400px; /* Limit height */
        overflow-y: auto; /* Add scroll if needed */
    }
    
    /* Position each dropdown under its respective button */
    .iteration-dropdown {
        left: 0; /* Align with left edge of iterations button */
        right: auto;
    }
    
    .milestone-dropdown {
        left: 0; /* Align with left edge of milestones button */
        right: auto;
        margin-left: 140px; /* Approximate width of the Iterations button + gap */
    }
    
    .milestone-dropdown.show,
    .iteration-dropdown.show {
        display: block;
        opacity: 1;
        transform: translateY(0);
    }
    .milestone-dropdown-item,
    .iteration-dropdown-item {
        padding: 1rem 1.25rem;
        border-bottom: 1px solid var(--gl-gray-200);
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
        overflow: hidden;
        background: white;
        box-shadow: 0 1px 0 rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
    }
    .milestone-dropdown-item:last-child,
    .iteration-dropdown-item:last-child {
        border-bottom: none;
    }
    .milestone-dropdown-item:hover,
    .iteration-dropdown-item:hover {
        background: white; /* Keep background white on hover */
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    .milestone-dropdown-item:hover::before,
    .iteration-dropdown-item:hover::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 4px;
        background: var(--gl-primary);
    }
    .milestone-dropdown-title,
    .iteration-dropdown-title {
        font-weight: 600;
        color: var(--gl-secondary);
        margin-bottom: 0.375rem;
        font-size: 0.9375rem;
    }
    .milestone-dropdown-due,
    .iteration-dropdown-due {
        font-size: 0.8125rem;
        color: #666;
        display: flex;
        align-items: center;
        gap: 0.375rem;
    }
    .milestone-dropdown-due::before,
    .iteration-dropdown-due::before {
        content: "📅";
        font-size: 0.875rem;
        opacity: 0.75;
    }
    """

def _css_iteration_dropdown():
    """Generates CSS specifically for the iteration dropdown menu."""
    return """
    /* Additional iteration dropdown styles (most shared styles are in milestone dropdown) */
    .iteration-dropdown {
        /* Any iteration-specific styles can go here */
    }
    """

def _css_content_layout():
    """Generates CSS for the main content area and headings."""
    return """
    .view { display: none; }
    .view.active { display: block; }
    .content {
        max-width: 1280px;
        margin: 2rem auto;
        padding: 0 2rem;
    }
    h1 {
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--gl-secondary);
        margin-bottom: 1rem;
    }
    h2 {
        font-size: 1.5rem;
        font-weight: 600;
        color: var(--gl-secondary);
        margin: 2rem 0 1rem;
    }
    .generation-info {
        color: #666;
        font-size: 0.875rem;
        margin-bottom: 2rem;
    }
    """

def _css_stat_cards():
    """Generates CSS for the statistics cards."""
    return """
    .stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    .stat-card {
        background: white;
        border: none;
        border-radius: 0.5rem;
        padding: 1.25rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .stat-card h3 {
        font-size: 0.875rem;
        color: #666;
        margin-bottom: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .stat-card p {
        font-size: 2rem;
        font-weight: 600;
    }
    .stat-card a,
    .stat-card a:hover {
        text-decoration: none !important;
    }
    """

def _css_milestone_card_base():
    """Generates base CSS for the milestone card container and header."""
    return """
    .milestone-card {
        background: white;
        border: none;
        border-radius: 0.5rem;
        margin: 1rem 0 1.5rem;
        padding: 1.75rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .milestone-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.12);
    }
    .milestone-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        flex-wrap: wrap;
        gap: 0.5rem;
    }
    .milestone-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: var(--gl-secondary);
    }
    .milestone-dates {
        font-size: 0.875rem;
        color: #666;
        text-align: right;
        flex-shrink: 0;
    }
    """

def _css_milestone_card_stats():
    """Generates CSS for the stats grid within a milestone card."""
    return """
    .milestone-stats {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
        padding: 1.25rem;
        background: white;
        border: 1px solid var(--gl-gray-200);
        border-radius: 0.5rem;
    }
    .milestone-stat {
        display: flex;
        flex-direction: column;
    }
    .milestone-stat-label {
        font-size: 0.8125rem;
        color: #666;
        margin-bottom: 0.25rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .milestone-stat-value {
        font-size: 1.5rem;
        font-weight: 600;
    }
    """

def _css_milestone_card_anomalies_container():
    """Generates CSS for the anomalies section container within a milestone card."""
    return """
    .milestone-anomalies h4 {
        font-size: 1rem;
        font-weight: 600;
        color: var(--gl-secondary);
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--gl-gray-200);
    }
    """

def _css_anomaly_item_base():
    """Generates base CSS for the anomaly item container and link."""
    return """
    .anomaly-item {
        background: white;
        border: 1px solid var(--gl-gray-300);
        border-radius: 0.5rem;
        margin: 1rem 0;
        padding: 1.25rem;
        box-shadow: 0 1px 4px rgba(0,0,0,0.06);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-left: 4px solid var(--gl-gray-300);
    }
    .anomaly-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .anomaly-item.high { border-left-color: var(--gl-high); }
    .anomaly-item.medium { border-left-color: var(--gl-medium); }
    .anomaly-item.low { border-left-color: var(--gl-low); }
    .anomaly-item h3 {
        font-size: 1.125rem;
        margin-bottom: 0.75rem;
    }
    .issue-link, .assignee-link {
        color: var(--gl-primary);
        text-decoration: none;
        font-weight: 600;
    }
    .issue-link:hover, .assignee-link:hover {
        text-decoration: underline;
    }
    """

def _css_anomaly_item_details():
    """Generates CSS for the details/summary/pre elements within an anomaly item."""
    return """
    details {
        margin-top: 1rem;
        background-color: #f9f9f9;
        border: 1px solid var(--gl-gray-200);
        border-radius: 0.25rem;
        padding: 0.75rem;
    }
    summary {
        cursor: pointer;
        color: var(--gl-primary);
        font-weight: 600;
        list-style-position: inside;
    }
    summary:hover {
        text-decoration: underline;
    }
    pre {
        background: var(--gl-gray-100);
        padding: 1rem;
        border-radius: 0.25rem;
        margin-top: 0.75rem;
        overflow-x: auto;
        font-size: 0.875rem;
        border: 1px solid var(--gl-gray-200);
        white-space: pre-wrap; /* Allow wrapping */
        word-wrap: break-word; /* Break long words */
    }
    """

def _css_severity_helpers():
    """Generates CSS helper classes for severity colors."""
    return """
    .severity-high { 
        color: var(--gl-high);
        text-decoration: none;
    }
    .severity-medium { 
        color: var(--gl-medium);
        text-decoration: none;
    }
    .severity-low { 
        color: var(--gl-low);
        text-decoration: none;
    }
    """

def _css_anomaly_filter():
    """Generates CSS for the anomaly category filter dropdown."""
    logger.debug("Generating CSS: Anomaly Filter")
    return """
    .anomaly-filter-container {
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
    }
    
    .anomaly-filter-container.top-filter {
        background-color: #f8f8f8;
        padding: 0.75rem 1rem;
        border-radius: 0.25rem;
        border: 1px solid var(--gl-gray-200);
        margin-bottom: 1rem;
        position: sticky;
        top: 48px; /* Same as navbar height */
        z-index: 100;
        justify-content: space-between;
    }
    
    .anomaly-filter-container label {
        margin-right: 0.5rem;
        font-weight: 600;
        color: var(--gl-secondary);
        white-space: nowrap;
    }
    
    .anomaly-filter-btn {
        padding: 0.5rem 1rem;
        border: 1px solid var(--gl-gray-200);
        background: white;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.875rem;
        color: var(--gl-text);
        transition: all 0.2s ease;
    }
    
    .anomaly-filter-btn:hover,
    .anomaly-filter-btn:focus {
        border-color: var(--gl-primary);
        outline: none;
    }
    
    /* Export button styles */
    .export-btn {
        padding: 0.5rem 1rem;
        background-color: var(--gl-primary);
        color: white;
        border: none;
        border-radius: 0.25rem;
        cursor: pointer;
        font-size: 0.875rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        transition: background-color 0.2s ease;
        margin-left: auto; /* Push to the right */
    }
    
    .export-btn:hover {
        background-color: #5555b0;
    }
    
    .export-btn:before {
        content: '📊';
        margin-right: 0.5rem;
    }
    
    /* Category badges */
    .category-badge {
        display: inline-block;
        padding: 0.125rem 0.5rem;
        border-radius: 1rem;
        font-size: 0.75rem;
        margin-left: 0.5rem;
        text-transform: capitalize;
    }
    
    .category-badge.impediment {
        background-color: #ffcdd2;
        color: #c62828;
    }
    
    .category-badge.hygiene {
        background-color: #bbdefb;
        color: #1565c0;
    }
    """

def generate_css():
    """Generates the complete CSS string by combining granular helper functions."""
    logger.debug("Generating CSS content...")
    css_parts = [
        _css_root_variables(),
        _css_global_styles(),
        _css_navbar(),
        _css_view_switcher_base(),
        _css_milestone_dropdown(),
        _css_iteration_dropdown(),
        _css_content_layout(),
        _css_stat_cards(),
        _css_milestone_card_base(),
        _css_milestone_card_stats(),
        _css_milestone_card_anomalies_container(),
        _css_anomaly_item_base(),
        _css_anomaly_item_details(),
        _css_severity_helpers(),
        _css_anomaly_filter()
    ]
    css_content = "\n".join(css_parts)
    logger.debug("CSS content generated.")
    return css_content
