#! /bin/bash

# need to get the swagger json from the flask server
docker run --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli generate \
    -i /local/swagger.json \
    -l rust \
    -o /local/crates/api_client