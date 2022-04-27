const express = require('express');
const bodyParser = require('body-parser');
require("dotenv").config();
const path = require('path');

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

  // Openapi validator:
  // Any paths defined in openapi.yml will be
  // validated and parsed by openapi-validator
  // before it calls a route code.
  const middleware = openApiMiddleware({
    apiSpec,
    validateRequests: true,
    validateResponses: true, // default false
  });
  app.use( middleware);

  // Create express routes
  require("./routes/routes.js")(app);

  // Handle errors
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

// Init database connection
async function initDatabaseConnection(onReady) {
  const db = require("./models");
  await db.init(onReady);
}

// Server module exports two functions: run and test
module.exports = {
  /**
   * Init the server, connect with the data base and run the callback function
   * @param {function} onReady callback executed when the server is ready
   */
  run: async function (onReady) {
    const app = await initServer();
    app.on ( "ready",()=> {
      const PORT = process.env.NODE_DOCKER_PORT || 3000;
      app.listen(PORT, ()=> {
        console.log(`Server is running on port ${PORT}.`);
        if (onReady) {
          onReady(app);
        }
      });
    });
    await initDatabaseConnection(() => app.emit("ready"));
  },

  /**
   * Init the server and run the callback function (only for testing purposes)
   * @param {function} onReady callback executed when the server is ready
   */
  test: async function (onReady) {
    const app = await initServer();
    app.on ( "ready",()=> {
      onReady(app);
    });
    await initDatabaseConnection(() => app.emit("ready"));
  }
};


