'use strict';

const Communities = require('../service/CommunitiesService');

module.exports.getCommunities = function getCommunities (req, res, next) {
  Communities.getCommunities()
    .then(function (response) {
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
    });
};

module.exports.getCommunityById = function getCommunityById (req, res, next) {
  const communityId = req.enforcer.params['community-id'];
  Communities.getCommunityById(communityId)
    .then(function (response) {
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
    });
};

module.exports.listCommunityUsers = function listCommunityUsers (req, res, next) {
  const communityId = req.enforcer.params['community-id'];
  Communities.listCommunityUsers(communityId)
    .then(function (response) {
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
    });
};
