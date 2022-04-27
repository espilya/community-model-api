/**
 * This module returns an object with a function to init the database connection
 * and the DAOs employed to access the communities and the similarity values in the database
 */

const dbConfig = require("../config/db.config.js");

const mongoose = require("mongoose");

const db = {};
db.mongoose = mongoose;
db.url = dbConfig.url;

// These DAOs are created using mongoose
db.communityDAO = require("./community.model.js")(mongoose);
db.similarityDAO = require("./similarity.model.js")(mongoose);

module.exports = {
    /**
     * Creates a conection with the database using mongoose
     * @param {function} onReady Callback function when the database is ready
     */
    init: async function(onReady) {
        console.log(db.url);
        db.mongoose
        .connect(db.url, {
            useNewUrlParser: true,
            useUnifiedTopology: true
        })
        .then(() => {
            console.log("Connected to the database!");
            onReady();
        })
        .catch(err => {
            console.log("Cannot connect to the database!", err);
            process.exit();
        });
    },
    // DAO for accesing data about communities
    communities: db.communityDAO,
    // DAO for accessing data about similarity values
    similarities: db.similarityDAO
};
