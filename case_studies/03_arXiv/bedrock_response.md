# Bedrock Response: Basal Sliding in the Bagley Ice Valley

> Model: us.anthropic.claude-sonnet-4-6 | Tokens: 321 in, 2,048 out | Cost: $0.03

---

# Basal Sliding at Bagley Ice Valley: Context and Mechanisms

## 1. Literature Context for Sliding Speeds and Variability

Your inferred sliding speeds of **40–150 m/yr** are well within the range documented for large temperate valley glaciers, and the ratio of sliding to total motion (~50–75%) is consistent with expectations for warm-based systems of this scale.

### Comparable Measurements from the Literature

**Alaskan systems specifically:**

- **Bering Glacier** (the downstream lobe fed partly by Bagley): Fatland & Lingle (2002, *Journal of Glaciology*, 48(160)) used InSAR to document surface speeds exceeding 200 m/yr during quiescent phases, with sliding inferred to account for the majority of motion. During the 1993–95 surge, speeds reached >10 km/yr, but even inter-surge basal motion was substantial.

- **Gulkana Glacier**: Rabus & Echelmeyer (1997, *Journal of Glaciology*, 43(145), pp. 223–244) measured deformation profiles in boreholes and found that basal sliding contributed roughly 50–80% of surface motion depending on season — a ratio strikingly similar to what you are inferring for Bagley.

- **Columbia Glacier** (a tidewater system, so not a perfect analog, but same climatic region): Meier & Post (1987) and later Howat et al. (2005, *Geophysical Research Letters*, 32, L22502) documented sliding-dominated flow with speeds of 2–10 m/day at peak, but even in slow reaches, sliding dominated over deformation.

**Broader temperate valley glacier literature:**

- **Haut Glacier d'Arolla, Switzerland**: Mair et al. (2001, *Journal of Glaciology*, 47(159), pp. 467–478) used borehole inclinometry combined with surface GPS to partition deformation from sliding. They found sliding contributions of 45–90% depending on subglacial hydrological conditions — directly relevant to your mechanism discussion below.

- **Storglaciären, Sweden**: Hooke et al. (1992, *Journal of Glaciology*, 38(130), pp. 129–144) remains a foundational study showing that for a relatively thin (~250 m) temperate glacier, basal motion accounted for 60–80% of total motion. Scaling to your much thicker ice (650–1200 m), higher deformation velocities are expected (Glen's law gives deformation speed scaling as H^(n+1)), yet sliding still dominates your budget, which is physically coherent.

- **Variegated Glacier** (Alaska, pre-surge): Raymond (1987, *Journal of Geophysical Research*, 92(B9), pp. 9121–9134) is a landmark paper documenting the transition from sliding-dominated to surge motion and is essential reading for any Alaskan glacier dynamics study. Inter-surge sliding was on the order of 50–150 m/yr.

**Quantitative synthesis:**

Cuffey & Paterson (2010, *The Physics of Glaciers*, 4th ed., Chapter 11) synthesize borehole and surface data across many glaciers and suggest that for temperate glaciers with sustained subglacial water, sliding typically accounts for **50–90% of surface velocity**, which brackets your 50–75% estimate well.

---

## 2. Physical Mechanisms Explaining the Sliding Speed Range

Your spatial variability (40–150 m/yr along an 18 km profile) is as interesting as the magnitudes themselves. Several mechanisms operate simultaneously:

### 2a. Hard-Bed Sliding: Regelation and Viscous Flow Around Obstacles

The classical Weertman (1957, *Journal of Glaciology*, 3(21), pp. 33–38) sliding theory describes two complementary mechanisms operating at the bed:

- **Regelation**: pressure melting on the upstream side of obstacles, refreezing downstream. Dominates at **small obstacle wavelengths** (<~1 m).
- **Enhanced viscous creep**: ice deforms around obstacles. Dominates at **large wavelengths**.

For a dominant obstacle size *λ*, sliding speed scales roughly as:

$$u_s \propto \frac{\tau_b^n}{\mathcal{R}}$$

where τ_b is basal shear stress and *R* is a bed roughness parameter. Your varying ice thickness (650–1200 m) along the profile means **τ_b = ρgH sin α** varies by nearly a factor of two, which under n=3 would give roughly an **8× variation in deformation speed** but a more modest variation in sliding if the bed is rough and relatively uniform. The fact that your *sliding* speed varies by only ~4× (40–150 m/yr) across a thickness doubling suggests bed roughness or water pressure variations are modulating what would otherwise be a larger response.

### 2b. Subglacial Water Pressure: The Dominant Control

This is almost certainly the primary explanation for your spatial variability. The **effective pressure** N = P_ice − P_water controls sliding via:

$$u_s = \frac{C \tau_b^p}{N^q}$$

(Budd et al. 1979, *Journal of Glaciology*, 23(89), pp. 157–170; Bindschadler 1983, *Journal of Glaciology*, 29(101), pp. 3–19)

where typical values are p ≈ 3, q ≈ 1. When N → 0 (water pressure approaches ice overburden), sliding becomes unbounded — the physical basis for surging.

**For Bagley specifically**, the subglacial hydrological system is fed by:

1. Surface meltwater routed through moulins and crevasses
2. Geothermal heat (the Wrangell–St. Elias region has elevated geothermal flux in places)
3. Frictional heat from basal motion itself (a positive feedback)

Variations in **subglacial drainage system configuration** along your 18 km profile — between efficient channelized (Röthlisberger) drainage and distributed (linked-cavity or till film) drainage — would produce exactly the kind of along-flow sliding variability you observe. Channelized areas have lower water pressure and slower sliding; distributed areas have higher water pressure and faster sliding.

**Key reference**: Fountain & Walder (1998, *Reviews of Geophysics*, 36(3), pp. 299–328) provide an essential review of subglacial hydrology and its relationship to sliding.

### 2c. Soft Sediment Deformation

If the bed contains deformable till (entirely possible given the heavily glaciated and sediment-rich Wrangell–St. Elias terrain), a portion of "basal motion" may actually be **till deformation** rather than sliding in the strict sense. Iverson et al. (1999, *Geology*, 27(6), pp. 503–506) demonstrated at Storglaciären that till can deform down to ~0.5 m depth and contribute meaningfully to apparent basal motion.

For Bagley, this is speculative without borehole or radar bed-character data, but the **radar bed reflectivity** in existing data (see Muskett et al. below) may give indirect evidence.

### 2d. Ice Thickness Gradient Effects (Longitudinal Stress Coupling)

Along your 18 km profile, thickness varies from 650 to 1200 m. This produces **longitudinal stress gradients** that can transfer driving stress upstream or downstream, decoupling local sliding from local ice thickness. Kamb & Echelmeyer (1986, *Journal of Glaciology*, 32(112), pp. 267–284) showed that effective driving stress should be averaged over a longitudinal coupling length of ~10–20 ice thicknesses. For your system, this is **6–24 km** — comparable to your profile length. This means local sliding speeds need not scale simply with local thickness, which may partly explain spatial patterns you observe.

### 2e. Seasonal and Interannual Variability

If your ITS_LIVE velocities are annual composites, they already integrate over seasonal acceleration events. Temperate Alaskan glaciers commonly show **spring speed-up events** (factor of 2–5× above winter speeds) when surface meltwater first overwhelms drainage capacity. Annual means therefore reflect a time-averaged sliding rate that may mask large seasonal excursions.

---

## 3. Specific Papers and Datasets for Comparison

###
