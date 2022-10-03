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
  "id": "1000",
  "name": "HEHCT Perspective",
  "algorithm": {
    "name": "agglomerative",
    "params": [
    ]
  },
  "similarity_functions": [
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "beleifR",
          "att_type": "String"
        },
        "weight": 0.8
      }
    },
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "beliefJ",
          "att_type": "String"
        },
        "weight": 0.6
      }
    },
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "DemographicReligous",
          "att_type": "String"
        },
        "weight": 0.2
      }
    },
    {
      "sim_function": {
        "name": "TableSimilarityDAO",
        "params": [
        ],
        "on_attribute": {
          "att_name": "DemographicPolitics",
          "att_type": "String"
        },
        "weight": 0.2
      }
    }
  ]
}

]);

db.createCollection('communitiesVisualization', { capped: false });
db.communitiesVisualization.deleteMany({});

db.createCollection('communities', { capped: false });
db.communities.deleteMany({});

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

db.createCollection('flags', { capped: false });
db.flags.deleteMany({});
db.flags.insertOne({ "flag" : true});


db.createCollection('distanceMatrixes', { capped: false });
db.distanceMatrixes.deleteMany({});



