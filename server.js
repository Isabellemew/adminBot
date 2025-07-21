const express = require('express');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
const PORT = 3000;
const TOKEN = '7257032872:AAGrW1dPt1T-Rh3BhDX3Xvtk0_fK3OXHrNo'; // Replace with your token
const ANNOUNCE_FILE = path.join(__dirname, 'announcements.json');

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// Main admin page
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// Add announcement
app.post('/add', (req, res) => {
  const { announcement } = req.body;
  if (!announcement) return res.status(400).send('No announcement text');
  let announcements = [];
  if (fs.existsSync(ANNOUNCE_FILE)) {
    announcements = JSON.parse(fs.readFileSync(ANNOUNCE_FILE));
  }
  announcements.push({ text: announcement, date: new Date().toISOString() });
  fs.writeFileSync(ANNOUNCE_FILE, JSON.stringify(announcements, null, 2));
  res.redirect('/');
});

// API to get announcements
app.get('/api/announcements', (req, res) => {
  const token = req.query.token;
  if (token !== TOKEN) return res.status(403).send('Forbidden');
  let announcements = [];
  if (fs.existsSync(ANNOUNCE_FILE)) {
    announcements = JSON.parse(fs.readFileSync(ANNOUNCE_FILE));
  }
  res.json(announcements);
});

app.listen(PORT, () => {
  console.log(`Admin panel running on http://localhost:${PORT}`);
});
