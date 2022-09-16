'use strict';
const db = require("../models");

const FlagDAO = db.flag;

/**
* Flags
* Access to specific flag to check it
*
* returns flag document
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

