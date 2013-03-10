from peewee import *


DATABASE_PATH = "nap.db"
db = SqliteDatabase(DATABASE_PATH)

class NapModel(Model):
    class Meta:
        database = db


class Partition(NapModel):
	pid = PrimaryKeyField()
	diameter = IntegerField()
	num_nodes = IntegerField()
	density = FloatField()


class Node(NapModel):
	nid = PrimaryKeyField()
	pid = ForeignKeyField(Partition, related_name="nodes")
	degree = IntegerField()
	closeness = FloatField()
	eccentricity = FloatField()
	betweenness = FloatField()


def connect():
	db.connect()

def create_tables():
	connect()
	Partition.create_table()
	Node.create_table()

def clear_tables():
	connect()
	rm_partitions = Partition.delete().execute()
	rm_nodes = Node.delete().execute()
	return rm_partitions, rm_nodes
