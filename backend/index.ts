import express  from 'express';
import bodyParser from 'body-parser';

import config from './private.json';

/** Initialized Express App*/ 
const app = express();
const PORT = 3000;

app.use(bodyParser.json());

/**
 * Root endpoint for the backend API
 * 
 * @test curl -X POST -H "Content-Type: application/json" -d "{\"key\":\"value\"}" http://localhost:3000
 * @param {string} key - The key to use for authentication, found in private.json
 */
app.post('/', (req, res) => {
  const key = req.body.key || "";
  if (!key || key !== config.key) {
    res.send('Hello, Express!');
  } else {
    res.send('<h1>Key Accepted</h1>');
  }
});

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
