# 013 directory output

Status: current

## Purpose

Standalone consumer repository for directory outputs, local repair and
fresh-runner CacheDir restoration using a declarative repository-owned builder.

## Public contract

The case proves:

1. complete generated directory trees preserve nested files and empty
   directories;
2. missing directory output is restored without re-running the action;
3. tampered output is repaired to the declared result;
4. a fresh local SCons state can restore the directory output from CacheDir.

The check invokes only the released public CLI.

## Declarative builder contract

The item `ci.yml` contains only identity, kind, builder selection and watch
configuration.

The repository-owned `directory-output` builder owns the executable build
step, implementation script and declared `generated` directory output.

No executable `steps:` or `run:` remain in item or root configuration.

## Failure ownership

Directory-output ownership, repair and cache restoration belong in
`lib.py.cad.ci`.
