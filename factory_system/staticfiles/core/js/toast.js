// core/static/core/js/toast.js
document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    toastElList.forEach(function(toastEl) {
        new bootstrap.Toast(toastEl).show();
    });
});