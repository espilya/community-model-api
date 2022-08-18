'use strict';
const db = require("../models");
const PerspectiveDAO = db.perspectives;
const CommunityDAO = db.communities;


/**
* Perspectives in the model
* Access to a list of the Perspectives
*
* returns List
**/
exports.getPerspectives = function () {
  return new Promise(function (resolve, reject) {
    let result = {};
    PerspectiveDAO.all((perspectives) => {
      result['application/json'] = perspectives;
      if (Object.keys(result).length > 0) {
        resolve(result[Object.keys(result)[0]]);
      } else {
        resolve();
      }
    });
  });

};


/**
* Returns information about a perspective
**/
exports.getPerspectiveById = function (perspectiveId) {
  return new Promise(function (resolve, reject) {
    let result = {};
    PerspectiveDAO.getById(perspectiveId,
      data => {
        result['application/json'] = data;
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
};


/**
* Users who belong to a community
* Returns a list with the ids of the users who belong to a community
*
* communityId Long ID of community to return
* returns List
**/
exports.listPerspectiveCommunities = function (perspectiveId) {
  return new Promise(function (resolve, reject) {
    let result = {};
    let data = []
    let communities = {};
    CommunityDAO.all((com) => {
      communities = com;
      if (communities.length == 0) {
        resolve();
      }

      for (var i = 0; i < communities.length; i++) {
        var community = communities[i]
        console.log(community);
        if (community.perspectiveId == perspectiveId) {
          data.push(community);
        }
      }
      console.log("data:");
      console.log(data);
      // communities.forEach(element => {
      //   var community = JSON.parse(element);
      //   console.log(community);
      //   if (community.perspective == perspectiveId) {
      //     data.push(communities);
      //   }
      // });

      result['application/json'] = data;
      if (Object.keys(result).length > 0) {
        resolve(result[Object.keys(result)[0]]);
      } else {
        resolve();
      }
    });

  });
};


const http = require('http');
/**
 * Update community model with new users
 * This service is employed to inform the Community Model the users who where created/updated in the User Model
 *
 * body List User generated content object that will be added to the model
 * no response value expected for this operation
 **/
exports.perspectivePOST = function (body) {
  return new Promise(function (resolve, reject) {
    var user = JSON.stringify(body)
    
    const options = {
      hostname: 'host.docker.internal',
      port: 8090,
      path: '/perspective',
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