#!/bin/bash

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

if [ ! -f ../data/soc-pokec-profiles.txt ]; then
  echo 'unzip profiles...'
  gunzip < soc-pokec-profiles.txt.gz | sed -e 's/null//g' -e 's~^~P~' >> ../data/soc-pokec-profiles.txt
fi

if [ ! -f ../data/soc-pokec-relationships.txt ]; then
  echo "unzip relations..."
  gzip -dc soc-pokec-relationships.txt.gz | awk -F"\t" '{print "P" $1 "\tP" $2}' >> ../data/soc-pokec-relationships.txt
fi

#echo 'install necessary python modules..'
pip install profilehooks
pip install gremlinpython
pip install futures

echo 'sanitize profile input file...'
sed -i -e 's/\"/ /g' ../data/soc-pokec-profiles.txt
sed -i -e 's/\\/ /g' ../data/soc-pokec-profiles.txt

echo 'remove non ascii characters'
perl -i.bak -pe 's/[^[:ascii:]]//g' ../data/soc-pokec-profiles.txt

echo 'run python import script'
./import_data_to_cosmos.py
