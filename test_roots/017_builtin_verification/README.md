# Built-in builder + verification acceptance

Status: current

## Purpose

Black-box the released generic built-in CAD builder and reusable verification
integration through the exact released tool stack.

## Public contract

- `builder: build123d` and `builder: cadquery` are library-owned built-ins;
- compatible models share one immutable `reference` runtime batch;
- root `verification.package` injects one exact released verification wheel;
- item-template `verification.adapter: mesh-geometry` verifies the exported STL;
- repeated identical execution remains CURRENT without another runtime batch;
- one changed shared geometry contract affects both public model items.

## Fixture / method

Both engines create the same centered 10 x 20 x 30 mm box. One shared schema-1
geometry contract checks bounds, volume and watertightness against
`ghcr.io/brainboxemb/cad-reference:v0.3.4`.

The case invokes only the public `cad-ci` CLI exposed by the released reusable
workflow and inspects public model/verification output plus command output.

## Failure ownership

Builder/runtime/batching/configuration failures belong to `lib.py.cad.ci`.
Geometry-contract interpretation belongs to `lib.py.cad.verification`.
Workflow/bootstrap failures belong to `tool.cad.ci`.
