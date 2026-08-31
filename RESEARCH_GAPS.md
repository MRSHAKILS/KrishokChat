# Research Gaps

## Gap 1

### Gap Title
Direct Regression of Matric Potential (kPa) from Single Field RGB Images Validated Against Tensiometer Ground Truth

### Evidence
Reviewed image-based studies report strong performance when they predict volumetric water content (VWC) in controlled settings. PLOS ONE (2026) achieves R2 = 0.973 with DenseNet121 on iPhone 12 Pro RGB paired with sensors at 3 cm, 10 cm, 15 cm in a greenhouse for ginseng. Zhang et al. (2024) reports R2 = 0.950, RMSE = 1.351% with LG-SWC-R3 on 3,175 cropped images (256×256) of loess soil in a darkroom with controlled lighting. Hossain et al. (2023) reports SVR R2 = 0.96, RMSE = 0.06 on 629 smartphone images from 7 sites in Sydney. MIS-ME (Rakib et al., 2024) reports MAPE = 10.14% for multi-modal RGB + weather fusion. Sensor literature (Sensors, 2023; MDPI, 2024) establishes tensiometers as low-cost (USD 3K-8K), temperature/salinity-insensitive instruments that measure matric potential over 0-100 kPa but fail above 80-85 kPa and require frequent maintenance. No reviewed image-based paper trains or evaluates a model to predict kPa directly from RGB with co-located tensiometer readings as target. Studies either use gravimetric/VWC labels or avoid sensor validation entirely (Indian soils study, 2025, across 5 soil groups and 14 agroecological regions).

### Why Existing Work Falls Short
Existing work optimizes for VWC or classification accuracy in a range that masks agronomic decision thresholds used in Bangladesh AWD practice. VWC requires conversion to matric potential before irrigation scheduling, and that conversion is soil-specific. Lab and greenhouse studies control lighting and exclude non-soil objects, so their feature-to-moisture mapping does not transfer to field conditions where tensiometers operate. Sensor comparison papers document tensiometer limits (85% accuracy, failure in dry and sandy soils) but no image study tests whether surface color and texture encode the same matric signal that the tensiometer measures. This leaves an empirical void: we lack evidence that a single surface RGB frame contains a learnable mapping to kPa under field variability.

### Research Opportunity
Curate paired field RGB and tensiometer time-series for Bangladesh soils and formulate kPa regression as a bounded continuous prediction task (0-100 kPa) with explicit censoring above 80 kPa. Train single-image regressors (e.g., EfficientNetV2, ResNet18 baselines from MIS-ME) with loss functions that respect tensiometer operating limits and evaluate error conditioned on moisture stratum (wet vs. dry) and depth. Compare direct kPa regression against a two-stage VWC→kPa conversion baseline using soil-water retention curves to isolate whether direct prediction reduces propagated error. Include tensiometer maintenance logs as exclusion criteria to avoid fitting instrument failure.

### Expected Impact
A validated RGB→kPa model would connect image estimation to the instrument farmers and extension services already use for AWD decisions. It replaces a controlled-lab VWC proxy with a field-actionable variable, creates a new benchmark target for low-cost deployment, and clarifies the operating envelope where image prediction can substitute for or complement tensiometers. Success would justify single-image inference where installing or maintaining tensiometers is infeasible.

---

## Gap 2

### Gap Title
Illumination- and Debris-Invariant Field RGB Estimation Through Segmentation and Attention Preprocessing

### Evidence
Suud et al. (2026) provides the only field-captured RGB report in the review and documents collapse: CNN accuracy falls from 0.513 (2 classes) to 0.256 (4 classes) and ResNet-50 from 0.487 to 0.205 on 200 in-situ images from rainfed fields, with RMSE 0.433-0.507. Authors attribute failure to inconsistent lighting, shadows, and non-soil objects. Hossain et al. (2023) shows indirect sunlight outperforms direct sunlight and treats lighting as a primary confounder but tests only 38 soil samples without segmentation. Kim et al. (2023) achieves 97.5% accuracy but only after systematic segmentation to 216×216 patches under 6400K CCT controlled lighting with a Canon EOS 100d. Zhang et al. (2024) uses an automated acquisition platform in a darkroom and reports that only 25% of pixels contribute to prediction, which suggests spatial selection matters, but offers no field validation. No study compares a common model with and without explicit soil segmentation or attention-based masking on field images from the same site.

### Why Existing Work Falls Short
The dominant methodology assumes clean soil pixels. Greenhouse, darkroom, and segment-selected inputs remove the two field confounders that dominate error: variable illumination and scene clutter. When those controls are absent, models overfit to brightness rather than moisture (Suud et al.). Existing augmentation is generic (flip, crop) and does not simulate field illumination or occlusions. Attention mechanisms appear only in LG-SWC-R3 (Zhang et al.) under lab conditions, so we lack evidence that attention or segmentation restores performance on field debris and shadow without discarding moisture-relevant texture.

