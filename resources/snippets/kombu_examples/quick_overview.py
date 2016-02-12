from kombu import Connection, Exchange, Queue

media_exchange = Exchange('media', 'direct', durable=True)
video_queue = Queue('video', exchange=media_exchange, routing_key='video')


def process_media(body, message):
    print body
    message.ack()


# connections
with Connection('amqp://guest:guest@localhost//') as conn:
    # produce
    producer = conn.Producer(serializer='json')
    producer.publish({'name': '/tmp/lolcat1.avi', 'size': 1301013},
                     exchange=media_exchange, routing_key='video',
                     declare=[video_queue])

    # the declare above, makes sure the video queue is declared
    # so that the messages can be delivered.
    # It's a best practice in Kombu to have both publishers and
    # consumers declare the queue.  You can also declare the
    # queue manually using:
    #     video_queue(conn).declare()

    # consume
    with conn.Consumer(video_queue, callbacks=[process_media]) as consumer:
        # Process messages and handle events on all channels
        while True:
            conn.drain_events()

with Connection('amqp://guest:guest@localhost//') as conn:
    # Consume from several queues on the same channel:
    video_queue = Queue('video', exchange=media_exchange, key='video')
    image_queue = Queue('image', exchange=media_exchange, key='image')

    with conn.Consumer([video_queue, image_queue], callbacks=[process_media]) as consumer:
        while True:
            conn.drain_events()
