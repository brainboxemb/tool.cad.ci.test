# Selective startup case

Status: transitional — candidate for removal from external acceptance

## Purpose

Prove that inactive targets do not participate in source preparation while an
explicitly selected unsafe target still fails normally.

## Why transitional

This primarily guards a library startup optimization/internal active-closure
boundary. It should live in `lib.py.cad.ci` once equivalent owner coverage is
confirmed.

## Fixture and method

The case generates many unrelated items plus an inactive symlink-owning item,
runs one selected dependency closure, then explicitly selects the unsafe item.

## Failure ownership

`lib.py.cad.ci`. Do not expand this into performance benchmarking here.
