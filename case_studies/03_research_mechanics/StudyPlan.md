# Case Study 03 — Using Programmatic AWS-AI for Scientific Research


This document is the 'behind the scenes' working notes for the CloudBank 
"Cloud Clinic" presented circa June 2026.


## Leading Welcome Remarks


Today's presentation will run from a laptop. The intent is to touch upon three modes of AI use in research. These modes are *website* (AI2 AstaLabs), *IDE* using the `kiro` variant of VSCode, and *programmatic access* to the AWS cloud Bedrock AI service via API.


## Open Topics / Action Items / To Do


- [ ] Get API key from Semantic Scholar
- [x] Get API key from AI2 Asta
- [x] Finish successfully running `find_paper.py` (blocked by S2 rate limit; key resolves this)
- [x] Run `summarize.py` end-to-end
- [x] Decide output format for presentation → Marp (HTML slides)
- [x] Investigate AI2 Asta / Semantic Scholar for Step 7 (AutoDiscovery, browser-based)
- [x] Locate the RAGU code: https://github.com/btobers/RAGU
- [x] Locate the IceBridge/Alaska data associated with the paper
- [x] ITS_LIVE velocity integration
- [x] Deformation velocity calculation (Glen's flow law)
- [x] Bedrock science reasoning call (basal sliding literature context)

## Presentation Title

"Using Programmatic AWS-AI For Scientific Research"

## Presentation Medium

When asked for alternatives to Google Slides, the Kiro IDE 
suggested Markdown-based presentation tools:

| Tool | How It Works |
|------|-------------|
| Reveal.js | HTML/Markdown slides in a browser |
| **Marp** | Markdown → HTML/PDF/PPTX; VS Code extension available |
| Jupyter + RISE | Notebook cells become live-demo slides |
| Slidev | Vue-powered Markdown slides |

**Chosen:** Marp — lightweight, lives in the repo, version-controlled, and renders
beautifully in any browser.

**Setup:**
1. Needed Node.js ≥ 18 (WSL had v12). Fixed via `nvm install 20`.
2. Installed the CLI: `npm install -g @marp-team/marp-cli`
3. Slides are authored in `presentation.md` using standard Markdown with `---` as
   slide separators and a YAML front-matter block for theme/pagination.
4. Render: `marp presentation.md -o presentation.html --allow-local-files`
5. Copy to Windows Downloads for browser viewing: `cp presentation.html ~/D/`

The Marp VS Code/Kiro extension also provides a live preview in the editor.

## Presentation Sequence

The presentation is transparent — every step of the pipeline
so the audience understands what's happening, where AWS enters.

| Step | Action | Tool / Service |
|------|--------|----------------|
| 1 | Using AI2's Semantic Scholar API: Locate a paper | Semantic Scholar API (no AWS) |
| 2 | Download it and extract the text | pymupdf (local, no AWS) |
| 3 | Use AWS Bedrock API: Task Claude Sonnet to summarize | Bedrock → Claude Sonnet |
| 4 | Detect code/data availability | Bedrock → Claude Sonnet |
| 5 | Chart glacier thickness from the data repository | Kiro IDE → Python (matplotlib) |
| 6 | Pose a related research question | Bedrock → Claude Sonnet |
| 7 | Ask Asta to run experiments on extracted data | AI2 Asta AutoDiscovery (browser) |
| 8 | Cost accounting | Aggregate token usage |
| 9 | Making everything open/public | `mimetes` repo on GitHub |
| 10 | Building with the `kiro` IDE | — |

**Design note:** Steps 1–2 are pre-Bedrock. The audience sees that accessing an LLM
requires preparation — find the paper, get it into text form — before you can ask the
model anything. This demystifies the process.

## Target Paper

| Field | Value |
|-------|-------|
| Title | Alaskan Glacier Depths from a Decade of Airborne Radar Sounding |
| Authors | Brandon Scott Tober, Michael Steven Christoffersen, John W Holt, Martin Truffer, Christopher F Larsen |
| DOI | `https://doi.org/10.31223/X53T78` |
| Source | EarthArXiv |
| License | CC BY 4.0 |
| Local file | `tober_2025_alaskan_glacier_depths.pdf` (~24.5 MB) |

## Progress

- [x] Step 1: Paper identified and downloaded via web search
- [x] Step 2: Text extraction — 43 pages, 79,738 chars, clean
- [x] Step 3: Summarize — Bedrock call successful (27,257 in / 2,111 out, $0.11)
- [x] Step 4: Code/data detection — Sonnet identified RAGU, NSIDC DOIs, GitHub data
- [x] Step 5: Bagley profile chart from KML data + ITS_LIVE velocity + deformation calc
- [x] Step 6: Science reasoning — Bedrock call on basal sliding (321 in / 2,048 out, $0.03)
- [ ] Step 7: Asta AutoDiscovery — upload CSV, screencap results (browser demo)
- [x] Step 8: Cost accounting — total ~$0.25 across all Bedrock calls
- [x] Steps 9–10: Presentation framing complete (Marp deck, 20+ slides)

## Architecture

```
Step 1: find_paper.py
    → Semantic Scholar REST API (GET /graph/v1/paper/search)
    → filter by author
    → display metadata (title, authors, DOI, open-access PDF URL)
    → download PDF via DOI → doi.org → EarthArXiv
    → save metadata as JSON

Step 2: extract_text.py
    → pymupdf opens the PDF locally
    → extracts text page by page
    → writes tober_2025_extracted.txt
    → no chunking needed (43 pages fits within Sonnet's 200k token window)

Step 3: summarize.py
    → load extracted text
    → construct prompt (summarize + find code/data)
    → call Bedrock invoke_model (Claude Sonnet, us-west-2)
    → parse response, tally token usage
    → write tober_2025_summary.md

Step 5: bagley_profile.py + get_velocity.py + deformation_velocity.py
    → parse KML from OIB-AK_radar repo
    → filter to Bagley Ice Valley, isolate single flight line
    → compute along-track distance
    → query ITS_LIVE Zarr datacube for observed velocity
    → compute deformation-only velocity (Glen's law, constant slope)
    → produce combined chart + CSV

Step 6: ask_bedrock.py
    → science reasoning prompt about basal sliding
    → Bedrock → Claude Sonnet (5 min timeout, 2048 max tokens)
    → write bedrock_response.md

Step 7: AI2 Asta AutoDiscovery (browser)
    → upload bagley_profile.csv
    → provide context about the data
    → AutoDiscovery autonomously runs multiple experiments

Steps 8–10: Presentation framing
    → presentation.md (Marp) → presentation.html
    → render: marp presentation.md -o presentation.html --allow-local-files --html
```

## What This Exercises

| Skill | Detail |
|-------|--------|
| PDF text extraction | pymupdf to get paper text from downloaded PDF |
| AWS Bedrock API | Invoking Claude Sonnet programmatically via boto3 |
| Prompt engineering | Structured prompts for summarization, extraction, hypothesis |
| Semantic Scholar / AI2 Asta | Programmatic literature search |
| Cost accounting | Tracking token usage and mapping to Bedrock pricing |
| Presentation narrative | Building a demo that tells a coherent story |

## Dependencies (additions to requirements.txt)

- `boto3` — AWS SDK for Bedrock calls
- `pymupdf` — PDF text extraction
- `requests` — HTTP calls to Semantic Scholar / AI2 Asta API
- `xarray` — N-dimensional array analysis (for ITS_LIVE datacubes)
- `zarr` — chunked array storage format
- `s3fs` — S3 filesystem access for cloud-hosted Zarr cubes
- `pyproj` — coordinate projection (lat/lon → UTM for ITS_LIVE grid)
- `shapely` — geometric operations (point-in-polygon for cube catalog lookup)
- `Pillow` — image cropping for figure extraction

## ITS_LIVE Integration (Surface Velocity)

### Discovery Path

Starting from the directive "find surface ice velocities for Alaska glaciers from
NASA or NOAA," web search leads directly to **ITS_LIVE** — a NASA MEaSUREs project
providing global glacier velocity from satellite imagery (1985–present, 120m resolution).

- **URL:** https://its-live.jpl.nasa.gov
- **API:** STAC API at `https://stac.itslive.cloud`
- **Data format:** Cloud-optimized Zarr datacubes accessible via xarray
- **Coverage:** Global, all land ice areas > 5 km²
- **Variables:** `v` (speed m/yr), `vx`/`vy` (components → flow azimuth), plus error estimates

### Implementation Notes

- The official `itslive` Python package (nasa-jpl/itslive-py) exists but has
  dependency resolution issues with pip in our environment. We use direct Zarr
  access instead.
- The datacube catalog is a GeoJSON file (~5MB) mapping the globe into tiles:
  `https://its-live-data.s3.amazonaws.com/datacubes/catalog_v02.json`
- Each cube is in a projected coordinate system (typically UTM). Must transform
  lat/lon → projected coords using pyproj before querying.
- Initial attempt returned uniform values (22.5 m/yr for all points) because
  all profile points mapped to one grid cell — caused by incorrect projection handling.
  Fixed by using the catalog to find the correct cube and its EPSG code.
- The cube's time dimension (`mid_date`) gives full observation history. We
  report the median speed to be robust against outliers.

### What We Get

- Median surface flow speed at each point along the Bagley profile
- Full time series (scatter plot showing all observations since ~1985)
- Combined chart: ice thickness cross-section + velocity on dual axes

## Key Notes

- **Step 1 does not use AWS.** The paper search and download happen via Semantic
  Scholar and EarthArXiv directly. Bedrock enters at Step 3.
- **Step 2 (text extraction) is also local** — no AWS, no network call. pymupdf only.
- **No chunking needed.** The paper is 43 pages and extracts cleanly. The full text
  fits comfortably within Sonnet's 200k token context window, so we send it as one
  prompt — no splitting or summarize-then-merge strategy required.
- **Data availability (from EarthArXiv metadata):** "Data available upon manuscript
  publication." — This will be interesting to probe in Step 4.
- **The paper is a preprint** (not yet peer reviewed as of the EarthArXiv listing).

## AWS Configuration

| Setting | Value |
|---------|-------|
| Region | `us-west-2` |
| Credentials | `~/.aws/credentials` |
| Inference Profile | `us.anthropic.claude-sonnet-4-6` |
| Note | Newer Bedrock models require an inference profile ID, not a bare model ID |

### Getting to a Working Bedrock Call (Checklist)

The path from zero to a successful `invoke_model` call:

```bash
# 1. Check CLI version — need v2.13+ for Bedrock commands
aws --version
# If too old:
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install --update

# 2. Confirm credentials work
aws sts get-caller-identity

# 3. List available Sonnet inference profiles (NOT model IDs)
aws bedrock list-inference-profiles --region us-west-2 \
  --query "inferenceProfileSummaries[?contains(inferenceProfileId, 'sonnet')].inferenceProfileId" \
  --output table

# 4. Pick a non-legacy profile. Use the "us." prefix for regional access.
#    As of mid-2025, the working choice is:
#      us.anthropic.claude-sonnet-4-6
#
#    Do NOT use:
#      - Bare model IDs (anthropic.claude-sonnet-4-20250514) → "invalid model"
#      - Model IDs with version suffix (anthropic.claude-...-v1:0) → "needs inference profile"
#      - Dated profiles that Bedrock flags as legacy → "access denied"

# 5. Test with a trivial call
aws bedrock-runtime invoke-model \
  --region us-west-2 \
  --model-id us.anthropic.claude-sonnet-4-6 \
  --content-type application/json \
  --accept application/json \
  --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":50,"messages":[{"role":"user","content":"Say hello"}]}' \
  /dev/stdout
```

**Key lesson:** Bedrock model identifiers have three layers — the base model ID,
the versioned model ID, and the inference profile ID. Only the inference profile
works with `invoke_model` for newer models. Use `list-inference-profiles` to find
the right one.

## Timeline (8-day arc)

| Days | Focus |
|------|-------|
| 1–2 | PDF extraction working; first Bedrock call returning a summary |
| 3–4 | Steps 3–5: code/data detection, consequence exploration, hypothesis |
| 5–6 | Step 6: AI2 Asta integration for related papers |
| 7–8 | Cost accounting, presentation assembly, dry run |

## Design Decisions Still Open

1. **Asta AutoDiscovery** — browser demo for Step 7; screencap the results for the slide deck.
2. **Batch vs. single** — Presentation demos one paper; the tool could generalize.

## Bedrock Science Reasoning

A follow-up Bedrock call (`ask_bedrock.py`) posed the question: given deformation
speeds of 15–100 m/yr and observed speeds of 140–220 m/yr, what does the literature
say about basal sliding for temperate glaciers at this scale?

Key findings from Sonnet's response:
- Inferred sliding of 40–150 m/yr is consistent with published values for large
  temperate Alaskan glaciers (Fatland & Lingle 2002 on Bering; Raymond 1987 on
  Variegated; Rabus & Echelmeyer 1997 on Gulkana)
- Sliding typically accounts for 50–90% of surface velocity in temperate glaciers
  (Cuffey & Paterson 2010)
- Spatial variability is best explained by subglacial hydrology variations
  (channelized vs. distributed drainage)
- The Nye shape factor and longitudinal stress coupling are relevant at this scale

Note: The default boto3 read timeout (60s) was insufficient for this call.
Increased to 300s via `botocore.config.Config(read_timeout=300)`.

## Data

### GitHub User: `btobers` (Brandon S. Tober)

| Repo | Contents | URL |
|------|----------|-----|
| `RAGU` | Radar Analysis Graphical Utility — Python, GPL-3.0, 29 stars | https://github.com/btobers/RAGU |
| `OIB-AK_radar` | Downsampled IceBridge Alaska radar data as KML | https://github.com/btobers/OIB-AK_radar |
| `radar_tools` | Misc radar processing tools (Jupyter) | https://github.com/btobers/radar_tools |
| `mass_con` | Glacier mass conservation tools (Jupyter) | https://github.com/btobers/mass_con |

### Archival Data at NSIDC (full resolution)

| Dataset | DOI |
|---------|-----|
| IceBridge lidar altimetry | https://doi.org/10.5067/AATE4JJ91EHC |
| UAFHF processed radar sounding | https://doi.org/10.5067/Q0AVPHN3250H |
| ARES processed radar sounding | https://doi.org/10.5067/X2H7MP5DBTYP |
| UAFHF-derived bed/thickness (2013–2015) | https://doi.org/10.5067/225AMW1MQB4O |
| ARES-derived bed/thickness (2015–2021) | https://doi.org/10.5067/IW2LCD7YPOV2 |

### Quick Visualization: KML on Google Earth

The file `IRUAFHF2_IRARES2_250m_mean.kml` in the `OIB-AK_radar` repo contains
downsampled (250m) ice thickness measurements that can be overlaid on Google Earth
(web or desktop). This provides a fast visual of where data exists along flight lines
over Alaska's glaciers.

### RAGU on Zenodo

DOI: https://doi.org/10.5281/zenodo.3968981
