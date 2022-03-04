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


describe ("Test communities endpoint", ()=>{
    test ("GET /communities", (done)=>{
        request(app)
            .get('/communities')
            .expect('Content-Type', /json/)
            .expect(200)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
    test ("GET /communities/{id}/users", (done)=>{
        request(app)
            .get('/communities/621e53cf0aa6aa7517c2afdd/users')
            .expect('Content-Type', /json/)
            .expect(200)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
    test ("GET /communities/BAD_id/users", (done)=>{
        request(app)
            .get('/communities/wrongId/users')
            .expect(400)
            .end(function(err, res) {
                if (err) throw err;
                return done();
            });
    });
    test ("GET /communities/{id}", (done)=>{
        request(app)
            .get('/communities/621e53cf0aa6aa7517c2afdd/users')
            .expect('Content-Type', /json/)
            .expect(200)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
    test ("GET /communities/BAD_id", (done)=>{
        request(app)
            .get('/communities/wrongId')
            .expect(400)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
});

describe ("Test users endpoint", ()=>{
    test ("GET /users/{user-id}/communities", (done)=>{
        request(app)
            .get('/users/821e53cf0aa6aa7517c2afdd/communities')
            .expect('Content-Type', /json/)
            .expect(200)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
    // test ("POST /users/user-generated-content", (done)=>{
    //     request(app)
    //         .post('/users/user-generated-content')
    //         .expect(204)
    //         .end(function(err, res) {
        // if (err) return done(err);
        // return done();
    //         });
    // });
    // test ("GET /users/{BADUSERID}/communities", (done)=>{
    //     request(app)
    //         .get('/communities/wrongId/users')
    //         .expect(400)
    //         .end(function(err, res) {
        // if (err) return done(err);
        // return done();
    //         });
    // });
});

describe ("Test similarity endpoint", ()=>{
    test ("GET /communities/{community-id}/similarity", (done)=>{
        request(app)
            .get('/communities/821e53cf0aa6aa7517c2afdd/similarity')
            .query({ k: '2' })
            .expect('Content-Type', /json/)
            .expect(200)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
    test ("GET /communities/{community-id}/similarity NO QUERY PARAMETER", (done)=>{
        request(app)
            .get('/communities/821e53cf0aa6aa7517c2afdd/similarity')
            .expect(400)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
    test ("GET /communities/{BADCOMMUNITYID}/similarity", (done)=>{
        request(app)
            .get('/communities/badId/similarity')
            .query({ k: '2' })
            .expect(400)
            .end(function(err, res) {
                if (err) return done(err);
                return done();
            });
    });
});

