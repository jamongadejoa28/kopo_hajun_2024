const express = require('express');
const app = express();
const port = 80; // port number - ncp에서 열었던 포트 번호

app.get('/main', (req, res) => {
  res.sendfile('main.html');
});

app.get('/main2', (req, res) => {
  res.sendfile('main2.html');
});

app.get('/369game', (req, res) => {
  res.sendfile('369game.html');
});


app.listen(port, () => {
  console.log(`Example app listening on port ${port}`);
});
