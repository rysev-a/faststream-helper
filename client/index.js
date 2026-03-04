document.getElementById('load-projects').addEventListener('click', () => {
  const correlationID = uuidv4();

  fetch('/projects/', {
    headers: {
      'correlation-id': correlationID
    }
  }).then(r => r.json()).then(data => {
    document.getElementById('correlation-id').innerHTML = correlationID;
    document.getElementById('data-view').innerHTML = JSON.stringify(data, null, 2)
  })
})
