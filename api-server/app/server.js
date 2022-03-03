const Enforcer = require('openapi-enforcer');
const EnforcerMiddleware = require('openapi-enforcer-middleware');
const express = require('express');
require("dotenv").config();

const apiyaml = "./app/api/openapi.yaml";

async function initServer() {
  const app = express();
  app.use(express.json()); // for parsing application/json
  app.use(express.urlencoded({ extended: true })); // for parsing application/x-www-form-urlencoded

  // Any paths defined in your openapi.yml will validate and parse the request
  // before it calls your route code.
  const enforcerMiddleware = EnforcerMiddleware(await Enforcer(apiyaml));
  app.use(enforcerMiddleware.init());

  // Catch errors
  enforcerMiddleware.on('error', err => {
    console.error(err);
    process.exit(1);
  });

  app.set("enforcer", enforcerMiddleware);
  require("./routes/routes.js")(app);

  app.use((err, req, res, next) => {
    if (err.statusCode >= 400 && err.statusCode < 500 && err.exception) {
      res.set('Content-Type', 'text/plain');
      res.status(err.statusCode);
      res.send(err.message);
    } else {
      console.error(err.stack);
      res.sendStatus(err.statusCode || 500);
    }
  });
  return app;
}

async function initDatabaseConnection(onReady) {
  const db = require("./models");
  await db.init(onReady);
}

module.exports = {
  run: async function (onReady) {
    const app = await initServer();
    app.on ( "ready",()=> {
      const PORT = process.env.NODE_DOCKER_PORT || 3000;
      app.listen(PORT, ()=> {
        console.log(`Server is running on port ${PORT}.`);
        if (onReady) {
          onReady();
        }
      });
    });
    await initDatabaseConnection(() => app.emit("ready"));
  }
};


