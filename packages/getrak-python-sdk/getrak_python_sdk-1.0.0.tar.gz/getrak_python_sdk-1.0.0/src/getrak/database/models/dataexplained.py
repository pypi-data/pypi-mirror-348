# -*- coding: utf-8 -*-
from mongoengine import *
from mongoengine.fields import DateTimeField

class DataExplained(EmbeddedDocument):
	date = DateTimeField()
	timezone = StringField()
	timezone_type = IntField()