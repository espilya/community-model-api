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


  const http = require('http');

  return {
    update: function (user, onSuccess, onError) {
      // user = JSON.stringify(user)
      // // console.log("User:");
      // // console.log(users);

      // const options = {
      //   hostname: 'host.docker.internal',
      //   port: 8090,
      //   path: '/',
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //     'Content-Length': user.length,
      //   },
      // };

      // const req = http.request(options, res => {
      //   console.log(`statusCode: ${res.statusCode}`);

      //   res.on('data', d => {
      //     process.stdout.write(d);
      //   });
      // });

      // var a = 2222
      // req.on('error', function(err) {
      //   console.error(err);
      //   a = 4444
      //   console.log(a);
      //   throw err;
      //   onError(err)
      // });
      // console.log(a);
      // // onError(user)

      // req.write(user);
      // req.end();

      // // req.on('success', onSuccess(""))
      // onSuccess("");


    }
  };
};


/// Add user directly into mongoDB:
//
// const Users = mongoose.model("Users", schema);
//
// users.forEach(function (user) {
//     // console.log(typeof user);
//     var json = JSON.parse(JSON.stringify(user));
//     // console.log(json);
//     Users.updateOne({ userid: json["userid"], pname: json["pname"] }, user, { upsert: true }, function (err, res) {
//         if (err) {
//             console.log("updateOne: error");
//             onError(user);
//         }
//     });
// });
// onSuccess("");