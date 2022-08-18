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

db.createCollection('users', { capped: false });
db.users.deleteMany({});

db.users.insertMany([{
  "id": "1",
  "userid": "23",
  "origin": "a",
  "source_id": "b",
  "source": "c description",
  "pname": "DemographicGender",
  "pvalue": "F (for Female value)",
  "context": "application P:DemographicsPrep",
  "datapoints": 0
},
{
  "id": "2",
  "userid": "28",
  "origin": "a",
  "source_id": "b",
  "source": "Content description",
  "pname": "Age",
  "pvalue": "28",
  "context": "application P:DemographicsPrep",
  "datapoints": 0
},
{
  "id": "3",
  "userid": "44",
  "origin": "90e6d701748f08514b01",
  "source_id": "90e6d701748f08514b01",
  "source": "Content description",
  "pname": "DemographicGender",
  "pvalue": "M (for Female value)",
  "context": "application P:DemographicsPrep",
  "datapoints": 0
},
{
  "id": "4",
  "userid": "56",
  "origin": "90e6d701748f08514b01",
  "source_id": "90e6d701748f08514b01",
  "source": "Content description",
  "pname": "Age",
  "pvalue": "56",
  "context": "application P:DemographicsPrep",
  "datapoints": 0
}])

db.createCollection('perspectives', { capped: false });
db.perspectives.deleteMany({});

db.perspectives.insertMany([{
  "id": "100",
  "name": "Perspective_100",
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
  "id": "101",
  "name": "Perspective_101",
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
db.communities.deleteMany({});

db.communities.insertMany([{
  "id": "621e53cf0aa6aa7517c2afdd",
  "community-type": "explicit",
  "name": "elderly",
  "perspectiveId": "101",
  "explanation": "People above 65",
  "users": [
    "23",
    "28"
  ],
}, {
  "id": "721e53cf0aa6aa7517c2afdd",
  "community-type": "implicit",
  "explanation": "lorem ipsum",
  "perspectiveId": "101",
  "name": "impl_1",
  "users": [
    "44",
    "23"
  ]
}, {
  "id": "821e53cf0aa6aa7517c2afdd",
  "community-type": "explicit",
  "name": "teenager",
  "perspectiveId": "100",
  "explanation": "People whose age is between 12 and 17",
  "users": [
    "44",
    "56"
  ],
}]);

db.createCollection('similarities', { capped: false });
db.similarities.deleteMany({});

db.similarities.insertMany([{
  "target-community-id": "621e53cf0aa6aa7517c2afdd",
  "other-community-id": "721e53cf0aa6aa7517c2afdd",
  "similarity-function": "cosine",
  "value": 0.893,
}, {
  "target-community-id": "721e53cf0aa6aa7517c2afdd",
  "other-community-id": "821e53cf0aa6aa7517c2afdd",
  "similarity-function": "cosine",
  "value": 0.563,
}, {
  "target-community-id": "621e53cf0aa6aa7517c2afdd",
  "other-community-id": "821e53cf0aa6aa7517c2afdd",
  "similarity-function": "cosine",
  "value": 0.915,
}, {
  "target-community-id": "721e53cf0aa6aa7517c2afdd",
  "other-community-id": "621e53cf0aa6aa7517c2afdd",
  "similarity-function": "cosine",
  "value": 0.893,
}, {
  "target-community-id": "821e53cf0aa6aa7517c2afdd",
  "other-community-id": "621e53cf0aa6aa7517c2afdd",
  "similarity-function": "cosine",
  "value": 0.915,
}, {
  "target-community-id": "821e53cf0aa6aa7517c2afdd",
  "other-community-id": "721e53cf0aa6aa7517c2afdd",
  "similarity-function": "cosine",
  "value": 0.563,
}]);