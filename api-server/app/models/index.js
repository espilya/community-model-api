const dbConfig = require("../config/db.config.js");

const mongoose = require("mongoose");

const db = {};
db.mongoose = mongoose;
db.url = dbConfig.url;
db.communityDAO = require("./community.model.js")(mongoose);
db.similarityDAO = require("./similarity.model.js")(mongoose);

module.exports = {
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
    communities: db.communityDAO,
    similarities: db.similarityDAO
};
