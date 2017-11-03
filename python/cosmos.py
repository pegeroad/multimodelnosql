from gremlin_python.driver import client
import gremlin_python.driver.serializer
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

uri = 'wss:/<app_name>.graphs.azure.com:443/'
key = '<primary_key>'



serializer = gremlin_python.driver.serializer.GraphSONSerializersV2d0()
client = client.Client(uri, 'g', username='/dbs/graphdb/colls/pokec', password=key, message_serializer=serializer)

print "start"


def create_add_vertex_gremlin(line):
    document = json.loads(line)
    gremlin = 'g.addV("profile")'

    for key, value in document.iteritems():
        gremlin = gremlin + '.property("' + str(key) + '", "' + str(value) + '")'
    return gremlin

def create_add_edge_gremlin(line):
    document = json.loads(line)
    gremlin = 'g.V().hasLabel("profile").has("_key", "' + str(document['_from']) \
              + '").addE("knows").to(g.V().hasLabel("profile").has("_key", "' + str(document['_to']) + '"))'
    return gremlin

def process_nodes(db_client):
    with open('..\\transformation\\min_profiles.json') as node_file:
        for line in node_file:
            gremlin = create_add_vertex_gremlin(line)
            print gremlin
            db_client.submit(gremlin)

def process_edges(db_client):
    with open('..\\transformation\\min_relations.json') as edge_file:
        for line in edge_file:
            gremlin = create_add_edge_gremlin(line)
            print gremlin
            db_client.submit(gremlin)


process_edges(client)