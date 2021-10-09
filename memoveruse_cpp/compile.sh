#!/usr/bin/env bash

g++ -c -fPIC memoveruse_cpp.cpp -o memoveruse_cpp.o
g++ -shared -Wl,-soname,libmemoveruse_cpp.so -o libmemoveruse_cpp.so memoveruse_cpp.o
