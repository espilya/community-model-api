/**
 * Controller for COMMUNITIES endpoint.
 * The controller checks some parameter values in the request,
 * it delegates in CommunitiesService to run the corresponding function
 * and generates the corresponding responese
 */

// Name of the commmunityId parameter in the request
const idParam = 'communityId';
const Communities = require('../service/CommunitiesService.js');

/**
 * Method for resolving GET /communities/
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.getCommunities = function getCommunities (req, res, next) {
  Communities.getCommunities()
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.send(response);
    });
};

/**
 * Method for resolving GET /communities/{communityId}
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.getCommunityById = function getCommunityById (req, res, next) {
  const communityId = req.params[idParam];
  Communities.getCommunityById(communityId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid community id");
    });
};

/**
 * Method for resolving GET /communities/{communityId}/users
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.listCommunityUsers = function listCommunityUsers (req, res, next) {
  const communityId = req.params[idParam];
  Communities.listCommunityUsers(communityId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid community id");
    });
};
