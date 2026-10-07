# 04: Reusable materials (photos, open data, libraries, fonts)

Research date: **2026-10-07**. Method: Wikimedia Commons API (`imageinfo` + `extmetadata`) run from the sandbox; WebFetch of Pexels/Unsplash pages; npm registry and jsDelivr file listings; `git ls-remote` plus raw `LICENSE` files; fontTools glyph checks on downloaded font files.
Test downloads are only in `scratchpad/assets-test/` (nothing went into the repo).
Legend: **[V]** = I opened or downloaded it myself. **[V-dl]** = a file download with curl worked. **[U]** = not verified (stated in a source only).

---

## 0. TL;DR

1. **Photos.** Commons has **real Central-European residential and compact rigs**: Hungary on a grass plot, Minsk among houses, Hamburg, a Czech garden casing, Kołobrzeg ZiŁ, Unimog/Atego rigs. Pexels has the best "drilling next to houses" shots (Freek Wolsink, Netherlands, 3888×2592). Also found: Poznań-county landscapes (Kicin, Rogalinek, an aerial of Żydowo in gm. Rokietnica from 08.2026), a real well screen with a submersible pump plus a strata board (Wasserwerk Weiler), and PVC pipes and clear water.
2. **Download quirk.** Commons **originals return HTTP 429 from the sandbox**. Standard thumbnail sizes work: `Special:FilePath/<name>?width=1920` or `2560` (2560 snaps to 3840). Pexels originals download fine (`images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg`). Unsplash CDN works (`images.unsplash.com/photo-…?w=3000`), but the unsplash.com pages/API are behind bot protection.
3. **Groundwater data exists and is usable.** The PIG-PIB ArcGIS REST service `hydrogeologia/gzwp` returns **GeoJSON in EPSG:4326**. For the Poznań bbox it returns GZWP **143, 144, 145, 139, 146, 150**. The metadata says "Brak warunków dostępu i użytkowania". `hydrogeologia/cbdh_otwory` has **5 608 CBDH boreholes** in the Poznań-county bbox, with depth, year, stratigraphy and locality. **Caveat:** Incapsula WAF blocks almost every request from this sandbox (403). I verified the data through WebFetch, which uses a different egress. So fetch the files once on a dev machine (URLs in §2) and commit them as static GeoJSON.
4. **GUGiK works from the sandbox.** PRG WFS (powiat/gmina boundaries, GML) and NMT shaded-relief WMS GetMap both respond. I downloaded both.
5. **Libraries:** GSAP 3.15 (all plugins incl. SplitText/ScrollSmoother/MorphSVG, free "standard no-charge license"), Lenis 1.3.26 (MIT, UMD), `@paper-design/shaders` (Apache-2.0, includes a ready **water** shader, grain-gradient, paper-texture), d3-geo + topojson-simplify (ISC, UMD), OGL (Unlicense), Equinor **esv-intersection** (MIT, a wellbore/strata cross-section lib that needs a bundler or import map).
6. **Fonts with verified Polish glyphs (ąćęłńóśźż + caps):** Big Shoulders, Archivo (wdth axis), Martian Mono, Mona Sans/Hubot Sans, Tektur, Space Grotesk, Barlow Condensed, Unbounded (all OFL). Velvetyne: Lineal, Sporting Grotesque, Grotesk, BackOut, Sligoil (OFL). Velvetyne Format 1452, AMDAL, Facade and Compagnon **lack Polish glyphs**. Fontshare's FFL 2.0 allows self-hosting but **forbids subsetting/format conversion**.

---

## 1. Photos

Licence notes:
- **CC BY / BY-SA:** credit "Author, licence, link" next to the photo or in a credits page. Under BY-SA, a *modified image* (crop + colour grade is arguably an adaptation) must itself be released under BY-SA. The page around it is not affected.
- **CC0 / PD:** no conditions.
- **Pexels / Unsplash licence:** free commercial use, no attribution required (but nice to give). You may not sell unaltered copies, and you may not imply endorsement by people shown.

### 1a. Drilling rigs, drilling on plots (most important)

