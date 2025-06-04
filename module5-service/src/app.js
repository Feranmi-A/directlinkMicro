const express = require('express');
const app     = express();
const PORT    = 3000;

app.get('/', (req, res) => {
  res.send(`
    <h1>Module 5 Service</h1>
    <p>This is a placeholder front end for Module 5.</p>
    <p><a href="http://localhost:3000/">← Back to Portfolio</a></p>
  `);
});

app.get('/api/v1/info', (req, res) => {
  res.json({ name: "Module 5 Service", description: "React + Node.js + MongoDB" });
});

app.listen(PORT, () => console.log(\`Module5 listening on port \${PORT}\`));
