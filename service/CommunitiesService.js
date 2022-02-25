'use strict';


/**
 * Communities in the model
 * Access to a list of the communities in the community model
 *
 * returns List
 **/
exports.getCommunities = function() {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ {
  "contributions" : [ {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  }, {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  } ],
  "community-type" : "explicit",
  "size" : 5,
  "name" : "elderly",
  "id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "explanation" : "People whose age is above 65",
  "users" : ['23', '24' ]
}, {
  "contributions" : [ {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  }, {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  } ],
  "community-type" : "explicit",
  "size" : 5,
  "name" : "elderly",
  "id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "explanation" : "People whose age is above 65",
  "users" : ['23', '24' ]
} ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * community description and explanation
 * Returns information about a community
 *
 * communityId Long ID of community to return
 * returns List
 **/
exports.getCommunityById = function(communityId) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ {
  "contributions" : [ {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  }, {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  } ],
  "community-type" : "explicit",
  "size" : 5,
  "name" : "elderly",
  "id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "explanation" : "People whose age is above 65",
  "users" : [ "22", "23" ]
}, {
  "contributions" : [ {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  }, {
    "generated-content-id" : "https://...",
    "user-id" : "http://example.com/aeiou",
    "values" : [ "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]", "[\"https://w3id.org/spice/SON/PlutchikEmotion/Amazement\"]" ],
    "parent-item-id" : "http://example.com/aeiou"
  } ],
  "community-type" : "explicit",
  "size" : 5,
  "name" : "elderly",
  "id" : "d290f1ee-6c54-4b01-90e6-d701748f0851",
  "explanation" : "People whose age is above 65",
  "users" : [ "22", "23" ]
} ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}


/**
 * Users who belong to a community
 * Returns a list with the ids of the users who belong to a community
 *
 * communityId Long ID of community to return
 * returns List
 **/
exports.listCommunityUsers = function(communityId) {
  return new Promise(function(resolve, reject) {
    var examples = {};
    examples['application/json'] = [ "d290f1ee-6c54-4b01-90e6-d701748f0851", "d290f1ee-6c54-4b01-90e6-d701748f0851" ];
    if (Object.keys(examples).length > 0) {
      resolve(examples[Object.keys(examples)[0]]);
    } else {
      resolve();
    }
  });
}

