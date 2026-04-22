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

  // Read data from JSON script tag
  const gestureData = JSON.parse(document.getElementById('gestureData').textContent);
  const gestureStats = gestureData.gestureStats || [];
  const gestureHistory = gestureData.gestureHistory || [];

  // Detection Accuracy Line Chart - using real confidence data from history
  const accuracyCtx = document.getElementById('accuracyChart').getContext('2d');
  
  // Group confidence by time for the line chart
  const accuracyLabels = [];
  const accuracyData = [];
  
  if (gestureHistory.length > 0) {
    // Take last 20 entries for the chart
    const recentHistory = gestureHistory.slice(0, 20).reverse();
    recentHistory.forEach(entry => {
      if (entry.timestamp) {
        accuracyLabels.push(new Date(entry.timestamp).toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }));
        accuracyData.push(entry.confidence);
      }
    });
  } else {
    // Default data if no history
    accuracyLabels.push('No Data');
    accuracyData.push(0);
  }

  new Chart(accuracyCtx, {
    type: 'line',
    data: {
      labels: accuracyLabels,
      datasets: [{
        label: 'Confidence %',
        data: accuracyData,
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
          beginAtZero: true,
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

  // Gesture Frequency Bar Chart - using real stats from database
  const gestureCtx = document.getElementById('gestureChart').getContext('2d');
  
  const gestureLabels = gestureStats.map(stat => stat.gesture);
  const gestureCounts = gestureStats.map(stat => stat.count);
  
  // Generate gradient colors
  const backgroundColors = gestureCounts.map((_, i) => {
    const opacity = 0.7 - (i * 0.05);
    return `rgba(107, 103, 255, ${Math.max(opacity, 0.3)})`;
  });

  new Chart(gestureCtx, {
    type: 'bar',
    data: {
      labels: gestureLabels.length > 0 ? gestureLabels : ['No Data'],
      datasets: [{
        label: 'Count',
        data: gestureCounts.length > 0 ? gestureCounts : [0],
        backgroundColor: backgroundColors.length > 0 ? backgroundColors : ['rgba(107, 103, 255, 0.7)'],
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
