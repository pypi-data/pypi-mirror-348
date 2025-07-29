import logging

logger = logging.getLogger(__name__)

def _js_add_view_button_listeners():
    """Generates JS code to add listeners to view switcher buttons."""
    return """
    // --- Event Listener Setup: View Buttons ---
    function addViewButtonListeners() {
        // Adds click listeners to the 'backlog view' and 'Milestones View' buttons.
        dom.viewButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const viewName = button.dataset.view;
                console.log(`View button clicked: ${viewName}`);
                if (viewName === 'issues') {
                    // Switch to backlog view directly
                    switchView('issues');
                } else if (viewName === 'milestones') {
                    // For the milestone button, toggle its dropdown instead of directly switching view
                    e.stopPropagation(); // Prevent the document click listener from closing it immediately
                    const isShowing = dom.dropdown.classList.contains('show');
                    toggleDropdown(!isShowing, 'milestone');
                    // View switch happens when a dropdown item is clicked
                } else if (viewName === 'iterations') {
                    // For the iteration button, toggle its dropdown instead of directly switching view
                    e.stopPropagation(); // Prevent the document click listener from closing it immediately
                    const isShowing = dom.iterationDropdown.classList.contains('show');
                    toggleDropdown(!isShowing, 'iteration');
                    // View switch happens when a dropdown item is clicked
                }
            });
        });
    }
    """

def _js_add_document_listeners():
    """Generates JS code for document-level listeners (e.g., closing dropdown)."""
    return """
    // --- Event Listener Setup: Document ---
    function addDocumentListeners() {
        // Adds a listener to the whole document to close the milestone dropdown
        // if a click occurs outside the dropdown and its toggle button.
        document.addEventListener('click', (e) => {
            // Check if the click target is outside the milestone button AND outside the dropdown itself
            if (!dom.milestoneBtn.contains(e.target) && !dom.dropdown.contains(e.target)) {
                // If the dropdown is currently shown, hide it
                if (dom.dropdown.classList.contains('show')) {
                    console.log("Clicked outside dropdown, closing it.");
                    toggleDropdown(false, 'milestone');
                }
            }

            // Check if the click target is outside the iteration button AND outside the dropdown itself
            if (!dom.iterationBtn.contains(e.target) && !dom.iterationDropdown.contains(e.target)) {
                // If the dropdown is currently shown, hide it
                if (dom.iterationDropdown.classList.contains('show')) {
                    console.log("Clicked outside dropdown, closing it.");
                    toggleDropdown(false, 'iteration');
                }
            }
        });
    }
    """

def _js_add_dropdown_listener():
    """Generates JS code for handling clicks within the milestone dropdown."""
    return """
    // --- Event Listener Setup: Dropdown ---
    function addDropdownListener() {
        // Uses event delegation on the dropdown container to handle clicks on its items.
        dom.dropdown.addEventListener('click', (e) => {
            // Find the clicked dropdown item, if any
            const item = e.target.closest('.milestone-dropdown-item');
            if (item) {
                e.preventDefault(); // Prevent potential default link behavior
                e.stopPropagation(); // Prevent document click listener
                
                // Capture current filter selection before switching views
                const milestoneFilter = document.getElementById('milestone-anomaly-filter');
                const selectedCategory = milestoneFilter ? milestoneFilter.value : 'all';
                
                // Get the milestone ID (or 'all') from the clicked item's data attribute
                const milestoneId = item.dataset.milestone;
                console.log(`Dropdown item clicked: ${milestoneId} with filter: ${selectedCategory}`);
                
                // Switch to the milestone view with the selected filter, preserving the current filter
                // This will prevent the flicker effect when switching views
                const shouldPreserveFilter = selectedCategory !== 'all';
                switchView('milestones', milestoneId, shouldPreserveFilter);
                
                // Close the dropdown after selection
                toggleDropdown(false, 'milestone');
            }
        });


        dom.iterationDropdown.addEventListener('click', (e) => {
            // Find the clicked dropdown item, if any
            const item = e.target.closest('.iteration-dropdown-item');
            if (item) {
                e.preventDefault(); // Prevent potential default link behavior
                e.stopPropagation(); // Prevent document click listener
                
                // Capture current filter selection before switching views
                const iterationFilter = document.getElementById('iteration-anomaly-filter');
                const selectedCategory = iterationFilter ? iterationFilter.value : 'all';
                
                // Get the iteration ID (or 'all') from the clicked item's data attribute
                const iterationId = item.dataset.iteration;
                console.log(`Dropdown item clicked: ${iterationId} with filter: ${selectedCategory}`);
                
                // Switch to the iteration view with the selected filter, preserving the current filter
                // This will prevent the flicker effect when switching views
                const shouldPreserveFilter = selectedCategory !== 'all';
                switchView('iterations', iterationId, shouldPreserveFilter);
                
                // Close the dropdown after selection
                toggleDropdown(false, 'iteration');
            }
        });
    }
    """

