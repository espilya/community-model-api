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
*
* perspectiveId Long ID of perspective to return
* returns perspective
**/
exports.getPerspectiveById = function (perspectiveId) {
  return new Promise(function (resolve, reject) {

    let result = {};
    PerspectiveDAO.getById(perspectiveId,
      data => {
        // console.log(data)
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
* Returns list with communities that have the same perspectiveId
*
* perspectiveId Long ID of perspective 
* returns List
**/
exports.listPerspectiveCommunities = function (perspectiveId) {
  return new Promise(function (resolve, reject) {
    // obtains all communities and then filter them by perspectiveId
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
        if (community.perspectiveId == perspectiveId) {
          data.push(community);
        }
      }
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
// TODO: devolver error si la dao no pudo meterla 

/**
 * Redirects POST request to api_loader
 * Used to inform the community model about new perspectives 
 * 
 * no response value expected for this operation
 */
exports.PostPerspective = function (body) {
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
        console.log(`BODY: ${d}`);
        process.stdout.write(d);
      });

      res.on('end', () => {
        console.log("_end_");
        resolve()
      })

      var myStatus = req.status;
      if (myStatus >= 400) {
        req.on('error', (err) => {
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

    req.on('error', (err) => {
      console.error(err);
      reject()
    })

  });
}