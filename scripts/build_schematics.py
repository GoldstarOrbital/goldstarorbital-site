"""Rebuild the original, editable Rev B concept drawings (standard library only)."""
from pathlib import Path
from html import escape
import math
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets' / 'schematics' / 'rev-b'
OUT.mkdir(parents=True, exist_ok=True)
GOLD, BLUE, GREEN, WHITE, DIM = '#dac08a', '#8abac8', '#91b49b', '#f3f1eb', '#a3acad'

def text(x, y, value, size=18, color=WHITE, weight=400):
    return f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" font-weight="{weight}">{escape(value)}</text>'

def lines(x, y, items, size=17, color=DIM, step=27):
    return ''.join(text(x, y+i*step, s, size, color) for i, s in enumerate(items))

def panel(x,y,w,h,title,items=(),color=GOLD):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#111a1e" stroke="#344044"/><path d="M{x+20} {y+1}h45" stroke="{color}" stroke-width="3"/>'+text(x+22,y+37,title,21,color,500)+lines(x+22,y+72,items)

def arrow(x1,y1,x2,y2,color=GOLD,dashed=False):
    dash='stroke-dasharray="6 7"' if dashed else ''
    return f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{color}" stroke-width="2" fill="none" {dash} marker-end="url(#{"blue" if color==BLUE else "gold"})"/>'

def satellite(x,y,scale=1):
    return f'''<g transform="translate({x} {y}) scale({scale})">
    <path d="M-95 -20h-100v80h100 M65 -20h100v80H65" fill="#142830" stroke="{BLUE}"/>
    <path d="M-170 -20v80m25 -80v80m25 -80v80m-75 -40h100m160 0h100m-75 -40v80m25 -80v80m25 -80v80" stroke="#36505a"/>
    <path d="M-75 -55L25 -80 75 -45 -25 -20Z" fill="#293638" stroke="{GOLD}"/>
    <path d="M-75 -55v115l50 35V-20Z" fill="#182326" stroke="{GOLD}"/>
    <path d="M-25 -20L75 -45v115L-25 95Z" fill="#655536" stroke="{GOLD}"/>
    <path d="M-15 -3L60 -21v70L-15 67Z" fill="#111a1e" stroke="{GOLD}"/>
    <circle cx="24" cy="27" r="14" fill="#080d11" stroke="{BLUE}" stroke-width="3"/>
    <path d="M-45 -63v-32m-14 0h28" stroke="{WHITE}" stroke-width="2"/>
    </g>'''

def save(slug,number,title,subtitle,body,note):
    s=f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 760" role="img" aria-labelledby="title desc">
    <title id="title">{escape(title)}</title><desc id="desc">{escape(subtitle+' '+note)}</desc>
    <defs><pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0v40" fill="none" stroke="#ffffff" stroke-opacity=".025"/></pattern>
    <marker id="gold" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4 0 8" fill="{GOLD}"/></marker>
    <marker id="blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4 0 8" fill="{BLUE}"/></marker></defs>
    <rect width="1200" height="760" fill="#0b1115"/><rect width="1200" height="760" fill="url(#grid)"/>
    <g font-family="Arial, Helvetica, sans-serif">{text(45,43,'GOLDSTAR / ORBITAL',14,GOLD,600)}{text(870,43,f'CONCEPT STUDY  /  REV B  /  {number:02}',13,DIM)}
    <path d="M45 62H1155" stroke="#344044"/>{text(45,112,title,34,WHITE,500)}{text(45,147,subtitle,17,DIM)}
    {body}<path d="M45 686H1155" stroke="#344044"/>{text(45,718,note,15,DIM)}{text(45,745,'NOT TO SCALE · PROPOSED SYSTEM · NO FLIGHT PERFORMANCE IMPLIED',11,GOLD)}</g></svg>'''
    (OUT/f'{slug}.svg').write_text(s,encoding='utf-8')

figures=[]
def diagram(slug,title,subtitle,body,note,description):
    number=len(figures)+1
    save(slug,number,title,subtitle,body,note)
    figures.append(dict(src=f'assets/schematics/rev-b/{slug}.svg',title=title,desc=description,number=number))

body=satellite(605,365,1.18)
body+=panel(45,195,310,157,'01 / Power & survival',['Solar + battery for a LEO test','Power source traded per mission','Independent safe-mode rail'])
body+=panel(45,415,310,187,'02 / Thermal path',['Payload → spreader → radiator','MLI limits unwanted heat flow','Sensors close the control loop','Radiator area requires a budget'])
body+=panel(845,195,310,157,'03 / Navigation',['Star tracker + reaction wheels','Fine optical pointing stage','RF recovery / command link'])
body+=panel(845,415,310,187,'04 / Experiment deck',['Photonic accelerator + electronics','ECC storage + flight computer','Isolated optical-terminal mount','Radiation / vibration qualification'])
body+=arrow(355,275,462,310)+arrow(355,475,493,422)+arrow(845,275,685,284)+arrow(845,480,685,405)
diagram('satellite','A spacecraft around the experiment.','Functional layout · solar demonstrator shown; deep-space power remains a trade.',body,'Add a testable flight bus before scaling a constellation. Hardware geometry is illustrative.','A proposed solar-powered demonstrator with battery, thermal control, optical terminal, attitude control, flight computer, and a hybrid photonic payload. The drawing is a functional concept, not a mechanical design.')

body=panel(45,218,255,140,'Electronic input',['ECC memory / DMA','Scheduler + digital logic'],BLUE)
body+=panel(360,218,240,140,'Optical preparation',['DAC + modulator drivers','Laser / wavelength control'])
body+=panel(660,218,220,140,'Photonic core',['Calibrated MZI mesh','Matrix operations'])
body+=panel(940,218,215,140,'Readout',['Detector + TIA','ADC + validation'],BLUE)
for a,b in [(300,360),(600,660),(880,940)]: body+=arrow(a,286,b,286)
body+=panel(45,452,335,157,'Control & calibration',['Temperature / phase feedback','Reference vectors + error checks','Electronic fallback for rejected jobs'])
body+=panel(425,452,335,157,'Measure the whole system',['Laser + converters + memory','Control + compute + cooling','Joules per validated workload'],BLUE)
body+=panel(805,452,350,157,'Benchmark on equal terms',['Same precision and task accuracy','Same I/O and utilization boundary','No inferred exaFLOP rating'])
body+=arrow(210,452,210,375,BLUE,True)+arrow(590,452,770,375,BLUE,True)
diagram('photonic-core','Light does the matrix work.','Hybrid accelerator · electronic memory, conversion, control, and validation remain explicit.',body,'MZI = Mach–Zehnder interferometer · TIA = transimpedance amplifier · DAC / ADC = data converters.','An explicit electronic-to-optical-to-electronic pipeline replaces the zero-conversion assumption. System energy includes lasers, drivers, converters, memory, calibration, and thermal support. Optical component energy alone is not a GPU benchmark.')

body=panel(45,215,500,320,'CONTROLLER / computation & orchestration',['Flight computer and job scheduling','Hybrid photonic accelerator','Optical terminal + RF recovery link','Replicated metadata and command authority','Power, thermal, attitude, and fault management'])
body+=panel(675,215,480,320,'STORAGE NODE / active, minimal compute',['Low-power MCU + authenticated commands','ECC nonvolatile storage + data scrubbing','Optical transceiver / pointing control','Watchdog, power, thermal, and health telemetry','Local safe state during controller loss'])
body+=arrow(545,310,675,310)+arrow(675,425,545,425,BLUE)
body+=text(556,289,'WRITE',13,GOLD)+text(556,451,'ACK / READ',13,BLUE)
body+=text(65,592,'OPTICAL MEMORY RESEARCH',16,GOLD,500)+text(65,624,'Isolated test payload: retention, read fidelity, refresh energy, and environmental tolerance must be measured.',17,DIM)
diagram('storage-node','Separate computation from persistence.','Durable storage is a service with error correction, state, and power requirements.',body,'“Passive” is reserved for truly passive devices; this baseline storage spacecraft is active.','The storage node now has the minimum local electronics needed for authentication, error correction, scrubbing, pointing, and survival. Long-lived optical or quantum storage remains a separate research payload, not the baseline archive.')

body='<ellipse cx="600" cy="410" rx="350" ry="205" fill="none" stroke="#58615a" stroke-dasharray="7 9"/>'
body+='<circle cx="600" cy="410" r="100" fill="#342b24" stroke="#a58960"/>'+text(560,417,'MARS',24,GOLD)
for x,y in [(355,267),(855,277),(350,549),(856,550)]: body+=satellite(x,y,.31)
body+=arrow(422,267,785,277)+arrow(790,550,415,549,BLUE)+arrow(364,306,354,506,BLUE,True)
body+=panel(45,355,245,118,'Earth gateway',['Scheduled contacts','Rate varies with range'],BLUE)
body+=arrow(290,407,333,318,BLUE,True)
body+=panel(920,355,235,118,'Surface user',['Local data products','Independent operations'])
body+=arrow(889,316,958,355,GOLD,True)
body+=text(350,640,'STORE → WAIT FOR CONTACT → FORWARD → VERIFY',17,GOLD)
diagram('network','A network that expects interruptions.','Illustrative topology · contact windows, occultation, and distance drive the design.',body,'Lines show logical paths, not a solved orbital geometry or a guaranteed simultaneous link.', 'A delay-tolerant relay network buffers authenticated data between scheduled contacts. Orbit altitude, coverage, collision risk, pointing, link budget, and station access must be simulated before choosing node counts. Deep-space and local optical links have separate budgets.')

body=panel(45,215,335,180,'01 / Source and storage',['Solar / RPS trade study','Battery for transient loads','End-of-life power allocation','Conversion efficiency + margin'])
body+=panel(435,215,320,180,'02 / Electrical loads',['Laser + accelerator + memory','Avionics + terminal + ADCS','Heaters and fault recovery','Average and peak load cases'])
body+=panel(810,215,345,180,'03 / Heat rejection',['Conduct heat to a radiator','Include absorbed environmental heat','Isolate any RPS waste heat','Verify hot / cold orbital cases'])
body+=arrow(380,305,435,305)+arrow(755,305,810,305)
body+=panel(45,450,525,180,'DECAY IS NOT SERVICE LIFE',['Pu-238 heat fraction: 2^(−t / 87.7 years)','At 50 years: about 67% of initial isotope heat','Electrical output also depends on converter aging'],GOLD)
body+=panel(625,450,530,180,'FIRST-ORDER RADIATOR CHECK',['Q ≈ εσA(T⁴ − Tspace⁴), ideal deep-space view','100 W at 300 K, ε = 0.85 → A ≈ 0.26 m²','Illustration only; absorbed flux and margins omitted'],BLUE)
diagram('power-thermal','Every watt needs a path.','Power and thermal engineering · source heat, electrical output, and useful work are different quantities.',body,'RPS = radioisotope power system · flight mass, lifetime, and power are not specified by this sketch.','Vacuum removes convection, not heat generation. A conductive path and radiator are required. The sample radiator equation is an idealized sizing check, not a flight thermal model; source decay does not certify service lifetime.')

body=panel(45,218,245,190,'Wavelength',['256 candidate states','log₂(256) = 8 bits','Channel spacing / crosstalk'],GOLD)
body+=panel(333,218,245,190,'Phase',['64 candidate states','log₂(64) = 6 bits','Phase noise / calibration'],BLUE)
body+=panel(622,218,245,190,'Polarization',['16 candidate states','log₂(16) = 4 bits','State separability / SNR'],GOLD)
body+=panel(910,218,245,190,'Amplitude',['256 candidate states','log₂(256) = 8 bits','Noise / detector range'],BLUE)
body+=text(62,481,'8 + 6 + 4 + 8 = 26 bits',38,GOLD,500)
body+=lines(62,523,['Formal alphabet count only, assuming independent and distinguishable states.','This does not establish achievable bits per photon, storage capacity, or net link throughput.'],20)
body+=text(62,608,'NEXT MEASUREMENT',14,GOLD)+text(62,641,'Measure symbol errors and mutual information; report net rate after coding and protocol overhead.',18,DIM)
diagram('encoding','Count states. Then measure information.','Correction to the original 32-bit alphabet claim · an ideal count is not a hardware result.',body,'256 × 64 × 16 × 256 = 67,108,864 joint labels = 2²⁶; independence is an unverified assumption.','The original four counts sum to 26 ideal label bits, not 32. Correlated or noisy dimensions can reduce recoverable information. Capacity must be derived from tested storage density, retention, error correction, redundancy, and usable node count.')

body=panel(45,220,290,165,'AUTHORIZE',['Provision device identity','Authenticate each command','Enforce roles + expiry'],GOLD)
body+=panel(455,220,290,165,'PROTECT',['Authenticated encryption','Sequence / replay checks','Bundle integrity across relays'],BLUE)
body+=panel(865,220,290,165,'RECOVER',['Verified boot + signed updates','Key rotation / revocation','Safe-mode command path'],GOLD)
body+=arrow(335,301,455,301)+arrow(745,301,865,301)
body+=panel(45,460,530,155,'Fault-aware storage',['ECC, scrub, replicate, verify before acknowledging','Recover metadata and keys after controller loss'],BLUE)
body+=panel(625,460,530,155,'Link-aware operations',['Pointing and narrow beams reduce exposure','They do not replace cryptography or availability planning'])
diagram('security','Trust is designed into the protocol.','Proposed controls · security comes from verifiable mechanisms, not a secret orbit.',body,'A threat model and implementation review are required before claiming secure operation.','Authenticated, replay-resistant commands, verified boot, key lifecycle management, replicated storage, and independent recovery replace security-by-obscurity claims. Narrow beams do not guarantee non-interception or availability.')

body=panel(45,215,520,330,'BASELINE / orbital data experiment',['Benchmark a hybrid accelerator on Earth','Qualify power, thermal, and radiation behavior','Test optical contacts and durable storage','Fly a small demonstrator before constellation scale','Advance only when measured budgets close'],GOLD)
body+=panel(635,215,520,330,'RESEARCH / surface oxygen production',['Define the chemical reaction and feedstock','Measure reactor energy per mass of oxygen','Compare surface power with beamed delivery','Include pointing, atmosphere, and conversion losses','No yield or terraforming timeline established'],BLUE)
body+=arrow(565,390,635,390,BLUE,True)
body+=text(65,594,'OPTIONAL DATA INTERFACE',15,GOLD)+text(65,629,'Telemetry and experiment scheduling may be shared; reactor power and hardware are separate.',19,DIM)
diagram('research-boundary','Keep the frontier. Bound the claim.','A separate research track protects the compute mission from unproven dependencies.',body,'An oxygen experiment is not a demonstrated planetary atmosphere-generation system.','Oxygen generation is retained as a research direction with its own reactor, energy, mass, efficiency, and logistics budgets. No kg/day or breathable-atmosphere schedule is inferred from an orbital node count.')

body=panel(45,215,320,200,'ORBIT / proposed controller',['Photonic workload optimization','Reactor telemetry + scheduling','Candidate tunable optical source','Dedicated beam-power budget'])
body+=panel(435,215,320,200,'PATH / unvalidated delivery',['Pointing + receiver aperture','Dust / atmosphere / visibility','Optical conversion losses','Compare with local illumination'],BLUE)
body+=panel(825,215,330,200,'SURFACE / contained reactor',['Water + defined reaction pathway','Catalyst or biological system','Oxygen collection + measurement','Feedstock, heat, and power supply'],GREEN)
body+=arrow(365,312,435,312)+arrow(755,312,825,312)
body+=arrow(980,440,980,498,BLUE)+arrow(980,498,205,498,BLUE)+arrow(205,498,205,440,BLUE)
body+=text(405,480,'TELEMETRY / CONTROL FEEDBACK',15,BLUE)
body+=text(65,571,'LONG-TERM VISION: A CONTRIBUTION TO MARS HABITABILITY',18,GOLD)
body+=lines(65,609,['Contained oxygen production would be an early milestone; planet-scale terraforming is not demonstrated.','Atmospheric mass, pressure, temperature, losses, and sustained energy remain separate open problems.'],17)
diagram('photosynthesis','From light to a living-world vision.','Satellite-assisted photosynthesis research · the proposed loop is not a demonstrated capability.',body,'In oxygenic photosynthesis, oxygen originates from water. CO₂ conversion alone is a different pathway.', 'A proposed satellite coordinates a contained surface reactor and studies tuned optical delivery. Telemetry closes the experimental loop. Water oxidation can produce oxygen; catalyst chemistry, feedstock access, energy efficiency, and environmental conditions must be validated before any yield claim. Terraforming remains a long-term vision.')

body=text(65,221,'TWO OPTICAL INPUTS',14,BLUE)+text(960,221,'TWO OUTPUTS',14,BLUE)
body+='<path d="M65 300H295 M65 410H295 M345 300C415 300 400 265 455 265H695C760 265 745 300 805 300 M345 410C415 410 400 445 455 445H695C760 445 745 410 805 410 M855 300H1125 M855 410H1125" fill="none" stroke="#dac08a" stroke-width="3"/>'
body+='<rect x="295" y="276" width="50" height="158" rx="12" fill="#203640" stroke="#8abac8"/><rect x="805" y="276" width="50" height="158" rx="12" fill="#203640" stroke="#8abac8"/>'
body+='<rect x="498" y="245" width="150" height="40" rx="6" fill="#4a4030" stroke="#dac08a"/>'
body+=text(520,272,'Phase φ',21,GOLD)+text(252,482,'Coupler 1',18,BLUE)+text(766,482,'Coupler 2',18,BLUE)
body+=arrow(572,565,572,293,BLUE,True)
body+=panel(45,545,370,105,'Interference sets the split',['Control amplitude mixing via phase'],GOLD)
body+=panel(445,565,310,85,'Calibrated phase driver',[],BLUE)
body+=panel(795,545,360,105,'Tile into a mesh',['Program supported linear transforms'],GOLD)
body+=text(65,337,'x₁',22,WHITE)+text(65,447,'x₂',22,WHITE)+text(1080,337,'y₁',22,WHITE)+text(1080,447,'y₂',22,WHITE)
diagram('interferometer','Inside the photonic building block.','Conceptual 2 × 2 Mach–Zehnder interferometer · waveguide paths and phase control.',body,'A mesh needs further phase controls, calibration, loss modeling, and electronic I/O. Not a fabrication layout.','Two optical inputs are split and recombined through couplers. A controlled relative phase changes interference at the outputs. Arrays of these cells, with additional phase controls and appropriate scaling, can implement supported linear transforms; calibration, finite precision, insertion loss, and drift limit useful performance.')

(OUT/'manifest.json').write_text(json.dumps(figures,indent=2),encoding='utf-8')
print(f'Built {len(figures)} concept diagrams in {OUT}')
