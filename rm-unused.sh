#!/bin/sh
for file in blog/static/*
do
    file=`basename "$file"`
    if ! (ag "static/${file}" > /dev/null); then
        rm "blog/static/$file"
    fi
done
