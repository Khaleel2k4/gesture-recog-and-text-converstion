document.addEventListener('DOMContentLoaded', () => {
  const saveBtn = document.getElementById('save-settings');
  const resetBtn = document.getElementById('reset-settings');

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

  // Load saved settings from localStorage (mock)
  function loadSettings() {
    const stored = localStorage.getItem('signspeak-settings');
    if (stored) {
      const settings = JSON.parse(stored);
      document.getElementById('username').value = settings.username || 'nagamjyothi691@gmail.com';
      document.getElementById('email').value = settings.email || 'nagamjyothi691@gmail.com';
      document.getElementById('language').value = settings.language || 'en';
      document.getElementById('theme').value = settings.theme || 'dark';
      document.getElementById('email-notifications').checked = settings.emailNotifications ?? true;
      document.getElementById('push-notifications').checked = settings.pushNotifications ?? false;
      document.getElementById('sensitivity').value = settings.sensitivity || 7;
      document.getElementById('camera').value = settings.camera || '0';
      document.getElementById('video-quality').value = settings.videoQuality || 'medium';
      document.getElementById('share-data').checked = settings.shareData ?? false;
      document.getElementById('save-history').checked = settings.saveHistory ?? true;
    }
  }

  // Save settings to localStorage (mock)
  function saveSettings() {
    const settings = {
      username: document.getElementById('username').value,
      email: document.getElementById('email').value,
      language: document.getElementById('language').value,
      theme: document.getElementById('theme').value,
      emailNotifications: document.getElementById('email-notifications').checked,
      pushNotifications: document.getElementById('push-notifications').checked,
      sensitivity: document.getElementById('sensitivity').value,
      camera: document.getElementById('camera').value,
      videoQuality: document.getElementById('video-quality').value,
      shareData: document.getElementById('share-data').checked,
      saveHistory: document.getElementById('save-history').checked,
    };
    localStorage.setItem('signspeak-settings', JSON.stringify(settings));
    showToast('Settings saved successfully!', 'success');
  }

  // Reset to defaults
  function resetSettings() {
    localStorage.removeItem('signspeak-settings');
    document.getElementById('username').value = 'nagamjyothi691@gmail.com';
    document.getElementById('email').value = 'nagamjyothi691@gmail.com';
    document.getElementById('language').value = 'en';
    document.getElementById('theme').value = 'dark';
    document.getElementById('email-notifications').checked = true;
    document.getElementById('push-notifications').checked = false;
    document.getElementById('sensitivity').value = 7;
    document.getElementById('camera').value = '0';
    document.getElementById('video-quality').value = 'medium';
    document.getElementById('share-data').checked = false;
    document.getElementById('save-history').checked = true;
    showToast('Settings reset to defaults', 'info');
  }

  // Simple toast notification
  function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      padding: 12px 20px;
      border-radius: 8px;
      color: white;
      font-size: 14px;
      z-index: 1000;
      animation: slideInRight 0.3s ease-out;
      background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#6b67ff'};
    `;
    document.body.appendChild(toast);
    setTimeout(() => {
      toast.style.animation = 'slideOutRight 0.3s ease-out';
      setTimeout(() => toast.remove(), 300);
    }, 3000);
  }

  // Add toast animations
  const style = document.createElement('style');
  style.textContent = `
    @keyframes slideInRight {
      from { transform: translateX(100%); opacity: 0; }
      to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
      from { transform: translateX(0); opacity: 1; }
      to { transform: translateX(100%); opacity: 0; }
    }
  `;
  document.head.appendChild(style);

  // Event listeners
  saveBtn.addEventListener('click', saveSettings);
  resetBtn.addEventListener('click', resetSettings);

  // Initial load
  loadSettings();
});
