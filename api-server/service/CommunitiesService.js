'use strict';
const db = require("../models");
const CommunityDAO = db.communities;

/**
* Communities in the model
* Access to a list of the communities in the community model
*
* returns List
**/
exports.getCommunities = function() {
  return new Promise(function(resolve, reject) {
    let result = {};

    CommunityDAO.all( (communities) => {
      result['application/json'] = communities;
      console.log(result);
      if (Object.keys(result).length > 0) {
        resolve(result[Object.keys(result)[0]]);
      } else {
        resolve();
      }   
    });
  });

}


/**
* community description and explanation
* Returns information about a community
*
* communityId Long ID of community to return
* returns community
**/
exports.getCommunityById = function(communityId) {
  return new Promise(function(resolve, reject) {
    let result = {};
    CommunityDAO.getById(communityId, 
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
      });    
  });  
};


/**
* Users who belong to a community
* Returns a list with the ids of the users who belong to a community
*
* communityId Long ID of community to return
* returns List
**/
exports.listCommunityUsers = function(communityId) {
  return new Promise(function(resolve, reject) {
    let result = {};
    CommunityDAO.getById(communityId, 
      data => {
        result['application/json'] = data.users;
        if (Object.keys(result).length > 0) {
          resolve(result[Object.keys(result)[0]]);
        } else {
          resolve();
        }
      },
      error => {
        reject(error);
      });    
  });  


  // return new Promise(function(resolve, reject) {
  //   var examples = {};
  //   examples['application/json'] = [ "d290f1ee-6c54-4b01-90e6-d701748f0851", "d290f1ee-6c54-4b01-90e6-d701748f0851" ];
  //   if (Object.keys(examples).length > 0) {
  //     resolve(examples[Object.keys(examples)[0]]);
  //   } else {
  //     resolve();
  //   }
  // });
}

