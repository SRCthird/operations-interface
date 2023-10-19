import express  from 'express';
import fs from 'fs';
import path from 'path';
import graph, { Client } from '@microsoft/microsoft-graph-client';
import axios from 'axios';

import config from './private.json';

/** Initialized Express App*/ 
const app = express();
const PORT = 5000;
const STATIC_DIR = path.join(__dirname, 'static');

// Define middleware
app.use(express.json());
app.use('/static', express.static(STATIC_DIR));

// Set static routes
app.use('/static', express.static(STATIC_DIR));
app.use('/static/pfp', express.static(path.join(STATIC_DIR, 'pfp')));

const getAuthenticatedClient = (accessToken: string) => {
  return Client.init({
      authProvider: (done) => {
          done(null, accessToken);
      },
  });
}

/**
 * Root endpoint for the backend API
 * 
 * @test curl -X POST -H "Content-Type: application/json" -d "{\"key\":\"value\"}" http://localhost:5000/api
 * @param {string} key - The key to use for authentication, found in private.json
 */
app.post('/api', (req, res) => {
  const key = req.body.key;
  if (!key || key !== config.key) { // If key doesn't exist or is incorrect, status is 401 (Unauthorized)
    return res.status(401).send('Key Not Accepted');
  }
  res.send('Key Accepted');
});

/**
 * Endpoint for getting the current user's profile information
 * 
 * @test curl -X POST -H "Content-Type: application/json" -d "{\"key\":\"value\", \"token\":\"value\"}" http://localhost:5000/api/me
 * @param {string} key - The key to use for authentication, found in private.json
 * @param {string} token - The AAD token to use for user authentication.
 */
app.post('/api/me', async (req, res) => {
  const key = req.body.key;
  if (!key || key !== config.key) {
    return res.status(401).send('Key Not Accepted');
  }
  const userToken = req.body.token;
  if (!userToken) {
      return res.status(400).send('Token not provided');
  }

  try {
      const client = getAuthenticatedClient(userToken);

      const user = await client.api('/me').get();
      res.json(user);
  } catch (error: any) {
      res.status(500).send(error.message);
  }
});

/**
 * Endpoint for getting the current user's profile picture
 * 
 * @test curl -X POST -H "Content-Type: application/json" -d "{\"key\":\"value\", \"token\":\"value\"}" -o picture.jpg http://localhost:5000/api/me
 * @param {string} key - The key to use for authentication, found in private.json
 * @param {string} token - The AAD token to use for user authentication.
 */
app.post('/api/me/photo', async (req, res) => {
  const key = req.body.key;
  if (!key || key !== config.key) {
    return res.status(401).send('Key Not Accepted');
  }
  const userToken = req.body.token;
  if (!userToken) {
      return res.status(400).send('Token not provided');
  }
  
  try {
      const client = getAuthenticatedClient(userToken);

      const user = await client
        .api('/me')
        .version('beta')
        .get();

      const profileImageUrl = 'https://graph.microsoft.com/v1.0/me/photo/$value';
      const targetDirectory = 'static/profiles';
      const targetFilePath = path.join(targetDirectory, `${user.mailNickname}.jpeg`);

      if (!fs.existsSync(targetDirectory)){
          fs.mkdirSync(targetDirectory, { recursive: true });
      }

      axios.get(profileImageUrl, {
        responseType: 'arraybuffer',
        headers: {
            'Authorization': `Bearer ${userToken}`
        }
      })
      .then(response => {
          const buffer = Buffer.from(response.data, 'binary');
          fs.writeFile(targetFilePath, buffer, (err) => {
              if (err) {
                  console.error('Error saving the image:', err);
                  return;
              }
              console.log(`${user.displayName} saved profile picture to ${targetFilePath}`);
          });
      })
      .catch(error => {
          console.error('Error fetching image:', error);
      });

      res.status(200).send(`/static/profile/${user.mailNickname}.jpeg`);

  } catch (error: any) {
      res.status(500).send(error.message);
  }
});


app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
