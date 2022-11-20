module.exports = mongoose => {
    var schema = mongoose.Schema({ any: {} });

    // schema.method("toJSON", function () {
    //   const { __v, _id, ...object } = this.toObject();
    //   // object.id = _id.toString();
    //   return object;
    // });

    // const Flags = mongoose.model("Flags", schema);

    // Access mongobd and retrieve requested flag
    return {
        load: function (data, onSuccess, onError) {
            var model;
            for (var coll of data) {
               console.log(coll);
                // model = mongoose.model("communitiesVisualization", schema, "communitiesVisualization");
            }
            // Flags.create(data, function (err, res) {
            //   if (err) {
            //     console.log("insertFlag: error");
            //     onError(user);
            //   }
            //   else {
            //     onSuccess(res._id.toString());
            //   }
            // });
        }
    }
};


