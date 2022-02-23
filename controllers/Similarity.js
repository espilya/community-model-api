'use strict';

var utils = require('../utils/writer.js');
var Similarity = require('../service/SimilarityService');

module.exports.computeDissimilarity = function computeDissimilarity (req, res, next, communityId, otherCommunityId) {
  Similarity.computeDissimilarity(communityId, otherCommunityId)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.computeKmostDissimilar = function computeKmostDissimilar (req, res, next, communityId, k) {
  Similarity.computeKmostDissimilar(communityId, k)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.computeKmostSimilar = function computeKmostSimilar (req, res, next, communityId, k) {
  Similarity.computeKmostSimilar(communityId, k)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.computeSimilarity = function computeSimilarity (req, res, next, communityId, otherCommunityId) {
  Similarity.computeSimilarity(communityId, otherCommunityId)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
