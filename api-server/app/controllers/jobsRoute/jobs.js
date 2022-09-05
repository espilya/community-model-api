'use strict';
const db = require("../../models");
const Perspectives = require('../../service/PerspectivesService.js');
const Flags = require('../../service/FlagsService.js');

const FlagDAO = db.flag;

var jobManager = require('./jobsQueue');



var express = require('express');
const { response } = require("express");
var router = express.Router();


// en desarrollo


var jobStarted_Template = {
    "job": {
        "@uri": "/jobs/xxxxxxxx",
        "id": "2130040",
        "name": "Update Community Model",
        "job-state": "STARTED",
        "job-status": "INPROGRESS",
        "percent-complete": "30",
        "scheduled-start-time": "01-01-2013 10:50:45 PM GMT",
        "start-time": "01-01-2013 10:50:55 PM GMT",
        "end-time": "",
        "owner": "Admin",
        "summary": "random text"
    }
}
var jobCompleted_Template = {
    "job": {
        "@uri": "/api/company/job-management/jobs/2130040",
        "id": "2130040",
        "name": "Update Resource",
        "job-state": "COMPLETED",
        "job-status": "SUCCESS",
        "percent-complete": "100",
        "scheduled-start-time": "01-01-2013 10:50:45 PM GMT",
        "start-time": "01-01-2013 10:50:55 PM GMT",
        "end-time": "01-01-2013 10:52:18 PM GMT",
        "owner": "Admin",
        "summary": "random text"
    }
}

var jobStarted = {
    "job": {
        "@uri": "xxx",
        "jobId": "xx",
        "name": "CM Update",
        "job-state": "STARTED",
        "job-status": "INPROGRESS",
        "data": {}
    }
}
var jobCompleted = {
    "job": {
        "@uri": "",
        "jobId": "",
        "name": "CM Update",
        "job-state": "COMPLETED",
        "job-status": "SUCCESS",
        "data": {}
    }
}



function generateCompletedResponse(jobId, data) {
    var response = jobCompleted;
    response["job"]["@uri"] = "/jobs/" + jobId;
    response["job"]["jobId"] = jobId;
    response["job"]["data"] = data
    return response
}

function generateProgressResponse(jobId) {
    var response = jobStarted;
    response["job"]["@uri"] = "/jobs/" + jobId;
    response["job"]["jobId"] = jobId;
    return response
}

router.get('/:job_id', function (req, res, next) {
    var jobId = req.params.job_id
    var job = jobManager.getJob(req.params.job_id)

    if (job == null) {
        res.status(404).send("JobsManager: Job not found");
    }
    else {
        var param = job.param;
        var request = job.request;
        console.log("Monitoring Job: <" + jobId + ">, from request: <" + request + ">, with param: <" + param + ">");

        Flags.getFlags(param)
            .then(function (data) {
                if (data.flag) {
                    var data = {};
                    getData(request, param)
                        .then(function (data) {
                            res.status(200).send(generateCompletedResponse(jobId, data));
                            jobManager.removeJob(jobId);
                        })
                        .catch(function (data) {
                            res.status(404).send("JobsManager: generateCompletedResponse exception");
                        });
                }
                else {
                    res.send(generateProgressResponse(jobId));
                }
            })
            .catch(function (data) {
                res.status(404).send("JobsManager: flag not found");
            });

    }
});

function getData(request, param) {
    return new Promise(function (resolve, reject) {
        if (request == "listPerspectiveCommunities") {
            Perspectives.listPerspectiveCommunities(param)
                .then(function (response) {
                    resolve(response);
                })
                .catch(function (response) {
                    reject("JobsManager: MongoBD access error");
                });
        }
        else if (request == "a") {
            // ...
        }
    });
}


module.exports = router;