def _js_add_hashchange_listener():
    """Generates JS code for handling URL hash changes for navigation."""
    return """
    // --- Event Listener Setup: Hash Change ---
    function addHashChangeListener() {
        // Listens for changes in the URL hash (e.g., back/forward buttons, manual changes)
        // and triggers the handler to update the view or scroll accordingly.
        window.addEventListener('hashchange', handleHashChange);
        console.log("Hash change listener added.");
    }
    """

def _js_severity_link_setup():
    """Generates JS code for setting up severity link behavior."""
    return """
    // --- Event Listener Setup: Severity Links ---
    function setupSeverityLink(linkElement, count, anomalies, severity) {
        // Configures a severity count element (e.g., in stat cards) to act as a link
        // that scrolls to the first anomaly of that severity in the backlog view.
        linkElement.textContent = count ?? '0'; // Display the count

        // Find the first anomaly matching the severity
        const firstAnomalyOfSeverity = anomalies.find(a => a.severity === severity);

        // Replace the link element with a clone to remove any previous listeners
        const newLink = linkElement.cloneNode(true);
        linkElement.parentNode.replaceChild(newLink, linkElement);

        if (firstAnomalyOfSeverity && count > 0) {
            // If found and count > 0, make it a clickable link
            newLink.href = `#anomaly-${firstAnomalyOfSeverity.issue_id}`;
            newLink.style.cursor = 'pointer';
            newLink.addEventListener('click', (e) => {
                e.preventDefault(); // Prevent default hash jump
                // Ensure the backlog view is active before trying to scroll
                if (!dom.issuesView.classList.contains('active')) {
                    switchView('issues');
                }
                // Use requestAnimationFrame to ensure scrolling happens after any potential view switch repaint
                requestAnimationFrame(() => {
                    const targetElement = document.getElementById(`anomaly-${firstAnomalyOfSeverity.issue_id}`);
                    if (targetElement) {
                        // Scroll the target anomaly into view smoothly
                        targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                });
            });
        } else {
            // If no matching anomaly or count is 0, make it non-interactive
            newLink.href = '#';
            newLink.style.cursor = 'default';
            newLink.addEventListener('click', (e) => e.preventDefault()); // Prevent hash change
        }
    }
    """

