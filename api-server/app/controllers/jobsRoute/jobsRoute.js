'use strict';
const Perspectives = require('../../service/PerspectivesService.js');
const Communities = require('../../service/CommunitiesService');
const Flags = require('../../service/FlagsService.js');


var jobManager = require('./jobsManager.js');



var express = require('express');
const { response } = require("express");
const { communities } = require('../../models/index.js');
var router = express.Router();


/**Response templates */
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
        "path": "xxx",
        "jobId": "xx",
        "name": "CM Update",
        "job-state": "STARTED",
        "job-status": "INPROGRESS",
        "start-time": "",
        "time-to-autoremove-job": "",
        "data": {}
    }
}
var jobCompleted = {
    "job": {
        "path": "",
        "jobId": "",
        "name": "CM Update",
        "job-state": "COMPLETED",
        "job-status": "SUCCESS",
        "start-time": "",
        "time-to-autoremove-job": "",
        "data": {}
    }
}


/**
 * Returns filled response template 
 * @param {Job id} jobId 
 * @returns Completed response
 */
function generateCompletedResponse(job, data) {
    var response = jobCompleted;
    response["job"]["path"] = "/jobs/" + job.jobId;
    response["job"]["jobId"] = job.jobId;
    response["job"]["data"] = data;
    response["job"]["start-time"] = job["start-time"];
    var timeLeft = (job["start-time"].getTime() + (5 * 60 * 1000)) - (new Date().getTime());
    response["job"]["time-to-autoremove-job"] = timeLeft / (1000 * 60) + " minutes";

    return response
}

/**
 * Returns filled response template 
 * @param {string} jobId 
 * @returns Progress response
 */
function generateProgressResponse(job) {
    var response = jobStarted;
    response["job"]["path"] = "/jobs/" + job.jobId;
    response["job"]["jobId"] = job.jobId;
    response["job"]["start-time"] = job["start-time"];
    var timeLeft = (job["start-time"].getTime() + (30 * 60 * 1000)) - (new Date().getTime());
    response["job"]["time-to-autoremove-job"] = timeLeft / (1000 * 60) + " minutes";

    return response
}


/**
 * /jobs/:job_id GET request
 * Allows to monitor job status and get data if CM update is finished.
 * 
 */
router.get('/:job_id', function (req, res, next) {
    console.log(jobManager.getJobs())
    var jobId = req.params.job_id
    var job = jobManager.getJob(req.params.job_id)

    if (job == null) {
        res.status(404).send("JobsManager: Job not found");
    }
    else {
        var param = job.param;
        var request = job.request;
        console.log("Monitoring Job: <" + jobId + ">, from request: <" + request + ">, with param: <" + param + ">");

        // var checkState;
        // if (request == "getPerspectives" || request == "getCommunities") {
        //     checkState = Flags.getFlags();
        // }
        // else {
        //     checkState = Flags.getFlagsById(param);
        // }
        // Checks for specific flag

        if (request == "getPerspectives" || request == "getCommunities") {
            Flags.getFlags()
                .then(function (data) {
                    if (data == null) {
                        var data = {};
                        // Get data from mongodb if flag is positive
                        getData(request, param)
                            .then(function (data) {
                                jobManager.removeJobWithTimeout(jobId, 60 * 5); // 5 min
                                res.status(200).send(generateCompletedResponse(job, data));
                            })
                            .catch(function (data) {
                                res.status(404).send("JobsManager: getData exception");
                            });
                    }
                    else {
                        res.send(generateProgressResponse(job));
                    }
                })
                .catch(function (data) {
                    res.status(404).send("JobsManager: flag not found");
                });
        }
        else {
            Flags.getFlagsById(param)
                .then(function (data) {
                    if (data == null) {
                        var data = {};
                        // Get data from mongodb if flag is positive
                        getData(request, param)
                            .then(function (data) {
                                jobManager.removeJobWithTimeout(jobId, 60 * 5); // 5 min
                                res.status(200).send(generateCompletedResponse(job, data));
                            })
                            .catch(function (error) {
                                res.status(404).send("JobsManager: getData error: " + error);
                            });
                    }
                    else {
                        res.send(generateProgressResponse(job));
                    }
                })
                .catch(function (data) {
                    res.status(404).send("JobsManager: flag not found");
                });
        }

    }
});

/**
 * Get specified promises
 * @param {string} request request type
 * @param {string} param parameters
 * @returns requested data
 */
function getData(request, param) {
    switch (request) {
        case "getPerspectives":
            return Perspectives.getPerspectives();
            break;
        case "getPerspectiveById":
            return Perspectives.getPerspectiveById(param);
            break;
        case "listPerspectiveCommunities":
            return Perspectives.listPerspectiveCommunities(param);
            break;
        case "getCommunities":
            return Communities.getCommunities();
            break;
        case "getCommunityById":
            return Communities.getCommunityById(param);
            break;
        case "listCommunityUsers":
            return Communities.listCommunityUsers(param);
            break;
        default:
            break;
    }
}


module.exports = router;