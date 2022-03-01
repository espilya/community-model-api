module.exports = app => {
    
    const customControllers =  {
        Users: require("../controllers/users"),
        Communities: require("../controllers/communities"),
        Similarity: require("../controllers/similarity")
    };

    const enforcer = app.get("enforcer");
    app.use(enforcer.route(customControllers, {xController: "x-swagger-router-controller", xOperation: "operationId"}));

};