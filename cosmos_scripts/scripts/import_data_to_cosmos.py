#!/usr/bin/python

from profilehooks import timecall
import csv
from gremlin_python.driver.client import Client

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CosmosLoader(object):

    def __init__(self, url, db_name, graph_name, key, profiles_path, relations_path):

        self.profiles_path = profiles_path
        self.relations_path = relations_path

        import gremlin_python.driver.serializer

        serializer = gremlin_python.driver.serializer.GraphSONSerializersV2d0()

        self.client = Client(url, 'g', username='/dbs/' + db_name + '/colls/' + graph_name, password=key,
                             message_serializer=serializer)

    @staticmethod
    def create_add_vertex_gremlin(document):
        gremlin = "g.addV('profile')"
        for key, value in document.iteritems():
            if key != None:
                gremlin = gremlin + ".property('" + str(key) + "', '" + str(value) + "')"
        return gremlin

    @staticmethod
    def create_add_edge_gremlin(document):
        gremlin = "g.V().hasLabel('profile').has('_key', '" + str(document["_from"]) \
                  + "').addE('knows').to(g.V().hasLabel('profile').has('_key', '" + str(document["_to"]) + "'))"
        return gremlin

    def process_profiles_from_csv(self):
        csv_file = open(self.profiles_path, 'r')
        fieldnames = ("_key", "public", "completion_percentage", "gender", "region", "last_login", "registration",
                      "AGE", "body", "I_am_working_in_field", "spoken_languages", "hobbies", "I_most_enjoy_good_food",
                      "pets", "body_type", "my_eyesight", "eye_color", "hair_color", "hair_type", "completed_level_of_education",
                      "favourite_color", "relation_to_smoking", "relation_to_alcohol", "sign_in_zodiac",
                      "on_pokec_i_am_looking_for", "love_is_for_me", "relation_to_casual_sex", "my_partner_should_be",
                      "marital_status", "children", "relation_to_children", "I_like_movies", "I_like_watching_movie",
                      "I_like_music", "I_mostly_like_listening_to_music", "the_idea_of_good_evening",
                      "I_like_specialties_from_kitchen", "fun", "I_am_going_to_concerts", "my_active_sports",
                      "my_passive_sports", "profession", "I_like_books", "life_style", "music", "cars", "politics",
                      "relationships", "art_culture", "hobbies_interests", "science_technologies",
                      "computers_internet", "education", "sport", "movies", "travelling", "health", "companies_brands", "more")

        reader = csv.DictReader(csv_file, fieldnames, delimiter='\t')
        for row in reader:
            gremlin = CosmosLoader.create_add_vertex_gremlin(row)
            print gremlin
            self.client.submit(gremlin)

    def process_relations_from_csv(self):
        csv_file = open(self.relations_path, 'r')
        fieldnames = ("_from", "_to")

        reader = csv.DictReader(csv_file, fieldnames, delimiter='\t')
        for row in reader:
            gremlin = CosmosLoader.create_add_edge_gremlin(row)
            print gremlin
            self.client.submit(gremlin)

@timecall(immediate=True)
def process_data():
    uri = 'wss://<app_id>.graphs.azure.com:443/'
    key = '<primary_key>'
    profiles_csv = '../data/soc-pokec-profiles.txt'
    relations_csv= '../data/soc-pokec-relationships.txt'
    cosmos_loader = CosmosLoader(uri, 'graphdb', 'pokec', key, profiles_csv, relations_csv)
    cosmos_loader.process_profiles_from_csv()
    cosmos_loader.process_relations_from_csv()

def main():
    process_data()

if __name__ == "__main__":
    main()
