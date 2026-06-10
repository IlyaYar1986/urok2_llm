# Education Tools, MCP and Skills Page Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a responsive lecture continuation that teaches educators how to create MCP servers and Agent Skills, then provides practical catalogs and ready-to-use workflows.

**Architecture:** Add one self-contained HTML page that follows the existing lecture's CSS and JavaScript conventions. Protect the page contract with a focused Python `unittest`, then add navigation links from the agent-systems page and the main landing page. Keep advanced code examples inside native `<details>` elements so the page works without JavaScript.

**Tech Stack:** HTML5, CSS3, vanilla JavaScript, Python `unittest`, local static HTTP server, Playwright browser verification.

---

## File Map

- Create `web/instrumenty_mcp_skills.html`: page content, styles, diagrams, code samples, copy controls, scroll navigation.
- Create `tests/check_education_tools_page.py`: structural, content, accessibility, and integration-link checks.
- Modify `web/agentnye_sistemy.html`: add the continuation link in navigation and after the final section.
- Modify `index.html`: expose the practical continuation from the main lecture landing.

### Task 1: Define the page contract with a failing test

**Files:**
- Create: `tests/check_education_tools_page.py`

- [ ] **Step 1: Write the failing page test**

```python
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "web" / "instrumenty_mcp_skills.html"
AGENTS_PAGE = ROOT / "web" / "agentnye_sistemy.html"
INDEX = ROOT / "index.html"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.id_counts = {}
        self.details = 0

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            value = values["id"]
            self.ids.add(value)
            self.id_counts[value] = self.id_counts.get(value, 0) + 1
        if tag == "details":
            self.details += 1


class EducationToolsPageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8") if PAGE.exists() else ""
        cls.parser = PageParser()
        cls.parser.feed(cls.html)

    def test_page_exists_with_required_sections(self):
        self.assertTrue(PAGE.is_file())
        required = {"hero", "mcp", "skill", "tools", "mcp-catalog", "skills", "kits", "safety"}
        self.assertTrue(required.issubset(self.parser.ids))
        self.assertEqual([], [key for key, count in self.parser.id_counts.items() if count > 1])

    def test_beginner_and_advanced_material_are_present(self):
        for marker in ("tools", "resources", "prompts", "SKILL.md", "FastMCP", "lesson-designer"):
            self.assertIn(marker, self.html)
        self.assertGreaterEqual(self.parser.details, 4)

    def test_catalogs_and_safety_guidance_are_present(self):
        for marker in ("NotebookLM", "Google Colab", "GitHub MCP", "code-review-teacher"):
            self.assertIn(marker, self.html)
        for marker in ("только чтение", "персональн", "подтвержден"):
            self.assertIn(marker, self.html.lower())

    def test_existing_pages_link_to_the_continuation(self):
        href = 'href="instrumenty_mcp_skills.html"'
        self.assertIn(href, AGENTS_PAGE.read_text(encoding="utf-8"))
        self.assertIn('href="web/instrumenty_mcp_skills.html"', INDEX.read_text(encoding="utf-8"))
```

- [ ] **Step 2: Run the test and verify the expected failure**

Run:

```bash
python3 -m unittest tests/check_education_tools_page.py -v
```

Expected: failures because `web/instrumenty_mcp_skills.html` and its links do not exist.

- [ ] **Step 3: Commit the failing test**

```bash
git add tests/check_education_tools_page.py
git commit -m "test: define education tools page contract"
```

### Task 2: Build the educational page

**Files:**
- Create: `web/instrumenty_mcp_skills.html`
- Test: `tests/check_education_tools_page.py`

- [ ] **Step 1: Create semantic page structure**

Create the fixed nav, hero, and these section IDs:

```html
<section id="mcp">...</section>
<section id="skill">...</section>
<section id="tools">...</section>
<section id="mcp-catalog">...</section>
<section id="skills">...</section>
<section id="kits">...</section>
<section id="safety">...</section>
```

Use the formula `Инструмент → MCP → Skill → результат` as the main visual organizer.

- [ ] **Step 2: Add the beginner MCP explanation**

Show host/client/server/external-service flow and explain:

```text
resources = data to read
tools = functions the model can call
prompts = reusable task templates
```

Include a visible project tree and a numbered creation sequence.

- [ ] **Step 3: Add the advanced MCP example in `<details>`**

Use the official Python SDK shape:

