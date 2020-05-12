import os
import redis

from rq import Worker, Queue, Connection

# Nothing to do here.
# This file starts the Redis worker that handles tasks.
listen = ['high', 'default', 'low']

# This is the address of the Redis docker image.
redis_url = os.getenv('REDISTOGO_URL', 'redis://redis:6379')
conn = redis.from_url(redis_url)

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()
