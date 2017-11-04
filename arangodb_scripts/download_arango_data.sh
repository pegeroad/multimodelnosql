#!/bin/bash

# this script is a piece of the arango import script from https://github.com/weinberger/nosql-tests

# import: POKEC Dataset from Stanford Snap
# https://snap.stanford.edu/data/soc-pokec-readme.txt

if [ ! -f soc-pokec-profiles.txt.gz ]; then
  echo "Downloading PROFILES"
  curl -OL https://snap.stanford.edu/data/soc-pokec-profiles.txt.gz
fi

if [ ! -f soc-pokec-relationships.txt.gz ]; then
  echo "Downloading RELATIONS"
  curl -OL https://snap.stanford.edu/data/soc-pokec-relationships.txt.gz
fi

if [ ! -f soc-pokec-profiles-arangodb.txt ]; then
  echo "Converting PROFILES"
  echo '_key    public  completion_percentage   gender  region  last_login      registration    AGE  pe      my_eyesight     eye_color       hair_color      hair_type       completed_level_of_education or      love_is_for_me  relation_to_casual_sex  my_partner_should_be    marital_status  children     _to_music       the_idea_of_good_evening        I_like_specialties_from_kitchen fun     I_am_going_tousic    cars    politics        relationships   art_culture     hobbies_interests       science_techns       more'  > soc-pokec-profiles-arangodb.txt
  gunzip < soc-pokec-profiles.txt.gz | sed -e 's/null//g' -e 's~^~P~' -e 's~    $~~' >> soc-pokec-pro
fi

if [ ! -f soc-pokec-relationships-arangodb.txt ]; then
  echo "Converting RELATIONS"
  echo '_from   _to' > soc-pokec-relationships-arangodb.txt
  gzip -dc soc-pokec-relationships.txt.gz | awk -F"\t" '{print "profiles/P" $1 "\tprofiles/P" $2}' >>
fi