def _js_anomaly_filter():
    """Generates JS code for anomaly filtering functionality."""
    return """
    // --- Anomaly Category Filtering ---
    function filterAnomaliesByCategory(category, context = 'backlog') {
        console.log(`Filtering anomalies by category: ${category} in context: ${context}`);
        let anomalyItems;
        let visibleCount = 0;
        let severityCounts = { high: 0, medium: 0, low: 0 };
        
        if (context === 'backlog') {
            anomalyItems = document.querySelectorAll('#anomalies-list .anomaly-item');
        } else if (context === 'milestone') {
            anomalyItems = document.querySelectorAll('#milestones-list .milestone-card .anomaly-item');
        } else if (context === 'iteration') {
            anomalyItems = document.querySelectorAll('#iterations-list .iteration-card .anomaly-item');
        }
        
        if (!anomalyItems || anomalyItems.length === 0) {
            console.log(`No anomaly items found in context: ${context}`);
            return 0;
        }
        
        anomalyItems.forEach(item => {
            const itemCategory = item.getAttribute('data-category');
            const itemSeverity = item.classList.contains('high') ? 'high' : 
                               item.classList.contains('medium') ? 'medium' : 'low';
            
            if (category === 'all' || itemCategory === category) {
                item.style.display = '';
                visibleCount++;
                severityCounts[itemSeverity]++;
            } else {
                item.style.display = 'none';
            }
        });
        
        if (context === 'backlog') {
            dom.totalAnomaliesEl.textContent = visibleCount;
        } else if (context === 'milestone') {
            dom.totalMilestoneAnomaliesEl.textContent = visibleCount;
            
            const milestoneCards = document.querySelectorAll('#milestones-list .milestone-card');
            milestoneCards.forEach(card => {
                const cardId = card.id.replace('milestone-', '');
                const cardAnomalies = card.querySelectorAll('.anomaly-item');
                const visibleCardAnomalies = Array.from(cardAnomalies).filter(item => 
                    item.style.display !== 'none'
                );
                
                const cardSeverityCounts = { high: 0, medium: 0, low: 0 };
                visibleCardAnomalies.forEach(item => {
                    if (item.classList.contains('high')) cardSeverityCounts.high++;
                    else if (item.classList.contains('medium')) cardSeverityCounts.medium++;
                    else if (item.classList.contains('low')) cardSeverityCounts.low++;
                });
                
                const anomalyCountEl = card.querySelector('.milestone-stat:nth-child(2) .milestone-stat-value');
                if (anomalyCountEl) {
                    anomalyCountEl.textContent = visibleCardAnomalies.length;
                }
                
                ['high', 'medium', 'low'].forEach(severity => {
                    const severityLink = document.getElementById(`milestone-${cardId}-${severity}`);
                    if (severityLink) {
                        severityLink.textContent = cardSeverityCounts[severity];
                    }
                });
            });
        } else if (context === 'iteration') {
            dom.totalIterationAnomaliesEl.textContent = visibleCount;
            
            const iterationCards = document.querySelectorAll('#iterations-list .iteration-card');
            iterationCards.forEach(card => {
                const cardId = card.id.replace('iteration-', '');
                const cardAnomalies = card.querySelectorAll('.anomaly-item');
                const visibleCardAnomalies = Array.from(cardAnomalies).filter(item => 
                    item.style.display !== 'none'
                );
                
                const cardSeverityCounts = { high: 0, medium: 0, low: 0 };
                visibleCardAnomalies.forEach(item => {
                    if (item.classList.contains('high')) cardSeverityCounts.high++;
                    else if (item.classList.contains('medium')) cardSeverityCounts.medium++;
                    else if (item.classList.contains('low')) cardSeverityCounts.low++;
                });
                
                const anomalyCountEl = card.querySelector('.milestone-stat:nth-child(2) .milestone-stat-value');
                if (anomalyCountEl) {
                    anomalyCountEl.textContent = visibleCardAnomalies.length;
                }
                
                ['high', 'medium', 'low'].forEach(severity => {
                    const severityLink = document.getElementById(`iteration-${cardId}-${severity}`);
                    if (severityLink) {
                        severityLink.textContent = cardSeverityCounts[severity];
                    }
                });
            });
        }
        
        const highSeverityLink = document.getElementById('high-severity-link');
        const mediumSeverityLink = document.getElementById('medium-severity-link');
        const lowSeverityLink = document.getElementById('low-severity-link');
        
        if (highSeverityLink) highSeverityLink.textContent = severityCounts.high;
        if (mediumSeverityLink) mediumSeverityLink.textContent = severityCounts.medium;
        if (lowSeverityLink) lowSeverityLink.textContent = severityCounts.low;
        
        console.log(`${visibleCount} anomalies displayed after filtering in context: ${context}`);
        console.log(`Updated severity counts: High=${severityCounts.high}, Medium=${severityCounts.medium}, Low=${severityCounts.low}`);
        return visibleCount;
    }
    """

def _js_setup_anomaly_filter():
    """Generates JS code for setting up anomaly filter event listeners."""
    return """
    // --- Anomaly Filter Setup ---
    function setupAnomalyFilter() {
        console.log("Setting up anomaly category filters...");
        
        // Setup backlog filter
        const backlogFilter = document.getElementById('anomaly-category-filter');
        if (backlogFilter) {
            backlogFilter.addEventListener('change', () => {
                const selectedCategory = backlogFilter.value;
                filterAnomaliesByCategory(selectedCategory, 'backlog');
            });
            console.log("Backlog anomaly filter setup complete.");
        } else {
            console.error("Backlog anomaly filter element not found!");
        }
        
        // Setup milestone filter
        const milestoneFilter = document.getElementById('milestone-anomaly-filter');
        if (milestoneFilter) {
            milestoneFilter.addEventListener('change', () => {
                const selectedCategory = milestoneFilter.value;
                filterAnomaliesByCategory(selectedCategory, 'milestone');
            });
            console.log("Milestone anomaly filter setup complete.");
        } else {
            console.error("Milestone anomaly filter element not found!");
        }
        
        // Setup iteration filter
        const iterationFilter = document.getElementById('iteration-anomaly-filter');
        if (iterationFilter) {
            iterationFilter.addEventListener('change', () => {
                const selectedCategory = iterationFilter.value;
                filterAnomaliesByCategory(selectedCategory, 'iteration');
            });
            console.log("Iteration anomaly filter setup complete.");
        } else {
            console.error("Iteration anomaly filter element not found!");
        }
    }

    function applyDefaultFiltering() {
        console.log("Applying default filtering (All anomalies) to all views...");
        
        // Apply default filtering to backlog view
        const backlogFilter = document.getElementById('anomaly-category-filter');
        if (backlogFilter) {
            backlogFilter.value = 'all';
            filterAnomaliesByCategory('all', 'backlog');
        }
        
        // Apply default filtering to milestone view
        const milestoneFilter = document.getElementById('milestone-anomaly-filter');
        if (milestoneFilter) {
            milestoneFilter.value = 'all';
            filterAnomaliesByCategory('all', 'milestone');
        }
        
        // Apply default filtering to iteration view
        const iterationFilter = document.getElementById('iteration-anomaly-filter');
        if (iterationFilter) {
            iterationFilter.value = 'all';
            filterAnomaliesByCategory('all', 'iteration');
        }
    }
    """

