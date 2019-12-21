import threading
import time
from queue import Queue
from app.src.DataProcessor import DataProcessor


class StreamConsumer(threading.Thread):

    def __init__(self,
                 queue: Queue,
                 db_connection: any,
                 location_name: str):
        threading.Thread.__init__(self)
        self.db_connection = db_connection
        self.queue = queue
        self.thread_name = threading.current_thread().getName()
        self.location_name = location_name

        self.data_processor = DataProcessor(connection=self.db_connection)

    def run(self):
        print("{}: Ready to consume".format(threading.currentThread().getName()))
        while True:
            tweet = self.queue.get()
            tweet['location'] = self.location_name
            print("{}: consumed {}".format(threading.currentThread().getName(), tweet.get('id')))
            self.data_processor.process(data=tweet)
            self.queue.task_done()
            time.sleep(0.1)
