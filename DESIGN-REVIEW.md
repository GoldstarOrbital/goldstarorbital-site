# Architecture revision B — 2026-09-05

The nine original PNG drawings and original website claims were reviewed. Ten new SVG concept drawings replace the active gallery, with historical originals retained through an explicitly labeled archive. This is a conceptual engineering revision, not a validated spacecraft, fabrication package, or hardware performance report.

## Changes and rationale

- Make the photonic accelerator a hybrid system: electronic scheduling and durable storage, DAC/modulation, optical matrix core, detector/TIA/ADC readout, and calibration. Add an illustrative MZI cell drawing. Remove the unsupported whole-system efficiency multiplier and exaFLOP claim.
- Add a conductive thermal path, radiator, environmental load cases, and phase/temperature feedback. Vacuum does not provide zero heat or automatic millikelvin stability.
- Change the baseline storage node to active minimal electronics with ECC, scrubbing, authentication, health monitoring, and independent survival. Treat optical/quantum persistence as a separate experiment.
- Trade solar/battery for a low-Earth-orbit demonstrator against later radioisotope options. Distinguish electrical output, source heat, isotope decay, converter aging, and qualified mission life. Do not infer 1–5 kg node mass or century-long service life.
- Correct the candidate joint symbol count to 26 ideal bits (8+6+4+8); distinguish labels from recoverable information. Correct decimal capacity scaling at the explicitly hypothetical 10 TB/node assumption.
- Budget local links and the Earth–Mars link independently; add store-and-forward networking, contact windows, and recovery channels. No universal 100 Gbps capability is specified.
- Replace secrecy-based security claims with authentication, authenticated encryption, replay prevention, verified boot, key lifecycle, ECC, replication, and recovery. These are design requirements, not verified controls.
- Preserve satellite-assisted photosynthesis and Mars terraforming as a long-term vision. Show reactor feedstock, dedicated illumination energy, transmission losses, telemetry, and control. Separate oxygenic water oxidation from a generic CO₂-to-O₂ arrow; remove unvalidated yields and timelines.
- Remove named-vendor selections from the revised diagrams; no supplier agreements were verified. Patent descriptions are preserved as owner-provided historical filing notes.

## Evidence and calculations

Primary-source links and context are published in the architecture page's references section: NASA thermal/RPS/DTN/MOXIE material, JPL DSOC, DOE solar fuels, and photonic-computing/optical-memory papers. These do not endorse this architecture. The 2018 NASA terraforming study concerns accessible CO₂ for greenhouse warming, not a test of this satellite system.

First-order calculations are illustrative: emitting area for 100 W at 300 K and emissivity 0.85 is approximately 0.256 m² with an ideal 3 K sink and no absorbed flux. Pu-238 heat fractions are approximately 0.674 at 50 years and 0.454 at 100 years, before conversion degradation. The page does not use these as qualified specifications.

Open work: measured device benchmarks, optical loss/noise and link budgets, component selection, environmental tests, complete mass/power/thermal models, orbit/contact simulation, storage retention/error rates, lifecycle economics, and reactor experiments. No hardware tests or orbital simulations were performed for this revision.

## Rebuild

Requires Python 3.12 or newer; standard library only.

```sh
python scripts/build_schematics.py
python scripts/build_architecture.py
```

Edit the generators for diagram/page changes. `architecture.css`, `architecture.js`, `space.css`, and `space.js` are maintained directly. The architecture generator reuses homepage navigation and footer. The gallery progressively enhances static figures: all diagrams remain readable without JavaScript. Motion has a pause button and respects reduced-motion preferences.

## Verification

Browser checks cover homepage and architecture at 1440, 768, 390, and 320 px; figure selection and wraparound; SVG decoding and label bounds; expanded details; anchor targets; motion pause/resume; reduced motion; and the JavaScript-disabled gallery. Visual renders are reviewed for diagrams and both page layouts. Production verification must check Cloudflare's commit-specific result and both `/architecture` and `/architecture.html` after publishing.
