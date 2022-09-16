// post.js
// ========
/**
 * Sends a POST request to api_loader.py to update CM clustering 
 */

const http = require('http');

function oldPost() {
  var user = "hi"
  const options = {
    hostname: 'host.docker.internal',
    port: 8090,
    path: '/update_CM',
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Content-Length': user.length,
    },
  };
  const req = http.request(options, res => {

    res.on('data', d => {
      console.log(req.status)
      if (req.status != 102) {
        process.stdout.write(d);
        console.log(`BODY: ${d}`);
      }
    });

    res.on('end', () => {
      console.log("_end_");
    })

    var myStatus = req.status;
    if (myStatus >= 400) {
      req.on('error', (err) => {
        console.error(err);
      })
    }
    else if (myStatus == 102) {
      console.log("Received 102 Processing Status Code. Waiting...");
    }
    else if (myStatus == 200) {
      console.log("Received 200. OK.");
    }
  });

  req.write(user);
  req.end();

  req.on('error', (err) => {
    console.error("error");
    console.error(err);
  })
}


module.exports = {
  update_CM: function () {
    oldPost()
  }
};