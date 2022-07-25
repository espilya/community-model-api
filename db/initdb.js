let spiceUser = _getEnv('MONGODB_USER');
let spicePwd = _getEnv('MONGODB_PASSWORD');
let dbName = _getEnv('MONGO_INITDB_DATABASE');
db = new Mongo().getDB(dbName);
print("Connected to " + db.getName());

db.createUser({
  user: spiceUser,
  pwd: spicePwd,
  roles: [
    {
      role: 'readWrite',
      db: db.getName()
    }
  ]
});

db.createCollection('perspectives', { capped: false });
// db.perspectives.delete_many({});

db.perspectives.insertMany([{
    "id": 100,
    "name": "String",
    "algorithm": {
      "name": "String",
      "params": {
        "param_a": "String",
        "param_b": "String"
      }
    },
    "similarity_functions": [{
      "sim_function": {
        "name": "String",
        "params": {
          "param_a": "String",
          "param_b": "String"
        },
        "on_attribute": {
          "att_name": "String",
          "att_type": "String"
        },
        "weight": 100
      }
    }]
  }, {
    "id": 101,
    "name": "String",
    "algorithm": {
      "name": "String",
      "params": {
        "param_a": "String",
        "param_b": "String"
      }
    },
    "similarity_functions": [{
      "sim_function": {
        "name": "String",
        "params": {
          "param_a": "String",
          "param_b": "String"
        },
        "on_attribute": {
          "att_name": "String",
          "att_type": "String"
        },
        "weight": 101
      }
    }]
  }]);

db.createCollection('communities', { capped: false });
// db.communities.delete_many({});

// db.communities.insertMany( [{
//     "_id": ObjectId("621e53cf0aa6aa7517c2afdd"),
//     "community-type": "explicit",
//     "name": "elderly",
//     "explanation": "People above 65",
//     "users": [
//       "23",
//       "28"
//     ],
//   },{
//     "_id": ObjectId("721e53cf0aa6aa7517c2afdd"),
//     "community-type": "implicit",
//     "explanation": "lorem ipsum",
//     "name": "impl_1",
//     "users": [
//       "44",
//       "23"
//     ]
//   }, {
//     "_id": ObjectId("821e53cf0aa6aa7517c2afdd"),
//     "community-type": "explicit",
//     "name": "teenager",
//     "explanation": "People whose age is between 12 and 17",
//     "users": [
//       "44",
//       "56"
//     ],
//   }]);

db.createCollection('similarities', { capped: false });
// db.similarities.delete_many({});

// db.similarities.insertMany( [{
//     "target-community-id": "621e53cf0aa6aa7517c2afdd",
//     "other-community-id": "721e53cf0aa6aa7517c2afdd",
//     "similarity-function": "cosine",
//     "value": 0.893,
//   },{
//     "target-community-id": "721e53cf0aa6aa7517c2afdd",
//     "other-community-id": "821e53cf0aa6aa7517c2afdd",
//     "similarity-function": "cosine",
//     "value": 0.563,
//   },{
//     "target-community-id": "621e53cf0aa6aa7517c2afdd",
//     "other-community-id": "821e53cf0aa6aa7517c2afdd",
//     "similarity-function": "cosine",
//     "value": 0.915,
//   },{
//     "target-community-id": "721e53cf0aa6aa7517c2afdd",
//     "other-community-id": "621e53cf0aa6aa7517c2afdd",
//     "similarity-function": "cosine",
//     "value": 0.893,
//   },{
//     "target-community-id": "821e53cf0aa6aa7517c2afdd",
//     "other-community-id": "621e53cf0aa6aa7517c2afdd",
//     "similarity-function": "cosine",
//     "value": 0.915,
//   },{
//     "target-community-id": "821e53cf0aa6aa7517c2afdd",
//     "other-community-id": "721e53cf0aa6aa7517c2afdd",
//     "similarity-function": "cosine",
//     "value": 0.563,
// }]);