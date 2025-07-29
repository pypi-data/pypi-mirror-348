import logging

logger = logging.getLogger(__name__)

def _js_utilities():
    """Generates JS utility functions (formatDate, escapeHtml)."""
    return """
    // --- Utilities ---
    function getIterationSpillCount(anomaly) {
        if (!Array.isArray(anomaly.iteration_activities)) return 0
        return anomaly.iteration_activities.length
    }

    function formatDate(dateString) {
        // Formats date string for display, handles nulls and basic date-only strings.
        if (!dateString) return 'N/A';
        const date = new Date(dateString);
        if (isNaN(date.getTime())) {
            // If parsing fails, return the original string
            return dateString;
        }
        // Check if it's just a date (YYYY-MM-DD)
        if (dateString.match(/^\\d{4}-\\d{2}-\\d{2}$/)) {
            // Add time part to treat it consistently as UTC for date display
            return new Date(dateString + 'T00:00:00Z').toLocaleDateString(undefined, {
                year: 'numeric', month: 'short', day: 'numeric' // Adjust format as needed
            });
        }
        // Otherwise, format as full date and time
        return date.toLocaleString(undefined, {
             year: 'numeric', month: 'short', day: 'numeric',
             hour: 'numeric', minute: '2-digit', timeZoneName: 'short' // Adjust format as needed
        });
    }

    function escapeHtml(unsafe) {
        // Escapes HTML special characters to prevent XSS.
        if (typeof unsafe !== 'string') {
            if (unsafe === null || unsafe === undefined) return '';
            try {
                unsafe = String(unsafe); // Convert non-strings
            } catch (e) {
                return ''; // Return empty if conversion fails
            }
        }
        return unsafe
             .replace(/&/g, "&amp;")
             .replace(/</g, "&lt;")
             .replace(/>/g, "&gt;")
             .replace(/"/g, "&quot;")
             .replace(/'/g, "&#039;");
    }
    """

def _js_render_anomaly_item():
    """Generates JS function to render a single anomaly item."""
    return """
    // --- Rendering Helpers ---
    function renderAnomalyItem(anomaly) {
        // Generates the HTML string for a single anomaly item.
        // Includes link, type, severity, description, and expandable details.
        return `
            <div id="anomaly-${anomaly.issue_id}" class="anomaly-item ${anomaly.severity}" data-category="${anomaly.category || 'hygiene'}">
                <h3>
                    <a href="${anomaly.web_url}" target="_blank" rel="noopener noreferrer" class="issue-link">
                        Issue #${anomaly.issue_id}: ${escapeHtml(anomaly.title)}
                    </a>
                    <span class="category-badge ${anomaly.category || 'hygiene'}">${escapeHtml(anomaly.category || 'hygiene')}</span>
                </h3>
                <p class="description"><strong>Description:</strong> ${escapeHtml(anomaly.description)}</p>
                
                <details>
                    <summary>More information</summary>
                    <p><strong>Type:</strong> ${escapeHtml(anomaly.type)}</p>
                    <p><strong>Severity:</strong> <span class="severity-${anomaly.severity}" style="text-transform: capitalize;">${escapeHtml(anomaly.severity)}</span></p>
                    <p><strong>Assignees:</strong> ${anomaly.assignees && anomaly.assignees.length > 0 ? 
                        anomaly.assignees.map(a => `<a href="${escapeHtml(a.web_url)}" class="assignee-link" target="_blank" rel="noopener noreferrer">${escapeHtml(a.name)}</a>`).join(', ') : 
                        'Unassigned'}</p>
                    <p><strong>Status:</strong> ${escapeHtml(anomaly.state)}</p>
                    <p><strong>Current Iteration:</strong> ${escapeHtml(anomaly.current_iteration || 'N/A')}</p>
                    <p><strong>Total Iterations:</strong> ${getIterationSpillCount(anomaly)}</p>
                    ${anomaly.details ? `
                    <details>
                        <summary>Technical Details</summary>
                        <pre>${escapeHtml(JSON.stringify(anomaly.details, null, 2))}</pre>
                    </details>
                    ` : ''}
                </details>
            </div>
        `;
    }
    """

