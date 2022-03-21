FROM node:16-alpine AS builder-backend
LABEL autodelete-inspice="true"
# Para borrarla luego (tiene que ser a mano)
# list=$(docker images -q -f "dangling=true" -f "label=autodelete-inspice=true")
# if [ -n "$list" ]; then
#      docker rmi $list
# fi
COPY ./package.json .
RUN npm install
COPY ./app app
COPY ./*.js ./
RUN npm run build-deploy
RUN ls -la /build
# El resultado se queda en ./build/

FROM node:16-alpine
WORKDIR /app
#EXPOSE 80
#ENTRYPOINT [ "/sbin/tini","--", "node", "lib/server.js" ]
ENTRYPOINT [ "node", "main.js" ]
RUN chown node:node .
USER node
COPY --from=builder-backend /app/controllers/. ./app/controllers
COPY --from=builder-backend /build/. ./

# FROM node:16

# WORKDIR /api-server
# COPY package.json .
# RUN npm install
# COPY . .
# CMD npm start