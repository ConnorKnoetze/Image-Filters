# Image Filters

An instanced upload, image filters website where users upload images to apply a selected filter.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the app (development)](#running-the-app-development)
- [Available Filters](#available-filters)

---

## Overview

Image Filters is a small web application that lets users upload images and apply client- or server-side filters to them (e.g., grayscale, sepia, invert, blur). It was built as an interactive, upload-based image processing demo with a simple UI and a Python/Flask backend.

---

## Features

- Upload one or more images
- Preview images in the browser
- Apply a variety of image filters (server-side)
- Download or save the filtered image(s)
- Responsive UI using HTML/CSS/JavaScript
- Backend processing implemented in Python with Flask

---

## Tech Stack

- Python (Flask backend)
- HTML, CSS, JavaScript (frontend)
- Pillow and NumPy for image processing (listed in requirements)

Key files discovered:
- Application entrypoint: `wsgi.py` (creates/exports `app`)
- Flask app factory: `filters/create_app` (in `filters/__init__.py`)
- Per-filter blueprints under `filters/blueprints/filter_types/`
- Upload helpers under `filters/blueprints/upload/`
- Requirements: `requirements.txt` (Flask, Werkzeug, pillow, numpy)

---

## Getting Started

These instructions will help you run a local copy of the project for development and testing.

### Prerequisites

- Python 3.8+
- pip
- (Optional) virtualenv or venv
- Git

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/ConnorKnoetze/Image-Filters.git
   cd Image-Filters
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # macOS / Linux
   .venv\Scripts\activate      # Windows (PowerShell)
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

---

### Running the app (development)

This project exposes the Flask application as the module-level `app` in `wsgi.py`. There are two simple ways to run it in development:

Option A — run the entrypoint directly (recommended for quick local runs):
```bash
python wsgi.py
```
This will run the app on `0.0.0.0:5000` by default. The script reads `FLASK_DEBUG` (default "1") to enable the reloader/debug mode.

Option B — use `flask run` (uses the exported `app` from the module):
```bash
# POSIX (macOS / Linux)
export FLASK_APP=wsgi:app
export FLASK_DEBUG=1
flask run --host=0.0.0.0 --port=5000

# Windows (PowerShell)
$env:FLASK_APP="wsgi:app"
$env:FLASK_DEBUG="1"
flask run --host=0.0.0.0 --port=5000
```

Notes:
- The project creates an `uploads` directory at runtime if it doesn't exist.
- The app's debug behavior is controlled by the `FLASK_DEBUG` environment variable (the `wsgi.py` file checks this).

---

## Available Filters

Implemented filter blueprints:
- Grayscale
- Pixelate
- Inverted
- Duotone
- Gaussian

---
