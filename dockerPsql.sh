source .env
docker exec -it thiccbot_postgres_1 psql -U $THICC_USER -w $THICC_PASSWORD -d $THICC_DB