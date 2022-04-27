/**
 * Controller for SIMILARITY endpoint.
 * The controller checks some parameter values in the request,
 * it delegates in SimilarityService to run the corresponding function
 * and generates the corresponding responese
 */
const Similarity = require('../service/SimilarityService.js');

// Name of the commmunityId and otherCommunityId parameters in the request
const idParam = 'communityId';
const otherIdParam = 'otherCommunityId';

/**
 * Method for resolving GET /communities/{communityId}/dissimilarity/{otherCommunityId}
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.computeDissimilarity = function computeDissimilarity (req, res, next) {
  const communityId = req.params[idParam];
  const otherCommunityId = req.params[otherIdParam];
  Similarity.computeDissimilarity(communityId, otherCommunityId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("Invalid communityIds (target or other)");
    });
};

/**
 * Method for resolving GET /communities/{communityId}/dissimilarity/
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.computeKmostDissimilar = function computeKmostDissimilar (req, res, next) {
  const communityId = req.params[idParam];
  const k = req.query['k'];
  Similarity.computeKmostDissimilar(communityId, k)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("Invalid communityId or query parameters");
    });
};

/**
 * Method for resolving GET /communities/{communityId}/similarity/
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.computeKmostSimilar = function computeKmostSimilar (req, res, next) {
  const communityId = req.params[idParam];
  const k = req.query['k'];
  Similarity.computeKmostSimilar(communityId, k)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("Invalid communityId or query parameters");
    });
};

/**
 * Method for resolving GET /communities/{communityId}/similarity/{otherCommunityId}
 * @param {Object} req Request
 * @param {Object} res Response
 * @param {Object} next 
 */
module.exports.computeSimilarity = function computeSimilarity (req, res, next) {
  const communityId = req.params[idParam];
  const otherCommunityId = req.params[otherIdParam];
  Similarity.computeSimilarity(communityId, otherCommunityId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("Invalid communityIds (target or other)");
    });
};
