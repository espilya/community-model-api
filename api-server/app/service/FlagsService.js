'use strict';
const db = require("../models");

const FlagDAO = db.flag;

/**
* Communities in the model
* Access to a list of the communities in the community model
*
* returns List
**/
exports.getFlags = function (flagId) {
    return new Promise(function (resolve, reject) {
        FlagDAO.checkFlag(flagId,
            data => {
                resolve(data)
            },
            error => {
                console.log("flagService error: " + error);
                reject(error)
            })
    });
};

