const request = require('supertest');
const assert = require('assert');
let app = {};
beforeAll(()=>{
    return new Promise(function(resolve, reject) {
        const server = require("../app/server.js");
        if (!server) {
            console.error("Unable to load server");    
        }
        else {
            app = server.test((theApp)=> {
                app =theApp;
                resolve();
            }).catch(console.error);
        }
    });
});


describe ("Test example", ()=>{
    test ("GET /communities", (done)=>{
        request(app)
            .get('/communities')
            .expect('Content-Type', /json/)
            .expect(200)
            .end(function(err, res) {
                if (err) throw err;
                return done();
            });
    });
});


