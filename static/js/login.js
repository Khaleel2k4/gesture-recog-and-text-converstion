document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('form');
  const usernameInput = document.querySelector('input[name="username"]');
  const passwordInput = document.querySelector('input[name="password"]');
  const submitBtn = document.querySelector('.btn');

  // Simple client-side validation hints
  function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(String(email).toLowerCase());
  }

  function checkInputs() {
    const username = usernameInput.value.trim();
    const password = passwordInput.value.trim();
    let valid = true;

    // Clear previous states
    usernameInput.style.borderColor = '';
    passwordInput.style.borderColor = '';

    if (!username) {
      usernameInput.style.borderColor = '#ef4444';
      valid = false;
    } else if (!validateEmail(username)) {
      usernameInput.style.borderColor = '#f59e0b';
    }

    if (!password || password.length < 3) {
      passwordInput.style.borderColor = '#ef4444';
      valid = false;
    }

    submitBtn.disabled = !valid;
  }

  usernameInput.addEventListener('input', checkInputs);
  passwordInput.addEventListener('input', checkInputs);

  // Prevent double-submit
  let submitting = false;
  form.addEventListener('submit', (e) => {
    if (submitting) {
      e.preventDefault();
      return;
    }
    submitting = true;
    submitBtn.textContent = 'Logging in...';
    submitBtn.disabled = true;

    // Optional: show spinner (you can add a spinner element)
    setTimeout(() => {
      submitting = false;
      submitBtn.textContent = 'Log in to SignSpeak';
    }, 5000);
  });

  // Focus first field on load
  usernameInput.focus();
});
