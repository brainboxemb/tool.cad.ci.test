# Changed-item selection case

Status: current

The directory name is historical; the contract is changed-item selection.

## Purpose

Prove coarse Git/change-path selection separately from SCons target freshness.

## Public contract

A change owned only by alpha selects/runs alpha, while a shared watched file
selects both alpha and beta.

## Fixture and method

Two independent items plus one shared input are copied to a disposable
repository. The public `plan` and `run --changed` interfaces are observed.

## Failure ownership

Selection/configuration semantics belong in `lib.py.cad.ci`.
