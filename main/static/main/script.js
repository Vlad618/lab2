document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.querySelector('.category-filter select');
    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            this.form.submit();
        });
    }
});
