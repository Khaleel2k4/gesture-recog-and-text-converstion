document.addEventListener('DOMContentLoaded', () => {
  // Sidebar navigation active state
  const navItems = document.querySelectorAll('.nav-item');
  navItems.forEach(item => {
    item.addEventListener('click', e => {
      // Allow navigation if href points to a different page
      if (item.getAttribute('href') !== '#') {
        return;
      }
      e.preventDefault();
      navItems.forEach(i => i.classList.remove('active'));
      item.classList.add('active');
    });
  });

  // Animate status circle on load
  const statusCircle = document.querySelector('.status-circle-fill');
  if (statusCircle) {
    setTimeout(() => {
      statusCircle.style.strokeDashoffset = '16.96';
    }, 300);
  }

  // Animate bars on scroll into view
  const observer = new IntersectionObserver(
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animation = 'slideUp 0.6s ease-out forwards';
        }
      });
    },
    { threshold: 0.3 }
  );

  document.querySelectorAll('.bar').forEach(bar => {
    const height = bar.style.height;
    bar.style.height = '0';
    observer.observe(bar);
    setTimeout(() => {
      bar.style.height = height;
    }, 100);
  });

  // Simulate live activity updates
  const activityList = document.querySelector('.activity-list');
  if (activityList) {
    const sampleActivities = [
      { label: 'PLEASE', time: 'just now' },
      { label: 'SORRY', time: '1 min ago' },
      { label: 'GOOD', time: '3 min ago' },
      { label: 'HELLO', time: '5 min ago' },
      { label: 'THANK YOU', time: '7 min ago' }
    ];

    function addActivity(activity) {
      const item = document.createElement('div');
      item.className = 'activity-item';
      item.innerHTML = `
        <div class="activity-icon">${activity.label[0]}</div>
        <div class="activity-details">
          ${activity.label}
          <span>${activity.time}</span>
        </div>
      `;
      item.style.animation = 'slideDown 0.3s ease-out';
      activityList.insertBefore(item, activityList.firstChild);
      if (activityList.children.length > 6) {
        activityList.removeChild(activityList.lastChild);
      }
    }

    // Add new activity every ~8 seconds
    setInterval(() => {
      const random = sampleActivities[Math.floor(Math.random() * sampleActivities.length)];
      addActivity({ ...random, time: 'just now' });
    }, 8000);
  }

  // Simple chart hover effect
  document.querySelectorAll('.bar').forEach(bar => {
    bar.addEventListener('mouseenter', () => {
      bar.style.opacity = '0.8';
    });
    bar.addEventListener('mouseleave', () => {
      bar.style.opacity = '1';
    });
  });

  // Update last detected time
  const lastDetected = document.querySelector('.status-list li:last-child');
  if (lastDetected) {
    let minutes = 2;
    setInterval(() => {
      minutes++;
      lastDetected.textContent = `Last Detected: ${minutes}m ago`;
    }, 60000);
  }
});

// Add slideUp animation for bars
const style = document.createElement('style');
style.textContent = `
  @keyframes slideUp {
    from {
      transform: translateY(10px);
      opacity: 0;
    }
    to {
      transform: translateY(0);
      opacity: 1;
    }
  }
`;
document.head.appendChild(style);
