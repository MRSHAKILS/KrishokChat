# Demo Images

Real images staged for the live investor demo. **All files are genuine photos from
the project's verified corpora — nothing synthetic, nothing scraped at demo time.**

## Provenance

| Folder | Files | Source |
|--------|-------|--------|
| `rice/` | `leaf_blast.jpg` (Rice Leaf Blast), `brown_spot.jpg` (Rice Brown Spot), `healthy_leaf.jpg` | `backend/ml_assets/vision/test_images/full_library/Rice__*/0001.jpg` — originals from the released crop-disease corpus |
| `potato/` | `late_blight.jpg`, `early_blight.jpg`, `healthy_leaf.jpg` | `backend/ml_assets/vision/test_images/full_library/Potato__*/0001.jpg` |
| `tomato/` | `late_blight.jpg`, `healthy_leaf.jpg` | `backend/ml_assets/vision/test_images/full_library/Tomato__*/0001.jpg` |
| `soil/` | `P0001_Doash_8.0kpa.jpg`, `P0064_Bele_0.0kpa.jpg`, `P0406_Atel_16.5kpa.jpg` | `frontend/public/assets/soil_samples/` — real field images from the released soil-moisture dataset |

## How to use during the demo

- **Easiest:** the /detect page has a built-in sample button (`ধানের পাতার নমুনা নিন`)
  which loads `frontend/public/assets/close_rice.jpg` with the crop pre-selected
  (rice). Use it if you want zero file-drag risk.
- **Alternative:** drag `rice/leaf_blast.jpg` from this folder into the intake zone
  and select **ধান** in the crop selector (the crop classifier has no rice class;
  the crop is declared by the farmer and routes to the rice disease model).
- **Soil:** the /soil page has its own built-in samples (দোআঁশ/বেলে/এঁটেল). The
  copies here are a fallback for the "pick your own photo" story.

> The wheat disease test images in `wheat_disease/` are augmented variants of real
> photos; the originals in `full_library/` above were preferred for the demo.

## Support boundary

Tomato images are retained as **unsupported-routing examples**, not as guaranteed
diagnosis demos. The crop classifier can emit the broad `Solanacea` class, but the
checked-in registry currently has no `solanacea`/tomato disease model. A reviewer
asking about tomato should be shown the explicit `no_disease_model` boundary rather
than a fabricated tomato diagnosis. Supported disease-model families currently
registered by the backend are rice, wheat, corn, potato, and brassica.