| # | What it shows | Direct file URL | Author | Licence | Resolution | Verified-download | Notes |
|---|---|---|---|---|---|---|---|
| P1 | Crawler water-drilling rig (blue ECO-WELL unit) on a street next to brick terraced houses, crew working, sunny | https://images.pexels.com/photos/31249536/pexels-photo-31249536.jpeg (page: https://www.pexels.com/photo/construction-worker-operating-drilling-machine-outdoors-31249536/) | Freek Wolsink | Pexels | 3888×2592 | **yes, full original 1.9 MB [V-dl]** | **Best hero candidate.** Residential European context. NL houses look close to PL suburbs. |
| P2 | Same site: two workers at the rig with mud hoses and the mud tank | https://images.pexels.com/photos/31249554/pexels-photo-31249554.jpeg (page …/construction-workers-operating-heavy-machinery-outdoors-31249554/) | Freek Wolsink | Pexels | 3888×2592 | yes (600px thumb) [V] | Good "proces" section image. |
| C11 | Orange/red truck rig (Hungarian water utility) on a grassy plot with trees, pipes on the ground, worker | https://upload.wikimedia.org/wikipedia/commons/7/70/Baktal%C3%B3r%C3%A1nth%C3%A1za%2C_Hungary_-_panoramio_%2841%29.jpg | Szemes Elek | CC BY-SA 3.0 | 1790×1164 | thumb yes; original 429 from sandbox | **Looks most like a Wielkopolska plot.** Low resolution, so use it at ≤1200px. Sister shots: `…_(42).jpg` 1822×1226, `…_(54).jpg` 1823×1226. |
| C01 | Small truck rig in a suburban street of single-family houses (Minsk, 05/2023), pipes on the verge | https://upload.wikimedia.org/wikipedia/commons/7/7b/2023.05.25_Well_Drilling_in_Tsna_Minsk_Belarus.jpg | Rabbi Mendl | CC BY-SA 4.0 | 3024×4032 (portrait) | thumb yes [V] | Rig is small in frame. Good portrait crop for mobile. |
| C02 | Drinking-water exploratory drilling, Hamburg: mast between trees, yellow container | https://upload.wikimedia.org/wikipedia/commons/5/52/Trinkwasserbohrung_in_Hamburg.jpg | Karbohut | CC BY-SA 4.0 | 3888×5184 | **yes, 1920px thumb [V-dl]** | Green and calm, a good background texture. |
| C03 | Drilled well casing (black pipe) in a garden lawn after drilling "without heavy machinery", bucket of cuttings (Czech) | https://upload.wikimedia.org/wikipedia/commons/5/51/Vrt_studny.jpg | Anebilbo | CC BY-SA 4.0 | 1800×2326 | thumb yes [V] | Real "after" picture on a private plot, ø145 mm. |
| C10 | Klemm KR 805-2W yellow crawler rig on a muddy urban site | https://upload.wikimedia.org/wikipedia/commons/6/61/Klemm_KR_805-2W_IMG_0419_%28Nemo5576%29.JPG | Nemo5576 | CC BY 3.0 | 2592×1944 | thumb yes [V] | Compact rig, the type small firms use. |
| C07 | Old ZiŁ-131 drilling truck, geological drilling in **Kołobrzeg (PL)** | https://upload.wikimedia.org/wikipedia/commons/8/89/Ko%C5%82obrzeg_-_Zi%C5%81_wiertnik.jpg | Radosław Drożdżewski (Zwiadowca21) | CC BY-SA 3.0 | 3008×2000 | thumb yes [V] | Polish, retro. Good for an "experience since…" section. |
| C06 | GAZ-66 with a water-well drilling rig parked by a house (Bicske, HU) | https://upload.wikimedia.org/wikipedia/commons/6/61/GAZ-66%2C_Kertv%C3%A1ros%2C_2017_Bicske.jpg | Globetrotter19 | CC BY-SA 3.0 | 1600×1200 | thumb yes [V] | Description explicitly says "water well drilling rig". |
| C08 | Unimog-based vertical drill, mast lowered, urban street (DE) | https://upload.wikimedia.org/wikipedia/commons/a/a5/Unimog-based_drilling_machine_%283%29.JPG | High Contrast | CC BY 3.0 DE | 4608×3072 | thumb yes [V] | Sharp and detailed. |
| C09 | Mercedes Atego truck drilling rig (DE), mast up | https://upload.wikimedia.org/wikipedia/commons/2/28/Mercedes_Benz_Atego_-_Bohranlage_%281%29.jpg | High Contrast | CC BY 3.0 DE | 2570×3590 | thumb yes [V] | Portrait. |
| C05 | Dutch army water-drilling unit mast in a heath, sheep flock in foreground (Bargerveen 2020) | https://upload.wikimedia.org/wikipedia/commons/9/9b/Oefening_Bargerveen_04.jpg | Ministerie van Defensie / sgt. Cristian Schrik | **CC0** | 5250×3500 | thumb yes [V] | Only CC0 rig photo. Military context, rural feel. |
| C04 | Simco 5000 truck-mounted water-well rig (US) | https://upload.wikimedia.org/wikipedia/commons/8/82/Water_well_drilling_rig.jpg | Mcfly05 | CC BY-SA 4.0 | 3264×2448 | thumb yes [V] | Clean side view. US truck, so it looks less local. |
| P3 | Water-well rig at night under work lights, worker (India) | https://images.pexels.com/photos/21047659/pexels-photo-21047659.jpeg | Rahul Bokhare | Pexels | 3000×4000 | thumb yes [V] | Dramatic and dark. Good for a "praca 24h" or dark-mode hero. |
| P4 | Auger/drill head in sandy soil, close-up | https://images.pexels.com/photos/14840752/pexels-photo-14840752.jpeg | iwashere | Pexels | 4608×3456 | thumb yes [V] | Macro detail for section dividers. |
| P5 | Crawler rig with dust cloud, operator (cloudy) | https://images.pexels.com/photos/15391048/pexels-photo-15391048.jpeg | Ulrick T | Pexels | 4000×6016 | thumb yes [V] | Portrait, gritty. |
| U1 | Tall drilling derrick in a ploughed field, grey sky | https://images.unsplash.com/photo-1712069951097-b37e02e372fb (page: https://unsplash.com/photos/a-drilling-rig-in-the-middle-of-a-field-laDsdizvnIs) | Natalia Grela | Unsplash | 3000×2000 at `?w=3000` | **yes [V-dl]** | It is an **oil/gas derrick**, not a water rig. Use only as moody atmosphere. |

