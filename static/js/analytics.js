document.addEventListener('DOMContentLoaded', () => {
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

  // Chart defaults
  Chart.defaults.color = '#rgba(255, 255, 255, 0.7)';
  Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.1)';

  // Detection Accuracy Line Chart
  const accuracyCtx = document.getElementById('accuracyChart').getContext('2d');
  new Chart(accuracyCtx, {
    type: 'line',
    data: {
      labels: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
      datasets: [{
        label: 'Accuracy %',
        data: [92, 93, 95, 94, 96, 95],
        borderColor: '#6b67ff',
        backgroundColor: 'rgba(107, 103, 255, 0.1)',
        tension: 0.3,
        fill: true,
        pointBackgroundColor: '#6b67ff',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 4,
        pointHoverRadius: 6
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          callbacks: {
            label: (context) => `${context.datasets[0].label}: ${context.parsed.y}%` 
          }
        }
      },
      scales: {
        x: {
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: 'rgba(255, 255, 255, 0.6)' }
        },
        y: {
          beginAtZero: false,
          min: 88,
          max: 100,
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: {
            color: 'rgba(255, 255, 255, 0.6)',
            callback: (value) => value + '%'
          }
        }
      }
    }
  });

  // Gesture Frequency Bar Chart
  const gestureCtx = document.getElementById('gestureChart').getContext('2d');
  new Chart(gestureCtx, {
    type: 'bar',
    data: {
      labels: ['HELLO', 'THANK YOU', 'YES', 'NO', 'PLEASE', 'SORRY'],
      datasets: [{
        label: 'Count',
        data: [145, 132, 118, 95, 87, 76],
        backgroundColor: [
          'rgba(107, 103, 255, 0.7)',
          'rgba(107, 103, 255, 0.65)',
          'rgba(107, 103, 255, 0.6)',
          'rgba(107, 103, 255, 0.55)',
          'rgba(107, 103, 255, 0.5)',
          'rgba(107, 103, 255, 0.45)'
        ],
        borderColor: '#6b67ff',
        borderWidth: 1,
        borderRadius: 6,
        hoverBackgroundColor: 'rgba(107, 103, 255, 0.85)'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          titleColor: '#fff',
          bodyColor: '#fff',
          callbacks: {
            label: (context) => `${context.datasets[0].label}: ${context.parsed.y}` 
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: { color: 'rgba(255, 255, 255, 0.6)' }
        },
        y: {
          beginAtZero: true,
          grid: { color: 'rgba(255, 255, 255, 0.05)' },
          ticks: { color: 'rgba(255, 255, 255, 0.6)' }
        }
      }
    }
  });
});
