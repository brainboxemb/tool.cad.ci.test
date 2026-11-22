# Dependency case

Status: current

## Purpose

Prove dependency traversal, fan-out and explicit downstream execution through
the public released stack.

## Public contract

Dependency changes rebuild required consumers, unrelated consumer changes stay
local, and explicit summary execution makes prerequisites current before the
summary target.

## Fixture and method

A library feeds two consumers and a summary item. The case mutates controlled
inputs and observes public CLI output.

## Failure ownership

Dependency graph/SCons execution belongs in `lib.py.cad.ci`.
