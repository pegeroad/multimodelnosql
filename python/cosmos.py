from gremlin_python.driver.client import Client
from profilehooks import timecall
from multi_model_dao import *


class CosmosDao(multi_model_dao):
    def __init__(self, url, db_name, graph_name, key):
        import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')

        import gremlin_python.driver.serializer

        serializer = gremlin_python.driver.serializer.GraphSONSerializersV2d0()

        self.client = Client(url, 'g', username='/dbs/' + db_name + '/colls/' + graph_name, password=key,
                             message_serializer=serializer)

    def get_neighbors_for_node(self, vertex_key, vertex_label):
        return self.client.submit('g.V().hasLabel("' + str(vertex_label)
                                  + '").has("_key", "' + str(vertex_key) + '").out()').all().result()

    def get_shortest_path(self, vertex_a, vertex_b, vertex_label):
        return self.client.submit('g.V().hasLabel("' + str(vertex_label) + '").has("_key", "'
                                  + str(vertex_a) + '").repeat(out().simplePath()).until(has("_key", "'
                                  + str(vertex_b) + '")).path().limit(1)').all().result()

    def get_distance(self, vertex_a, vertex_b, vertex_label):
        count = self.client.submit('g.V().hasLabel("' + str(vertex_label) + '").has("_key", "'
                                   + str(vertex_a) + '").repeat(out().simplePath()).until(has("_key", "'
                                   + str(vertex_b) + '")).path().limit(1).count(local)').all().result()[0]
        count = count - 1 if count > 0 else count
        return count

    def get_age_group_statistic(self, collection_name):

        result_dict = {
            'gender_1': self.client.submit("g.V().hasLabel('" + str(collection_name)
                    + "').where(values('gender').is(eq(1))).groupCount().by('AGE').order().by(values, decr).as('val').as('k').select('k', 'val').by(keys).by(values)") \
            .all().result()[0],

            'gender_0': self.client.submit("g.V().hasLabel('" + str(collection_name)
                    + "').where(values('gender').is(eq(0))).groupCount().by('AGE').order().by(values, decr).as('val').as('k').select('k', 'val').by(keys).by(values)") \
            .all().result()[0]}

        return result_dict

    def get_leaves(self, vertex_label):
        return self.client.submit("g.V().hasLabel('" + str(vertex_label)
                                  + "').where(outE().count().is(eq(0))).where(inE().count().is(gt(1)))").all().result()


def main():
    uri = 'wss://<app_id>.graphs.azure.com:443/'
    key = '<primary_key>'

    cosmos = CosmosDao(uri, 'graphdb', 'pokec', key)

    # result_set = cosmos.get_neighbors_for_node("P13", "profile")
    # result_set = cosmos.get_shortest_path("P13", "P406", "profile")
    #result_set = cosmos.get_distance("P13", "P405", "profile")
    result_set = cosmos.get_age_group_statistic('profile')
    # ('g.V().hasLabel("profile").has("_key", "P13").out()').all().result()
    # future_results = result_set.all()
    # results = future_results.result()
    print result_set

#("g.V().hasLabel('profile').where(properties('gender').is(1)).values('AGE').groupCount()")\
#("g.V().hasLabel('profile').where(values('gender').is(1)).groupCount().by('AGE').as('countage','genders').select('countage','genders').by(values('AGE').groupCount()).by(values('gender'))")\


# g.V(3).repeat(out().simplePath()).until(hasId(4)).path().limit(1)
# g.V().hasLabel("profile").has("_key", "P13").repeat(out().simplePath()).until(has("_key", "P13")).path().limit(1).count(local)
if __name__ == "__main__":
    main()
    #
