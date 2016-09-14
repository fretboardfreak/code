#!/bin/bash

rm -rf ~/.config/unity3d/Squad/

pushd ~/.steam/steam/steamapps/common/Kerbal\ Space\ Program/

export LC_ALL=C
export LD_PRELOAD="libpthread.so.0 libGL.so.1"
export __GL_THREADED_OPTIMIZATIONS=1
exec taskset -c 2-3 ./KSP.x86_64

popd
