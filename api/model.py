from api import db
from mongoengine.queryset import queryset_manager


class Group(db.Document):
    name = db.StringField(max_length=50, required=True, primary_key=True)
    full_name = db.StringField(max_length=250, required=True)
    image = db.FileField(default=None)
    members = db.ListField(db.ReferenceField('Individual'), default=None, unique=True)
    memos = db.ListField(db.ReferenceField('Memo'), default=None)

    @queryset_manager
    def specific_objects(doc_cls, queryset, specifier, value):
        if specifier == 'name':
            return queryset.filter(name__iexact=value)
        elif specifier == 'full_name':
            return queryset.filter(ful_name__iexact=value)
        else:
            if value:
                return queryset.filter(image__ne=None)
            else:
                return queryset.filter(image=value)

    def __repr__(self):
        return "%s (%s)" % (self.full_name, self.name)


class Individual(db.Document):
    id_no = db.StringField(max_length=10, required=True, primary_key=True)
    name = db.StringField(max_length=100, required=True)
    image = db.FileField(default=None)
    groups = db.ListField(db.ReferenceField('Group'), default=None)
    memos = db.ListField(db.ReferenceField('Memo'), default=None)

    def equals(self):
        pass

    def __repr__(self):
        return "%s (%s)" % (self.name, self.id_no)


class Position(db.Document):
    position = db.StringField(max_length=50, required=True)
    group = db.ReferenceField(Group, required=True)
    individual = db.ReferenceField(Individual, required=True)

    def __repr__(self):
        return "%s - %s(%s)" % (self.position, self.individual.name, self.group.name)


class Memo(db.Document):
    recipient = db.GenericReferenceField(required=True)
    sender = db.GenericReferenceField(required=True)
    date = db.DateTimeField(required=True)
    subject = db.StringField(max_length=250)
    body = db.StringField()
    priority = db.StringField(max_length=20, required=True)
    status = db.StringField(max_length=10, required=True)
    images = db.ListField(db.FileField(), default=None)

    def __repr__(self):
        return "%s (%s/%s)[%s]" % (self.subject, self.recipient, self.sender, self.date)
