#!/bin/bash

# a tool for cleaninig UUIIDs from asset files when imported until that feature is fixed

cd ../assets/CSC330
for f in *; do
    #fnew=${f:6}
    fext=${f: -4}
    fnew=${f%-*.*}${fext}
    mv ${f} ${fnew}
done