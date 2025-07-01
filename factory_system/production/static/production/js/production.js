document.addEventListener('DOMContentLoaded', function () {
    initDataTables();
    setupStatusUpdateHandlers();
});

function initDataTables() {
    ['#productionTable', '#productionDetailTable'].forEach(selector => {
        const table = $(selector);
        if (table.length && $.fn.DataTable && !$.fn.DataTable.isDataTable(selector)) {
            table.DataTable({
                pageLength: 25,
                autoWidth: false,
                responsive: true,
                order: [[0, 'asc']],
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                language: {
                    searchPlaceholder: "Quick Search...",
                    search: "",
                    lengthMenu: "_MENU_ entries per page",
                    paginate: {
                        previous: "<",
                        next: ">"
                    }
                }
            });
        }
    });
}

function setupStatusUpdateHandlers() {
    document.querySelectorAll('[data-action="update-status"]').forEach(item => {
        item.addEventListener('click', function (e) {
            e.preventDefault();
            const stageId = this.dataset.stageId;
            const fieldName = this.dataset.field;
            const newStatus = this.dataset.value;
            updateStatus(stageId, fieldName, newStatus);
        });
    });
}

function updateStatus(stageId, fieldName, newStatus) {
    const url = `/production/${stageId}/update_status/`;
    const csrfToken = getCookie('csrftoken');

    if (!csrfToken) {
        showAlert('Security error. Please refresh the page.', 'danger');
        return;
    }

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            status_field: fieldName,
            new_value: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            updateStatusUI(data.stage_id, data.status_field, data.new_value);
        } else {
            showAlert(`Failed to update: ${data.error}`, 'danger');
        }
    })
    .catch(error => {
        console.error('Fetch Error:', error);
        showAlert('Network error while updating status.', 'danger');
    });
}

function updateStatusUI(stageId, fieldName, newStatus) {
    const field = fieldName.replace('_status', '');
    const badgeId = `dropdownMenu${field}${stageId}`;
    const badge = document.getElementById(badgeId);

    if (!badge) {
        console.warn(`⚠️ Badge not found: #${badgeId}`);
        return;
    }

    // Update class
    badge.className = badge.className.replace(/bg-\w+/g, '').trim();
    badge.classList.add(`bg-${getBadgeColor(newStatus)}`, 'dropdown-toggle', 'text-decoration-none');

    // Update text
    badge.textContent = formatStatusText(newStatus);
}

function getBadgeColor(status) {
    switch (status) {
        case 'NOT_STARTED': return 'secondary';
        case 'IN_PROGRESS': return 'warning';
        case 'STUCK': return 'danger';
        case 'ON_HOLD': return 'dark';
        case 'COMPLETED': return 'success';
        case 'READY': return 'info';
        case 'CONFIRMATION': return 'primary';
        case 'NO_PAPERWORK': return 'danger';
        default: return 'secondary';
    }
}

function formatStatusText(status) {
    return status.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return decodeURIComponent(parts[1].split(';')[0]);
    return null;
}

function showAlert(message, type = 'info') {
    const existing = document.querySelector('.custom-alert');
    if (existing) existing.remove();

    const alert = document.createElement('div');
    alert.className = `alert alert-${type} custom-alert position-fixed top-0 start-50 translate-middle-x mt-3`;
    alert.style.zIndex = '1050';
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    document.body.appendChild(alert);
    setTimeout(() => alert.remove(), 4000);
}
