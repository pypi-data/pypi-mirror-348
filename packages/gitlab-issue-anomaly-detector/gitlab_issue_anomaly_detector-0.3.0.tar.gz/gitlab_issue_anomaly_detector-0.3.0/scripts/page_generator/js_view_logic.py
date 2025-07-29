import logging

logger = logging.getLogger(__name__)

def _js_state_and_dom_elements():
    """Generates JS code for state variables and DOM element selection."""
    return """
    // --- State and DOM Elements ---
    window.reportData = null; // Holds the fetched data from data.json globally accessible
    window.activeMilestoneId = 'all'; // Tracks the currently selected milestone filter ('all' or an ID)
    window.activeIterationId = 'all'; // Tracks the currently selected iteration filter ('all' or an ID)

    // Cache frequently accessed DOM elements for performance and readability
    const dom = {
        viewButtons: document.querySelectorAll('.view-btn'), // All view switching buttons
        views: document.querySelectorAll('.view'), // All main view containers (issues, milestones)
        milestoneBtn: document.querySelector('.view-btn[data-view="milestones"]'), // The 'Milestones View' button
        dropdown: document.querySelector('.milestone-dropdown'), // The dropdown menu itself
        iterationBtn: document.querySelector('.view-btn[data-view="iterations"]'), // The 'Iterations View' button
        iterationDropdown: document.querySelector('.iteration-dropdown'), // The iteration dropdown menu
        issuesView: document.getElementById('issues-view'), // Container for the issues list view
        milestonesView: document.getElementById('milestones-view'), // Container for the milestones list view
        iterationsView: document.getElementById('iterations-view'), // Container for the iterations list view
        generationTimeEl: document.getElementById('generation-time'), // Span to display report generation time
        totalIssuesEl: document.getElementById('total-issues'), // Stat card element for total issues
        totalAnomaliesEl: document.getElementById('total-anomalies'), // Stat card element for total anomalies
        highSeverityLink: document.getElementById('high-severity-link'), // Link/Stat for high severity count
        mediumSeverityLink: document.getElementById('medium-severity-link'), // Link/Stat for medium severity count
        lowSeverityLink: document.getElementById('low-severity-link'), // Link/Stat for low severity count
        anomaliesListEl: document.getElementById('anomalies-list'), // Container for the list of anomalies in the backlog view
        totalMilestonesEl: document.getElementById('total-milestones'), // Stat card element for total active milestones
        totalMilestoneAnomaliesEl: document.getElementById('total-milestone-anomalies'), // Stat card for anomalies in active milestones
        milestonesListEl: document.getElementById('milestones-list'), // Container for the list of milestone cards
        totalIterationsEl: document.getElementById('total-iterations'), // Stat card element for total active iterations
        totalIterationAnomaliesEl: document.getElementById('total-iteration-anomalies'), // Stat card for anomalies in active iterations
        iterationsListEl: document.getElementById('iterations-list') // Container for the list of iteration cards
    };
    """

