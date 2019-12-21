import psycopg2
from psycopg2 import pool


class PostgresConnector:
    def __init__(self, db_options: dict):
        self.db_options = db_options

    def get_connection_pool(self, min_conn, max_conn):
        try:
            threaded_pool = pool.ThreadedConnectionPool(min_conn, max_conn, **self.db_options)

            if threaded_pool:
                print('Connection pool created successfully!')
                # # Use this method to release the connection object and send back ti connection pool
                # threaded_postgreSQL_pool.putconn(ps_connection)
                # print("Put away a PostgreSQL connection")
                return threaded_pool
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)

    def connect(self):
        """ Connect to the PostgreSQL database server """
        try:
            # read connection parameters
            params = self.db_options

            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params)

            return conn

        except (Exception, psycopg2.DatabaseError) as error:
            raise Exception(error)
        # finally:
        #     if conn is not None:
        #         conn.close()
        #         print('Database connection closed.')
