# TODO: for PROD use web pack to build prod and deploy with ngix
FROM mhart/alpine-node:6

RUN apk update && apk upgrade && \
    apk add --no-cache bash curl python g++ make

RUN npm install -g bs-platform
RUN npm install webpack-dev-server -g

# Copy just the package.json first to install deps
WORKDIR /thiccweb
COPY package.json .
RUN npm install

# Now copy the rest
COPY . .
EXPOSE 4000
