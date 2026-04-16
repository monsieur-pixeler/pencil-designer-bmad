#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
First Breath — Deterministic sanctum scaffolding for Pencil Design Agent.

Creates the sanctum folder structure, copies template files with config values
substituted, copies all capability files into the sanctum, and auto-generates
CAPABILITIES.md from capability prompt frontmatter.

After this script runs, the sanctum is fully self-contained.

Usage:
    uv run scripts/init-sanctum.py <project-root> <skill-path>

    project-root: The root of the project (where _bmad/ lives)
    skill-path:   Path to the skill directory (where SKILL.md, references/, assets/ live)
"""

import sys
import re
import shutil
from datetime import date
from pathlib import Path

# --- Agent-specific configuration ---

SKILL_NAME = "pencil-design"
SANCTUM_DIR = SKILL_NAME

# Files that stay in the skill bundle (only used during First Breath, not copied to sanctum)
SKILL_ONLY_FILES = {
    "first-breath.md",
    "memory-guidance.md",
    "capability-authoring.md",
    "design-knowledge.md",
}

TEMPLATE_FILES = [
    "INDEX-template.md",
    "PERSONA-template.md",
    "CREED-template.md",
    "BOND-template.md",
    "MEMORY-template.md",
    "PULSE-template.md",
]

# Owner can teach Pencil new capabilities over time
EVOLVABLE = True

# --- End agent-specific configuration ---


def parse_yaml_config(config_path: Path) -> dict:
    """Simple YAML key-value parser for top-level scalar values."""
    config = {}
    if not config_path.exists():
        return config
    with open(config_path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if ":" in line:
                key, _, value = line.partition(":")
                value = value.strip().strip("'\"")
                if value:
                    config[key.strip()] = value
    return config


def parse_frontmatter(file_path: Path) -> dict:
    """Extract YAML frontmatter from a markdown file."""
    meta = {}
    with open(file_path) as f:
        content = f.read()

    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return meta

    for line in match.group(1).strip().split("\n"):
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("'\"")
    return meta


def copy_references(source_dir: Path, dest_dir: Path) -> list[str]:
    """Copy capability files (not skill-only files) into the sanctum."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []

    for source_file in sorted(source_dir.iterdir()):
        if source_file.name in SKILL_ONLY_FILES:
            continue
        if source_file.is_file():
            shutil.copy2(source_file, dest_dir / source_file.name)
            copied.append(source_file.name)

    return copied


def copy_scripts(source_dir: Path, dest_dir: Path) -> list[str]:
    """Copy scripts (except init itself) into the sanctum."""
    if not source_dir.exists():
        return []
    dest_dir.mkdir(parents=True, exist_ok=True)
    copied = []

    for source_file in sorted(source_dir.iterdir()):
        if source_file.is_file() and source_file.name != "init-sanctum.py":
            shutil.copy2(source_file, dest_dir / source_file.name)
            dst = dest_dir / source_file.name
            dst.chmod(0o755)
            copied.append(source_file.name)

    return copied


def discover_capabilities(references_dir: Path, sanctum_refs_path: str) -> list[dict]:
    """Scan references/ for capability prompt files with name and code frontmatter."""
    capabilities = []

    for md_file in sorted(references_dir.glob("*.md")):
        if md_file.name in SKILL_ONLY_FILES:
            continue
        meta = parse_frontmatter(md_file)
        if meta.get("name") and meta.get("code"):
            capabilities.append({
                "name": meta["name"],
                "description": meta.get("description", ""),
                "code": meta["code"],
                "source": f"{sanctum_refs_path}/{md_file.name}",
            })
    return capabilities


