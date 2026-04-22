document.addEventListener('DOMContentLoaded', () => {
  const recognizedText = document.getElementById('recognized-text');
  const confidenceValue = document.getElementById('confidence-value');
  const gestureValue = document.getElementById('gesture-value');
  const videoFeed = document.getElementById('video-feed');

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

  // Poll for recognition results
  let lastGesture = '';
  let lastConfidence = 0;

  function fetchRecognitionResults() {
    fetch('/recognition_results')
      .then(response => response.json())
      .then(data => {
        if (data.gesture && data.confidence) {
          // Only update if there's a meaningful change
          if (data.gesture !== lastGesture || Math.abs(data.confidence - lastConfidence) > 5) {
            recognizedText.textContent = data.gesture;
            confidenceValue.textContent = `${data.confidence}%`;
            gestureValue.textContent = data.gesture;
            
            // Add animation class for new recognition
            recognizedText.style.animation = 'none';
            setTimeout(() => {
              recognizedText.style.animation = 'fadeIn 0.4s ease-out';
            }, 10);
            
            lastGesture = data.gesture;
            lastConfidence = data.confidence;
          }
        }
      })
      .catch(error => {
        console.error('Error fetching recognition results:', error);
      });
  }

  // Poll every 100ms for real-time updates
  setInterval(fetchRecognitionResults, 100);

  // Handle video feed errors
  videoFeed.addEventListener('error', () => {
    recognizedText.textContent = 'Camera Error';
    confidenceValue.textContent = '0%';
    gestureValue.textContent = 'Error';
  });

  // Initial fetch
  fetchRecognitionResults();
});
