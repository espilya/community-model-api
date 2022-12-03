/**
 * Jobs queue manager.
 * Contains a list with jobs, and basic CRUD operations. Used to add, remove and read for specific job
 */

var jobsList = []


createJob = function (perspectiveId, requestTypeName) {
    var jobId = generateId()
    console.log("<JobsQueue> generateId: " + jobId)
    console.log("<JobsQueue> perspectiveId: " + perspectiveId)
    addJob(jobId, requestTypeName, perspectiveId);
    var path = "/v1.1/jobs/" + jobId
    var data = {
        "path": path
    }
    return data;
}

/**
 * Returns requested job by id
 */
getJob = function (jobId) {
    return jobsList.find(element => element.jobId == jobId);
};

/**
 * Returns jobs
 */
getJobs = function () {
    return jobsList;
};

/**
 * Adds new job to the job list
 */
addJob = function (jobId, request, param) {
    var job = {
        jobId: jobId,
        request: request,
        param: param,
        "start-time": new Date(),
        autoremove: false
    }
    jobsList.push(job);

    removeJobWithTimeout(jobId, 60 * 30); // 30 min = 60 * 30
};

/**
 * Removes job by id
 */
removeJob = function (jobId) {
    var job = jobsList.find(element => element.jobId == jobId);
    if (job != undefined) { //if still not removed removed by timeout
        console.log(`<JobsQueue> removing job => ${jobId}`);
        const index = jobsList.indexOf(job);
        if (index > -1) { // only splice array when item is found
            jobsList.splice(index, 1); // 2nd parameter means remove one item only
        }
    }
};

removeJobWithTimeout = removeTimeout = function (jobId, seconds) {
    // if (!getJob(jobId).autoremove) {
    getJob(jobId).autoremove = true;
    setTimeout(() => {
        // console.log(`<JobsQueue> auto-removing job => ${jobId}`);
        try {
            removeJob(jobId)
        } catch (error) {
            console.log(error)
        }
    }, seconds * 1000, jobId, jobsList);
    // }

}


/**
 * Generates non-repeating random 4-digit job id
 * @returns id
 */
generateId = function (jobId) {
    var id = 0;
    var ok = false;
    while (!ok) {
        id = Math.floor(
            Math.random() * (9999 - 1000) + 1000
        );
        if (jobsList.find(element => element.jobId == jobId) == null)
            ok = true;
    }
    return id;
};



exports.createJob = createJob;
exports.getJob = getJob;
exports.getJobs = getJobs
exports.addJob = addJob;
exports.removeJob = removeJob;
exports.removeJobWithTimeout = removeJobWithTimeout;
exports.generateId = generateId;



// Refactoring for future

/*

var map = {};

map[Date.now()] = ['a', 'b'];
console.log(map);

setTimeout(function() {
  map[Date.now()] = ['c', 'd'];
  console.log(map);
}, 5000);

setInterval(function() {
  var times = Object.keys(map);
  
  times.forEach(function(time) {
    if(Date.now() > (+time + 14000)) {
      delete map[time];
    }
  });
  
  console.log(map);
}, 1000);

*/