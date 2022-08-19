// post.js
// ========

const http = require('http');

module.exports = {
    update_CM: function () {
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
              process.stdout.write(d);
            });
      
            res.on('end', () =>{
              // console.log("_end_");
            })
      
            var myStatus = req.status;
            if(myStatus >= 400){
              req.on('error', (err) =>{
                console.error(err);
              })
            }
          });
      
          req.write(user);
          req.end();
      
          req.on('error', (err) =>{
            console.error(err);
          })
    }
  };
  
