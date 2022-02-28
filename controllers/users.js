'use strict';

var utils = require('../utils/writer.js');
var Users = require('../service/UsersService');

module.exports.updateUsers = function updateUsers (req, res, next) {
  console.log(req.body);
  Users.updateUsers(req.enforcer.body)
    .then(function (response) {
      res.status(204);
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
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
      res.enforcer.send(response);
    });
};
