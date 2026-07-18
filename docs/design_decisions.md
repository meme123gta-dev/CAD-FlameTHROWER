# Design Decisions

## Why a two-piece screw-together enclosure?

Serviceable lid retention with heat-set inserts is more durable across repeated openings than PLA snap fits for this sample.

## Why parametric dataclasses?

Named parameters keep the Python source the editable master and allow variants without rewriting geometry operations.

## Why separate base/lid exports?

Manufacturing and slicing treat them as separate printable bodies; assembly composition is handled in `main_assembly.py`.

## Why placeholder modules for bracket/grip?

The repository structure reserves future product families while keeping the first validated sample focused on the enclosure.

## Safety boundary

This sample intentionally models only a low-voltage electronics housing. Fuel, ignition, combustion, and pressure systems are out of scope and must not be added to this geometry.
