# Local Setup Guide

## Overview
This is a static HTML site that uses Showdown.js to render Markdown blog posts dynamically. The site fetches Markdown content from GitHub and renders it client-side.

## Running Locally

### Option 1: Python HTTP Server (Recommended)
```bash
cd webroot
python3 -m http.server 8000
```
Then open http://localhost:8000 in your browser.

### Option 2: Node HTTP Server
If you have Node.js installed:
```bash
npx http-server webroot -p 8000
```
Then open http://localhost:8000 in your browser.

### Option 3: VS Code Live Server
If using VS Code:
1. Install the "Live Server" extension
2. Right-click on `webroot/index.html`
3. Select "Open with Live Server"

## Site Structure
- `webroot/` - Main web root directory
  - `index.html` - Main HTML file that loads and renders Markdown
  - `blog/content/` - Markdown blog posts
- `docs/` - Documentation directory

## How It Works
1. The site uses client-side JavaScript to fetch Markdown files
2. Showdown.js converts Markdown to HTML
3. Highlight.js provides syntax highlighting for code blocks
4. Bootstrap provides styling

## Note
The current setup fetches content from the GitHub repository. When running locally, blog posts will still be fetched from the remote GitHub repository unless you modify the fetch URL in `index.html`.