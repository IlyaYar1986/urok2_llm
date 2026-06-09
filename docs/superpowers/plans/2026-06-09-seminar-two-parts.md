# Two-Part Seminar Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a separate responsive seminar page that presents the approved 25-minute and 45-minute theory routes using the project's existing visualizations and infographics.

**Architecture:** Create one self-contained parent page at `web/seminar_25_45.html`. It will reuse sibling interactive HTML files through iframe cards and reuse existing PNG infographics through a zoomable lightbox. Page-level JavaScript will provide section navigation, scroll reveal, accordion notes, fullscreen iframe viewing, and image zoom/pan without introducing dependencies.

**Tech Stack:** HTML5, embedded CSS, vanilla JavaScript, existing local HTML visualizations and PNG assets.

---

### Task 1: Add structural verification

**Files:**
- Create: `tests/check_seminar_page.py`
- Test: `web/seminar_25_45.html`

- [ ] **Step 1: Write a failing structural test**

Create a standard-library Python test that asserts:

- `web/seminar_25_45.html` exists;
- page title and both timing labels are present;
- required section IDs exist;
- required iframe and image paths resolve;
- four generation controls are named;
- theory-to-practice transition text is present;
- no embedded practice form or practical assignment section is present.

- [ ] **Step 2: Run the test and verify RED**

Run:

```bash
python3 -m unittest tests/check_seminar_page.py -v
```

Expected: failure because `web/seminar_25_45.html` does not exist.

### Task 2: Build the seminar page

**Files:**
- Create: `web/seminar_25_45.html`

- [ ] **Step 1: Implement the page shell**

Add:

- fixed navigation;
- hero with audience, title, two timing badges, and chapter links;
- two visually distinct chapter headers;
- reusable section, iframe-card, image-card, callout, and accordion components;
- responsive styles following the existing indigo/cyan visual system.

- [ ] **Step 2: Implement Part 1**

Add timed sections for:

- GPT and next-token prediction;
- data and training;
- tokenization with `tokenizator.html`;
- embeddings with `word_embeddings_3d.html` and `omonimy2.html`;
- shared semantic space using `../png/zanyatie2_agentnye_sistemy/05_02_odna_karta_smyslov.png`;
- a visual transition to the separate image-generation practice.

- [ ] **Step 3: Implement Part 2**

Add timed sections for:

- context and attention with `механизм Attension2.html`;
- training, SFT, preferences, Outcome Reward and Process Reward;
- inference and sampling;
- Temperature, Top-K, Top-P and Min-P with `Рычаги управления нейросетью.html`;
- System 1/System 2 and pedagogical process assessment;
- agents, ReAct, RAG and MCP using existing agent infographics;
- pedagogical-agent summary and transition to the separate agent practice.

- [ ] **Step 4: Implement interaction behavior**

Add:

- accordion toggles with `aria-expanded`;
- iframe fullscreen overlay;
- image lightbox with zoom and pan;
- Escape-key closing;
- scroll reveal;
- active navigation tracking.

- [ ] **Step 5: Run structural test and verify GREEN**

Run:

```bash
python3 -m unittest tests/check_seminar_page.py -v
```

Expected: all tests pass.

### Task 3: Add navigation entry

**Files:**
- Modify: `index.html`
- Test: `tests/check_seminar_page.py`

- [ ] **Step 1: Extend the test**

Assert that `index.html` contains a link to `web/seminar_25_45.html`.

- [ ] **Step 2: Run test and verify RED**

Run:

```bash
python3 -m unittest tests/check_seminar_page.py -v
```

Expected: failure because the link is absent.

- [ ] **Step 3: Add the navigation link**

Add a prominent link to the new two-part seminar in the existing hero actions and fixed navigation without removing current links.

- [ ] **Step 4: Run test and verify GREEN**

Run:

```bash
python3 -m unittest tests/check_seminar_page.py -v
```

Expected: all tests pass.

### Task 4: Browser verification and polish

**Files:**
- Modify if needed: `web/seminar_25_45.html`

- [ ] **Step 1: Start a local server**

Run:

```bash
python3 -m http.server 8000
```

- [ ] **Step 2: Check desktop layout**

Open `http://127.0.0.1:8000/web/seminar_25_45.html` at approximately 1440×900 and verify:

- hero hierarchy;
- chapter transition;
- readable iframe sizing;
- no horizontal overflow;
- lightbox and fullscreen overlay;
- accordions and navigation.

- [ ] **Step 3: Check tablet and mobile**

Verify approximately 768×1024 and 390×844:

- nav remains usable;
- grids collapse cleanly;
- text and timing labels remain readable;
- no clipped controls or images.

- [ ] **Step 4: Check browser console**

Confirm no missing-resource, JavaScript, or accessibility-state errors during core interactions.

- [ ] **Step 5: Run final verification**

Run:

```bash
python3 -m unittest tests/check_seminar_page.py -v
git diff --check
git status --short
```

Expected: tests pass, no whitespace errors, and only intended files are modified.