def _js_export_anomalies():
    """Generates JavaScript functions for exporting anomalies to Excel."""
    return """
    // --- Excel Export Functionality ---
    function exportAnomaliestoExcel(anomalies, filename = 'anomalies-export.xlsx') {
        console.log(`Exporting ${anomalies.length} anomalies to Excel...`);
        
        if (!anomalies || anomalies.length === 0) {
            alert('No anomalies to export.');
            return;
        }
        
        // Create a new workbook and worksheet
        const wb = XLSX.utils.book_new();
        
        // Transform anomalies to a format suitable for Excel
        const excelData = anomalies.map(anomaly => ({
            'Issue ID': anomaly.issue_id,
            'Title': anomaly.title,
            'Type': anomaly.type,
            'Category': anomaly.category || 'hygiene',
            'Severity': anomaly.severity,
            'Description': anomaly.description,
            'Status': anomaly.state,
            'Assignees': anomaly.assignees && anomaly.assignees.length > 0 ? 
                anomaly.assignees.map(a => a.name).join(', ') : 'Unassigned',
            'Current Iteration': anomaly.current_iteration || 'N/A',
            'Total Iterations': anomaly.total_iterations || 0,
            'URL': anomaly.web_url
        }));
        
        // Create worksheet from the data
        const ws = XLSX.utils.json_to_sheet(excelData);
        
        // Add worksheet to workbook
        XLSX.utils.book_append_sheet(wb, ws, 'Anomalies');
        
        // Generate Excel file and trigger download
        XLSX.writeFile(wb, filename);
        console.log(`Excel export complete: ${filename}`);
    }
    
    function getVisibleAnomalies(context = 'backlog') {
        console.log(`Getting visible anomalies for context: ${context}`);
        
        // First check if reportData exists and has anomalies
        if (!window.reportData || !window.reportData.anomalies || !window.reportData.anomalies.length) {
            console.log('No anomalies data found in reportData');
            return [];
        }
        
        // Get the currently selected category filter value
        let categoryFilter;
        if (context === 'backlog') {
            categoryFilter = document.getElementById('anomaly-category-filter')?.value || 'all';
        } else if (context === 'milestone') {
            categoryFilter = document.getElementById('milestone-anomaly-filter')?.value || 'all';
        } else if (context === 'iteration') {
            categoryFilter = document.getElementById('iteration-anomaly-filter')?.value || 'all';
        }
        
        console.log(`Current category filter for ${context}: ${categoryFilter}`);
        
        // If category filter is not 'all', filter the anomalies by category
        let filteredAnomalies = window.reportData.anomalies;
        
        if (categoryFilter !== 'all') {
            filteredAnomalies = window.reportData.anomalies.filter(anomaly => {
                return (anomaly.category || 'hygiene') === categoryFilter;
            });
            console.log(`Filtered anomalies by category '${categoryFilter}': ${filteredAnomalies.length} anomalies`);
        }
        
        // If context is milestones or iterations, we need to further filter by the active milestone/iteration
        if (context === 'milestone' && window.activeMilestoneId !== 'all') {
            // Find the active milestone and get its issues
            const milestone = window.reportData.milestones.find(m => String(m.id) === window.activeMilestoneId);
            if (milestone && milestone.issues) {
                const milestoneIssueIds = milestone.issues.map(issue => issue.id);
                filteredAnomalies = filteredAnomalies.filter(anomaly => {
                    return milestoneIssueIds.includes(anomaly.issue_id);
                });
                console.log(`Filtered anomalies by milestone '${window.activeMilestoneId}': ${filteredAnomalies.length} anomalies`);
            }
        } else if (context === 'iteration') {
            // For iterations, we need to filter by the active iteration or show only iteration-related anomalies
            if (window.activeIterationId && window.activeIterationId !== 'all') {
                // If a specific iteration is selected, filter by that iteration
                const iteration = window.reportData.iterations.find(it => String(it.id) === window.activeIterationId);
                if (iteration && iteration.issues) {
                    const iterationIssueIds = iteration.issues.map(issue => issue.id);
                    filteredAnomalies = filteredAnomalies.filter(anomaly => {
                        return iterationIssueIds.includes(anomaly.issue_id);
                    });
                    console.log(`Filtered anomalies by iteration '${window.activeIterationId}': ${filteredAnomalies.length} anomalies`);
                }
            } else {
                // If no specific iteration is selected, show anomalies from all iterations
                // Collect all issue IDs from all iterations
                const allIterationIssueIds = [];
                if (window.reportData.iterations && window.reportData.iterations.length > 0) {
                    window.reportData.iterations.forEach(iteration => {
                        if (iteration.issues && iteration.issues.length > 0) {
                            iteration.issues.forEach(issue => {
                                allIterationIssueIds.push(issue.id);
                            });
                        }
                    });
                    
                    // Filter anomalies to only include those in iterations
                    filteredAnomalies = filteredAnomalies.filter(anomaly => {
                        return allIterationIssueIds.includes(anomaly.issue_id);
                    });
                    console.log(`Filtered anomalies for all iterations: ${filteredAnomalies.length} anomalies`);
                }
            }
        }
        
        console.log(`Found ${filteredAnomalies.length} matching anomalies for export`);
        return filteredAnomalies;
    }
    
    function setupExportButtons() {
        console.log('Setting up export buttons...');
        
        // Load the SheetJS library dynamically
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
        script.async = true;
        script.onload = () => {
            console.log('SheetJS library loaded successfully');
        };
        script.onerror = () => {
            console.error('Failed to load SheetJS library');
            alert('Failed to load Excel export functionality. Please try again later.');
        };
        document.head.appendChild(script);
        
        // Setup export button for issues view
        const exportIssuesBtn = document.getElementById('export-issues-btn');
        if (exportIssuesBtn) {
            exportIssuesBtn.addEventListener('click', () => {
                const visibleAnomalies = getVisibleAnomalies('backlog');
                exportAnomaliestoExcel(visibleAnomalies, 'anomalies-export.xlsx');
            });
        }
        
        // Setup export button for milestones view
        const exportMilestonesBtn = document.getElementById('export-milestones-btn');
        if (exportMilestonesBtn) {
            exportMilestonesBtn.addEventListener('click', () => {
                const visibleAnomalies = getVisibleAnomalies('milestone');
                exportAnomaliestoExcel(visibleAnomalies, 'milestone-anomalies-export.xlsx');
            });
        }
        
        // Setup export button for iterations view
        const exportIterationsBtn = document.getElementById('export-iterations-btn');
        if (exportIterationsBtn) {
            exportIterationsBtn.addEventListener('click', () => {
                const visibleAnomalies = getVisibleAnomalies('iteration');
                exportAnomaliestoExcel(visibleAnomalies, 'iteration-anomalies-export.xlsx');
            });
        }
        
        console.log('Export buttons setup complete');
    }
    """

def _js_setup_event_listeners_orchestrator():
    """Generates the orchestrator function to call all event listener setup functions."""
    return """
    // --- Event Listener Orchestrator ---
    function setupEventListeners() {
        // Calls all individual event listener setup functions.
        // Ensures listeners are added only once after the initial data load and render.
        console.log("Setting up event listeners...");
        addViewButtonListeners();
        addDocumentListeners();
        addDropdownListener();
        addHashChangeListener();
        setupAnomalyFilter(); // Setup anomaly category filter dropdown
        setupExportButtons(); // Setup Excel export functionality
        console.log("Event listeners setup complete.");
    }
    """

def generate_event_listeners():
    """Generates the complete event listeners JavaScript."""
    logger.debug("Generating event listeners JavaScript...")
    js_parts = [
        _js_add_view_button_listeners(),
        _js_add_document_listeners(),
        _js_add_dropdown_listener(),
        _js_add_hashchange_listener(),
        _js_severity_link_setup(),
        _js_anomaly_filter(),
        _js_setup_anomaly_filter(),
        _js_export_anomalies(),
        _js_setup_event_listeners_orchestrator()
    ]
    js_content = "\n\n".join(js_parts)
    logger.debug("Event listeners JavaScript generated.")
    return js_content
