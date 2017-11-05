#!/bin/bash

# This script is inspired by the arango import script from https://github.com/weinberger/nosql-tests 
# However, the JSON files are refactored and the structure of the scipt as well.
# We assume here, the reference data are already in place. 
# Data can be produced by the download_orient_data.sh script.

# It can be run using the 'time ./import_orient.sh' command to be able to measure the running time.

sed -i -e "s/@RootPassword/$ORIENTDB_ROOT_PASSWORD/g" /orientdb/data/profiles-etl.json
sed -i -e "s/@RootPassword/$ORIENTDB_ROOT_PASSWORD/g" /orientdb/data/relations-etl.json

cd /orientdb/bin

./oetl.sh /orientdb/data/profiles-etl.json
./oetl.sh /orientdb/data/relations-etl.json