### Research Opportunity
Define illumination and debris invariance as the primary objective rather than a post-hoc observation. Construct a field image pipeline that first isolates soil pixels (learned segmentation or color-space masking) then applies an attention module trained to weight moisture-relevant texture over brightness gradients. Run controlled ablations on a fixed backbone: (a) raw field image, (b) segmented soil only, (c) segmented + photometric augmentation that mimics direct/indirect sunlight variation reported by Hossain et al., (d) segmented + attention. Evaluate on stratified field splits that vary time-of-day and debris presence, report R2 and RMSE per stratum, and quantify pixel retention vs. error trade-off analogous to Zhang's 25% finding. Test whether segmentation reduces cross-device variance across smartphone models.

### Expected Impact
This gap separates sensor-grade accuracy claims from deployable accuracy. If segmentation plus attention recovers a substantial fraction of lab performance on field images, the result redefines minimal preprocessing requirements for farmer-captured photos. If it does not, it establishes a measured upper bound for pure RGB methods under realistic clutter and directs future work toward multi-resolution capture or active illumination control. Either outcome prevents repetition of lab-only evaluations that mask field failure.

---

## Gap 3

### Gap Title
Cross-Soil and Cross-Depth Generalization for Bangladesh Tropical Soils Without Multi-Sensor Fusion

### Evidence
Dataset analysis shows single-soil, single-depth, single-environment bias. Zhang et al. (2024) uses one soil type (loess). Hossain et al. (2023) uses one dominant soil context (Sydney, 7 areas but one region). Kim et al. (2023) uses one soil under controlled conditions. PLOS ONE (2026) is the only study that attempts depth prediction (3 cm, 10 cm, 15 cm) but does so in a greenhouse with sensor data as auxiliary input and Random Forest outperforming DenseNet121 at deeper layers (RF R2 = 0.906 vs. DenseNet surface R2 = 0.973). The Indian soils study (2025) scales across 5 soil groups and 14 regions with interpretable ML and identifies Random Forest as consistently best, but provides no sensor validation and no Bangladesh sites. Bangladesh context appears only in IoT sensor systems: Dey et al. (2024) solar-powered irrigation for rice, Ahmed et al. (2024) sustainable smart irrigation, Sarkar et al. (2024) AWD monitoring at ~USD 42, Das et al. (2025) SoilSense (ESP32 + capacitive + Telegram), and Banna (2024) weather-invariant prediction on 9,000 points with XGBoost R2 = 0.93 for moisture. No reviewed paper evaluates an RGB-only model across multiple Bangladesh soil types or asks whether surface RGB predicts subsurface moisture (10-15 cm) without weather or sensor fusion.

### Why Existing Work Falls Short
Fusion approaches (MIS-ME multi-modal, PLOS ONE image+sensor, Banna weather+soil) improve numbers but entangle image contribution with auxiliary signals that are unavailable in a phone-only deployment. Single-soil studies leave transfer untested, so a model that appears strong on loess or Sydney soils carries no guarantee for Bangladesh alluvial, clay, or silty soils under tropical rainfall and AWD wet-dry cycles. Depth prediction remains fused or absent: we have no estimate of how quickly surface-photograph information degrades with depth or whether surface color retains predictive power for the root zone where irrigation decisions matter.

### Research Opportunity
Design an RGB-only benchmark that isolates soil and depth as generalization axes. Collect surface RGB from multiple Bangladesh soil types and paired gravimetric/tensiometer labels at surface and at 10 cm and 15 cm. Train surface-moisture regressors and test three transfer settings: (a) within-soil, (b) cross-soil (train on N-1 soils, test on held-out soil), (c) cross-depth (train on surface labels, predict subsurface labels). Compare a single-task regressor against a multi-task model that jointly predicts surface and subsurface moisture to test whether shared texture features support depth transfer. Report R2 and RMSE per soil and per depth and include a fusion-free baseline so image contribution is measured without weather or sensor leakage.

### Expected Impact
This gap determines whether a single phone-based model can serve diverse Bangladesh fields or whether soil-specific calibration is required. Measured cross-soil and cross-depth degradation quantifies deployment cost (number of soil-specific models, need for depth-specific heads) before any app is built. A fusion-free benchmark gives the field a lower-complexity reference point against which multi-modal gains (MIS-ME +3.25% over weather-only, +2.15% over image-only) can be judged for actual added value in smallholder settings rather than in instrumented plots.
