# Agents Guidelines

**Purpose:** Establish conventions for all AI agents working on this project.  
**Rule:** Follow these conventions for EVERY task. No exceptions.

---

## 1. Folder Organization Rule

**Always create a dedicated folder for any new work. Never dump files in the project root.**

```
Soil Moisture Detection/
├── dataset/              # ALL data-related work (images, scripts, metadata, reports)
├── literature review/    # Papers, references, citation notes
├── docs/                 # Project documentation, meeting notes, plans
└── paper/                # LaTeX/Markdown paper files, figures, tables
```

### When to Create a Folder

| You are doing... | Create folder at... |
|------------------|---------------------|
| Data preprocessing | `dataset/scripts/` |
| New experiment | `dataset/experiments/{experiment_name}/` |
| Model training | `dataset/models/{model_name}/` |
| Results/plots | `dataset/results/{experiment_name}/` |
| Literature notes | `literature review/notes/` |
| Paper figures | `paper/figures/` |
| Meeting notes | `docs/meetings/` |
| Progress tracking | `docs/` |

---

## 2. Script Naming Convention

**Pattern:** `{descriptive_name}_{step_number}.py`

| Good | Bad |
|------|-----|
| `preprocess_step0.py` | `script1.py` |
| `normalize_filenames_step0b.py` | `fix.py` |
| `train_resnet_fold1.py` | `train.py` |
| `evaluate_model_v2.py` | `eval.py` |

### Rules

1. **Use lowercase with underscores** (snake_case)
2. **Include step number** when part of a pipeline: `_step0`, `_step1a`, `_step1b`
3. **Be descriptive** - name should explain WHAT the script does
4. **Version suffixes** if needed: `_v2`, `_final` (but prefer step numbers)
5. **Never use spaces** in filenames

---

## 3. Output Organization

**Every script must write outputs to a predictable location.**

```python
# GOOD: Relative to script location
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = DATASET_DIR / "preprocessed"

# BAD: Hardcoded absolute paths
OUTPUT_DIR = Path(r"C:\Users\raiya\...")
```

### Output Folder Convention

```
dataset/
├── scripts/          # Code (read-only after writing)
├── raw/              # Original data (never modify)
├── clean/            # Processed data (regenerable)
├── preprocessed/     # Intermediate outputs (CSVs, JSONs)
├── experiments/      # Experiment-specific outputs
│   └── {name}/
│       ├── models/   # Saved model weights
│       ├── results/  # Metrics, plots
│       └── logs/     # Training logs
└── metadata/         # Annotation files
```

---

## 4. File Naming for Outputs

**Pattern:** `{descriptive_name}.{ext}`

| Type | Pattern | Example |
|------|---------|---------|
| CSV | `{purpose}.csv` | `image_manifest.csv` |
| JSON | `{purpose}.json` | `anomalies.json` |
| Model weights | `{model}_{epoch}.pt` | `resnet50_epoch10.pt` |
| Plots | `{metric}_{condition}.png` | `loss_curve_baseline.png` |
| Logs | `{experiment}_{date}.log` | `exp01_20260707.log` |

### Rules

1. **No spaces** in filenames
2. **Use underscores** not hyphens
3. **Lowercase** for all output files
4. **Include date** for time-sensitive outputs: `_{YYYYMMDD}`
5. **Version suffix** only when needed: `_v2`, `_final`

---

## 5. Path Handling

**Always use relative paths from the script location.**

```python
from pathlib import Path

# CORRECT: Relative to script
SCRIPT_DIR = Path(__file__).resolve().parent
DATASET_DIR = SCRIPT_DIR.parent
RAW_DIR = DATASET_DIR / "raw"

# WRONG: Hardcoded paths
RAW_DIR = Path(r"E:\CSE498R\Soil Moisture Detection\Image")

# WRONG: Relative to CWD (unreliable)
RAW_DIR = Path("../Image")
```

---

## 6. Document Structure

**Every markdown file must have:**

1. **Title** with project context
2. **Table of Contents** (for files > 100 lines)
3. **Numbered sections** for easy referencing
4. **Code blocks** with language tags
5. **Tables** for structured data

### Document Naming

| Type | Name | Location |
|------|------|----------|
| Dataset docs | `dataset_details.md` | `dataset/` |
| Experiment plan | `{experiment_name}_plan.md` | `docs/` |
| Literature notes | `{paper_author}_year.md` | `literature review/` |
| Meeting notes | `{YYYY-MM-DD}_meeting.md` | `docs/meetings/` |

---

## 7. Version Control

### Commit Messages

```
type(scope): description

Examples:
feat(dataset): add preprocessing pipeline
fix(scripts): correct path resolution on Windows
docs(paper): update methodology section
```

### What to Track

| Track | Don't Track |
|-------|-------------|
| Scripts | `raw/` images |
| Config files | `clean/` images |
| Documentation | `preprocessed/` outputs |
| Metadata templates | `__pycache__/` |
| `agents.md` | `.pyc` files |

---

## 8. Common Mistakes to Avoid

| Mistake | Why It's Bad | Do This Instead |
|---------|-------------|-----------------|
| Dumping files in root | Unfindable, messy | Create a folder |
| Hardcoded paths | Breaks on other machines | Use `Path(__file__)` |
| `script.py` | Uninformative | `preprocess_step0.py` |
| Mixing raw and processed | Accidental data loss | Separate `raw/` and `clean/` |
| No output folder | Files scattered everywhere | Define `OUTPUT_DIR` |
| Single-letter variables | Unreadable | Use `image_dir`, `output_path` |

---

## 9. Agent Checklist

Before completing ANY task, verify:

- [ ] All files are in the correct folder
- [ ] Script names follow `{name}_{step}.py` convention
- [ ] Paths are relative (no hardcoded absolute paths)
- [ ] Output files go to a designated output folder
- [ ] No files left in project root that belong in a subfolder
- [ ] Documentation updated if new folders/files created
- [ ] `agents.md` updated if new conventions needed

---

## 10. Quick Reference

```
PROJECT ROOT/
├── dataset/
│   ├── dataset_details.md      # Full dataset documentation
│   ├── raw/                    # Original images (DO NOT MODIFY)
│   ├── clean/                  # Normalized images (regenerable)
│   ├── preprocessed/           # CSVs, JSONs, split assignments
│   ├── scripts/                # All Python scripts
│   ├── metadata/               # Excel templates, annotations
│   ├── reports/                # Analysis reports
│   └── experiments/            # Experiment outputs (create as needed)
├── literature review/          # Papers and references
├── docs/                       # Project documentation
└── paper/                      # Research paper files
```
