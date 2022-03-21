const Users = require('../service/UsersService.js');
const userParam = 'userId';


module.exports.updateUsers = function updateUsers (req, res, next) {
  Users.updateUsers(req.body)
    .then(function (response) {
      res.status(204);
      res.send(response);
    })
    .catch(function (response) {
      res.send(response);
    });
};

module.exports.listUserCommunities = function listUserCommunities (req, res) {
  const userId = req.params[userParam];
  Users.listUserCommunities(userId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid user id");
    });
};
