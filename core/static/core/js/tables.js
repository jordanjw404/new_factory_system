document.addEventListener('DOMContentLoaded', () => {
  // Find every table marked for DataTables
  document.querySelectorAll('.datatable').forEach(table => {
    // Initialize DataTables via jQuery
    $(table).DataTable({
      // Default to 25 rows, but allow user to change
      pageLength: 25,
      lengthChange: true,              // enable the rows-per-page dropdown
      lengthMenu: [                    // define the dropdown options
        [10, 25, 50, 100, -1],         // values
        [10, 25, 50, 100, "All"]       // labels
      ],
      autoWidth: false
    });
  });
});

// ----- Status dropdown AJAX (no inline JS; CSP-safe) -----
(function () {
  // Keep in sync with server get_badge_color()
  const BADGE_COLOR = {
    NOT_STARTED: 'secondary',
    IN_PROGRESS: 'warning',
    STUCK: 'danger',
    ON_HOLD: 'dark',
    COMPLETED: 'success',
    READY: 'info',
    CONFIRMATION: 'primary',
    NO_PAPERWORK: 'danger'
  };

  function getCookie(name) {
    const m = document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)');
    return m ? decodeURIComponent(m.pop()) : '';
  }

  function setBadge(el, value, label) {
    if (!el) return;
    if (label) el.textContent = label;
    // remove any existing bg-* classes then apply the new one
    el.className = el.className.replace(/\bbg-\w+\b/g, '').trim();
    el.classList.add('bg-' + (BADGE_COLOR[value] || 'secondary'));
  }

  document.addEventListener('click', async (e) => {
    const link = e.target.closest('a[data-action="update-status"]');
    if (!link) return;

    e.preventDefault();

    const dd     = link.closest('.dropdown');
    const url    = dd && dd.dataset && dd.dataset.url;      // {% url 'production:production_update_status' stage.id %}
    const field  = link.dataset.field;                      // e.g. "build_status"
    const value  = link.dataset.value;                      // e.g. "IN_PROGRESS"
    const label  = link.textContent.trim();                 // "In Progress"
    const toggle = dd && dd.querySelector('[data-bs-toggle="dropdown"].badge');

    if (!field || !value) return;

    // Fallback if data-url wasn't added (still works)
    const stageId = (dd && dd.dataset && dd.dataset.stageId) || link.dataset.stageId;
    const postUrl = url || (stageId ? `/production/${stageId}/update_status/` : null);
    if (!postUrl) return;

    // subtle saving hint
    if (toggle) toggle.classList.add('opacity-75');

    try {
      const res = await fetch(postUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // harmless if view is csrf_exempt; required if you later enable CSRF
          'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ status_field: field, new_value: value })
      });

      if (!res.ok) {
        // show server response to help debugging (404 from bad id, 400 from bad value, etc.)
        console.error('Update failed:', await res.text());
        alert('Update failed — check server logs.');
        return;
      }

      // Update the badge instantly
      setBadge(toggle, value, label);

      // Close the dropdown (Bootstrap 5) if available
      try {
        const inst = window.bootstrap && window.bootstrap.Dropdown
          ? window.bootstrap.Dropdown.getOrCreateInstance(toggle)
          : null;
        if (inst) inst.hide();
      } catch (_) {}
    } catch (err) {
      console.error(err);
      alert('Network error while saving.');
    } finally {
      if (toggle) toggle.classList.remove('opacity-75');
    }
  });
})();
