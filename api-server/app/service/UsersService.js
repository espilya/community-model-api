'use strict';
const db = require("../models");
const CommunityDAO = db.communities;
const UsersDAO = db.users;

/**
 * Communities that a user belongs
 * Returns a list with the ids of the communities that the user belongs to
 *
 * userId Long ID of user
 * returns List
 **/
exports.listUserCommunities = function (userId) {
  return new Promise(function (resolve, reject) {
    let result = {};
    CommunityDAO.allWithUserId(userId,
      data => {
        // Response only includes ids
        result['application/json'] = data.map(c => c.id);
        if (Object.keys(result).length > 0) {
          resolve(result[Object.keys(result)[0]]);
        } else {
          resolve();
        }
      },
      error => {
        reject(error);
      }
    );
  });
}

const http = require('http');
/**
 * Update community model with new users
 * This service is employed to inform the Community Model the users who where created/updated in the User Model
 *
 * body List User generated content object that will be added to the model
 * no response value expected for this operation
 **/
exports.updateUsers = function (body) {
  return new Promise(function (resolve, reject) {
    var user = JSON.stringify(body)

    const options = {
      hostname: 'host.docker.internal',
      port: 8090,
      path: '/updateUsers',
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
        resolve()
      })

      var myStatus = req.status;
      if(myStatus >= 400){
        req.on('error', (err) =>{
          console.error(err);
        })
        reject()
      }
      // else{
      //   console.error("ok");
      //   resolve()
      // }
    });

    req.write(user);
    req.end();

    req.on('error', (err) =>{
      console.error(err);
      reject()
    })

  });
}

