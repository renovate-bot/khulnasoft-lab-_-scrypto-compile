#!/usr/bin/env bash

### Test truffle integration

DIR=$(mktemp -d)
cd "$DIR" || exit 255

npm install -g truffle
truffle unbox metacoin
scryto-compile . --compile-remove-metadata

if [ $? -ne 0 ]
then
    echo "Truffle test failed"
    exit 255
fi
# TODO: for some reason truffle output is not deterministc
# The assigned id changes
#cd -
#
#DIFF=$(diff "$DIR/scryto-export/contracts.json" tests/expected/truffle-metacoin.json)
#if [ "$DIFF" != "" ]
#then  
#    echo "Truffle test failed"
#    echo $DIFF
#    exit 255
#fi

