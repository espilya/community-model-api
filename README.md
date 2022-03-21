# SPICE Community Model

The Community Model supports the social cohesion across groups, by the understanding of their differences and recognizing what they have in common. The community model is responsible for storing information about explicit communities that users belong to. Additionally, it creates the implicit communities inferred from user interactions and it computes the metrics needed to define the similarity (and dissimilarity) among group of users. The Community Model will support the recommender system in the variety and serendipity to the recommendation results, that will not be oriented to the typically popular contents or based on providing similar contents to the users (the so called, filter bubble) but to the inter-group similarities and the intra-group differences. 

## Quick start

You can try the Community Model using Docker:

```
docker compose up
```
## Developing

### Built With

#### API server

The API server is implemented using Node.js. Dependencies are available at package.json in the `api-server` folder. Main dependencies are:

- [Express](https://expressjs.com/)
- [express-openapi-validator](https://github.com/cdimascio/express-openapi-validator)
- [mongoose](https://mongoosejs.com/)

#### Database

Database is implemented using [MongoDB](https://www.mongodb.com/)

## Tests

### API server

The CM API server is tested using [Jest](https://jestjs.io/) and [supertest](https://www.npmjs.com/package/supertest). To run the tests, mongodb must be launched, and run the following command in `api-server` folder:

```
npm test
```

## Api Reference

Documentation for the Community Model is available at <https://app.swaggerhub.com/apis-docs/gjimenezUCM/SPICE-CommunityModelAPI/v.1.1>

## License

The content of this repository is distributed under [CC-BY 4.0](https://creativecommons.org/licenses/by/4.0/) license.