def _js_view_switching_logic():
    """Generates JS functions for view switching and dropdown toggling."""
    return """
    // --- View Switching Logic ---
    function switchView(viewName, filterId = 'all', preserveFilter = false) {
        // Switches the active view (issues or milestones) and updates button states.
        console.log(`Switching view to: ${viewName}, filter: ${filterId}, preserveFilter: ${preserveFilter}`);
        
        // Store current filter values before switching
        let currentFilter = 'all';
        if (viewName === 'milestones') {
            window.activeMilestoneId = filterId;
            const milestoneFilter = document.getElementById('milestone-anomaly-filter');
            if (preserveFilter && milestoneFilter) {
                currentFilter = milestoneFilter.value;
            }
        }
        if (viewName === 'iterations') {
            window.activeIterationId = filterId;
            const iterationFilter = document.getElementById('iteration-anomaly-filter');
            if (preserveFilter && iterationFilter) {
                currentFilter = iterationFilter.value;
            }
        }

        // Toggle the 'active' class on the main view containers
        dom.views.forEach(view => {
            view.classList.toggle('active', view.id === `${viewName}-view`);
        });

        // Toggle the 'active' class on the view switcher buttons
        dom.viewButtons.forEach(btn => {
            // For milestones and iterations buttons, we need to check if the view is active
            if (btn.dataset.view === 'milestones') {
                btn.classList.toggle('active', viewName === 'milestones');
            } else if (btn.dataset.view === 'iterations') {
                btn.classList.toggle('active', viewName === 'iterations');
            } else {
                btn.classList.toggle('active', btn.dataset.view === viewName);
            }
        });

        // Close both dropdowns when switching views
        closeAllDropdowns();
        
        // Only reset filters if we're not preserving the current filter
        if (!preserveFilter) {
            resetFilterDropdowns(viewName);
        }

        // If switching to the milestone view (or changing its filter), re-render its content
        if (viewName === 'milestones' && window.reportData) {
            renderMilestoneView(window.reportData);
            
            // If we need to preserve the filter, apply it immediately after rendering
            if (preserveFilter && currentFilter !== 'all') {
                const milestoneFilter = document.getElementById('milestone-anomaly-filter');
                if (milestoneFilter) {
                    milestoneFilter.value = currentFilter;
                    filterAnomaliesByCategory(currentFilter, 'milestone');
                }
            }
        }

        // If switching to the iteration view (or changing its filter), re-render its content
        if (viewName === 'iterations' && window.reportData) {
            renderIterationView(window.reportData);
            
            // If we need to preserve the filter, apply it immediately after rendering
            if (preserveFilter && currentFilter !== 'all') {
                const iterationFilter = document.getElementById('iteration-anomaly-filter');
                if (iterationFilter) {
                    iterationFilter.value = currentFilter;
                    filterAnomaliesByCategory(currentFilter, 'iteration');
                }
            }
        }
    }
    
    function resetFilterDropdowns(currentView) {
        // Reset only the filters not in the current view to avoid resetting user's active filter selection
        if (currentView !== 'issues') {
            const backlogFilter = document.getElementById('anomaly-category-filter');
            if (backlogFilter) backlogFilter.value = 'all';
        }
        
        if (currentView !== 'milestones') {
            const milestoneFilter = document.getElementById('milestone-anomaly-filter');
            if (milestoneFilter) milestoneFilter.value = 'all';
        }
        
        if (currentView !== 'iterations') {
            const iterationFilter = document.getElementById('iteration-anomaly-filter');
            if (iterationFilter) iterationFilter.value = 'all';
        }
        
        console.log(`Reset filter dropdowns except for ${currentView} view`);
    }

    function closeAllDropdowns() {
        // Helper function to close all dropdowns
        dom.dropdown.classList.remove('show');
        dom.iterationDropdown.classList.remove('show');
        dom.milestoneBtn.setAttribute('aria-expanded', 'false');
        dom.iterationBtn.setAttribute('aria-expanded', 'false');
    }

    function toggleDropdown(show, dropdownType) {
        // Shows or hides the milestone or iteration filter dropdown menu.
        console.log(`Toggling ${dropdownType} dropdown: ${show ? 'Show' : 'Hide'}`);
        
        // First, close all dropdowns
        closeAllDropdowns();
        
        // Then, if we're showing a dropdown, open the specific one
        if (show) {
            if (dropdownType === 'milestone') {
                dom.dropdown.classList.add('show');
                dom.milestoneBtn.setAttribute('aria-expanded', 'true');
            } else if (dropdownType === 'iteration') {
                dom.iterationDropdown.classList.add('show');
                dom.iterationBtn.setAttribute('aria-expanded', 'true');
            }
        }

        // Update the active state of the view buttons based on the current view
        updateViewButtonsActiveState();
    }
    
    function updateViewButtonsActiveState() {
        // Helper function to update the active state of view buttons based on which view is currently active
        const activeView = document.querySelector('.view-container.active');
        if (!activeView) return;
        
        const viewName = activeView.id.replace('-view', '');
        dom.viewButtons.forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === viewName);
        });
    }
    """