### 1b. Casing, pipes, pump, well head

| # | What it shows | Direct file URL | Author | Licence | Res. | Verified-dl | Notes |
|---|---|---|---|---|---|---|---|
| C21 | Real **well screen with a submersible pump** in a display cage, plus an info board showing a **strata cross-section** (Wasserwerk Weiler, DE) | https://upload.wikimedia.org/wikipedia/commons/2/23/Brunnenfilter_mit_eingeh%C3%A4ngter_Unterwasserpumpe%2C_Wasserwerk_Weiler-3571.jpg | Elke Wetzig (Elya) | CC BY-SA 4.0 | 4480×6720 | thumb yes [V] | Excellent explanatory image. Municipal scale. |
| C22 | Submersible pump inserted in a turquoise PVC well pipe, in grass | https://upload.wikimedia.org/wikipedia/commons/2/24/Norip-Rohr_mit_Unterwasserpumpe.jpg | GWE Team | CC BY-SA 4.0 | 2632×3543 | thumb yes [V] | **Looks like a render/composite** (manufacturer marketing), so it may look fake. |
| — | Submersible pump fitted in ground | https://upload.wikimedia.org/wikipedia/commons/b/ba/Submersible_pump_30-07-2012.JPG | Joydeep | CC BY-SA 3.0 | 1958×2800 | metadata only [U visual] | India. Not visually checked. |
| P8 | Stack of grey PVC pipes on a site | https://images.pexels.com/photos/29301874/pexels-photo-29301874.jpeg | sejio402 | Pexels | 6000×4000 | thumb yes [V] | Close to PVC casing (rury osłonowe). |
| P15 | Garden water-pipe installation in a pit, orange/blue fittings, autumn leaves | https://images.pexels.com/photos/29090712/pexels-photo-29090712.jpeg | Joerg Hartmann | Pexels | 4635×3067 | thumb yes [V] | Looks like a well head / connection pit. |
| P14 | Gloved hands assembling a water-pipe fitting | https://images.pexels.com/photos/14598653/pexels-photo-14598653.jpeg | Taha Kose | Pexels | 3376×6000 | thumb yes [V] | Service/"serwis" section. |
| C12 | Historic deep-well house "Studnia głębinowa" Łódź-Chojny (1935, Lindley) | https://upload.wikimedia.org/wikipedia/commons/e/e5/Studnia_g%C5%82ebinowa_%C5%81%C3%B3d%C5%BA_Chojny.jpg | Grover ldz | CC BY-SA 3.0 | 2832×4256 | thumb yes [V] | History/heritage angle only. |
| C20 | Physical aquifer model: sand/gravel layers in a perspex tank with wells | https://upload.wikimedia.org/wikipedia/commons/4/42/Physical_Aquifer_Model.jpg | Asknapp | CC BY-SA 4.0 | 3264×1836 | thumb yes [V] | Reference for the strata illustration style. |

### 1c. Water

