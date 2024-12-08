// Copyright @emontj 2024

document.addEventListener('DOMContentLoaded', () => {
    const searchForm = document.getElementById('searchForm');
    searchForm.addEventListener('submit', (event) => {
        event.preventDefault();
        const query = document.getElementById('searchInput').value;

        // TODO: Most basic search functionality, make better in the future.
        if (query) {
            // Redirect to /person/{input}
            window.location.href = `/person/${encodeURIComponent(query)}`;
        } else {
            alert('Please enter a valid search term.');
        }
    });
});
