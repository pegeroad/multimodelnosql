import pyorient
from multi_model_dao import *


class orient_dao(multi_model_dao):

    def __init__(self, db_name, hostname, port=2424, username="root", password="root"):
        self.client = pyorient.OrientDB(hostname, port)
        self.client.db_open(db_name, username, password)

    def get_neighbors_for_node(self, node_key, graph_name):
        query = "select from (TRAVERSE out('" + graph_name + "') FROM (select @rid from Profile where _key='" \
                + node_key + "' LIMIT 1) MAXDEPTH 1) WHERE $depth=1"
        print query
        return self.client.query(query)

    def get_shortest_path(self, node_a, node_b, graph_name):
        query = """
              select expand(path) from (select shortestPath( $a.rid, $b.rid) as path
                LET $a = (select @rid from """ + graph_name + """ where _key='""" + node_a + """' LIMIT 1), 
                $b = (select @rid from """ + graph_name + """ where _key='""" + node_b + """' LIMIT 1) 
                UNWIND path)
              """
        return self.client.query(query)

    def get_distance(self, node_a, node_b, graph_name):
        query = """
              select count(*) from (select shortestPath( $a.rid, $b.rid) as path
                LET $a = (select @rid from """ + graph_name + """ where _key='""" + node_a + """' LIMIT 1), 
                $b = (select @rid from """ + graph_name + """ where _key='""" + node_b + """' LIMIT 1) 
                UNWIND path)
              """
        result = self.client.query(query)
        return result[0].oRecordData['count']

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

    def get_leaves(self, vertex_collection, edge_collection):
        query = """
            SELECT * from (SELECT _key, bothE('""" + edge_collection + """').size() AS friendCount FROM """ + vertex_collection + """) where friendCount<=1
            """
        return self.client.query(query)

def main():
    orient = orient_dao("plocal:pokec", "??")
    #shortestPath = orient.get_shortest_path('P7', 'P318', 'Profile')

    #print shortestPath[0]
    count = orient.get_distance('P7', 'P318', 'Profile')
   # print orient.get_neighbors_for_node('P7', 'Relation')[0]
    #print shortestPath[0].oRecordData['shortestPath'][0]
    print orient.get_leaves()


if __name__ == "__main__":
    main()