| # | What it shows | Direct file URL | Author | Licence | Res. | Verified-dl | Notes |
|---|---|---|---|---|---|---|---|
| C13 | Water splashing out of a clear glass, blue background | https://upload.wikimedia.org/wikipedia/commons/9/93/Water_splashing_out_of_a_full_clear%2C_glass_cup._%2815055172195%29.jpg | US EPA | **Public domain** | 2700×4144 | thumb yes [V] | Classic and clean. |
| P6 | Clear water stream from a metal pipe outdoors, bokeh | https://images.pexels.com/photos/35667687/pexels-photo-35667687.jpeg | edanuraygun | Pexels | 3791×5687 | thumb yes [V] | "Pierwsza woda ze studni" feel. **Top pick.** |
| P7 | Water flowing from a pipe into a trough, backlit rural field | https://images.pexels.com/photos/16668354/pexels-photo-16668354.jpeg | skylake | Pexels | 3188×5668 | thumb yes [V] | Rural and sunny. |
| P9 | Water thrown from a glass against a landscape | https://images.pexels.com/photos/3775199/pexels-photo-3775199.jpeg | aviz | Pexels | 4000×6000 | thumb yes [V] | Dynamic splash. |
| P10 | Water poured from a bottle into a glass, dark blue | https://images.pexels.com/photos/327090/pexels-photo-327090.jpeg | Pixabay | Pexels | 5491×3036 | thumb yes [V] | Wide banner crop. |
| P16 | Water poured into a wine glass, light blue studio | https://images.pexels.com/photos/30422065/pexels-photo-30422065.jpeg | João Vitor | Pexels | 2253×3633 | thumb yes [V] | Minimal. Good for a "badanie wody" section. |

### 1d. Wielkopolska / Polish countryside

| # | What it shows | Direct file URL | Author | Licence | Res. | Verified-dl | Notes |
|---|---|---|---|---|---|---|---|
| C14 | **Aerial: Żydowo palace, gm. Rokietnica (powiat poznański)**, fields to the horizon, 24.08.2026 | https://upload.wikimedia.org/wikipedia/commons/8/89/Pa%C5%82ac_w_%C5%BBydowie_z_lotu_ptaka%2C_24.08.2026%2C_Lesiex.jpg | Lesiex | CC BY-SA 4.0 | 4580×3430 | **yes, 2560→3840px thumb [V-dl]** | Truly local. The same author also has `Pałac w Objezierzu o wschodzie słońca z lotu ptaka, 10.05.2026` (5043×3777, pow. obornicki). |
| C16 | Kicin (gm. Czerwonak, pow. poznański): dirt road, poppies, fields, forest | https://upload.wikimedia.org/wikipedia/commons/3/33/Kicin_north.JPG | MOs810 | CC BY-SA 4.0 | 2048×1360 | thumb yes [V] | Local. Low resolution. |
| C15 | Rogalinek (gm. Mosina, pow. poznański): flat green field, pine wood | https://upload.wikimedia.org/wikipedia/commons/4/41/Rogalinek_view.JPG | MOs810 | CC BY-SA 4.0 | 2048×1360 | thumb yes [V] | Local and muted. |
| C17 | Brzeźno Stare near Wągrowiec: rapeseed field, farmhouses | https://upload.wikimedia.org/wikipedia/commons/6/66/2015_Brze%C5%BAno_Stare_%2C_Polska_._Widok_z_pola_w_kierunku_W%C4%85growca_-_panoramio.jpg | Kazimierz Mendlik | CC BY-SA 3.0 | 4608×2592 | thumb yes [V] | Wielkopolska. Has a small watermark "K. Mendlik" bottom right. |
| P12 | Aerial: Polish village with strip fields (Małopolska) | https://images.pexels.com/photos/31595059/pexels-photo-31595059.jpeg | Dawid Zawiła | Pexels | 4000×3000 | thumb yes [V] | Graphic, but not Wielkopolska (hilly strip fields). |
| P11 | Green rolling fields and fence, overcast, Poland | https://images.pexels.com/photos/12663062/pexels-photo-12663062.jpeg | Ryszard Zaleski | Pexels | 6000×4000 | thumb yes [V] | Generic PL. |
| P13 | Hay bales on a meadow, blue sky, Poland | https://images.pexels.com/photos/38791437/pexels-photo-38791437.jpeg | Piotr Jachowicz | Pexels | 3024×4032 | thumb yes [V] | Summer and drought mood. |
| — | Diego Delso rapeseed field, Malbork | `File:Campo de colza (Brassica napus), Malbork, Polonia, 2013-05-19, DD 01.jpg` | Diego Delso | CC BY-SA 3.0 | 5616×3744 | metadata only | Very high quality. Pomorze. |

**Not found:** a CC/free photo of a modern *domestic* well head (obudowa studni, cap with cable gland) in Poland, and a real-photo cross-section of an aquifer. Draw both as SVG/WebGL instead (see §3).

---

## 2. Open data for an interactive map

