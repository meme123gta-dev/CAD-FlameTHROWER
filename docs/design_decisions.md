# Design Decisions

## Why an empty modular shell first?

Iteration 1 needs printable volume for a ~2.5 gal tank and dual pump footprints before
joints, lids, and mounting ears are finalized. A hollow shell keeps the CadQuery source
as the master while exports stay regenerable.

## Why Havoc-inspired proportions?

The requested silhouette is a long barrel with a thick mid-body and stubby stock.
Those proportions map cleanly onto barrel / receiver / stock modules without copying
game assets or claiming a licensed replica.

## Why left/right halves?

A ~1 m assembled envelope will not fit typical FDM beds. Splitting each module on the
Y=0 plane yields printable halves (~55–155 mm wide) that can be joined along a flat face.

## Why exclusion cavities instead of modeled pumps/tank?

Exact Amazon tank SKU and pump brands are unknown. Parametric cavities with documented
assumptions are safer than inventing fake mounting geometry that will be wrong.

## Why Rev B dual barrel channels?

Flame V3 Tinkercad showed hollow runs through the barrel. For a **water gun**, those map
to (1) a water-nozzle packing bore and (2) an inert low-voltage wiring/sensor conduit.
They must not be interpreted as high-voltage ignition or spark hardware.

## Why a stock motor bay?

V3 placed a cylindrical motor/pump in the rear assembly. Rev B adds a dedicated
cylindrical motor packing bay in the stock, separate from the battery/LV bay, so a
water-pump motor can be staged without inventing sealed plumbing.

## Safety boundary

Exterior shell and inert water/fluid packing envelopes only. Fuel, ignition, combustion,
pressurized-gas for flame effects, high-voltage spark, flame-effect, and weapon systems
are out of scope and must not be added.
