module.exports = app => {
    
    const customControllers =  {
        Users: require("../controllers/users.js"),
        Communities: require("../controllers/communities.js"),
        Similarity: require("../controllers/similarity.js")
    };

    const enforcer = app.get("enforcer");
    app.use(enforcer.route(customControllers, {xController: "x-swagger-router-controller", xOperation: "operationId"}));

};