| Source / service | Endpoint (verified) | What you get | Licence / terms | Works from sandbox? | Notes |
|---|---|---|---|---|---|
| **PIG-PIB GZWP** (ArcGIS REST) | `https://cbdgmapa.pgi.gov.pl/arcgis/rest/services/hydrogeologia/gzwp/MapServer` (layers: 0 = GZWP udokumentowane, 1 = nieudokumentowane, 2 = LZWP) | Polygons with fields NAZWA, NR_GZWP, POW_KM2, STRATYGRAFIA, TYP_OSRODKA, GL_OD_M/GL_DO_M/GL_SR_M (depth of aquifer), ROK_UDOKUMENTOWANIA. Query formats: JSON, **geoJSON**, PBF; maxRecordCount 1000; native EPSG:2180 | Metadata record 7a11e40b…: "Brak ograniczeń w publicznym dostępie" / "**Brak warunków dostępu i użytkowania**". Credit "PIG-PIB" (copyrightText). | Service JSON loaded twice. Queries **403 (Incapsula)**. **Verified via WebFetch** | GZWP **144 Dolina Kopalna Wielkopolska** (Q, porowy, 4122 km², śr. gł. 46 m) is a single Polygon (116 outer + 29 hole vertices at `maxAllowableOffset=0.01`). |
| GZWP for Poznań bbox | `…/gzwp/MapServer/0/query?geometry=16.35,52.0,17.45,52.8&geometryType=esriGeometryEnvelope&inSR=4326&spatialRel=esriSpatialRelIntersects&outFields=NAZWA,NR_GZWP,POW_KM2,STRATYGRAFIA,TYP_OSRODKA,GL_SR_M&outSR=4326&maxAllowableOffset=0.002&f=geojson` | Returns **143** Subzbiornik Inowrocław–Gniezno (Pg-Ng, 120 m), **144** Dolina Kopalna Wielkopolska (Q, 46 m), **145** Szamotuły–Duszniki (Q, 30 m), **139** Dolina kopalna Smogulec–Margonin (Q, 40 m), **146** Subzbiornik Jezioro Bytyńskie–Wronki–Trzciel (Pg-Ng, 100 m), **150** Pradolina Warszawa–Berlin (Q, 5 m) | as above | via WebFetch only | **Action:** open this URL in a browser on a dev machine, save it as `gzwp-poznan.geojson`, simplify with mapshaper/topojson, and commit. Also query layer 1 (nieudokumentowane). |
| GZWP WMS | `https://cbdgmapa.pgi.gov.pl/arcgis/services/hydrogeologia/gzwp/MapServer/WMSServer?service=wms&request=GetCapabilities&version=1.3.0` | Layers 0 LZWP, 1 GZWP nieudok., 2 GZWP udok. Formats include **image/svg+xml**, png32 | AccessConstraints point to PIG "zasady korzystania z ISP" | WebFetch only | EPSG:3857 **not advertised** (4326 is), so Leaflet would need a 4326 map or pre-rendering. A WFS also exists: `…/gzwp/MapServer/WFSServer?service=wfs&request=GetCapabilities&version=2.0.0`. INSPIRE WFS `http://epsh.pgi.gov.pl/gzwp-usr-wfs/service.svc/get` is listed in metadata, but got 403 from the sandbox [U]. |
| **CBDH boreholes** | `https://cbdgmapa.pgi.gov.pl/arcgis/rest/services/hydrogeologia/cbdh_otwory/MapServer/0/query?...` | **5 608** points in the Poznań-county bbox. Fields: NAZWA, **GLEBOKOSC**, RZEDNA, **DATA_WYKONANIA**, **STRATYGRAFIA_NA_DNIE**, TYP_OTWORU, PRZEZNACZENIE_OTWORU, **MIEJSCOWOSC**, WSP1/WSP2 (EPSG:2180), ZLIKWIDOWANY. Example: Kicin, wodociąg wiejski 1974, 160 m, Trzeciorzęd | Metadata 235b97a9…: same "brak warunków" | WebFetch only | Page with `resultOffset` (max 1000 per request, so 6 pages). Lets you build "średnia głębokość studni w Twojej gminie" from real data (aggregate by gmina using PRG polygons). WMS: `…/cbdh_otwory/MapServer/WMSServer`. |
| MWP: groundwater monitoring | `…/hydrogeologia/mwp/MapServer` (layer 0 points; tables 1 pomiary, 2 wskaźniki chemiczne) | Monitoring points with measurements | (PIG-PIB) | WebFetch only | Could feed a "poziom wód 2026 / niżówka" widget. Not explored further. |
| Other PIG-PIB hydro services (listed) | folder `hydrogeologia`: cbdh_otwory, gzwp, jcwpd, mineralne, mwp, mwp_auto, pobory, podtopienia | | | listing verified | `jcwpd` = groundwater bodies (JCWPd). `pobory` = abstractions. |
| MhP "pierwszy poziom wodonośny" (depth to first water table) | sheet-based files on `bazadata.pgi.gov.pl/data/hydro/mhp/ppw/wh/…` (seen in search results) | Per-sheet 1:50k layers and explanatory PDFs | | **403 from sandbox** [U] | I found no single national WMS for depth to the first water table [U]. The e-PSH portal (`epsh.pgi.gov.pl`) shows MhP. Hand-digitising or a sheet request may be needed. |
| **GUGiK PRG**: administrative boundaries | `https://mapy.geoportal.gov.pl/wss/service/PZGIK/PRG/WFS/AdministrativeBoundaries` (typenames `ms:A02_Granice_powiatow`, `ms:A03_Granice_gmin`, …) | GML 3.2 (no JSON output; `application/json` → 400). Example: GetFeature with BBOX → powiat poznański (3021) + Poznań (3064), 381 KB | Fees: "Brak opłat". PZGiK data is free. | **yes [V-dl]** | Convert GML→GeoJSON with mapshaper/ogr2ogr, then topojson-simplify for SVG gmina maps. |
| GUGiK NMT shaded relief | `https://mapy.geoportal.gov.pl/wss/service/PZGIK/NMT/GRID1/WMS/ShadedRelief?SERVICE=WMS&REQUEST=GetMap&VERSION=1.3.0&LAYERS=Raster&STYLES=&CRS=EPSG:2180&BBOX=490000,350000,510000,370000&WIDTH=400&HEIGHT=400&FORMAT=image/png` | Hillshade PNG | free | **yes [V-dl]** (98 KB PNG) | Pre-render a relief backdrop for the county map (Wielkopolska is flat, but the river valleys show). |
| GUGiK orthophoto | `…/PZGIK/ORTO/WMS/HighResolution` and `…/ORTO/WMTS/StandardResolution` | Aerial imagery | free | GetCapabilities 200 [V] | |

