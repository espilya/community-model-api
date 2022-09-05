// post.js
// ========

const http = require('http');
const axios = require('axios');



  // var user = "hi"
  // const options = {
  //     hostname: 'host.docker.internal',
  //     port: 8090,
  //     path: '/update_CM',
  //     method: 'POST',
  //     headers: {
  //       'Content-Type': 'application/json',
  //       'Content-Length': user.length,
  //     },
  //   };
  //   const req = http.request(options, res => {

  //     res.on('data', d => {
  //       process.stdout.write(d);
  //     });

  //     res.on('end', () =>{
  //       // console.log("_end_");
  //     })

  //     var myStatus = req.status;
  //     if(myStatus >= 400){
  //       req.on('error', (err) =>{
  //         console.error(err);
  //       })
  //     }
  //   });

  //   req.write(user);
  //   req.end();

  //   req.on('error', (err) =>{
  //     console.error(err);
  //   })
// }



function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


function oldPost(){
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
        if(req.status != 102){
          process.stdout.write(d);
          console.log(`BODY: ${d}`);
        }
      });

      res.on('end', () =>{
        console.log("_end_");
      })

      var myStatus = req.status;
      if(myStatus >= 400){
        req.on('error', (err) =>{
          console.error(err);
        })
      }
      else if(myStatus == 102){
        console.log("Received 102 Processing Status Code. Waiting...");
      }
      else if(myStatus == 200){
        console.log("Received 200. OK.");
      }
    });

    req.write(user);
    req.end();

    req.on('error', (err) =>{
      console.error("error");
      console.error(err);
    })
}

async function postData(url = '', data = "hi") {
  // Default options are marked with *
  // const response = await fetch(url, {
  //   method: 'POST', // *GET, POST, PUT, DELETE, etc.
  //   mode: 'no-cors', // no-cors, *cors, same-origin
  //   cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
  //   credentials: 'include', // include, *same-origin, omit
  //   headers: {
  //     'Content-Type': 'text/plain'
  //     // 'Content-Type': 'application/x-www-form-urlencoded',
  //   },
  //   redirect: 'follow', // manual, *follow, error
  //   referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
  //   body: data // body data type must match "Content-Type" header
  // });

}

module.exports = {
    update_CM:  function () {
      oldPost()
    }
  };