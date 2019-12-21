from threading import Thread
from queue import Queue
from app.src.StreamHandler import StreamHandler
from tweepy import Stream
from app.src.Authentication import Authentication


class StreamProducer(Thread):

    def __init__(self,
                 queue: Queue,
                 locations: list,
                 auth: Authentication):
        Thread.__init__(self)

        self.queue = queue
        self.locations = locations
        self.auth = auth
        self.handler = StreamHandler(queue=queue)

    def run(self):
        stream = Stream(auth=self.auth, listener=self.handler)
        while True:
            stream.filter(locations=self.locations)
