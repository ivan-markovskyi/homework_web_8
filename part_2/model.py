from mongoengine import connect, Document, StringField, BooleanField

connect(
    db="hw8",
    host="mongodb+srv://mi_user:12344321@micluster.hrtvdum.mongodb.net/?retryWrites=true&w=majority",
)


class Contact(Document):
    fullname = StringField(required=True, unique=True)
    e_mail = StringField(max_length=50)
    status = BooleanField(default=False)
    meta = {"collection": "contacts"}
