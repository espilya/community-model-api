const idParam = 'perspectiveId';
const Perspectives = require('../service/PerspectivesService.js');
const Flags = require('../service/FlagsService.js');
var post = require('./jobsRoute/post');

var jobManager = require('./jobsRoute/jobsQueue');

module.exports.getPerspectives = function getPerspectives(req, res, next) {
  Perspectives.getPerspectives()
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.send(response);
    });
};

module.exports.getPerspectiveById = function getPerspectiveById(req, res, next) {
  const perspectiveId = req.params[idParam];
  Perspectives.getPerspectiveById(perspectiveId)
    .then(function (response) {
      res.send(response);
    })
    .catch(function (response) {
      res.status(400).send("invalid perspective id");
    });
};

module.exports.listPerspectiveCommunities = function listPerspectiveCommunities(req, res, next) {
  const perspectiveId = req.params[idParam];

  Flags.getFlags(idParam)
    .then(function (response) {
      var flag = response.flag
      console.log("response: " + flag)
      if (flag == true) {
        Perspectives.listPerspectiveCommunities(perspectiveId)
          .then(function (response) {
            res.status(200).send(response);
          })
          .catch(function (response) {
            res.status(400).send("invalid perspective id");
          });
      }
      else {
        post.update_CM();
        const jobId = jobManager.generateId()
        console.log("generateId: " + jobId)
        console.log("perspectiveId: " + perspectiveId)
        jobManager.addJob(jobId, "listPerspectiveCommunities", perspectiveId);

        var path = "/jobs/" + jobId

        var data = {
          "path": path
        }
        res.status(202).send(data);
      }
    })
    .catch(function (response) {
      res.status(400).send("invalid perspective id");
    });

};

module.exports.perspectivePOST = function perspectivePOST(req, res, next) {
  Perspectives.perspectivePOST(req.body)
    .then(function (response) {
      res.status(204);
      res.send(response);
    })
    .catch(function (response) {
      res.status(501);
      res.send(response);
    });
};