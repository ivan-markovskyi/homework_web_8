import json
import os
import sys
import time
from model import Contact

import pika


def send_email() -> None:
    print("Message has been send")


def main():
    credentials = pika.PlainCredentials("guest", "guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()

    QUEUE_NAME = "hw_queue"
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    def callback(ch, method, properties, body):
        message = json.loads(body.decode())
        for contact in Contact.objects:
            if str(contact.id) == message["id"]:
                send_email()
                contact.update(status=True)
        print(f" [x] Received {message}")
        time.sleep(0.5)
        print(f" [x] Completed {method.delivery_tag} task")
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=callback)

    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
