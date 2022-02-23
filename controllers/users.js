'use strict';

var utils = require('../utils/writer.js');
var Users = require('../service/UsersService');

module.exports.addContribution = function addContribution (req, res, next, body, userId) {
  Users.addContribution(body, userId)
    .then(function (response) {
      utils.writeJson(res, response);
    })
    .catch(function (response) {
      utils.writeJson(res, response);
    });
};

module.exports.listUserCommunities = function listUserCommunities (req, res) {
  const userId = req.enforcer.params['user-id'];
  Users.listUserCommunities(userId)
    .then(function (response) {
      //utils.writeJson(res, response);
      res.enforcer.send(response);
    })
    .catch(function (response) {
      //utils.writeJson(res, response);
      console.log(response);
    });
};
