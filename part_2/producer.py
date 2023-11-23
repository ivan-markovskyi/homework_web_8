import json

from model import Contact
from faker import Faker
import pika

fake = Faker("uk-UA")

EXCHANGE = "hw_8"
QUEUE_NAME = "hw_queue"

credentials = pika.PlainCredentials("guest", "guest")
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct")
channel.queue_declare(queue=QUEUE_NAME, durable=True)
channel.queue_bind(exchange=EXCHANGE, queue=QUEUE_NAME)


def add_contact():
    contact = Contact(fullname=fake.name(), e_mail=fake.email())
    contact.save()


def create_tasks():
    for contact in Contact.objects:
        message = {"id": str(contact.id)}

        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=QUEUE_NAME,
            body=json.dumps(message).encode(),
        )

    connection.close()


if __name__ == "__main__":
    for _ in range(10):
        add_contact()
    create_tasks()