def _js_render_issue_view():
    """Generates JS function to render the entire issue view."""
    return """
    // --- Issue View Rendering ---
    function renderIssueView(data) {
        // Populates the backlog view with stats and the list of all anomalies.
        console.log("Rendering backlog view...");

        // Update general stats
        dom.totalIssuesEl.textContent = data.total_issues ?? '0';
        dom.totalAnomaliesEl.textContent = data.total_anomalies ?? '0';

        // Get anomalies, sort by severity (high > medium > low)
        const anomalies = (data.anomalies || []).sort((a, b) => {
            const severityOrder = {'high': 0, 'medium': 1, 'low': 2};
            // Use ?? 3 to place unknown severities last
            return (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3);
        });

        // Update severity stat cards/links
        const severityCounts = data.anomalies_by_severity || { high: 0, medium: 0, low: 0 };
        setupSeverityLink(dom.highSeverityLink, severityCounts.high, anomalies, 'high');
        setupSeverityLink(dom.mediumSeverityLink, severityCounts.medium, anomalies, 'medium');
        setupSeverityLink(dom.lowSeverityLink, severityCounts.low, anomalies, 'low');

        // Render the list of anomaly items
        if (anomalies.length === 0) {
            dom.anomaliesListEl.innerHTML = '<p>No anomalies detected.</p>';
        } else {
            // Generate HTML for each anomaly and join them
            dom.anomaliesListEl.innerHTML = anomalies.map(renderAnomalyItem).join('');
            
            // Apply default filtering to show all anomalies
            applyDefaultFiltering();
        }
        console.log("backlog view rendering complete.");
    }
    """

