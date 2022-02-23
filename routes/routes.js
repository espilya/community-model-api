module.exports = app => {
    const Users = require("../controllers/users");
    console.log(Users);
  
    var router = require("express").Router();
  
    // Retrieve a single Tutorial with id
    router.get("/users/:userId/communities", Users.listUserCommunities);
  
    app.use("/", router);
};