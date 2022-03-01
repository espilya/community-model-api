'use strict';

const Users = require('../service/UsersService.js');

module.exports.updateUsers = function updateUsers (req, res, next) {
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
      res.enforcer.send(response);
    })
    .catch(function (response) {
      res.enforcer.send(response);
    });
};
