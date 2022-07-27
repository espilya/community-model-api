const idParam = 'perspectiveId';
const Perspectives = require('../service/PerspectivesService.js');

module.exports.getPerspectives = function getPerspectives (req, res, next) {
  Perspectives.getPerspectives()
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.send(response);
    });
};

module.exports.getPerspectiveById = function getPerspectiveById (req, res, next) {
  const perspectiveId = req.params[idParam];
  Perspectives.getPerspectiveById(perspectiveId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid perspective id");
    });
};

module.exports.listPerspectiveCommunities = function listPerspectiveCommunities (req, res, next) {
  const perspectiveId = req.params[idParam];
  Perspectives.listPerspectiveCommunities(perspectiveId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid perspective id");
    });
};
