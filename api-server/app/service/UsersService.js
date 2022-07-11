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


/**
 * Update community model with new users
 * This service is employed to inform the Community Model the users who where created/updated in the User Model
 *
 * body List User generated content object that will be added to the model
 * no response value expected for this operation
 **/
exports.updateUsers = function (body) {
  return new Promise(function (resolve, reject) {
    // try {
      UsersDAO.update(body,
        data => {
          resolve();
        },
        error => {
          reject(error);
        }
      );
        // } catch (error) {
      // console.error(error);
    // }

    // try {
    //   console.log(body);
    //   console.log("_1_");
    //   let data = body;
    //   fetch("http://localhost:8090/", {
    //     method: "POST",
    //     headers: {'Content-Type': 'application/json'}, 
    //     body: JSON.stringify(data)
    //   }).then(res => {
    //     console.log("Request complete! response:", res);
    //   });
    //   console.log("_2_");
    // } catch (error) {
    //   console.error(error);
    // }

  });
}

