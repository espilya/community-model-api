
require("dotenv").config();
const axios = require('axios').default;
const server = require("../app/server.js");
if (!server) {
    console.error("Unable to load server");    
}
else {
    server.run(testCommunities).catch(console.error);
}

function testCommunities() {
    const url = "http://localhost:"+ process.env.NODE_DOCKER_PORT;
    console.log("Testing /communities");
    axios.get(url+'/communities')
    .then(function (response) {
        // handle success
        console.log("OK:", response.status, response.data);
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    })
    .then( function () {
        console.log("Exit tests");
        process.exit(0);
    } );
}

