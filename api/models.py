"""Database models for the Memo API"""

import datetime
import mongoengine
from api import db


class CustomDocument(db.Document):
    meta = {
        'abstract': True
    }

    created_at = db.DateTimeField()
    updated_at = db.DateTimeField(default=datetime.datetime.now().replace(microsecond=0))

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now().replace(microsecond=0)

        self.updated_at = datetime.datetime.now().replace(microsecond=0)
        return super(CustomDocument, self).save(*args, **kwargs)


class Group(db.EmbeddedDocument):
    name = db.StringField(max_length=50)
    full_name = db.StringField(max_length=250)
    image = db.FileField(default=None)
    # members = db.ListField(db.ReferenceField('Individual'), default=None)
    #memos = db.ListField(db.ReferenceField('Memo'), default=None)

    def __repr__(self):
        return "%s (%s)" % (self.full_name, self.name)


class Individual(db.EmbeddedDocument):
    id_no = db.StringField(max_length=10)
    name = db.StringField(max_length=100)
    image = db.FileField(default=None)
    # groups = db.ListField(db.ReferenceField('Group'), default=None)
    #memos = db.ListField(db.ReferenceField('Memo'), default=None)

    def __repr__(self):
        return "%s (%s)" % (self.name, self.id_no)


class Position(db.Document):
    position = db.StringField(max_length=50, required=True)
    # group = db.ReferenceField(Group, required=True)
    #individual = db.ReferenceField(Individual, required=True)

    def __repr__(self):
        return "%s - %s(%s)" % (self.position, self.individual.name, self.group.name)


class Memo(CustomDocument):
    # recipient = db.GenericReferenceField(required=True)
    #sender = db.GenericReferenceField(required=True)
    date = db.DateTimeField(required=True, default=datetime.datetime.now().replace(microsecond=0))
    subject = db.StringField(max_length=250)
    body = db.StringField()
    priority = db.StringField(max_length=20, required=True)
    status = db.StringField(max_length=10, required=True)
    images = db.ListField(db.FileField(), default=None)

    def __repr__(self):
        return "%s (%s/%s)[%s]" % (self.subject, self.recipient, self.sender, self.date)


class User(CustomDocument):
    username = db.StringField(max_length=250, required=True, primary_key=True)
    email = db.StringField(max_length=250, required=True)
    password = db.StringField(max_length=100, required=True)
    user_type = db.StringField(max_length=10, required=True)
    user_profile = db.GenericEmbeddedDocumentField(required=True)

    def __repr__(self):
        return "User %s" % self.username

# Group.register_delete_rule(Individual, 'groups', mongoengine.PULL)
#Individual.register_delete_rule(Group, 'members', mongoengine.PULL)
