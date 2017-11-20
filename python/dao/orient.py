import pyorient
from multimodeldao import *


class OrientDao(MultiModelDao):

    def __init__(self, db_name, hostname, port=2424, username="root", password="rootpwd"):
        self.client = pyorient.OrientDB(hostname, port)
        self.client.db_open(db_name, username, password)

    @timecall(immediate=True)
    def get_neighbors_for_node(self, node_key, graph_name):
        query = "select from (TRAVERSE out('" + graph_name + "') FROM (select @rid from Profile where _key='" \
                + node_key + "' LIMIT 1) MAXDEPTH 1) WHERE $depth=1"
        return self.client.query(query)

    @timecall(immediate=True)
    def get_shortest_path(self, node_a, node_b, graph_name):
        query = """
              select expand(path) from (select shortestPath( $a.rid, $b.rid) as path
                LET $a = (select @rid from """ + graph_name + """ where _key='""" + node_a + """' LIMIT 1), 
                $b = (select @rid from """ + graph_name + """ where _key='""" + node_b + """' LIMIT 1) 
                UNWIND path)
              """
        return self.client.query(query)

    @timecall(immediate=True)
    def get_distance(self, node_a, node_b, graph_name):
        query = """
              select count(*) from (select shortestPath( $a.rid, $b.rid) as path
                LET $a = (select @rid from """ + graph_name + """ where _key='""" + node_a + """' LIMIT 1), 
                $b = (select @rid from """ + graph_name + """ where _key='""" + node_b + """' LIMIT 1) 
                UNWIND path)
              """
        result = self.client.query(query)
        return result[0].oRecordData['count']

    @timecall(immediate=True)
    def get_age_group_statistic(self, collection_name):
        query = """
            select expand($c)
            let $a = (select groupedAge, count(*), gender from (select eval("(AGE / 5) * 5") as groupedAge, gender from """ \
                + collection_name + """ where gender=1) group by groupedAge), 
            $b = (select groupedAge, count(*), gender from (select eval("(AGE / 5) * 5") as groupedAge, gender from """ \
                + collection_name + """ where gender=0) group by groupedAge),
            $c = unionAll( $a, $b )
            """
        return self.client.query(query)

    @timecall(immediate=True)
    def get_leaves(self, vertex_collection, edge_collection):
        query = """
            SELECT * from (SELECT _key, bothE('""" + edge_collection + """').size() AS friendCount FROM """ + vertex_collection + """) 
            where friendCount<=1
            """
        return self.client.query(query)

    @timecall(immediate=True)
    def get_edge_count(self):
        query = "select count(*) from Relation"
        return self.client.query(query)[0].oRecordData['count']

    @timecall(immediate=True)
    def get_node_count(self):
        query = "select count(*) from Profile"
        return self.client.query(query)[0].oRecordData['count']

    @timecall(immediate=True)
    def decrease_not_provided_age(self):
        query = "update Profile INCREMENT AGE=-1 WHERE AGE<=0"
        return self.client.query(query)
