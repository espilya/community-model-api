const Enforcer = require('openapi-enforcer');
const EnforcerMiddleware = require('openapi-enforcer-middleware');
const express = require('express');
require("dotenv").config();

const Communities = require('./controllers/Communities');
const Users = require('./controllers/users');

async function run () {
  const app = express();
  
  // Any paths defined in your openapi.yml will validate and parse the request
  // before it calls your route code.
  const enforcerMiddleware = EnforcerMiddleware(await Enforcer('api/openapi.yaml'));
  app.use(enforcerMiddleware.init());
  
  // Catch errors
  enforcerMiddleware.on('error', err => {
    console.error(err);
    process.exit(1);
  }); 
  
  app.get("/", (req, res) => {
    res.json({ message: "Welcome to Community model services" });
  });
  
  require("./routes/routes")(app);
  const PORT = process.env.NODE_DOCKER_PORT || 3000;
  app.listen(PORT, ()=> {
    console.log(`Server is running on port ${PORT}.`);
  });
}

run().catch(console.error);
