import time
import yaml
import os
from app.src.AuthTokens import AuthTokens
from app.src.Authentication import Authentication
from app.src.PostgresConnector import PostgresConnector
from app.src.StreamConsumer import StreamConsumer
from app.src.StreamProducer import StreamProducer
from queue import Queue


if __name__ == "__main__":
    is_local = True

    config_file_path = os.getcwd() + '/config.yaml'

    if os.environ.get('BUILD_ENV') is not None:
        is_local = False

    # Load config variables
    with open(config_file_path , 'r',
              encoding='utf-8') as config_file:
        cfg = yaml.load(config_file,
                        yaml.FullLoader)
    api_keys = cfg.get('api_keys')
    db_options = cfg.get('db_options')
    locations = cfg.get('locations')

    consumer_key = api_keys.get('CONSUMER_KEY')
    consumer_secret = api_keys.get('CONSUMER_SECRET')
    access_token = api_keys.get('ACCESS_TOKEN')
    access_token_secret = api_keys.get('ACCESS_TOKEN_SECRET')

    auth_tokens = AuthTokens(
        consumer_key=consumer_key,
        consumer_secret=consumer_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

    auth = Authentication(auth_tokens)
    postgres_connector = PostgresConnector(db_options=db_options)

    try:
        auth = auth.authenticate()
        connection_pool = postgres_connector.get_connection_pool(min_conn=2, max_conn=8)
        producers = []
        consumers = []

        for location in locations:
            location_queue = Queue(100)
            conn = connection_pool.getconn()
            print('got connection from pool!')
            location_details = locations.get(location)
            c = StreamConsumer(queue=location_queue,
                               db_connection=conn,
                               location_name=location)
            p = StreamProducer(auth=auth,
                               queue=location_queue,
                               locations=location_details)
            producers.append(p)
            consumers.append(c)

        [c.start() for c in consumers]

        for i in range(len(producers)):
            if i == 0:
                producers[i].start()
            else:
                time.sleep(15)
                producers[i].start()

    except Exception as error:
        print(error)

