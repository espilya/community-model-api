module.exports = mongoose => {
    var schema = mongoose.Schema(
        {
            "id": String,
            "userid": String,
            "origin": String,
            "source_id": String,
            "source": String,
            "pname": String,
            "pvalue": String,
            "context": String,
            "datapoints": Number
        }, {
        versionKey: false // Para que no se anyada el campo "__v"
    });

    schema.method("toJSON", function () {
        const { __v, _id, ...object } = this.toObject();
        object.id = _id.toString();
        return object;
    });

    const Users = mongoose.model("Users", schema);


    return {
        update: function (users, onSuccess, onError) {
            console.log(users);
            users.forEach(function (user) {
                // console.log(typeof user);
                var json = JSON.parse(JSON.stringify(user));
                // console.log(json);
                Users.updateOne({ userid: json["userid"], pname: json["pname"] }, user, { upsert: true }, function (err, res) {
                    if (err) {
                        console.log("updateOne: error");
                        onError(user);
                    }
                });
            });
            onSuccess("");
        }
    };
};



//   Users.insertOne(myobj, function(error, data){
//         if (error) {
//             console.log("__insert error__");
//             console.log(error);
//             throw error;
//             // onError(error);
//         }
//         else {
//             console.log("__users inserted__");
//             // onSuccess(items);
//       }
//   });