def generate_capabilities_md(capabilities: list[dict], evolvable: bool) -> str:
    """Generate CAPABILITIES.md from discovered capabilities."""
    lines = [
        "# Capabilities",
        "",
        "## Built-in",
        "",
        "| Code | Name | Description | Source |",
        "|------|------|-------------|--------|",
    ]
    for cap in sorted(capabilities, key=lambda c: c["code"]):
        lines.append(
            f"| [{cap['code']}] | {cap['name']} | {cap['description']} | `{cap['source']}` |"
        )

    if evolvable:
        lines.extend([
            "",
            "## Learned",
            "",
            "_Capabilities added by the owner over time. Prompts live in `capabilities/`._",
            "",
            "| Code | Name | Description | Source | Added |",
            "|------|------|-------------|--------|-------|",
            "",
            "## How to Add a Capability",
            "",
            'Tell me "I want you to be able to do X" and we\'ll create it together.',
            "I'll write the prompt, save it to `capabilities/`, and register it here.",
            "Next session, I'll know how.",
            "Load `./references/capability-authoring.md` for the full creation framework.",
        ])

    lines.extend([
        "",
        "## Tools",
        "",
        "### Pencil MCP (primary)",
        "_Connected via VS Code Extension or Desktop App. Tools: batch_design, get_screenshot,_",
        "_get_variables, set_variables, batch_get, get_guidelines, find_empty_space_on_canvas,_",
        "_snapshot_layout, export_nodes, open_document, search_all_unique_properties, replace_all_matching_properties_",
        "",
        "### User-Provided Tools",
        "_Additional MCP servers or services the owner has made available. Document them here._",
    ])

    return "\n".join(lines) + "\n"


def substitute_vars(content: str, variables: dict) -> str:
    """Replace {var_name} placeholders with values."""
    for key, value in variables.items():
        content = content.replace(f"{{{key}}}", value)
    return content


def main():
    if len(sys.argv) < 3:
        print("Usage: uv run scripts/init-sanctum.py <project-root> <skill-path>")
        sys.exit(1)

    project_root = Path(sys.argv[1]).resolve()
    skill_path = Path(sys.argv[2]).resolve()

    bmad_dir = project_root / "_bmad"
    sanctum_path = bmad_dir / "memory" / SANCTUM_DIR
    assets_dir = skill_path / "assets"
    references_dir = skill_path / "references"
    scripts_dir = skill_path / "scripts"

    sanctum_refs = sanctum_path / "references"
    sanctum_scripts = sanctum_path / "scripts"
    sanctum_refs_path = "./references"

    if sanctum_path.exists():
        print(f"Sanctum already exists at {sanctum_path}")
        print("Pencil has already been born. Skipping First Breath scaffolding.")
        sys.exit(0)

    # Load config for variable substitution
    config = {}
    for config_file in ["config.yaml", "config.user.yaml"]:
        config.update(parse_yaml_config(bmad_dir / config_file))

    today = date.today().isoformat()
    variables = {
        "user_name": config.get("user_name", "friend"),
        "communication_language": config.get("communication_language", "English"),
        "birth_date": today,
        "project_root": str(project_root),
        "sanctum_path": str(sanctum_path),
    }

    # Create sanctum structure
    sanctum_path.mkdir(parents=True, exist_ok=True)
    (sanctum_path / "capabilities").mkdir(exist_ok=True)
    (sanctum_path / "sessions").mkdir(exist_ok=True)
    print(f"Created sanctum at {sanctum_path}")

    # Copy capability reference files
    copied_refs = copy_references(references_dir, sanctum_refs)
    print(f"  Copied {len(copied_refs)} reference files to sanctum/references/")

    # Copy scripts (contrast-ratio.py, scan-hardcoded-values.py, etc.)
    copied_scripts = copy_scripts(scripts_dir, sanctum_scripts)
    if copied_scripts:
        print(f"  Copied {len(copied_scripts)} scripts to sanctum/scripts/")

    # Copy and substitute template files
    for template_name in TEMPLATE_FILES:
        template_path = assets_dir / template_name
        if not template_path.exists():
            print(f"  Warning: {template_name} not found, skipping")
            continue

        output_name = template_name.replace("-template", "").upper()
        output_name = output_name[:-3] + ".md"

        content = template_path.read_text()
        content = substitute_vars(content, variables)

        (sanctum_path / output_name).write_text(content)
        print(f"  Created {output_name}")

    # Auto-generate CAPABILITIES.md from frontmatter
    capabilities = discover_capabilities(references_dir, sanctum_refs_path)
    capabilities_content = generate_capabilities_md(capabilities, evolvable=EVOLVABLE)
    (sanctum_path / "CAPABILITIES.md").write_text(capabilities_content)
    print(f"  Created CAPABILITIES.md ({len(capabilities)} built-in capabilities)")

    print()
    print("First Breath scaffolding complete.")
    print("The conversational awakening can now begin.")
    print(f"Sanctum: {sanctum_path}")
    print()
    print("Next: start a conversation with Pencil and it will load first-breath.md automatically.")


if __name__ == "__main__":
    main()
