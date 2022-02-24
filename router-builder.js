const yaml = require('js-yaml');
const fs   = require('fs');

// Get document, or throw exception on error
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
                routes.push(`router.${action}("${newPath}", ${service}.${method});`);
            }
        }
    }
    console.log(routes);
} catch (e) {
    console.log(e);
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