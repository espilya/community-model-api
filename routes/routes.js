module.exports = app => {
    const yaml = require('js-yaml');
    const fs   = require('fs');
    
    const customControllers =  {
        Users: require("../controllers/users"),
        Communities: require("../controllers/communities"),
        Similarity: require("../controllers/similarity")
    };
    
    function initRouters(router){
        try {
            const doc = yaml.load(fs.readFileSync('./api/openapi.yaml', 'utf8'));
            let routes = [];
            for (let path in doc.paths) {
                let newPath = transformPath(path);
                const restActions = ['get','post','put','delete'];
                for (const action of restActions) {
                    if (doc.paths[path][action]) {
                        
                        let service = doc.paths[path][action]['x-swagger-router-controller'];
                        let method = doc.paths[path][action]['operationId'];
                        router[action](newPath, customControllers[service][method]);
                        console.log(action,newPath,service,customControllers[service][method]);
                        //push(`router.${action}("${newPath}", ${service}.${method});`);
                    }
                }
            }
        } catch (e) {
            console.log(e);
        }
    }
    
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
    
    
    
    var router = require("express").Router();
    
    // Retrieve a single Tutorial with id
    initRouters(router);
    //router.get("/users/:userId/communities", Users.listUserCommunities);
    //router.get("/communities/:communityId", customControllers.Communities.getCommunityById);
    
    app.use("/", router);
};