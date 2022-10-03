// postUpdateCM.js
// ========
/**
 * Sends a POST request to api_loader.py to update CM clustering 
 */

const http = require('http');

module.exports = {
    post_data: function (body, path) {
        return new Promise(function (resolve, reject) {
            var data = JSON.stringify(body)
            const options = {
                // hostname: '172.20.0.4',
                host: '172.20.0.4',
                port: process.env.CM_DOCKER_PORT || 8090,
                path: path,
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': data.length,
                },
            };

            const req = http.request(options, res => {
                res.on('data', d => {
                    process.stdout.write(d);
                });

                res.on('end', () => {
                    resolve()
                })

                var myStatus = req.status;
                if (myStatus >= 400) {
                    req.on('error', (err) => {
                        console.error(err);
                    })
                    reject()
                }
            });

            req.write(data);
            req.end();

            req.on('error', (err) => {
                console.error(err);
                reject()
            })
        });
    }
};