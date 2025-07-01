// production/static/production/js/production.js
function updateStatus(stageId, fieldName, newStatus) {
  let url = `/production/${stageId}/update_status/`;
  
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      status_field: fieldName,
      new_value: newStatus
    })
  })
  .then(response => {
    if (response.ok) {
      location.reload();
    } else {
      alert('Failed to update status.');
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert('Error updating status.');
  });
}

// Function to get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Attach event listeners when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
  // Add event listeners to dropdown items
  document.querySelectorAll('[data-action="update-status"]').forEach(item => {
    item.addEventListener('click', function(e) {
      e.preventDefault();
      const stageId = this.dataset.stageId;
      const fieldName = this.dataset.field;
      const newStatus = this.dataset.value;
      updateStatus(stageId, fieldName, newStatus);
    });
  });
  
  // Initialize DataTables
  $('#productionTable').DataTable({
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
});