---

## 3. Libraries and repos (visual effects, maps, scroll)

Sizes are npm `unpackedSize`. "No-build" means a UMD/IIFE or self-contained ESM file exists on jsDelivr/unpkg, checked from the file listing.

| Lib / repo | Version | Licence | Size | No-build? | Idea for us |
|---|---|---|---|---|---|
| **GSAP** https://github.com/greensock/GSAP | 3.15.0 | "Standard no-charge license" (gsap.com/standard-license): commercial use OK. The only prohibited use is no-code visual animation tools that compete with Webflow | 6.3 MB pkg; `gsap.min.js` + plugins | **yes**: `dist/*.min.js` incl. ScrollTrigger, ScrollSmoother, **SplitText**, DrawSVG, MorphSVG, MotionPath, ScrambleText, Flip, Observer, InertiaPlugin, CustomEase | Scroll-scrubbed "drill descends through strata" with ScrollTrigger + DrawSVG. Kinetic headings with SplitText. Self-host from `node_modules`/unpkg. |
| **Lenis** https://github.com/darkroomengineering/lenis | 1.3.26 | MIT | 458 KB pkg | **yes**: `dist/lenis.min.js`, `lenis.css`, `lenis-snap` | Smooth scroll, synced to ScrollTrigger (`lenis.on('scroll', ScrollTrigger.update)`). |
| **@paper-design/shaders** https://github.com/paper-design/shaders | 0.0.81 | Apache-2.0 | 880 KB | ESM `dist/index.js`, no deps. Works via `<script type=module>` from jsDelivr/esm | Ready-made **`water`** (caustic-like) shader for the hero/background, plus `grain-gradient`, `paper-texture`, `perlin-noise`, `god-rays`, `halftone-dots`, `fluted-glass`, `liquid-metal`. Fastest route to a caustics look. Pre-1.0 API, so pin the version. |
| **evanw/webgl-water** https://github.com/evanw/webgl-water | (git HEAD 73eda8be) | MIT (header in main.js) | small, plain JS | **yes** (plain scripts, needs OES_texture_float) | Classic interactive pool with ripples and caustics. Adapt it into a "lustro wody w studni" interactive. Old 2011 code, so test on mobile. |
| martinRenou/threejs-caustics https://github.com/martinRenou/threejs-caustics | HEAD e24fa186 | BSD-3-Clause (text verified) | small | needs three.js (ESM import map OK) | Real-time caustics on a ground plane. A heavier alternative. |
| **curtainsjs** https://github.com/martinlaxenaire/curtainsjs | 8.1.6 | MIT | 840 KB | **yes**: `dist/curtains.umd.min.js` | Turns DOM `<img>` into WebGL planes. Ripple/displacement on hover for project photos. |
| sirxemic/jquery.ripples https://github.com/sirxemic/jquery.ripples | HEAD e90bd54e | MIT | tiny | yes, but **needs jQuery** | Quick water-ripple on a background image on mouse move. |
| **OGL** https://github.com/oframe/ogl | 1.0.11 | Unlicense | 423 KB | ESM `src/index.js` (no deps) | Lightweight WebGL for a custom fluid/noise shader without three.js. |
| three.js https://github.com/mrdoob/three.js | 0.186.1 | MIT | 20 MB pkg (build ~700 KB) | ESM + import map | Only if we go 3D (borehole cylinder through stacked layers). |
| stegu/webgl-noise https://github.com/stegu/webgl-noise | HEAD 22434e04 | MIT (Ashima/Stefan Gustavson) | tiny GLSL | copy-paste GLSL | Simplex noise for strata texture and grain in custom shaders. |
| simplex-noise.js https://github.com/jwagner/simplex-noise.js | 4.0.3 | MIT | 109 KB | ESM `dist/esm/simplex-noise.js` | Procedural wavy strata boundaries in SVG (Python generator could also do this offline). |
| **d3-geo** https://github.com/d3/d3-geo | 3.1.1 | ISC | 227 KB | **yes**: `dist/d3-geo.min.js` | Render GZWP + gmina polygons to SVG paths. Can run at build time in Node, or pre-project in Python. |
| **topojson-simplify / -client / -server** https://github.com/topojson | 3.0.3 / 3.1.0 / 3.0.1 | ISC | 50–70 KB | **yes**: `dist/*.min.js` | Shrink PRG gmina boundaries and GZWP shapes for a light SVG map. |
| mapshaper https://github.com/mbloch/mapshaper | 0.7.80 | MPL-2.0 | 17 MB (CLI) | CLI (`npx mapshaper`) | One-off GML/GeoJSON → simplified GeoJSON/SVG at build time. Nothing ships to the browser. |
| proj4js https://github.com/proj4js/proj4js | 2.22.0 | MIT | 845 KB | UMD in dist | EPSG:2180 → 4326 for CBDH WSP1/WSP2 (or do it in Python with pyproj). |
| @turf/turf | 7.4.0 | MIT | 604 KB | `turf.min.js` | Point-in-polygon (borehole → gmina) and averages, if done client-side. |
| **Equinor esv-intersection** https://github.com/equinor/esv-intersection | 5.0.5 | MIT | 3.7 MB | ESM/CJS only, bare-import deps (d3-*, pixi.js), so it **needs esm.sh / import map / bundler** | Professional **wellbore + geological layer cross-section** widget. Best as design reference or for a "Twoja przyszła studnia" section. |
| Equinor videx-wellog https://github.com/equinor/videx-wellog | 1.6.8 | MIT | 462 KB | `dist/index.umd.js` (deps d3) | Well-log track renderer. A "karta otworu" visual (depth vs lithology). |
| d3-contour https://github.com/d3/d3-contour | (HEAD 8a3b95a6) | ISC | small | UMD | Contour/isoline art for backgrounds (pseudo-hydroisohypsy). |
| scrollama https://github.com/russellgoldenberg/scrollama | 3.2.0 | MIT | 370 KB | UMD | Lightweight step-based scrollytelling, if not using ScrollTrigger. |
| Splitting.js https://github.com/shshaw/splitting | 1.1.0 | MIT | 37 KB | UMD | CSS-var-based char splitting. SplitText now covers this. |
| grained https://github.com/sarathsaleem/grained | 0.0.2 | MIT | tiny | yes | Animated film grain overlay. A CSS/SVG `feTurbulence` grain is an alternative. |
| textures.js https://github.com/riccardoscalco/textures | 1.2.3 | MIT | 24 KB | UMD (needs d3-selection) | SVG hatch patterns for lithology (piasek/glina/żwir) in the cross-section and map legend. |
| Codrops demos, e.g. https://github.com/codrops/ScrollBasedLayoutAnimations, https://github.com/akella/webgl-mouseover-effects | — | MIT (verified) | small | plain JS + GSAP | Patterns for scroll layout transitions and WebGL hover distortions. |
| spite/codevember-2016 | — | CC BY (licence file) | — | — | Shader inspiration only (attribution needed). |
| vanta.js | 0.5.24 | MIT | 1.4 MB | UMD (+three) | Cheap animated "waves"/"fog" backgrounds. Generic look, so low priority. |

