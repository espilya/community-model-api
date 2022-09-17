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
    var path = "/jobs/" + jobId
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
 * Adds new job to the job list
 */
addJob = function (jobId, request, param) {
    var job = {
        jobId: jobId,
        request: request,
        param: param
    }
    jobsList.push(job);
};

/**
 * Removes job by id
 */
removeJob = function (jobId) {
    var job = jobsList.find(element => element.jobId == jobId);
    const index = array.indexOf(job);
    if (index > -1) { // only splice array when item is found
        array.splice(index, 1); // 2nd parameter means remove one item only
    }
};

/**
 * Generates non-repeating random job id
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
exports.addJob = addJob;
exports.removeJob = removeJob;
exports.generateId = generateId; 