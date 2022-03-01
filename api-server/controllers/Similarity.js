'use strict';

const Similarity = require('../service/SimilarityService.js');

module.exports.computeDissimilarity = function computeDissimilarity (req, res, next) {
  const communityId = req.enforcer.params['community-id'];
  const otherCommunityId = req.enforcer.params['other-community-id'];
  Similarity.computeDissimilarity(communityId, otherCommunityId)
    .then(function (response) {
      res.enforcer.send(response);
    })
    .catch(function (response) {
      return response;
    });
};

module.exports.computeKmostDissimilar = function computeKmostDissimilar (req, res, next) {
  const communityId = req.enforcer.params['community-id'];
  const k = 5;
  Similarity.computeKmostDissimilar(communityId, k)
    .then(function (response) {
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
    });
};

module.exports.computeKmostSimilar = function computeKmostSimilar (req, res, next) {
  const communityId = req.enforcer.params['community-id'];
  const k = 5;
  Similarity.computeKmostSimilar(communityId, k)
    .then(function (response) {
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
    });
};

module.exports.computeSimilarity = function computeSimilarity (req, res, next) {
  const communityId = req.enforcer.params['community-id'];
  const otherCommunityId = req.enforcer.params['other-community-id'];
  Similarity.computeSimilarity(communityId, otherCommunityId)
    .then(function (response) {
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
    });
};
