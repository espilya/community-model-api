const dbConfig = require("../config/db.config.js");

const mongoose = require("mongoose");

const db = {};
db.mongoose = mongoose;
db.url = dbConfig.url;
db.communities = require("./community.model.js")(mongoose);

const communityDAO = {
    all: function(onSuccess) {
        let items= [];
        db.communities.find({},function(error, data){
            let i=0;
            data.forEach(element => {
              items[i] = element.toJSON();
              i++;
            });
            onSuccess(items);
        });   

    },
    getById: function(id, onSuccess, onError) {
        db.communities.findOne({_id:id}, function (error, data) {
            if (error) {
                onError(error);
            } else {
                onSuccess(data.toJSON());
            }
        });
    }
};

module.exports = {
    init: function() {
        console.log(db.url);
        db.mongoose
        .connect(db.url, {
            useNewUrlParser: true,
            useUnifiedTopology: true
        })
        .then(() => {
            console.log("Connected to the database!");
        })
        .catch(err => {
            console.log("Cannot connect to the database!", err);
            process.exit();
        });
    },
    communities: communityDAO
};
