#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *


DATABASE_PATH = "nap.db"
db = SqliteDatabase(DATABASE_PATH, threadlocals=True) # threadlocals allow multiple threads to simultaneously access (write) the db

class NapModel(Model):
	class Meta:
		database = db


class Partition(NapModel):
	pid = PrimaryKeyField()
	#diameter = IntegerField()
	num_nodes = IntegerField()
	num_edges = IntegerField()
	num_artists = IntegerField()
	num_top_artists = IntegerField()
	density = FloatField()


class Node(NapModel):
	nid = PrimaryKeyField()
	pid = ForeignKeyField(Partition, related_name="nodes")
	name = CharField()
	node_type = CharField()
	degree = IntegerField()
	closeness = FloatField()
	#eccentricity = FloatField()
	#betweenness = FloatField()


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
