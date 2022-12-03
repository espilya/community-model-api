'use strict';
// const Perspectives = require('../../service/PerspectivesService.js');
const CommunitiesVis = require('../service/CommunitiesVisualizationService.js');
const Flags = require('../service/FlagsService.js');
var post = require('./postUpdateCM');
var jobManager = require('./jobsRoute/jobsManager.js');

var express = require('express');
var router = express.Router();


/**
    http://localhost:8080/visualizationAPI/....
    http://localhost:8080/visualizationAPI/file/{perspectiveId}     -> return the first file with name equal to "fileId" -- JSON
    http://localhost:8080/visualizationAPI/index                    -> return json files index (returns only perspectievId and name) -- list[JSON]
 */

router.get('/index', function (req, res, next) {

    Flags.getFlags()
        .then(function (response) {
            if (response == null) {
                CommunitiesVis.getIndex()
                    .then(function (response) {
                        res.status(200).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send(response);
                    });
            }
            else {
                post.update_CM("allPerspectives");
                var data = jobManager.createJob(0, "getFilesIndex")
                res.status(202).send(data);
            }
        })
        .catch(function (response) {
            console.error("CommunitiesVis.getIndex -> Flags.getFlags: error: " + response)
        });

    // CommunitiesVis.getIndex()
    //     .then(function (response) {
    //         res.status(200).send(response);
    //     })
    //     .catch(function (response) {
    //         res.status(400).send(response);
    //     });
});

router.get('/file/:fileId', function (req, res, next) {
    var fileId = req.params.fileId

    // console.log(file.perspectiveId)
    Flags.getFlagsById(fileId)
        .then(function (flag) {
            if (flag == null) { // flag does not exist => no update needed
                CommunitiesVis.getById(fileId)
                    .then(function (response) {
                        res.status(200).send(response);
                    })
                    .catch(function (response) {
                        res.status(400).send(response);
                    });
            }
            else { //flag exist
                post.update_CM(fileId);
                var data = jobManager.createJob(fileId, "getFileById")
                res.status(202).send(data);
            }
        })
        .catch(function (response) {
            console.error("Communities.getCommunityById -> Flags.getFlagsById: error: " + response)
        })
        .catch(function (response) {
            res.status(400).send("invalid file id");
        });

    // CommunitiesVis.getById(fileId)
    //     .then(function (response) {
    //         res.status(200).send(response);
    //     })
    //     .catch(function (response) {
    //         res.status(400).send(response);
    //     });
    // }
});



module.exports = router;