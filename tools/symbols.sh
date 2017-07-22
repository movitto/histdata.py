#!/bin/bash
# Get all symbols
curl -s http://www.histdata.com/download-free-forex-data/?/ascii/1-minute-bar-quotes  |  grep -Po '(?<=href=")[^"]*' | grep -i quotes | grep -o '......$'
