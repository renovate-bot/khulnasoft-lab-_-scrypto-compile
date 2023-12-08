#!/usr/bin/env bash

echo "Testing hardhat integration of $(realpath "$(which scryto-compile)")"

cd tests/hardhat || exit 255

npm install

if ! scryto-compile .
then echo "Monorepo test failed" && exit 255
else echo "Monorepo test passed" && exit 0
fi
