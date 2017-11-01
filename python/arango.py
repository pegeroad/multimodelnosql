from pyArango.connection import *
from profilehooks import timecall
import multi_model_dao



class arango_dao(multi_model_dao):

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


    def get_leaves_in_graph(self, graph_name):
        bind = {
            "graphName": graph_name
        }
        aql = """
        FOR v IN 0..10 INBOUND "worldVertices/world" GRAPH @graphName
            FILTER LENGTH(FOR vv IN INBOUND v GRAPH @graphName LIMIT 1 RETURN 1) == 0
        RETURN CONCAT(v.name, " (", v.type, ")")
        """
        return self.db.AQLQuery(aql, bindVars=bind)

def main():
    arango = arango_dao("http://???:8529", "_system", "??", "??")
    print arango
    db = arango.db

    print db

    profiles = arango.get_collection("profiles")
    # relations = arango.get_collection("relations")

    # neighbors = arango.get_neighbors_for_node('profiles/P19', "pokec")
    shortest_path = arango.get_shortest_path('profiles/P25', 'profiles/P163', 'pokec')
    # distance = arango.get_distance('profiles/P25', 'profiles/P163', 'pokec')
    # P244241

    # print neighbors
    print arango.get_age_group_statistic("profiles")


if __name__ == "__main__":
    main()
