# GitLab Issue Anomaly Detector

A Python package for detecting anomalies in GitLab issues and generating HTML reports.

## Overview

This package analyzes GitLab issues to detect various anomalies such as:
- Missing milestones or iterations
- Insufficient descriptions
- Stale issues
- Blocked issues without details
- And many more

It generates a comprehensive HTML report with interactive visualizations to help teams identify and address these anomalies.

## Installation

```bash
pip install gitlab-detector
```

## Usage

### Command Line

```bash
# Run the anomaly detector and generate a report
gitlab-anomaly-detector
```

### Environment Variables

Create a `.env` file with the following variables:

```
GITLAB_URL=https://gitlab.com
GITLAB_TOKEN=your_personal_access_token
GITLAB_PROJECT_ID=your_project_id
```

### Viewing the Report

After running the tool, you can view the generated report by starting a local HTTP server:

```bash
python -m http.server 8008 -d public/
```

Then open your browser to http://localhost:8008

## Features

### Anomaly Detection

- **Issue Hygiene**: Detect issues with poor descriptions, missing milestones, or missing iterations
- **Workflow Impediments**: Identify blocked issues, stale issues, and scope creep
- **Priority Management**: Flag high-priority issues that lack proper attention
- **Timeline Analysis**: Track issues that are at risk of missing deadlines

### Reporting

- **Interactive Dashboard**: Filter and sort anomalies by type, severity, and owner
- **Milestone View**: Group anomalies by milestone to identify at-risk deliverables
- **Iteration View**: Track anomalies within your agile iterations
- **Export Functionality**: Export data to Excel for further analysis

## Testing

This package follows strict test-driven development practices. To run the tests:

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run tests with pytest
python -m pytest tests/
```

## Logging

The package implements robust logging throughout the codebase. Logs are output to stdout by default but can be configured via Python's standard logging module.

Example log output:

```
2025-05-15 22:57:01,584 - scripts.issue_anomaly_detector - DEBUG - Categorized anomaly 'poor_description' as 'hygiene'
2025-05-15 22:57:01,584 - scripts.issue_anomaly_detector - DEBUG - Categorized anomaly 'missing_milestone' as 'hygiene'
```

## GitLab Pages with Dynamic Content

This project includes a custom GitLab CI/CD pipeline for GitLab Pages that generates dynamic content:

1. A `prepare-pages` stage runs before the `pages` stage
2. A Python script (`scripts/prepare_pages.py`) generates dynamic content:
   - Creates a `data.json` file with timestamp and sample data
   - Updates `index.html` to load and display the dynamic content
3. The `pages` stage deploys the generated content

When you push to the `main` branch, the pipeline automatically runs and deploys your site to GitLab Pages.

***

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Submit a pull request

### Development Setup

```bash
# Clone the repository
git clone https://gitlab.com/my-group-name2452611/my-project-name.git
cd my-project-name

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e .[dev]
```

### Coding Standards

This project follows strict test-driven development practices:

- Write tests before implementing features
- Maintain high test coverage
- Implement robust logging throughout the codebase
- Follow PEP 8 style guidelines

## License

This project is licensed under the MIT License - see the LICENSE file for details.
