from pyArango.connection import *
from multimodeldao import *


class ArangoDao(MultiModelDao):

    def __init__(self, url, db_name, username, password):
        conn = Connection(arangoURL=url, username=username, password=password)
        self.db = conn[db_name]

    @timecall(immediate=True)
    def get_neighbors_for_node(self, node_key, graph_name):
        aql = "FOR vertex IN OUTBOUND '" + node_key + "' GRAPH '" + graph_name + "' RETURN vertex"
        return self.db.AQLQuery(aql)

    @timecall(immediate=True)
    def get_collection(self, collection_name):
        return self.db.collections[collection_name]

    @timecall(immediate=True)
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

    @timecall(immediate=True)
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

    @timecall(immediate=True)
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

    @timecall(immediate=True)
    def get_leaves(self, vertex_collection, edge_collection):

        aql = """
        FOR prof IN """ + vertex_collection + """
            FILTER LENGTH(FOR e IN OUTBOUND prof """ + edge_collection + """ RETURN 1) == 1 
        RETURN prof
        """
        return self.db.AQLQuery(aql)

    @timecall(immediate=True)
    def get_edge_count(self):
        aql = """
            FOR doc IN relations
                COLLECT WITH COUNT INTO length
            RETURN length
        """
        return self.db.AQLQuery(aql).response['result'][0]

    @timecall(immediate=True)
    def get_node_count(self):
        aql = """
            FOR doc IN profiles
                COLLECT WITH COUNT INTO length
            RETURN length
        """
        return self.db.AQLQuery(aql).response['result'][0]

    @timecall(immediate=True)
    def decrease_not_provided_age(self):
        aql = """
            FOR p IN profiles
                FILTER p.AGE <= 0
                UPDATE p WITH { AGE: p.AGE - 1 } IN profiles
        """
        self.db.AQLQuery(aql)
