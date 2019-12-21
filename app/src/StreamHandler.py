from tweepy import StreamListener
from queue import Queue
import json
import threading


class StreamHandler(StreamListener):

    def __init__(self,
                 queue: Queue):
        StreamListener.__init__(self)
        self.queue = queue
        self.thread_name = threading.currentThread().getName()
        # self.analyzer = Analyzer()

    def on_connect(self):
        print('{}: Successfully connected to stream!'.format(threading.currentThread().getName()))

    def on_data(self, data):
        json_data = json.loads(data)
        self.queue.put(json_data)
        print('{}: produced tweet with id {}'.format(threading.currentThread().getName(), json_data.get('id')))
        # self.data_processor.process(data=json_data)
        # self.analyzer.analyze_data(json_data['text'])
        return True

    def on_error(self, status):
        print('{}: error with status: {}'.format(threading.currentThread().getName(), status))
        return

    def on_exception(self, exception):
        print('{}: stream exception: {}'.format(threading.currentThread().getName(), exception))
        return
