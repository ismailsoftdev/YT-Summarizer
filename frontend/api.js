function summarizeVideo() {
    const videoUrl = document.getElementById('video-url').value
    const data = { video_url: videoUrl }
    fetch('http://127.0.0.1:5000/summarize', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(data => {
        const summary = data.summary.join('<br/><br/>')
        const result = document.getElementById('result')
        const summaryElement = document.getElementById('summary')
        summaryElement.innerHTML = summary
        result.classList.remove('hidden')
      })
  }