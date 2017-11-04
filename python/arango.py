from pyArango.connection import *
from profilehooks import timecall
from multi_model_dao import *


class ArangoDao(multi_model_dao):

    def __init__(self, url, db_name, username, password):
        conn = Connection(arangoURL=url, username=username, password=password)
        self.db = conn[db_name]

    def get_neighbors_for_node(self, node_key, graph_name):
        aql = "FOR vertex IN OUTBOUND '" + node_key + "' GRAPH '" + graph_name + "' RETURN vertex"
        return self.db.AQLQuery(aql)

    def get_collection(self, collection_name):
        return self.db.collections[collection_name]

    def get_shortest_path(self, node_a, node_b, graph_name):
        bind = {
            "startId": node_a,
            "targetId": node_b,
            "graphName": graph_name
        }
        aql = """
                LET p = ( 
                  FOR v, e IN OUTBOUND SHORTEST_PATH @startId TO @targetId GRAPH @graphName 
                  RETURN {vertex: v, edge: e, weight: (IS_NULL(e) ? 0 : 1)}
                )
                FILTER LENGTH(p) > 0
                RETURN { 
                  vertices: p[*].vertex,
                  edges: p[* FILTER CURRENT.e != null].edge,
                  distance: SUM(p[*].weight)
                }
                """
        return self.db.AQLQuery(aql, bindVars=bind)

    def get_distance(self, node_a, node_b, graph_name):
        bind = {
            "startId": node_a,
            "targetId": node_b,
            "graphName": graph_name
        }
        aql = """
                LET p = ( 
                  FOR v, e IN OUTBOUND SHORTEST_PATH @startId TO @targetId GRAPH @graphName
                  RETURN {weight: IS_NULL(e) ? 0 : 1}
                )
                FILTER LENGTH(p) > 0 
                RETURN {
                  startVertex: @startId,
                  vertex: @targetId,
                  distance: SUM(p[*].weight)
                }
                """
        return self.db.AQLQuery(aql, bindVars=bind)

    def get_age_group_statistic(self, collection_name):
        aql = """
            FOR p IN """ + collection_name + """
                COLLECT ageGroup = FLOOR(p.AGE / 5) * 5,
                        gender = p.gender WITH COUNT INTO numUsers
                SORT ageGroup DESC
                RETURN {
                    ageGroup,
                    gender,
                    numUsers
                }
        """
        return self.db.AQLQuery(aql)

    def get_leaves(self, vertex_collection, edge_collection):

        aql = """
        FOR prof IN """ + vertex_collection + """
            FILTER LENGTH(FOR e IN OUTBOUND prof """ + edge_collection + """ RETURN 1) == 0 &&
            LENGTH(FOR e IN INBOUND prof """ + edge_collection + """ RETURN 1) >= 1
        RETURN prof
        """
        return self.db.AQLQuery(aql)

def main():
    arango = ArangoDao("http://???:8529", "_system", "??", "??")
    print arango
    db = arango.db

    print db

    #profiles = arango.get_collection("profiles")
    # relations = arango.get_collection("relations")

    # neighbors = arango.get_neighbors_for_node('profiles/P19', "pokec")
    #shortest_path = arango.get_shortest_path('profiles/P25', 'profiles/P163', 'pokec')
    # distance = arango.get_distance('profiles/P25', 'profiles/P163', 'pokec')
    # P244241

    # print neighbors
    #print arango.get_age_group_statistic("profiles")

    print arango.get_leaves("profiles", "relations")

if __name__ == "__main__":
    main()
