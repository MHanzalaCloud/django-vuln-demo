# Automated Vulnerability Detection in CI/CD Pipeline
### Final Project — BSCS | Cloud Security

---

## What This Project Demonstrates

This project shows how to automatically detect security vulnerabilities in a Django web application using a CI/CD security pipeline. Every time code is pushed to GitHub, 4 security tools run automatically — no human needed.

---

## Project Structure

```
django-vuln-demo/
├── .github/
│   ├── dependabot.yml          ← Auto-updates vulnerable packages
│   └── workflows/
│       └── security-scan.yml   ← The CI/CD security pipeline
├── notes_project/
│   ├── settings.py             ← ⚠️ Contains intentional vuln #3
│   └── urls.py
├── notes/
│   ├── models.py               ← Note model (title, content, subject)
│   ├── views.py                ← ⚠️ Contains intentional vuln #4
│   ├── urls.py
│   └── templates/
│       └── notes/
│           ├── index.html
│           └── detail.html
├── requirements.txt            ← ⚠️ Contains intentional vulns #1 and #2
├── setup.cfg                   ← Bandit scanner configuration
└── README.md
```

---

## Intentional Vulnerabilities (For Demo)

These 4 vulnerabilities were planted on purpose to demonstrate that the pipeline catches them:

| # | Vulnerability | Location | Tool That Catches It | Severity |
|---|---|---|---|---|
| 1 | `Pillow==9.0.1` — CVE-2022-45198 | `requirements.txt` | pip-audit, Trivy | HIGH |
| 2 | `requests==2.20.0` — CVE-2018-18074 | `requirements.txt` | pip-audit | MEDIUM |
| 3 | Hardcoded SECRET_KEY in settings | `notes_project/settings.py` | Bandit (B105) | HIGH |
| 4 | SQL Injection in search view | `notes/views.py` | Bandit (B608), CodeQL | MEDIUM |

---

## Security Tools Used

### 1. Bandit — Static Code Analysis (SAST)
- Scans Python source code line by line
- Finds hardcoded secrets, SQL injection, dangerous functions
- Rule B105 → hardcoded password/key
- Rule B608 → SQL injection via string concatenation

### 2. pip-audit — Dependency Vulnerability Scanner
- Scans `requirements.txt` against OSV database (Google's Open Source Vulnerabilities)
- Every package version is checked against publicly known CVEs
- Generates a clear report: package name, CVE ID, fixed version

### 3. Trivy (by Aqua Security) — Filesystem Scanner
- Scans both code and dependencies together
- Uploads results to GitHub Security tab automatically
- Detects CRITICAL, HIGH, and MEDIUM severity issues

### 4. CodeQL (by GitHub) — Deep Code Analysis
- AI-powered code scanner built into GitHub
- Detects complex vulnerability patterns
- Catches SQL injection, XSS, path traversal, and more
- Results appear in GitHub's Security tab

### 5. Dependabot — Automatic Fix PRs
- Monitors dependencies daily
- When a vulnerability is found, it opens a Pull Request with the fix automatically

---

## How the Pipeline Works

```
Developer pushes code to GitHub
           ↓
  Pipeline triggers automatically
           ↓
  ┌─────────────────────────────┐
  │  4 Jobs run in parallel:    │
  │  1. Bandit SAST Scan        │
  │  2. pip-audit CVE Scan      │
  │  3. Trivy Filesystem Scan   │
  │  4. CodeQL Deep Analysis    │
  └─────────────────────────────┘
           ↓
  Reports uploaded to:
  - GitHub Security Tab
  - Artifacts (downloadable reports)
  - Console output (visible in Actions)
           ↓
  Developer sees exactly what
  vulnerabilities exist and how to fix them
```

---

## How to Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/django-vuln-demo
cd django-vuln-demo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Start the server
python manage.py runserver

# 6. Run Bandit manually (optional)
pip install bandit
bandit -r . --exclude ./.git,./venv

# 7. Run pip-audit manually (optional)
pip install pip-audit
pip-audit --requirement requirements.txt
```

---

## How to Enable GitHub Security Features

1. Go to your repo → **Settings** → **Security** → **Code security and analysis**
2. Enable:
   - **Dependabot alerts** — ON
   - **Dependabot security updates** — ON
   - **CodeQL analysis** — ON
   - **Secret scanning** — ON
   - **Push protection** — ON

---

## Key Learning — Why This Matters

> The CI/CD pipeline automates the **process** of building and deploying code, but it does not automatically make code **secure**. Security tools must be deliberately added as checkpoints in the pipeline.
>
> Without automated scanning, a developer can push vulnerable code at 2 AM, it deploys automatically, and no one finds out until an attacker exploits it. With this pipeline, the same push triggers all 4 scanners instantly — vulnerabilities are caught before they reach production.

---

*Student Notes App — Django | Python | GitHub Actions | Bandit | pip-audit | Trivy | CodeQL*
