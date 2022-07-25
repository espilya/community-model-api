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
    });

    if (communities.length == 0) {
      resolve();
    }

    communities.forEach(function (community, i, array) {
      if(community[i].perspective == perspectiveId){
        data.push(communities)
      }
    });

    result['application/json'] = data;
        if (Object.keys(result).length > 0) {
          resolve(result[Object.keys(result)[0]]);
        } else {
          resolve();
        }
        
  });
};

