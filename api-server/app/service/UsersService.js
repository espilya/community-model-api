'use strict';
const db = require("../models");
const CommunityDAO = db.communities;


/**
 * Communities that a user belongs
 * Returns a list with the ids of the communities that the user belongs to
 *
 * userId Long ID of user
 * returns List
 **/
exports.listUserCommunities = function(userId) {
  return new Promise(function(resolve, reject) {
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


/**
 * Update community model with new users
 * This service is employed to inform the Community Model the users who where created/updated in the User Model
 *
 * body List User generated content object that will be added to the model
 * no response value expected for this operation
 **/
exports.updateUsers = function(body) {
  return new Promise(function(resolve, reject) {
    // TODO Notify communy model app
    resolve();
  });
}

