# CadQuery Assembly built-in acceptance

Status: current

## Purpose

Black-box the released generic CadQuery built-in when the final global
`model` is a real `cq.Assembly`.

## Public contract

- the consumer selects only `builder: cadquery`;
- a normal `cq.Assembly` is a supported final model form;
- the released stack exports it to the public `model.stl` output;
- identical execution remains CURRENT without restarting the shared reference
  runtime.

## Fixture / method

The fixture creates one centered 10 × 20 × 30 mm CadQuery box, adds it to a
`cq.Assembly`, and exposes that Assembly as global `model`.

The case invokes only the public `cad-ci` CLI already loaded by the released
reusable workflow. It requires the built-in batch to report pass, requires a
non-empty projected STL, then repeats the identical run and requires runtime
reuse.

## Failure ownership

CadQuery model-form/export behavior belongs to `lib.py.cad.ci`.
Workflow/bootstrap or exact-release loading belongs to `tool.cad.ci`.
This repository must not add a local exporter workaround.
