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
