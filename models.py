from peewee import *

db = SqliteDatabase("nap.db")

class Partition(Model):
	pid = PrimaryKeyField()
	diameter = IntegerField()
	num_nodes = IntegerField()
	density = FloatField()

	class Meta:
		database = db

class Node(Model):
	nid = PrimaryKeyField()
	pid = ForeignKeyField(Partition, related_name="nodes")
	degree = IntegerField()
	closeness = FloatField()
	eccentricity = FloatField()
	betweenness = FloatField()

	class Meta:
		database = db