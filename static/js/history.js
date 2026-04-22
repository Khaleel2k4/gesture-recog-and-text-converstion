document.addEventListener('DOMContentLoaded', () => {
  const tbody = document.getElementById('history-tbody');
  const prevBtn = document.getElementById('prev-page');
  const nextBtn = document.getElementById('next-page');
  const paginationInfo = document.getElementById('pagination-info');
  const applyBtn = document.getElementById('apply-filters');

  let currentPage = 1;
  const rowsPerPage = 12;

  // Mock data
  const mockData = [
    { date: '2024-04-23', time: '12:56 PM', gesture: 'HELLO' },
    { date: '2024-04-23', time: '12:56 PM', gesture: 'THANK YOU' },
    { date: '2024-04-23', time: '12:34 PM', gesture: 'YES' },
    { date: '2024-04-23', time: '11:59 AM', gesture: 'YELLOW' },
    { date: '2024-04-23', time: '11:53 AM', gesture: 'NUMBER' },
    { date: '2024-04-23', time: '11:53 AM', gesture: 'NUMBER' },
    { date: '2024-04-22', time: '04:21 PM', gesture: 'NO' },
    { date: '2024-04-22', time: '04:12 PM', gesture: 'PLEASE' },
    { date: '2024-04-22', time: '03:45 PM', gesture: 'HELLO' },
    { date: '2024-04-22', time: '03:30 PM', gesture: 'THANK YOU' },
    { date: '2024-04-22', time: '02:15 PM', gesture: 'YES' },
    { date: '2024-04-22', time: '01:55 PM', gesture: 'SORRY' },
    // Add more entries for pagination demo
    ...Array.from({ length: 30 }, (_, i) => ({
      date: '2024-04-21',
      time: `${10 + Math.floor(i / 4)}:${String((i % 4) * 15).padStart(2, '0')} AM`,
      gesture: ['HELLO', 'THANK YOU', 'YES', 'NO', 'PLEASE', 'SORRY'][i % 6]
    }))
  ];

  let filteredData = [...mockData];

  function renderRows() {
    const start = (currentPage - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const page = filteredData.slice(start, end);

    tbody.innerHTML = page.map(row => `
      <tr>
        <td>${row.date}</td>
        <td>${row.time}</td>
        <td>${row.gesture}</td>
        <td><button class="btn-detail">View Details ></button></td>
      </tr>
    `).join('');

    updatePagination();
  }

  function updatePagination() {
    const total = filteredData.length;
    const start = (currentPage - 1) * rowsPerPage + 1;
    const end = Math.min(currentPage * rowsPerPage, total);
    paginationInfo.textContent = `${start} - ${end} of ${total}`;
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = end >= total;
  }

  prevBtn.addEventListener('click', () => {
    if (currentPage > 1) {
      currentPage--;
      renderRows();
    }
  });

  nextBtn.addEventListener('click', () => {
    const maxPage = Math.ceil(filteredData.length / rowsPerPage);
    if (currentPage < maxPage) {
      currentPage++;
      renderRows();
    }
  });

  applyBtn.addEventListener('click', () => {
    const startDate = document.getElementById('start-date').value;
    const endDate = document.getElementById('end-date').value;
    const gesture = document.getElementById('gesture-filter').value;

    filteredData = mockData.filter(item => {
      const inDateRange = (!startDate || item.date >= startDate) && (!endDate || item.date <= endDate);
      const inGesture = gesture === 'all' || item.gesture.toLowerCase().includes(gesture.toLowerCase());
      return inDateRange && inGesture;
    });

    currentPage = 1;
    renderRows();
  });

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

  renderRows();
});
