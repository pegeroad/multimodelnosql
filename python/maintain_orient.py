from __future__ import division
import json
import csv
import pyorient

def init_db():
    db_name = "plocal:pokec"
    client = pyorient.OrientDB("??", 2424)
    client.db_open( db_name, "??", "??" )
    return client


def process_nodes(db_client):
    with open('..\\min_profiles.json') as node_file:
        for line in node_file:
            co = 'CREATE VERTEX Profile CONTENT ' + line
            print co + '\n'
            db_client.command(co)

def process_edges(db_client):
    with open('..\\min_relations.json') as node_file:
        for line in node_file:
            fromquery, toquery = create_inner_queries(line)
            co = 'CREATE EDGE Relation FROM (' + fromquery + ') TO (' + toquery + ')'
            print co + '\n'
            try:
                db_client.command(co)
            except pyorient.exceptions.PyOrientCommandException as e:
                print "couldn't perform query: " + co



def get_edge_endpoints(line):
    line_json = json.loads(line)
    return line_json['_from'], line_json['_to']

def create_inner_queries(line):
    fromid, toid = get_edge_endpoints(line)
    return "SELECT FROM Profile WHERE _key='" + fromid + "' LIMIT 1", \
           "SELECT FROM Profile WHERE _key='" + toid + "' LIMIT 1"

def convert_profiles_csv_to_json():
    csvfile = open('..\\orient_min_profiles.csv', 'r')
    jsonfile = open('..\\min_profiles.json', 'w')

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

    reader = csv.DictReader(csvfile, fieldnames, delimiter='\t')
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')

def convert_relations_csv_to_json():
    csvfile = open('..\\orient_min_relations.csv', 'r')
    jsonfile = open('..\\min_relations.json', 'w')

    fieldnames = ("_from", "_to")

    reader = csv.DictReader(csvfile, fieldnames, delimiter='\t')
    for row in reader:
        json.dump(row, jsonfile)
        jsonfile.write('\n')

def create_profile_class(db_client):
    db_client.command("CREATE CLASS Profile EXTENDS V CLUSTERS 1")

def create_profile_class(db_client):
    db_client.command("CREATE CLASS Relation EXTENDS E")

def create_properties(db_client):
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
    properties = ("STRING", "INTEGER", "INTEGER", "INTEGER",
                  "STRING", "DATETIME", "DATETIME", "INTEGER",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING", "STRING",
                  "STRING", "STRING", "STRING")
    i = 0
    while i<properties.__len__():
        db_client.command("CREATE PROPERTY Profile." + fieldnames[i] + " " + properties[i])
        i = i + 1

def create_index_for_profiles(db_client):
    db_client.command("CREATE INDEX Profile._key UNIQUE_HASH_INDEX")

db_client = init_db()
#create_profile_class(db_client)
process_edges(db_client)


#convert_relations_csv_to_json()

#db_client.command("ALTER DATABASE custom strictSQL=false")
#create_profile_class(db_client)
#create_properties(db_client)

#process_nodes(db_client)

print "hello"
#process_nodes(db_client)
#process_edges(db_client)
