module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      "target-community-id": String,
      "other-community-id": String,
      "similarity-function": String,
      value: Number
    }
  );
  
  schema.method("toJSON", function() {
    const { __v, _id, ...object } = this.toObject();
    return object;
  });

  const Similarity = mongoose.model("Similarities", schema);
  
  return {
    allForId: function(communityId, onSuccess, onError) {
      Similarity.find({ "target-community-id": communityId }, function(error, data){
        if (error) {
          onError(error);
        } else {
          let items= [];
          let i=0;
          data.forEach(element => {
            items[i] = element.toJSON();
            i++;
          });
          onSuccess(items);
        }
      }).sort({value: -1});   
      
    },
    getById: function(id, onSuccess, onError) {
      Similarity.findOne({_id:id}, function (error, data) {
        if (error) {
          onError(error);
        } else {
          onSuccess(data.toJSON());
        }
      });
    }
  };
};

// Example por saving a similarity document in the database
// const example = new Similarity({
//   "target-community-id": "621e53cf0aa6aa7517c2afdd",
//   "other-community-id": "721e53cf0aa6aa7517c2afdd",
//   "similarity-function": "cosine",
//   value: 0.893
// });
// example.save();
  