def _js_render_milestone_view():
    """Generates JS functions for milestone rendering."""
    return """
    // --- Milestone View Rendering ---
    function getActiveMilestones(allMilestones) {
        // Filters and sorts active milestones
        console.log("Filtering and sorting active milestones...");
        const currentDate = new Date();

        const active = (allMilestones || [])
            .filter(m => {
                if (m.state !== 'active') return false;
                const startDate = m.start_date ? new Date(m.start_date + 'T00:00:00Z') : null;
                const dueDate = m.due_date ? new Date(m.due_date + 'T23:59:59Z') : null;
                const isStarted = startDate ? startDate <= currentDate : true;
                const isNotDue = dueDate ? dueDate >= currentDate : true;
                return isStarted && isNotDue;
            })
            .sort((a, b) => {
                const dateA = a.due_date ? new Date(a.due_date) : new Date('9999-12-31');
                const dateB = b.due_date ? new Date(b.due_date) : new Date('9999-12-31');
                return dateA - dateB;
            });
        console.log(`Found ${active.length} active milestones.`);
        return active;
    }

    function updateMilestoneDropdown(activeMilestones) {
        console.log("Updating milestone dropdown...");
        const dropdownContent = activeMilestones.map(milestone => `
            <div class="milestone-dropdown-item" data-milestone="${milestone.id}" role="menuitem">
                <div class="milestone-dropdown-title">${escapeHtml(milestone.title)}</div>
                ${milestone.due_date ? `
                <div class="milestone-dropdown-due">Due: ${formatDate(milestone.due_date)}</div>
                ` : ''}
            </div>`).join('');

        dom.dropdown.innerHTML = `
            <div class="milestone-dropdown-item" data-milestone="all" role="menuitem">
                <div class="milestone-dropdown-title">All Active Milestones</div>
            </div>
            ${dropdownContent}`;
        console.log("Milestone dropdown updated.");
    }

    function renderSingleMilestoneCard(milestone) {
        // Sort anomalies by severity
        const anomalies = (milestone.anomalies || []).sort((a, b) => {
            const severityOrder = {'high': 0, 'medium': 1, 'low': 2};
            return (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3);
        });

        const severityCounts = milestone.anomalies_by_severity || { high: 0, medium: 0, low: 0 };
        const issuesCount = milestone.issues?.length ?? '0';
        const anomaliesCount = milestone.total_anomalies ?? '0';

        return `
            <div class="milestone-card" id="milestone-${milestone.id}">
                <div class="milestone-header">
                    <h3 class="milestone-title">
                        <a href="${milestone.web_url}" target="_blank" rel="noopener noreferrer" class="issue-link">
                            ${escapeHtml(milestone.title)}
                        </a>
                    </h3>
                    <div class="milestone-dates">
                        ${milestone.start_date ? `<strong>Start:</strong> ${formatDate(milestone.start_date)}<br>` : ''}
                        ${milestone.due_date ? `<strong>Due:</strong> ${formatDate(milestone.due_date)}` : 'No due date'}
                    </div>
                </div>
                <div class="milestone-stats">
                    <div class="milestone-stat"><div class="milestone-stat-label">Issues</div><div class="milestone-stat-value">${issuesCount}</div></div>
                    <div class="milestone-stat"><div class="milestone-stat-label">Anomalies</div><div class="milestone-stat-value">${anomaliesCount}</div></div>
                    <div class="milestone-stat"><span class="severity-high">High</span> <a href="#" class="severity-count-link severity-high milestone-stat-value" data-milestone="${milestone.id}" data-severity="high" id="milestone-${milestone.id}-high" tabindex="0">${severityCounts.high}</a></div>
                    <div class="milestone-stat"><span class="severity-medium">Medium</span> <a href="#" class="severity-count-link severity-medium milestone-stat-value" data-milestone="${milestone.id}" data-severity="medium" id="milestone-${milestone.id}-medium" tabindex="0">${severityCounts.medium}</a></div>
                    <div class="milestone-stat"><span class="severity-low">Low</span> <a href="#" class="severity-count-link severity-low milestone-stat-value" data-milestone="${milestone.id}" data-severity="low" id="milestone-${milestone.id}-low" tabindex="0">${severityCounts.low}</a></div>
                </div>
                ${anomalies.length > 0 ? `
                <div class="milestone-anomalies">
                    <h4 class="milestone-section-heading">Anomalies</h4>
                    ${anomalies.map(a => `
                        <div class="anomaly-item ${a.severity}" data-category="${a.category || 'hygiene'}" id="milestone-anomaly-${milestone.id}-${a.severity}">
                            <h3>
                                <a href="${a.web_url}" target="_blank" rel="noopener noreferrer" class="issue-link">
                                    Issue #${a.issue_id}: ${escapeHtml(a.title)}
                                </a>
                                <span class="category-badge ${a.category || 'hygiene'}">${escapeHtml(a.category || 'hygiene')}</span>
                            </h3>
                            <p>${escapeHtml(a.description)}</p>
                            <details>
                                <summary>More Information</summary>
                                <p><strong>Type:</strong> ${escapeHtml(a.type)}</p>
                                <p><strong>Severity:</strong> <span class="severity-${a.severity}" style="text-transform: capitalize;">${escapeHtml(a.severity)}</span></p>
                                <p><strong>Assignees:</strong> ${a.assignees && a.assignees.length > 0 ? 
                                    a.assignees.map(assignee => `<a href="${escapeHtml(assignee.web_url)}" class="assignee-link" target="_blank" rel="noopener noreferrer">${escapeHtml(assignee.name)}</a>`).join(', ') : 
                                    'Unassigned'}</p>
                                <p><strong>Status:</strong> ${escapeHtml(a.state)}</p>
                                <p><strong>Current Iteration:</strong> ${escapeHtml(a.current_iteration || 'N/A')}</p>
                                <p><strong>Total Iterations:</strong> ${getIterationSpillCount(a)}</p>
                                ${a.details ? `
                                <details>
                                    <summary>Technical Details</summary>
                                    <pre>${escapeHtml(JSON.stringify(a.details, null, 2))}</pre>
                                </details>
                                ` : ''}
                            </details>
                        </div>
                    `).join('')}
                </div>
                ` : ''}
            </div>
        `;
    }

    function renderMilestoneView(data) {
        console.log("Rendering milestone view...");
        const activeMilestones = getActiveMilestones(data.milestones);
        updateMilestoneDropdown(activeMilestones);
        dom.totalMilestonesEl.textContent = activeMilestones.length ?? '0';

        const totalAnomalies = activeMilestones.reduce((sum, m) => sum + (m.total_anomalies || 0), 0);
        dom.totalMilestoneAnomaliesEl.textContent = totalAnomalies ?? '0';

        let displayedMilestones = activeMilestones;
        if (window.activeMilestoneId !== 'all') {
            displayedMilestones = activeMilestones.filter(m => String(m.id) === String(window.activeMilestoneId));
        }

        if (displayedMilestones.length === 0) {
            dom.milestonesListEl.innerHTML = '<p>No active milestones found.</p>';
        } else {
            dom.milestonesListEl.innerHTML = displayedMilestones.map(renderSingleMilestoneCard).join('');
            filterAnomaliesByCategory('all', 'milestone');
        }
        console.log("Milestone view rendering complete.");
    }
    """

