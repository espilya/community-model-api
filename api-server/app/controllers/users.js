/**
 * Controller for USER endpoint.
 * The controller checks some parameter values in the request,
 * it delegates in UsersService to run the corresponding function
 * and generates the corresponding responese
 */
const Users = require('../service/UsersService.js');
const userParam = 'userId';

/**
 * Method for resolving POST /users/{userId}/update-generated-content
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.updateUsers = function updateUsers (req, res, next) {
  let paramUserId = req.params[userParam];
  // Check if the userid in the url and in every object in the list contained in the body are the same
  if (req.body.every( (ugc) => ugc.userid === paramUserId )) {
    Users.updateUsers(req.body)
    .then(function (response) {
      res.status(204);
      res.send(response);
    })
    .catch(function (response) {
      res.send(response);
    });
  } else {
    res.status(400).send("Invalid userId: userId URL differs form the userid in the body request");
  }

};

/**
 * Method for resolving GET /users/{userId}/communities
 * @param {Object} req Request
 * @param {Object} res Response
 */
module.exports.listUserCommunities = function listUserCommunities (req, res) {
  const userId = req.params[userParam];
  Users.listUserCommunities(userId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid user id");
    });
};
