module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      perspectiveId: String,
      flag: Boolean
    }
  );

  schema.method("toJSON", function () {
    const { __v, _id, ...object } = this.toObject();
    // object.id = _id.toString();
    return object;
  });

  const Flags = mongoose.model("Flags", schema);

  // Access mongobd and retrieve requested flag
  return {
    checkFlag: function (onSuccess, onError) {
      Flags.findOne({}, function (error, data) {
        // var res = JSON.stringify(data)
        if (error) {
          console.log("errorHere")
          onError(error);
        } else {
          if (data) {
            console.log(data.toJSON())
            onSuccess(data.toJSON());
          }
          else {
            onSuccess(null);
          }
        }
      });
    },
    checkFlagById: function (id, onSuccess, onError) {
      console.log("id " + id)
      Flags.findOne({ "perspectiveId": id }, { projection: { _id: 0 } }, function (error, data) {
        if (error) {
          console.log("errorHere")
          onError(error);
        } else {
          if (data) {
            console.log(data.toJSON())
            onSuccess(data.toJSON());
          }
          else {
            onSuccess(null);
          }
        }
      });
    }
  };
};

