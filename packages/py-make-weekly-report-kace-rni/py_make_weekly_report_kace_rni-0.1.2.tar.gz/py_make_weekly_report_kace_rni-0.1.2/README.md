# GI-KACE Weekly Report Generator

A simple CLI tool to generate and save a structured weekly report for GI-KACE RNI Department.
Outputs a text file and also copies the content to the clipboard for quick sharing.

The aim of this project was to speed up weekly reporting by letting you focus on the important content while automating
the formatting and file management.
---

## Features

- **NEW in 0.1.1**: Remembers your name and unit between sessions
- Automatically detects the current week's date range
- Prompts for achievements and challenges
- Formats the report with a clean layout
- Saves report as a text file to your desktop:  
  `Week [n] [Month] [monday's date] - [friday's date].txt`
- Copies report to clipboard for easy pasting into emails or other documents

---

## Installation

```bash
pip install py_make_weekly_report_kace_rni
```

To update to the latest version:

```bash
pip install --upgrade py_make_weekly_report_kace_rni
```

---

## Usage

Run the following command in your terminal to launch the tool.

```bash
py_make-weekly-report
```

### First-time use

You'll be prompted to enter:

- Your name
- Your unit
- Project name
- Key achievements (press Enter twice to finish)
- Challenges and next steps (press Enter twice to finish)

### Subsequent use

The tool will:

- Remember your name and unit
- Ask if you want to change them
- Only prompt for new project details and achievements/challenges

### Configuration

Your name and unit preferences are automatically saved to:

- Windows: ```%USERPROFILE%\AppData\Local\WeeklyReportGenerator\config.json```
- macOS/Linux: ```~/.config/WeeklyReportGenerator\config.json```

### Report Storage

A text file is saved to your desktop under the folder:

```
Weekly Reports/[current year]/Week #[n] [Month] [monday's date] - [friday's date].txt
```

## Example Output

```txt
Subject: Week Report of May 13th – May 17th, [Anthony]
Unit: SE
Project: Internal Tooling

Key Achievement(s):
  • Refactored legacy codebase to improve testability.
  • Automated weekly report generation using Python.

Challenges and Next Steps:
  • Integration testing for the new reporting module.
  • Coordinate with DevOps to deploy updates.
```

---

## License

MIT

---

## Changelog

### 0.1.2 - latest

Improved the title of the saved file to be more user friendly.
- previously: ```Week [n] [Month] [monday's date] - [friday's date].txt```
    - example: ```Week 20 May 12 - 16```
- currently: ```Week #[n] [Month] [monday's date][ordinal] to [friday's date][ordinal].txt```
    - example: ```Week #20 May 12th to 16th```

### 0.1.1

- Added persistent configuration to remember name and unit
- Improved error handling
- Better cross-platform support for config storage

### 0.1.0

Initial release

---
