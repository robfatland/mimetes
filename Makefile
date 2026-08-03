# Makefile — Render all Marp slide decks to self-contained HTML
#
# Usage:
#   make decks        # render all slide decks
#   make clean-decks  # remove generated HTML
#   make deck-pytorch # render just the root PyTorch deck
#   make deck-all     # combine all decks into one mega HTML
#
# Prerequisites:
#   npm install -g @marp-team/marp-cli  (via nvm)
#
# The --allow-local-files flag lets Marp read local images.
# The --html flag enables inline HTML in slides.
# Together they produce a self-contained HTML file with images embedded.

# Use bash and source nvm so marp is on PATH
SHELL := /bin/bash
export NVM_DIR := $(HOME)/.nvm
LOAD_NVM := source "$(NVM_DIR)/nvm.sh" 2>/dev/null;

MARP = $(LOAD_NVM) marp
MARP_FLAGS = --allow-local-files --html

# Root PyTorch deck
ROOT_DECK_SRC = slides.md
ROOT_DECK_OUT = slides.html

# Case study decks (only those that exist)
CS_DIRS = $(wildcard case_studies/*/.)
CS_SRCS = $(wildcard case_studies/*/slides.md)
CS_OUTS = $(CS_SRCS:.md=.html)

ALL_OUTS = $(ROOT_DECK_OUT) $(CS_OUTS)

.PHONY: decks clean-decks deck-pytorch deck-list deck-all deck-pptx

decks: $(ALL_OUTS)
	@echo ""
	@echo "All decks rendered:"
	@for f in $(ALL_OUTS); do echo "  $$f"; done

deck-pytorch: $(ROOT_DECK_OUT)

deck-list:
	@echo "Slide sources found:"
	@echo "  $(ROOT_DECK_SRC)"
	@for f in $(CS_SRCS); do echo "  $$f"; done

# Root deck — run from repo root so relative image paths resolve
$(ROOT_DECK_OUT): $(ROOT_DECK_SRC) $(wildcard images/*)
	$(MARP) $< -o $@ $(MARP_FLAGS)
	@echo "  -> $@"

# Case study decks — run from each case study's directory so local image
# paths resolve correctly, producing a self-contained HTML file
case_studies/%/slides.html: case_studies/%/slides.md
	cd $(dir $<) && $(MARP) slides.md -o slides.html $(MARP_FLAGS)
	@echo "  -> $@"

clean-decks:
	rm -f $(ALL_OUTS) all_slides.md all_slides.html
	rm -f $(ROOT_DECK_SRC:.md=.pptx) $(CS_SRCS:.md=.pptx)
	@echo "Cleaned all rendered decks."

# --- Combined mega-deck ---
# Concatenates all slides.md files, rewriting relative image paths so they
# resolve from the repo root. Renders one self-contained HTML.

ALL_DECK_OUT = all_slides.html
ALL_DECK_MD  = all_slides.md

# Order: root deck first, then case studies in directory order
ALL_DECK_SRCS = $(ROOT_DECK_SRC) $(CS_SRCS)

deck-all: $(ALL_DECK_OUT)

$(ALL_DECK_MD): $(ALL_DECK_SRCS) combine_slides.py
	@echo "Combining slide sources into $@..."
	python3 combine_slides.py $(ALL_DECK_SRCS) > $@
	@echo "  -> $@ ($(words $(ALL_DECK_SRCS)) sources combined)"

$(ALL_DECK_OUT): $(ALL_DECK_MD)
	$(MARP) $< -o $@ $(MARP_FLAGS)
	@echo "  -> $@"

# --- PPTX export (for Google Slides import) ---
# Renders each deck as a .pptx with slides as flat images.
# Upload to Google Drive → Open with Google Slides.

CS_PPTX = $(CS_SRCS:.md=.pptx)
ROOT_PPTX = slides.pptx

deck-pptx: $(ROOT_PPTX) $(CS_PPTX)
	@echo ""
	@echo "PPTX decks rendered:"
	@echo "  $(ROOT_PPTX)"
	@for f in $(CS_PPTX); do echo "  $$f"; done

$(ROOT_PPTX): $(ROOT_DECK_SRC) $(wildcard images/*)
	$(MARP) $< -o $@ $(MARP_FLAGS)
	@echo "  -> $@"

case_studies/%/slides.pptx: case_studies/%/slides.md
	cd $(dir $<) && $(MARP) slides.md -o slides.pptx $(MARP_FLAGS)
	@echo "  -> $@"