def _js_render_iteration_view():
    """Generates JS functions for iteration rendering."""
    return """
    // --- Iteration View Rendering ---
    function getActiveIterations(allIterations) {
        console.log("Filtering and sorting active iterations...");
        return (allIterations || [])
            .sort((a,b) => new Date(a.due_date||'9999-12-31') - new Date(b.due_date||'9999-12-31'));
    }

    function updateIterationDropdown(activeIterations) {
        console.log("Updating iteration dropdown...");
        const items = activeIterations.map(it => `
            <div class="iteration-dropdown-item" data-iteration="${it.id}" role="menuitem">
                <div class="iteration-dropdown-title">${escapeHtml(it.title)}</div>
                ${it.due_date ? `<div class="iteration-dropdown-due">Due: ${formatDate(it.due_date)}</div>` : ''}
            </div>`).join('');
        dom.iterationDropdown.innerHTML = `
            <div class="iteration-dropdown-item" data-iteration="all" role="menuitem">
                <div class="iteration-dropdown-title">All Active Iterations</div>
            </div>${items}`;
    }

    function renderSingleIterationCard(iteration) {
        const anomalies = (iteration.anomalies || []).sort((a, b) => {
            const severityOrder = {'high': 0, 'medium': 1, 'low': 2};
            return (severityOrder[a.severity] ?? 3) - (severityOrder[b.severity] ?? 3);
        });

        const severityCounts = iteration.anomalies_by_severity || { high: 0, medium: 0, low: 0 };
        const issuesCount = iteration.issues?.length ?? '0';
        const anomaliesCount = iteration.total_anomalies ?? '0';

        return `
            <div class="milestone-card iteration-card" id="iteration-${iteration.id}">
                <div class="milestone-header">
                    <h3 class="milestone-title">
                        ${escapeHtml(iteration.title)}
                    </h3>
                    <div class="milestone-dates">
                        ${iteration.start_date ? `<strong>Start:</strong> ${formatDate(iteration.start_date)}<br>` : ''}
                        ${iteration.due_date ? `<strong>Due:</strong> ${formatDate(iteration.due_date)}` : 'No due date'}
                    </div>
                </div>
                <div class="milestone-stats">
                    <div class="milestone-stat"><div class="milestone-stat-label">Issues</div><div class="milestone-stat-value">${issuesCount}</div></div>
                    <div class="milestone-stat"><div class="milestone-stat-label">Anomalies</div><div class="milestone-stat-value">${anomaliesCount}</div></div>
                    <div class="milestone-stat"><span class="severity-high">High</span> <a href="#" class="severity-count-link severity-high milestone-stat-value" data-iteration="${iteration.id}" data-severity="high" id="iteration-${iteration.id}-high" tabindex="0">${severityCounts.high}</a></div>
                    <div class="milestone-stat"><span class="severity-medium">Medium</span> <a href="#" class="severity-count-link severity-medium milestone-stat-value" data-iteration="${iteration.id}" data-severity="medium" id="iteration-${iteration.id}-medium" tabindex="0">${severityCounts.medium}</a></div>
                    <div class="milestone-stat"><span class="severity-low">Low</span> <a href="#" class="severity-count-link severity-low milestone-stat-value" data-iteration="${iteration.id}" data-severity="low" id="iteration-${iteration.id}-low" tabindex="0">${severityCounts.low}</a></div>
                </div>
                ${anomalies.length > 0 ? `
                <div class="milestone-anomalies">
                    <h4 class="milestone-section-heading">Anomalies</h4>
                    ${anomalies.map(a => `
                        <div class="anomaly-item ${a.severity}" data-category="${a.category || 'hygiene'}" id="iteration-anomaly-${iteration.id}-${a.severity}">
                            <h3>
                                <a href="${a.web_url}" target="_blank" rel="noopener noreferrer" class="issue-link">
                                    Issue #${a.issue_id}: ${escapeHtml(a.title)}
                                </a>
                                <span class="category-badge ${a.category || 'hygiene'}">${escapeHtml(a.category || 'hygiene')}</span>
                            </h3>
                            <p>${escapeHtml(a.description)}</p>
                            <details>
                                <summary>More Information</summary>
                                <p><strong>Type:</strong> ${escapeHtml(a.type)}</p>
                                <p><strong>Severity:</strong> <span class="severity-${a.severity}" style="text-transform: capitalize;">${escapeHtml(a.severity)}</span></p>
                                <p><strong>Assignees:</strong> ${a.assignees && a.assignees.length > 0 ? 
                                    a.assignees.map(assignee => `<a href="${escapeHtml(assignee.web_url)}" class="assignee-link" target="_blank" rel="noopener noreferrer">${escapeHtml(assignee.name)}</a>`).join(', ') : 
                                    'Unassigned'}</p>
                                <p><strong>Status:</strong> ${escapeHtml(a.state)}</p>
                                <p><strong>Current Iteration:</strong> ${escapeHtml(a.current_iteration || 'N/A')}</p>
                                <p><strong>Total Iterations:</strong> ${getIterationSpillCount(a)}</p>
                                ${a.details ? `
                                <details>
                                    <summary>Technical Details</summary>
                                    <pre>${escapeHtml(JSON.stringify(a.details, null, 2))}</pre>
                                </details>
                                ` : ''}
                            </details>
                        </div>
                    `).join('')}
                </div>
                ` : '<p>No anomalies in this iteration.</p>'}
            </div>
        `;
    }

    function renderIterationView(data) {
        console.log("Rendering Iterations View...");
        const activeIters = getActiveIterations(data.iterations);
        dom.totalIterationsEl.textContent = activeIters.length;
        dom.totalIterationAnomaliesEl.textContent = activeIters.reduce((sum,it)=>(sum + (it.total_anomalies||0)),0);
        updateIterationDropdown(activeIters);

        const displayed = window.activeIterationId==='all'?activeIters:activeIters.filter(it=>it.id.toString()===window.activeIterationId);
        
        if(!displayed.length){ 
            const msg=window.activeIterationId==='all'?'No active iterations found.':`Iteration ID ${escapeHtml(window.activeIterationId)} not found.`; 
            dom.iterationsListEl.innerHTML=`<p>${msg}</p>`;
        } else { 
            dom.iterationsListEl.innerHTML=displayed.map(renderSingleIterationCard).join('');
            
            // Apply filtering to iteration anomaly items
            filterAnomaliesByCategory('all', 'iteration');
            
            // Set up click handlers for severity links in iteration cards
            displayed.forEach(iteration => {
                ['high', 'medium', 'low'].forEach(severity => {
                    const link = document.getElementById(`iteration-${iteration.id}-${severity}`);
                    if (link) {
                        link.addEventListener('click', (e) => {
                            e.preventDefault();
                            const targetId = `iteration-anomaly-${iteration.id}-${severity}`;
                            const targetElement = document.getElementById(targetId);
                            if (targetElement) {
                                targetElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                                targetElement.classList.add('highlight-anomaly');
                                setTimeout(() => targetElement.classList.remove('highlight-anomaly'), 1200);
                            }
                        });
                    }
                });
            });
        }
        
        console.log("Iterations View rendering complete.");
    }
    """

def generate_rendering():
    """Generates the complete rendering JavaScript."""
    logger.debug("Generating rendering JavaScript...")
    js_parts = [
        _js_utilities(),
        _js_render_anomaly_item(),
        _js_render_issue_view(),
        _js_render_milestone_view(),
        _js_render_iteration_view()
    ]
    js_content = "\n\n".join(js_parts)
    logger.debug("Rendering JavaScript generated.")
    return js_content
