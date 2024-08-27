document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.sidebar .nav-link');
    const contentSections = document.querySelectorAll('.content-section');

    function showSection(sectionId) {
        contentSections.forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');
    }

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const sectionId = this.getAttribute('data-section');
            
            navLinks.forEach(navLink => {
                navLink.classList.remove('active');
            });
            this.classList.add('active');

            showSection(sectionId);

            // Update URL without page reload
            history.pushState(null, '', `#${sectionId}`);
        });
    });

    // Handle browser back/forward navigation
    window.addEventListener('popstate', function() {
        const sectionId = window.location.hash.slice(1) || 'home';
        showSection(sectionId);
        
        navLinks.forEach(link => {
            link.classList.toggle('active', link.getAttribute('data-section') === sectionId);
        });
    });

    // Initial load
    const initialSectionId = window.location.hash.slice(1) || 'home';
    showSection(initialSectionId);
});