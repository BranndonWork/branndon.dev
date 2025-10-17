# Scrapers

Independent scraper projects for data collection. Each scraper is a standalone project with its own dependencies and configuration.

## Architecture

```
scrapers/
├── utils/              # Shared utilities across all scrapers
├── JobsCrawler/        # Job board scraper
└── [future-scraper]/   # Add more scrapers as needed
```

## Usage

Each scraper directory:
- Is a complete, independent project
- Has its own README.md with origin info and setup instructions
- Uses Poetry for dependency management
- Can be run independently without affecting other scrapers

## Adding New Scrapers

1. Clone the source repo into `scrapers/`
2. Remove the `.git` directory: `rm -rf scrapers/[scraper-name]/.git`
3. Create a README.md documenting:
   - Original source URL
   - Clone date
   - Purpose and customizations
4. Install dependencies: `cd scrapers/[scraper-name] && poetry install`

## Shared Utilities

The `utils/` directory contains cross-scraper helpers that any scraper can import.
