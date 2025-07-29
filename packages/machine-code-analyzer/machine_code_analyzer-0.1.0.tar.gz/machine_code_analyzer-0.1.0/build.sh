#!/usr/bin/env bash 

# go into the main source directory
cd src/machine_code_analyzer

cd deps/uiCA
git apply ../uica.patch
./setup.sh
cd ../..

#
cd ../..
