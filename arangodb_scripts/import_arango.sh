#!/bin/bash

# This script is inspired by the arango import script from https://github.com/weinberger/nosql-tests 
# However this is massievly refactored, since it uses the new version of ArangoDb.
# We assume here, the reference data are already in place. 
# Data can be produced by the download_arango_data.sh script.

# It can be run using the time ./import_arango.sh command to be able to measure the running time.

ARANGOSH=/usr/bin/arangosh
ARANGOSH_CONF=/etc/arangodb3/arangosh.conf
ARANGOIMP=/usr/bin/arangoimp
ARANGOIMP_CONF=/etc/arangodb3/arangoimp.conf

INPUT_PROFILES=/data/soc-pokec-profiles-arangodb.txt
INPUT_RELATIONS=/data/soc-pokec-relationships-arangodb.txt
APATH=/

sed -i -e "s/# password =/password = $ARANGO_ROOT_PASSWORD/g" $ARANGOSH_CONF
sed -i -e "s/# username =/username =/g" $ARANGOSH_CONF

sed -i -e "s/# password =/password = $ARANGO_ROOT_PASSWORD/g" $ARANGOIMP_CONF
sed -i -e "s/# username =/username =/g" $ARANGOIMP_CONF

cd $APATH

$ARANGOSH --configuration $ARANGOSH_CONF << 'EOF'
  var db = require("org/arangodb").db;
  db._create("profiles");
  db._createEdgeCollection("relations");
  exit
EOF

$ARANGOIMP --configuration $ARANGOIMP_CONF --type tsv --collection profiles --file $INPUT_PROFILES

$ARANGOIMP --configuration $ARANGOIMP_CONF --type tsv --collection relations --file $INPUT_RELATIONS

