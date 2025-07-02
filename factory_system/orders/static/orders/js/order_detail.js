// static/orders/js/order_detail.js
$(document).ready(function() {
  $('#OrderDetailList').DataTable({
    pageLength: 10,
    lengthMenu: [
      [10, 25, 50, -1],
      [10, 25, 50, "All"]
    ],
    autoWidth: true,
    responsive: true,
    order: [[0, 'asc']],  
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