def _js_hash_change_handler():
    """Generates JS code for handling URL hash changes for navigation."""
    return """
    // --- Hash Change Handler ---
    function handleHashChange() {
        // Parses the URL hash and updates the view or scrolls to the relevant element.
        const hash = window.location.hash;
        console.log(`Hash changed to: ${hash}`);

        if (hash.startsWith('#milestone-')) {
            // If hash points to a milestone, switch view and filter
            const id = hash.substring(11); // Length of '#milestone-'
            console.log(`Hash change: Navigating to milestone ${id}`);
            switchView('milestones', id);
            // Maybe scroll to the milestone card itself?
            setTimeout(() => {
                const targetElement = document.getElementById(`milestone-${id}`);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);
        } else if (hash.startsWith('#iteration-')) {
            // If hash points to an iteration, switch view and filter
            const id = hash.substring(11); // Length of '#iteration-'
            console.log(`Hash change: Navigating to iteration ${id}`);
            switchView('iterations', id);
            // Maybe scroll to the iteration card itself?
            setTimeout(() => {
                const targetElement = document.getElementById(`iteration-${id}`);
                if (targetElement) {
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            }, 100);
        } else if (hash.startsWith('#anomaly-')) {
            // If hash points to an anomaly, ensure backlog view is active and scroll
            switchView('issues'); // Switch to backlog view if not already there
            const targetId = hash.substring(1); // Get ID without '#'
            console.log(`Hash change: Scrolling to anomaly ${targetId}`);

            // Use setTimeout to allow the browser time to potentially switch views
            // before attempting to scroll.
            setTimeout(() => {
                const targetElement = document.getElementById(targetId);
                if (targetElement) {
                    console.log(`Scrolling to anomaly: ${targetId}`);
                    targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                } else {
                    console.warn(`Anomaly element not found for hash: ${hash}`);
                }
            }, 100); // 100ms delay, adjust if needed
        } else {
            // If hash is empty or invalid, default to iterations view
            // on initial load or when hash is cleared
            if (!hash || hash === '#') {
                console.log("No valid hash, defaulting to iterations view.");
                switchView('iterations');
            } else {
                console.log("Hash changed to unrecognized value, no view change triggered.");
            }
        }
    }
    """

def _js_fetch_and_initialize():
    """Generates JS code for fetching data and initializing the report."""
    return """
    // --- Data Fetching and Initial Rendering ---
    function fetchDataAndRender() {
        console.log("Fetching data.json...");
        fetch('data.json') // Assumes data.json is in the same directory as index.html
            .then(response => {
                // Check if the fetch was successful
                if (!response.ok) {
                    // If not OK, try to read the response body for more details
                    return response.text().then(text => {
                        // Throw an error with status and potentially the response body
                        throw new Error(`HTTP error ${response.status}: ${text || response.statusText}`);
                    });
                }
                // If OK, parse the JSON response
                console.log("data.json fetched successfully, parsing JSON...");
                return response.json();
            })
            .then(data => {
                // Data fetched successfully
                console.log("Data loaded and parsed successfully:", data);
                window.reportData = data; // Store the data globally in window object

                // Update the report generation time display
                dom.generationTimeEl.textContent = formatDate(data.generated_at);

                // Perform the initial rendering of both views
                renderIssueView(data); // Render issues content
                renderMilestoneView(data); // Render milestones content (dropdown is populated here)
                renderIterationView(data); // Render iterations content (dropdown is populated here)

                // Setup event listeners now that the initial DOM is potentially modified
                setupEventListeners();

                // Handle any initial URL hash to set the correct view/scroll position
                handleHashChange();
            })
            .catch(error => {
                // Handle errors during fetch or JSON parsing
                console.error('Error loading or processing data.json:', error);
                // Display a user-friendly error message in the document body
                const errorMsg = `Failed to load report data (data.json). Please ensure the file exists in the same directory as this HTML file and is valid JSON. Error details: ${escapeHtml(error.message)}`;
                document.body.innerHTML = `<div style="padding: 2rem; border: 2px solid red; background-color: #ffebeb; color: #c00; margin: 1rem;"><h2>Error Loading Report</h2><p>${errorMsg}</p><p>Please check the browser console (F12) for more technical details.</p></div>`;
            });
    }

    // --- Initialization Trigger ---
    function initializeReport() {
        // Ensures the DOM is fully loaded before attempting to fetch data and manipulate elements.
        if (document.readyState === 'loading') {
            // If DOM is still loading, wait for the DOMContentLoaded event
            console.log("DOM not ready, waiting for DOMContentLoaded...");
            document.addEventListener('DOMContentLoaded', fetchDataAndRender);
        } else {
            // If DOM is already loaded (e.g., script is deferred or placed at end of body), run immediately
            console.log("DOM ready, fetching data...");
            fetchDataAndRender();
        }
    }
    """

def generate_view_logic():
    """Generates the complete view logic JavaScript."""
    logger.debug("Generating view logic JavaScript...")
    js_parts = [
        _js_state_and_dom_elements(),
        _js_view_switching_logic(),
        _js_hash_change_handler(),
        _js_fetch_and_initialize()
    ]
    js_content = "\n\n".join(js_parts)
    logger.debug("View logic JavaScript generated.")
    return js_content
