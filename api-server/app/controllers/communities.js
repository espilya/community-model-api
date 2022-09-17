const idParam = 'communityId';
const Communities = require('../service/CommunitiesService.js');
const Flags = require('../service/FlagsService.js');
var post = require('./post');
var jobManager = require('./jobsRoute/jobsManager.js');

// function checkPerspectives() {
//   var exist = false;
//   Communities.getCommunities()
//     .then(function (response) {
//       for (let i = 0; i < response.length; i++) {
//         var perspective = response[i].perspectiveId;
//         Flags.getFlagsById(perspective)
//           .then(function (response) {
//             if (response == null) { // flag does not exist => no update needed
//               Perspectives.listPerspectiveCommunities(perspective)
//                 .then(function (response) {
//                   res.status(200).send(response);
//                 })
//                 .catch(function (response) {
//                   res.status(400).send("invalid perspective id");
//                 });
//             }
//             else { //flag exist
//               post.update_CM();
//               var data = jobManager.createJob(perspective, "listPerspectiveCommunities")
//               res.status(202).send(data);
//             }
//           })
//           .catch(function (response) {
//             console.error("Communities.getCommunities -> Flags.getFlagsById: error: " + response)
//           });
//       }
//     })
// }


module.exports.getCommunities = function getCommunities(req, res, next) {
  Communities.getCommunities()
    .then(function (response) {
      res.status(200).send(response);
    })
    .catch(function (response) {
      res.status(400).send(response);
    });
};

module.exports.getCommunityById = function getCommunityById(req, res, next) {
  const communityId = req.params[idParam];
  Communities.getCommunityById(communityId)
    .then(function (response) {
      var community = response
      console.log(community.perspectiveId)
      Flags.getFlagsById(community.perspectiveId)
        .then(function (flag) {
          if (flag == null) { // flag does not exist => no update needed
            res.status(200).send(community);
          }
          else { //flag exist
            post.update_CM(perspectiveId);
            var data = jobManager.createJob(communityId, "getCommunityById")
            res.status(202).send(data);
          }
        })
        .catch(function (response) {
          console.error("Communities.getCommunityById -> Flags.getFlagsById: error: " + response)
        });
    })
    .catch(function (response) {
      res.status(400).send("invalid community id");
    });
};

module.exports.listCommunityUsers = function listCommunityUsers(req, res, next) {
  const communityId = req.params[idParam];
  //get users list
  Communities.listCommunityUsers(communityId)
    .then(function (response) {
      var users = response;
      //get community
      Communities.getCommunityById(communityId)
        .then(function (response) {
          var community = response;
          Flags.getFlagsById(community.perspectiveId)
            .then(function (flag) {
              if (flag == null) { // flag does not exist => no update needed
                res.status(200).send(users);
              }
              else { //flag exist
                post.update_CM(perspectiveId);
                var data = jobManager.createJob(communityId, "listCommunityUsers")
                res.status(202).send(data);
              }
            })
            .catch(function (response) {
              console.error("Communities.listCommunityUsers -> Flags.getFlagsById: error: " + response)
            });
        })
    })
    .catch(function (response) {
      res.status(400).send("invalid community id");
    });
};
