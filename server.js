const express = require('express');
const fetch = require('node-fetch'); // Install with: npm install node-fetch

const app = express();
const port = 3000;

// Serve the index.html file
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'index.html'));
});

// A new endpoint to fetch example.com's HTML
app.get('/fetch-html', async (req, res) => {
  try {
    const response = await fetch('https://www.example.com');
    const data = await response.text();
    res.send(data);
  } catch (error) {
    console.error('Error fetching HTML:', error);
    res.status(500).send('Error fetching HTML');
  }
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
