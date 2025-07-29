#!/bin/bash

# change package version in Cargo.toml to SEMVER
sed -i '/^\[package\]$/,/^\[/!b;/version = ".*"/ s/version = ".*"/version = "'"$SEMVER"'"/' Cargo.toml

command="maturin build --interpreter ${MATURIN_INTERPRETER} --release --sdist -j ${JOBS} --manylinux 2014 $@"
scl enable llvm-toolset-7.0 "${command}"
