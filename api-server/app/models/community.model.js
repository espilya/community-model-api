module.exports = mongoose => {
  var schema = mongoose.Schema(
    {
      "community-type": String,
      perspective: String,
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
    
    
    return {
      all: function(onSuccess) {
        let items= [];
        Communities.find({},function(error, data){
          let i=0;
          data.forEach(element => {
            items[i] = element.toJSON();
            i++;
          });
          onSuccess(items);
        });   
        
      },
      getById: function(id, onSuccess, onError) {
        Communities.findOne({_id:id}, function (error, data) {
          if (error) {
            onError(error);
          } else {
            if (data) {
              onSuccess(data.toJSON());
            }
            else {
              onError(id);
            }
          }
        });
      },
      allWithUserId: function(userId, onSuccess, onError) {
        let items= [];
        Communities.find({users: userId},function(error, data){
          if (data.length>0){
            let i=0;
            data.forEach(element => {
              items[i] = element.toJSON();
              i++;
            });
            onSuccess(items);
          }
          else {
            onError(userId);
          }
        }); 
      }
    };
  };
  