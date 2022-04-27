/**
 * It generates an object with the methods to access a Community DAO
 * @param {object} mongoose Mongoose object for accessing mongodb
 * @returns An object with the DAO functions employed by the CommunitiesService
 */
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
    
    
    return {
      /**
       * Creates a list with all the communities and passes it to the onSuccess callback function
       * @param {function} onSuccess Callback function invoked if the request was a success
       */
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
      /**
       * Looks for a community characterized by its communityId and passes it to the onSuccess callback function
       * It invokes onError callback function if the communityId does not exist in the database 
       * @param {string} communityId
       * @param {function} onSuccess Callback function invoked if the request was a success
       * @param {function} onError Callback function invoked if the communityId does not exist in the database
       */
      getById: function(communityId, onSuccess, onError) {
        Communities.findOne({_id:communityId}, function (error, data) {
          if (error) {
            onError(error);
          } else {
            if (data) {
              onSuccess(data.toJSON());
            }
            else {
              onError(communityId);
            }
          }
        });
      },
      /**
       * Creates a list wit all the communities that a user belongs to and passes it to the onSuccess callback function
       * It invokes onError callback function if the userId does not exist in the database 
       * @param {string} userId
       * @param {function} onSuccess Callback function invoked if the request was a success
       * @param {function} onError Callback function invoked if the userId does not exist in the database
       */
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
  