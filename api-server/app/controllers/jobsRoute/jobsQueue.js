/**
 * Jobs queue manager.
 * Contains a list with jobs. Used to add, remove and read for specific job
 */

var jobsList = []

getJob = function (jobId) {
    return jobsList.find(element => element.jobId == jobId);
};

addJob = function (jobId, request, param) {
    var job = {
        jobId: jobId,
        request: request,
        param: param
    }
    jobsList.push(job);
};

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



exports.getJob = getJob;
exports.addJob = addJob;
exports.removeJob = removeJob;
exports.generateId = generateId; 