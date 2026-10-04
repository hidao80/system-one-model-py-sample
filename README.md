# systemone-demo

A sample that uses [OpenThai-SystemOne](https://huggingface.co/iapp/OpenThai-SystemOne) to recommend which of Windows, macOS, Linux Desktop, Android, and iOS/iPadOS best fits a user's needs.

## How it works

The generic `decision(state, options, question, yes, no)` function in [main.py](main.py) builds the same yes/no question for each option as a `Noul` and passes it to `SystemOneClient.system_one()`. It returns the `(name, noul)` pairs (match scores) sorted in descending order. The question and the criteria are templates, so `decision()` is not tied to OS recommendation: change `options` and the templates to rank anything else.

The sample calls `decision()` once per need ("Does this OS match the customer's needs?"), so several needs can be evaluated in turn and the results are printed. The sample includes the following two needs:

- `Developer`: a developer who wants to avoid license fees and wants a highly customizable environment
- `Beginner`: a person who is looking for a device for web browsing and messaging, and is not familiar with computers

## Supported languages

According to the [model card](https://huggingface.co/iapp/OpenThai-SystemOne), OpenThai-SystemOne is a **Thai + English** model. The `state`, the questions (`instructions`, `criteria`), and the options can be written in either language. The model card documents no other languages, so other languages (including Japanese) are unverified.

- It is trained on a Thai-heavy mix, so English calibration is weaker than Thai (median ECE 0.15 vs. 0.05 or less). Treat the English match scores in this sample as rough guides.
- The model is small (0.8B parameters). Use the `confidence` field and route low-confidence cases to a bigger model or a human.
- It handles text only, with at most 255 options per question and 64k tokens per request.

This sample writes both the needs and the questions in English.

## Requirements

- Python 3.13 or later
- [uv](https://docs.astral.sh/uv/)
- Dependency: `openthai-systemone` (listed in `pyproject.toml`)

## Installation

1. Install uv (skip this if it is already installed).

   Windows (PowerShell):

   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   macOS / Linux:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. Move to the project directory and install the dependencies. Following `.python-version`, uv fetches Python 3.13 if it is not available.

   ```bash
   uv sync
   ```

   This creates a virtual environment, `.venv`, inside the project.

## Usage

```bash
uv run main.py
```

On the first run, the model (`iapp/OpenThai-SystemOne`) is downloaded. The execution device is selected automatically from CUDA, MPS, and CPU.

For each need, only the option name and its confidence (a real number from 0 to 1) are printed, from the best match down. The needs are printed one after another in the order of `NEEDS`, with no labels or separators. Example output (the numbers are illustrative):

```
Linux Desktop: 0.8500
macOS: 0.4000
Windows: 0.3000
Android: 0.1000
iOS/iPadOS: 0.0500
iOS/iPadOS: 0.6000
Android: 0.5500
macOS: 0.4500
Windows: 0.4000
Linux Desktop: 0.2000
```

## Customization

You only need to change the following two places in [main.py](main.py):

- `NEEDS`: a dictionary of user needs. Each key is a display label and each value is the need text (in English). Adding an entry makes that need get evaluated too
- `PRODUCTS`: the recommendation candidates. Each key is the display name and each value is the description embedded in the question

The question (`instructions`) and the criteria (`criteria`) are generated for each option from the templates passed to `decision()` (`question`, `yes`, `no`).
