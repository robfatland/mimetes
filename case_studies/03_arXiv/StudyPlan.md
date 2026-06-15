# Case Study 03 — Using Programmatic AWS-AI for Scientific Research


## Leading Welcome Remarks


- Today's presentation/demo will run from a laptop: Why?


## Open Topics / Action Items / To Do

- [ ] Get API key from Semantic Scholar
- [ ] Get API key from AI2 Asta (separate from S2): https://share.hsforms.com/1L4hUh20oT3mu8iXJQMV77w3ioxm
- [ ] Finish successfully running `find_paper.py`
- [ ] Run `summarize.py` end-to-end
- [ ] Decide output format for presentation (markdown? slides? both?)
- [ ] Investigate AI2 Asta / Semantic Scholar for Step 7 (related papers)
- [ ] Locate the RAGU code: https://github.com/btobers/RAGU
- [x] Locate the IceBridge/Alaska data associated with the paper

## Presentation Title

"Using Programmatic AWS-AI For Scientific Research"

## Presentation Medium

When asked for alternatives to Google Slides, the Kiro IDE suggested several
Markdown-based presentation tools:

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

The presentation is deliberately transparent — showing every step of the pipeline
so the audience understands exactly what's happening and where AWS enters.

| Step | Action | Tool / Service |
|------|--------|----------------|
| 1 | Search for and download an EarthArXiv paper | Semantic Scholar API (no AWS) |
| 2 | Extract text from the PDF | pymupdf (local, no AWS) |
| 3 | Summarize the paper | Bedrock → Claude Sonnet |
| 4 | Does the paper have data or code online? | Bedrock → Claude Sonnet |
| 5 | Explore the consequences of that | Bedrock → Claude Sonnet |
| 6 | Hypothesize a related scientific question | Bedrock → Claude Sonnet |
| 7 | Generate a list of relevant papers | AI2 Asta (Semantic Scholar) |
| 8 | Present a summary of what just happened + cost estimate | Aggregate token usage |
| 9 | Explain that this procedure is available in `mimetes` | — |
| 10 | Pull the camera back: `mimetes` was built using Kiro | — |

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
- [x] Step 2: Text extraction script written (`extract_text.py`) — 43 pages, 79,738 chars
- [x] Step 3: Summarize — first Bedrock call successful (27,257 input / 2,111 output tokens, $0.11)
- [ ] Step 4: Code/data detection
- [ ] Step 5: Explore consequences
- [ ] Step 6: Hypothesize
- [ ] Step 7: Related papers via AI2 Asta
- [ ] Step 8: Cost summary
- [ ] Steps 9–10: Presentation framing

## Architecture

```
Step 1: find_paper.py
    → Semantic Scholar REST API (GET /graph/v1/paper/search)
    → filter by author
    → display metadata (title, authors, DOI, open-access PDF URL)
    → download PDF
    → save metadata as JSON

Step 2: extract_text.py
    → pymupdf opens the PDF locally
    → extracts text page by page
    → writes tober_2025_extracted.txt
    → no chunking needed (43 pages fits within Sonnet's 200k token window)

Steps 3–6: summarize.py (and extensions)
    → load extracted text
    → construct prompt
    → call Bedrock invoke_model (Claude Sonnet, us-west-2)
    → parse response
    → tally token usage

Step 7: AI2 Asta / Semantic Scholar
    → search for related papers based on hypothesis from Step 6

Steps 8–10: Presentation framing (no code)
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

1. **Output format** — Markdown summary? JSON? Slide-ready bullets?
2. **AI2 Asta access** — MCP tool vs. Semantic Scholar REST API? Need to confirm access.
3. **Batch vs. single** — Presentation demos one paper; could the tool generalize?

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
