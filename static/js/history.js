document.addEventListener('DOMContentLoaded', () => {
  const prevBtn = document.getElementById('prev-page');
  const nextBtn = document.getElementById('next-page');
  const applyBtn = document.getElementById('apply-filters');

  // Mock data and rendering disabled - data now rendered by Jinja2 template from database
  // The table is now populated server-side with real gesture history data

  // Sidebar nav handling
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', e => {
      if (item.getAttribute('href') !== '#') {
        return;
      }
      e.preventDefault();
      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
    });
  });
});
