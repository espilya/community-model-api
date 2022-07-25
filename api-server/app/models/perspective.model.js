module.exports = mongoose => {
  var schema = mongoose.Schema(
  //   {
  //     id: Number,
  //     name: String,
  //     algorithm: String,
  //     similarity_functions: String
  //   }
  // );
    {
      id: String,
      name: String,
      algorithm: {
        name: String,
        params: [
          String
        ],
      },
      similarity_functions: [{
        sim_function: {
          name: String,
          params: [
            String
          ],
          on_attribute: {
            att_name: String,
            att_type: String
          },
          weight: Number
        }
      }]
    }
  );

  schema.method("toJSON", function () {
    const { __v, _id, ...object } = this.toObject();
    object.id = _id.toString();
    return object;
  });

  const Perspectives = mongoose.model("Perspectives", schema);


  return {
    all: function (onSuccess) {
      let items = [];
      Perspectives.find({}, function (error, data) {
        let i = 0;
        data.forEach(element => {
          items[i] = element.toJSON();
          i++;
        });
        onSuccess(items);
      });

    },
    getById: function (id, onSuccess, onError) {
      Perspectives.findOne({ "id": id }, function (error, data) {
        if (error) {
          onError(error);
        } else {
          console.log(data);
          if (data) {
            onSuccess(data.toJSON());
          }
          else {
            onError(id);
          }
        }
      });
    },
    allCommunitiesCreatedForPerspective: function (perspectiveId, onSuccess, onError) {
      let items = [];
      // Perspectives.find({ users: userId }, function (error, data) {
      //   if (data.length > 0) {
      //     let i = 0;
      //     data.forEach(element => {
      //       items[i] = element.toJSON();
      //       i++;
      //     });
      //     onSuccess(items);
      //   }
      //   else {
      //     onError(userId);
      //   }
      // });
    }
  };
};
