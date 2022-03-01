module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      "community-type": String,
      name: String,
      explanation: String,
      users: [String]
    }
  );

  schema.method("toJSON", function() {
    const { __v, _id, ...object } = this.toObject();
    object.id = _id.toString();
    return object;
  });

  const Communities = mongoose.model("Communities", schema);
  return Communities;
};
