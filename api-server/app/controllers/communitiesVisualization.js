'use strict';
// const Perspectives = require('../../service/PerspectivesService.js');
const CommunitiesVis = require('../service/CommunitiesVisualizationService.js');



var express = require('express');
var router = express.Router();


/**
    http://localhost:8080/visualizationAPI/....
    http://localhost:8080/visualizationAPI/file/{perspectiveId}     -> return the first file with name equal to "fileId" -- JSON
    http://localhost:8080/visualizationAPI/index                    -> return json files index (returns only perspectievId and name) -- list[JSON]
 */

router.get('/index', function (req, res, next) {
    CommunitiesVis.getIndex()
        .then(function (response) {
            res.status(200).send(response);
        })
        .catch(function (response) {
            res.status(400).send(response);
        });
});

router.get('/file/:fileId', function (req, res, next) {
    var fileId = req.params.fileId
    CommunitiesVis.getById(fileId)
        .then(function (response) {
            res.status(200).send(response);
        })
        .catch(function (response) {
            res.status(400).send(response);
        });
    // }
});



module.exports = router;