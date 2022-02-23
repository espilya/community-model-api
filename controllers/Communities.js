'use strict';

var utils = require('../utils/writer.js');
var Communities = require('../service/CommunitiesService');

module.exports.getCommunities = function getCommunities (req, res, next) {
  Communities.getCommunities()
    .then(function (response) {
      //utils.writeJson(res, response);
      return response;
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.getCommunityById = function getCommunityById (req, res, next, communityId) {
  console.log(communityId);
  Communities.getCommunityById(communityId)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.listCommunityUsers = function listCommunityUsers (req, res, next, communityId) {
  Communities.listCommunityUsers(communityId)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};
