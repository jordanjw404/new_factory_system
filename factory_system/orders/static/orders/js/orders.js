// static/orders.js/orders.js

// wrap in ready to ensure the table exists
$(document).ready(function() {
  $('#ordersTable').DataTable({
    pageLength: 10,
    lengthMenu: [
      [10, 25, 50, -1],
      [10, 25, 50, "All"]
    ],
    autoWidth: false,
    responsive: true,
    order: [[1, 'asc']],
    language: {
      lengthMenu: "_MENU_ entries per page",
      searchPlaceholder: "Quick Search…",
      search: "",
      paginate: {
        previous: "<",
        next: ">"
      }
    }
  });
});
