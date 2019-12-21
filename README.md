# Twitter stream handler
Connect to the free twitter stream api and filter data by location. Save data in a PostgreSQL db.

## Hints

`psql -h localhost -p 5432 -U postgres -d twitter_db` to query local postgres

## How to run

### Config
Following the template `config.template.yaml`, create a file called `config.local.yaml` for running locally.
For production you will need `config.yaml`. 

To run the project locally:
* `docker-compose -f postgres.compose.yaml up` - run local postgres image (be sure to delete the postgres-data folder to clean DB)
* `python -m app.main` - run python app

Otherwise, just `./scripts/build-and-run.sh` will do just fine.
