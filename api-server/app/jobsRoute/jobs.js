var express = require('express');
var router = express.Router();

// en desarrollo

var data = [
    {
        name: 'Bibi',
    },
    {
        name: 'Colt',
    },
    {
        name: 'Jessie',
    }
]

var jobStarted = {
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

var jobCompleted = {
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


router.get('/:name', function (req, res, next) {
    var name = req.params.name;
    var user = data.filter(u => u.name == name);
    return res.json({ message: 'Users Show', data: user });
});

module.exports = router;