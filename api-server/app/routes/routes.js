/**
 * Init the server routes using the openapi yaml file
 * It binds each path and action with the corresponding controller
 * @param {Object} app Express aplication
 */
module.exports = app => {
    const yaml = require('js-yaml');
    const fs   = require('fs');

    const customControllers =  {
        Users: require("../controllers/users.js"),
        Communities: require("../controllers/communities.js"),
        Similarity: require("../controllers/similarity.js")
    };
    /**
     * Configure a express router using our controllers.
     * The binding is created parsing the openapi.yaml file 
     * @param {Object} router Express router
     */
    function initRouters(router){
        try {
            const doc = yaml.load(fs.readFileSync(app.get("apiSpec"), 'utf8'));
            // Server url is stored in a custom attribute in router
            router.path = doc.servers[0].url;
            let routes = [];
            // We use paths section in openapi.yaml
            // paths:
            //    <path>:
            //       <restAction>: [get, post, put, delete]
            //          x-swagger-router-controller: [controller name]
            //          operationId: [method in the controller]
            for (let path in doc.paths) {
                let newPath = transformPath(path);
                const restActions = ['get','post','put','delete'];
                for (const action of restActions) {
                    if (doc.paths[path][action]) {                        
                        let service = doc.paths[path][action]['x-swagger-router-controller'];
                        let method = doc.paths[path][action]['operationId'];
                        router[action](newPath, customControllers[service][method]);
                    }
                }
            }
        } catch (e) {
            console.log(e);
        }
    }
    /**
     * It transforms a yaml path into express router path
     * Parameters in yaml are between {paramId}
     * Parameters in express start with :paramId
     * @param {string} path Represents a path in the yaml file
     * @returns The path in router format
     */
    function transformPath (path) {
        const regex = /{([^}]+)}/g;
        let parameters = path.match(regex);
        let result = path;
        if (parameters){
            
            for (let i=0; i<parameters.length; ++i) {
                let word = parameters[i].slice(1,-1);
                let words = word.split('-');
                for (let j=1; j<words.length; ++j) {
                    let temp = words[j];
                    words[j] = temp.charAt(0).toUpperCase()+temp.slice(1); 
                }
                parameters[i] = ":" + words.join('');
            }
            result = path.replace(regex, ()=> parameters.shift());
        }
        return result; 
    }
    
    const express = require("express");
    
    var router = express.Router();
    // Configure the router
    initRouters(router);
    app.use(router.path, router);
    
    // Add the documentation index stored in api folder and created using Redoc
    app.use('/', express.static('api'));  
};