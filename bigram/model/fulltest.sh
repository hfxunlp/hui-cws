#!/bin/bash

th test.lua
cd test
./runtest.sh
./gscore.sh
cd ..
