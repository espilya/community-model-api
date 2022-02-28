'use strict';


/**
 * Communities that a user belongs
 * Returns a list with the ids of the communities that the user belongs to
 *
 * userId Long ID of user
 * returns List
 **/
exports.listUserCommunities = function(userId) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ "d290f1ee-6c54-4b01-90e6-d701748f0851", "d290f1ee-6c54-4b01-90e6-d701748f0851" ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
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
    resolve();
  });
}