---

## 4. Fonts (industrial/engineering, Polish diacritics)

I checked Polish glyphs with fontTools on the actual downloaded files, testing `ąćęłńóśźż ĄĆĘŁŃÓŚŹŻ`. Google Fonts licence and axes come from `google/fonts/ofl/<name>/METADATA.pb`.

| Font | Source | Licence | PL glyphs | Axes / styles | Character / use |
|---|---|---|---|---|---|
| **Big Shoulders** (Display) | Google Fonts | OFL | **all OK [V]** | opsz, wght (Thin–Black) | Chicago-industrial condensed. **Top pick for headlines.** |
| **Archivo** | Google Fonts | OFL | **OK [V]** | **wdth** 62–125, wght | Grotesque with real width axis: condensed headlines and wide numerals from one file. |
| **Martian Mono** | Google Fonts | OFL | **OK [V]** | wdth, wght | Technical mono for depth readouts ("−48 m"), labels, data. |
| **Mona Sans / Hubot Sans** | Google Fonts (GitHub) | OFL | Mona **OK [V]**; Hubot latin-ext per metadata | wdth, wght | Hubot = engineered, mechanical feel. Mona = text. |
| **Tektur** | Google Fonts | OFL | **OK [V]** | wdth, wght | Angular, "machine" flavour. Use sparingly. |
| Space Grotesk / Space Mono | Google Fonts | OFL | Grotesk **OK [V]**; Mono latin-ext per metadata | wght | Techy. Overused. |
| Barlow / Barlow Condensed | Google Fonts | OFL | **OK [V]** | static weights | Road-sign / DIN-like. Very legible. |
| IBM Plex Sans Condensed / Plex Mono | Google Fonts | OFL | latin-ext (metadata) | static | Corporate engineering. |
| JetBrains Mono, Geist / Geist Mono, Azeret Mono, Red Hat Mono, Sometype Mono | Google Fonts | OFL | latin-ext (metadata) | wght | Mono alternatives. |
| Unbounded | Google Fonts | OFL | **OK [V]** | wght | Wide, bold display. |
| Oswald, Bebas Neue, Anton, Saira (wdth), Chakra Petch | Google Fonts | OFL | latin-ext (metadata) | | Classic condensed. Bebas Neue is caps-only. |
| **Lineal** (Velvetyne) https://gitlab.com/velvetyne/lineal | Velvetyne | OFL (LICENSE.txt) | **OK [V]** | static (Black…) | Geometric and rigid. Distinctive. |
| **Sporting Grotesque** https://gitlab.com/velvetyne/Sporting-Grotesque | Velvetyne | OFL | **OK [V]** | Regular/Bold | Quirky grotesque. |
| **Grotesk** https://gitlab.com/velvetyne/grotesk | Velvetyne | OFL | **OK [V]** | many widths (01 Extrafin…) | Variable-feel grotesque family. |
| **BackOut** https://gitlab.com/velvetyne/backout | Velvetyne | OFL | **OK [V]** | 1 | Stencil-like display. Use for big numerals. |
| **Sligoil** https://gitlab.com/velvetyne/sligoil | Velvetyne | OFL | **OK [V]** | Micro/… | Monospaced/technical feel. |
| Format 1452, AMDAL, Facade, Compagnon (Velvetyne) | Velvetyne | OFL | **MISSING Polish glyphs [V]** | | Do not use. |
| Collletttivo: Ronzino, Apfel Grotezk, Necto Mono, Mattone, Sprat, Halibut… https://www.collletttivo.it/typefaces | Collletttivo | OFL (site states it) | **[U]**: no direct download URL found (JS form) | | Necto Mono and Mattone could fit. Check Polish glyphs before using. |
| Fontshare: Satoshi, General Sans, Cabinet Grotesk, Clash Display, Switzer, Chillax | ITF | **ITF FFL v2.0 (17 Aug 2026)**, text read from the Satoshi download zip | **OK [V]** (woff2 from Fontshare CSS API) | | FFL **allows commercial use and self-hosting** on own sites. It **forbids modification incl. subsetting and format conversion**, redistribution (e.g. a public repo of font files is risky) and serving to third parties. Use the official woff2 as-is. Prefer OFL fonts for a generated static site. |

---

## 5. Practical notes for the build

- **Commons in the Python generator:** fetch `https://commons.wikimedia.org/wiki/Special:FilePath/<File>?width=1920` (or 2560/3840) with a descriptive User-Agent, and **throttle** (the API returned 429 after bursts). Keep author/licence from `extmetadata` and render a credits block automatically.
- **Pexels:** `https://images.pexels.com/photos/<id>/pexels-photo-<id>.jpeg?auto=compress&cs=tinysrgb&w=2400` works without an API key.
- **PIG-PIB from CI/sandbox is unreliable** (Incapsula). Treat the GZWP/CBDH data as static assets fetched once by a human or a browser and committed with a `source + date + "© PIG-PIB"` note. Check CORS before any live client-side fetch [U].
- Test files: `scratchpad/assets-test/` (thumbnails, `full_p01.jpg`, `u01_full.jpg`, `c14_2560.jpg`, `t2.jpg`, fonts/). PRG sample: `scratchpad/pig/pow.gml`.
