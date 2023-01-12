var express = require('express'); // Express web server framework
var request = require('request'); // "Request" library
var querystring = require('querystring');
const port = 8080;

var client_id = '0a9306c3f71745a29297ebf24323992a';
var redirect_uri = 'http://localhost:8080/callback';

var app = express();

app.get('/login', function(req, res) {

  var state = generateRandomString(16);
  var scope = 'user-read-private user-read-email';

  res.redirect('https://accounts.spotify.com/authorize?' +
    querystring.stringify({
      response_type: 'code',
      client_id: client_id,
      scope: scope,
      redirect_uri: redirect_uri,
      state: state
    }));
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
})