module.exports = mongoose => {
    var schema = mongoose.Schema(
      {
        id: String,
        flag: Boolean 
      }
    );
    
    schema.method("toJSON", function() {
      const { __v, _id, ...object } = this.toObject();

      return object;
    });
  
    const flag = mongoose.model("Flags", schema);
    
    return {
      checkFlag: function(id, onSuccess, onError) {
        flag.findOne({}, function(error, data){
            // var res = JSON.stringify(data)
            console.log(data)
            if (error) {
                console.log("errorHere")
                onError(error);
            } else {
                onSuccess(data);
            }
        });   
      }
    };

  };
  
