//const Enforcer = require('openapi-enforcer');
//const EnforcerMiddleware = require('openapi-enforcer-middleware');

const express = require('express');
const bodyParser = require('body-parser');
require("dotenv").config();

const path = require('path');
const jobManager = require('./controllers/jobsRoute/jobsManager.js');

const {
  middleware: openApiMiddleware,
  resolvers,
} = require('express-openapi-validator');

const apiSpec = path.resolve(__dirname, './api/openapi.yaml');

async function initServer() {
  const app = express();
  app.use(bodyParser.urlencoded({ extended: true }));
  app.use(bodyParser.json());
  app.set("apiSpec", apiSpec);


  const cors = require('cors');
  app.use(cors());

  // Any paths defined in your openapi.yml will validate and parse the request
  // before it calls your route code.
  //const enforcerMiddleware = EnforcerMiddleware(await Enforcer(apiyaml));
  //app.use(enforcerMiddleware.init());
  const middleware = openApiMiddleware({
    apiSpec,
    validateRequests: false,
    validateResponses: false, // default false
    // operationHandlers: {
    //   // 3. Provide the path to the controllers directory
    //   basePath: path.join(__dirname, 'controllers'),
    //   // 4. Provide a function responsible for resolving an Express RequestHandler
    //   //    function from the current OpenAPI Route object.
    //   resolver: resolvers.modulePathResolver,
    // },
  });
  app.use(middleware);


  // Catch errors
  // enforcerMiddleware.on('error', err => {
  //   console.error(err);
  //   process.exit(1);
  // });

  //app.set("enforcer", enforcerMiddleware);
  require("./routes/routes.js")(app);

  app.use((err, req, res, next) => {
    // format errors
    res.status(err.status || 500).json({
      message: err.message,
      errors: err.errors,
      status: err.status
    });
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
    app.on("ready", () => {
      const PORT = process.env.NODE_DOCKER_PORT || 3000;
      app.listen(PORT, () => {
        console.log(`Server is running on port ${PORT}.`);
        if (onReady) {
          onReady(app);
        }
      });
    });
    jobManager.startJobManager();
    await initDatabaseConnection(() => app.emit("ready"));
  },
  test: async function (onReady) {
    const app = await initServer();
    app.on("ready", () => {
      onReady(app);
    });
    await initDatabaseConnection(() => app.emit("ready"));
  }
};


