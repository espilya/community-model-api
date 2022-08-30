const idParam = 'communityId';
const Communities = require('../service/CommunitiesService.js');

module.exports.getCommunities = function getCommunities (req, res, next) {
  Communities.getCommunities()
    .then(function (response) {
      res.status(200).send(response);
    })
    .catch(function (response) {
      res.status(400).send(response);
    });
};

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
