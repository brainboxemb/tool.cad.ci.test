# Directory output case

Status: current

## Purpose

Prove directory outputs, local repair and fresh-runner CacheDir restoration.

## Public contract

Complete directory trees including empty directories are preserved; missing or
tampered output is restored/repaired; a fresh local state can restore from the
SCons cache.

## Fixture and method

One item owns a generated directory. The case deletes/tampers output and clears
local SCons state while invoking only the public CLI.

## Failure ownership

Output ownership/cache behavior belongs in `lib.py.cad.ci`.
