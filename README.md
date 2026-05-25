# Web Crawler – Cybersecurity Reconnaissance Pipeline

## Overview

This project is a modular web crawler designed for cybersecurity reconnaissance and attack-surface discovery.

The crawler does more than traditional scraping. It performs:

- Recursive crawling
- Endpoint discovery
- JavaScript intelligence extraction
- Authentication detection
- Secret detection
- Behavioral mapping
- Graph-based relationship analysis

The system collects and organizes web intelligence into structured outputs for further analysis.

---

# Core Modules

## fetcher.py

### Purpose
Handles downloading web pages.

### Responsibilities
- Async HTTP requests
- Timeout handling
- Retry logic
- Status code handling
- Rate limiting
- Custom headers

### Role in Pipeline
Fetches raw HTML content from target URLs.

---

## parser.py

### Purpose
Parses downloaded HTML pages.

### Extracts
- Links
- Scripts
- Endpoints
- Metadata
- Forms

### Role in Pipeline
Converts raw HTML into structured intelligence data.

---

## js_analyzer.py

### Purpose
Analyzes JavaScript files for hidden intelligence.

### Detects
- API routes
- Hidden endpoints
- Secrets
- Tokens
- JavaScript assets

### Importance
Modern applications expose many endpoints only inside JavaScript.

---

## parameter_analyzer.py

### Purpose
Extracts parameters and input points.

### Detects
- Query parameters
- API parameters
- User-controlled inputs

### Example

```text
?id=1
?page=2
/search?q=test
```

### Importance
Useful for attack-surface discovery and fuzzing preparation.

---

## auth_detector.py

### Purpose
Detects authentication-related behavior.

### Detects
- Login pages
- Protected routes
- Authentication flows
- Auth redirects

---

## form_extractor.py

### Purpose
Extracts HTML forms and input structures.

### Extracts
- Form actions
- Methods
- Input fields
- Form endpoints

### Importance
Forms reveal:
- Login systems
- APIs
- Attack entry points

---

## secret_detector.py

### Purpose
Detects exposed secrets and credentials.

### Detects
- API keys
- JWT tokens
- Access tokens
- Exposed credentials

### Importance
Critical for security reconnaissance.

---

## behavior_mapper.py

### Purpose
Maps application behavior and navigation flow.

### Tracks
- Endpoint relationships
- Page navigation
- Behavioral flow
- Logical application structure

### Importance
Creates application intelligence rather than simple scraping.

---

## json_writer.py

### Purpose
Converts collected intelligence into structured JSON output.

### Generates
- results.json
- formatted intelligence data

---

## normalizer.py

### Purpose
Normalizes URLs and extracted data.

### Responsibilities
- Canonicalization
- URL cleanup
- Duplicate reduction

---

## queue_manager.py

### Purpose
Manages crawler queue and recursion.

### Responsibilities
- Enqueue discovered URLs
- Deduplicate URLs
- Manage crawl depth
- Recursive crawling control

---

## store.py

### Purpose
Stores collected crawler data during execution.

### Handles
- Temporary storage
- Structured records
- Crawler state management

---

# Intelligence Layer

## graph_builder.py

### Location

```text
intelligence/graph_builder.py
```

### Purpose
Builds relationship graphs from extracted intelligence.

### Creates
- Nodes
- Edges
- Endpoint relationships
- Navigation maps

### Graph Examples
- Page → API
- Page → Form
- JS → Endpoint

### Importance
Transforms crawler data into attack-surface intelligence.

---

# Output Files

## results.json

### Contains
- Crawled URLs
- Endpoints
- Forms
- Parameters
- Scripts
- Metadata
- Authentication findings
- Secrets

---

## graph.json

### Contains
- Graph nodes
- Graph edges
- Relationships
- Crawl graph structure

### Used For
- Visualization
- Attack-surface mapping
- Intelligence analysis

---

# Current Features Implemented

## Crawling
- Recursive crawling
- Async fetching
- Queue management

## Parsing
- HTML parsing
- Link extraction
- Form extraction

## Intelligence Extraction
- JS analysis
- Parameter extraction
- Auth detection
- Secret detection
- Behavior mapping

## Intelligence Modeling
- Graph generation
- Relationship mapping

## Output Generation
- Structured JSON outputs
- Graph outputs

---

# Technologies Used

- Python
- Asyncio
- BeautifulSoup
- JSON
- Regex
- Graph-based intelligence modeling

---

# Current Project Stage

This project has evolved from:

- Basic scraping

Into:

- Cybersecurity reconnaissance
- Attack-surface discovery
- Intelligence extraction
- Graph-based application mapping

The crawler is now functioning as an intelligence pipeline rather than a simple web scraper.

---

# Future Improvements

## Planned Enhancements
- Browser automation
- Playwright integration
- Runtime interception
- SLM integration
- Vulnerability scoring
- Risk classification
- Visual graph dashboard
- API fingerprinting

---

# Main Entry Point

## main.py

Acts as the orchestration layer.

### Responsibilities
- Starts crawler
- Coordinates modules
- Controls workflow execution
- Manages recursion
- Triggers output generation
