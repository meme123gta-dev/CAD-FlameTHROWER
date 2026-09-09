# Hardware reference — Amazon tank ASIN B0BSDYNDQP

**Role in this repo:** packing-envelope reference for the theatrical **water-gun**
empty shell only. Do **not** treat this as approval to design a fuel, ignition,
combustion, or pressurized flame system. The shell cavities remain inert
water/fluid packing zones.

## Source

- URL: https://www.amazon.com/dp/B0BSDYNDQP
- ASIN: **B0BSDYNDQP**
- Captured: 2026-08-07 (from live Amazon product page)
- Screenshot evidence: `/opt/cursor/artifacts/amazon_tank_dimensions.webp`,
  `amazon_tank_title.webp`, `amazon_tank_bullets.webp`, `amazon_tank_product_info.webp`

## Listing identity (verbatim / near-verbatim)

| Field | Value |
|-------|-------|
| Title | 10" Gas Tank Aluminum Cylinder Red For Coleman CT200U BT200X Mini Bike \| For Predator 212cc 196cc/6.5HP Engine,For Coleman Powersports CT200U BT200X CT200u-ex Go Kart & Mini Bike Parts |
| Brand | SJVLXHI |
| Manufacturer | SJVLXHI |
| Manufacturer part # | AMFQYMK0238 |
| Model | TANK |
| Material | Aluminum |
| UPC | 730704597451 |

## Exact dimensions (seller-listed)

From Amazon bullet specs and product-description graphic (consistent across title / bullets / image):

| Spec | Value (US) | Value (metric) | Notes |
|------|------------:|---------------:|-------|
| Outer diameter | **3.00 in** | **76.2 mm** | Cylinder OD |
| Length | **10.00 in** | **254.0 mm** | Cylinder length along axis |
| Capacity | **0.31 gal (approx)** | **≈ 1.17 L** | Seller approximate |
| Center outlet | **1/8 in** | **≈ 3.175 mm** NPT-class | Center outlet for hose connection |
| Item weight | **0.56 kg** | **0.56 kg** | Product Information |

Conversion uses `1 in = 25.4 mm` and `1 US gal = 3.785411784 L`.

### Verbatim seller dimension string

> Dimension: 3" Diameter,10" Length,0.31 Gallon (Approx)

> Product Size: 3" Diameter; 10" Length; Fuel Capacity: 0.31 Gallon (Approx.);1/8" center outlet for seamless fuel flow

## Fit note vs current CadQuery shell (Rev B defaults)

| Shell packing parameter | Default | Tank need | Fit? |
|-------------------------|--------:|----------:|------|
| `tank_cavity_length_mm` | 330.0 | 254.0 | Yes (+76 mm spare before clearance) |
| `tank_cradle_diameter_mm` | 210.0 | 76.2 | Yes (cradle oversized; can tighten later) |
| `tank_cavity_width/height_mm` | 220.0 | 76.2 | Yes |

Recommended next-step packing envelope (not yet applied to geometry unless requested):

- Length packing: `254.0 + 2×clearance` mm along tank axis
- Diameter packing: `76.2 + 2×radial_clearance` mm
- Suggested starting clearances: 5–10 mm radial, 10 mm axial (each end) for FDM shell drop-in

## Safety / scope reminder

- Listing is sold as a mini-bike / go-kart **fuel** tank.
- In **this repository**, the dimension set is used only to size an inert
  water/fluid packing cavity in a theatrical/display shell.
- Do not add fuel plumbing, pressurization, ignition, or flame-effect internals.
