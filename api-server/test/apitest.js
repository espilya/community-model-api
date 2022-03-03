const server = require("../app/server.js");
if (!server) {
    console.error("Unable to load server");
    
}
else {
    server.run().catch(console.error)
    .then(testCommunities); 
}

function testCommunities() {
    // Test
    require("dotenv").config();
    const axios = require('axios').default;
    const url = "http://localhost:"+ process.env.NODE_DOCKER_PORT;
    axios.get(url+'/communities')
    .then(function (response) {
        // handle success
        console.log(response);
    })
    .catch(function (error) {
        // handle error
        console.log(error);
    });
}