```python
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("college-materials")
MATERIALS = Path(__file__).parent / "materials"


def safe_file(name: str) -> Path:
    candidate = (MATERIALS / name).resolve()
    if MATERIALS.resolve() not in candidate.parents:
        raise ValueError("Файл находится вне разрешённой папки")
    return candidate


@mcp.resource("material://{name}")
def read_material(name: str) -> str:
    return safe_file(name).read_text(encoding="utf-8")


@mcp.tool()
def list_materials() -> list[str]:
    return sorted(path.name for path in MATERIALS.glob("*.md"))


@mcp.prompt(title="План занятия")
def lesson_plan(topic: str, minutes: int = 90) -> str:
    return f"Составь план занятия по теме «{topic}» на {minutes} минут."


if __name__ == "__main__":
    mcp.run(transport="stdio")
```

Add install, run, and client JSON snippets. State that STDIO servers must not log to stdout.

- [ ] **Step 4: Add the beginner and advanced Skill explanations**

Show progressive disclosure and the folder tree:

```text
lesson-designer/
├── SKILL.md
├── references/
├── scripts/
└── assets/
```

Include an immediately visible minimal `SKILL.md`, plus a full `lesson-designer` example inside `<details>`. Explain that `name` and `description` are required and that the description determines implicit triggering.

- [ ] **Step 5: Add catalogs and ready-made kits**

Create cards for all tools, MCP servers, and skills listed in the approved design. Each catalog card must include purpose and a concrete use example. MCP cards also carry one access label: `Только чтение`, `С подтверждением`, or `Песочница`.

Create four workflow panels:

```text
Подготовка занятия
Проверка проекта
Организация кружка
Хакатон
```

- [ ] **Step 6: Add safety guidance and source links**

End with a seven-point checklist and links to:

- `https://modelcontextprotocol.io/docs/develop/build-server`
- `https://github.com/modelcontextprotocol/python-sdk`
- `https://agentskills.io/specification`
- `https://developers.openai.com/codex/skills`

- [ ] **Step 7: Add responsive styles and progressive enhancement**

Use CSS variables, lecture-compatible indigo/cyan colors, technical grid patterns, responsive card grids, visible keyboard focus, `prefers-reduced-motion`, and overflow-safe code blocks.

Add JavaScript only for:

```javascript
document.querySelectorAll("[data-copy]").forEach((button) => {
  button.addEventListener("click", async () => {
    const code = document.getElementById(button.dataset.copy);
    await navigator.clipboard.writeText(code.innerText);
    button.textContent = "Скопировано";
  });
});
```

Also add `IntersectionObserver` for reveal effects and active section navigation.

- [ ] **Step 8: Run the page test**

Run:

```bash
python3 -m unittest tests/check_education_tools_page.py -v
```

Expected: only the integration-link assertion may still fail.

- [ ] **Step 9: Commit the page**

```bash
git add web/instrumenty_mcp_skills.html
git commit -m "feat: add education tools MCP skills guide"
```

### Task 3: Integrate the continuation into the lecture

**Files:**
- Modify: `web/agentnye_sistemy.html`
- Modify: `index.html`
- Test: `tests/check_education_tools_page.py`

- [ ] **Step 1: Add a continuation link to the agent-systems navigation**

Add:

```html
<a class="nav-link" href="instrumenty_mcp_skills.html">Практика: MCP + Skills →</a>
```

- [ ] **Step 2: Add a final continuation panel**

Place a prominent panel after section 6 that explains that the next page moves from concepts to building and selecting educational tools.

- [ ] **Step 3: Add a main landing link**

Add a CTA linking to:

```html
<a href="web/instrumenty_mcp_skills.html">Практика: инструменты, MCP и Skills</a>
```

- [ ] **Step 4: Run all tests**

Run:

```bash
python3 -m unittest discover -s tests -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit the integration**

```bash
git add index.html web/agentnye_sistemy.html tests/check_education_tools_page.py
git commit -m "feat: link education tools continuation"
```

### Task 4: Browser verification

**Files:**
- Modify if needed: `web/instrumenty_mcp_skills.html`

- [ ] **Step 1: Start the local server**

Run:

```bash
python3 -m http.server 8000
```

- [ ] **Step 2: Verify desktop, tablet, and mobile**

Open `http://127.0.0.1:8000/web/instrumenty_mcp_skills.html` at:

- 1440×900
- 768×1024
- 390×844

Check `scrollWidth === clientWidth`, section navigation, all `<details>`, copy buttons, and source links.

- [ ] **Step 3: Check console errors**

Expected: no JavaScript errors.

- [ ] **Step 4: Run final verification**

Run:

```bash
python3 -m unittest discover -s tests -v
git diff --check
git status --short
```

Expected: tests pass, no whitespace errors, only intended changes remain.
