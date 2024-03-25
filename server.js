const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000; // You can choose any port that's available
const jsonDictionaryPath = path.join(__dirname, 'json_dictionary');
// Enable CORS for all routes
app.use(cors());

app.get('/word/:word', (req, res) => {
    const word = req.params.word;
    const subdirectory = word.substring(0, 1); // First letter
    const subsubdirectory = word.length > 1 ? word.substring(0, 2) : 'a'; // First two letters or 'a' if word has only one letter
    const filePath = path.join(jsonDictionaryPath, subdirectory, subsubdirectory, `${word}.json`);

    fs.readFile(filePath, (err, data) => {
        if (err) {
            return res.status(404).send({ error: 'Word not found.' });
        }
        res.type('application/json');
        res.send(data);
    });
});

app.get('/data', (req, res) => {
  res.json({ message: "Hello, Sqirld!" });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});