# YC Scraper

YC Scraper is a web scraping and indexing tool designed to extract company information from Y Combinator's database. The project uses Python, Scrapy for web scraping, Docker for containerization, and Elasticsearch for data indexing and searching.

## Features
- Automated web scraping of Y Combinator company data
- Optional image data collection
- Elasticsearch-based search functionality
- Docker containerization for easy deployment
- Interactive search interface
- Configurable crawling options

## Prerequisites

The setup script will automatically check and install most requirements, but you should have:
- Windows operating system
- Internet connection
- Administrator privileges

The script will automatically install/check for:
- Python (version 3.12.0 - 3.12.x)
- Docker and Docker Compose
- Firefox browser
- Required Python packages

## Project Structure
```
YC-Scraper/
├── setup.bat          # Environment setup and dependency installer
├── crawler.bat        # Web scraping script
├── indexbuilder.bat   # Elasticsearch indexing script
├── search.bat         # Search interface script
├── requirements.txt   # Python dependencies
├── docker-compose.yaml
├── PyElasticDumper.py
├── SearchQuery.py
├── ycombinator/
│   └── ycombinator/
│       └── spiders/
│           └── yscraper.py
└── ycombinator_with_image/
    └── ycombinator/
        └── spiders/
            └── yscraper.py
```

## Installation and Setup

Simply run the setup script:
```bash
setup.bat
```
The setup script will automatically:
- Check and verify Docker installation
- Check and verify Docker Compose installation
- Check and install Firefox browser if needed
- Verify Python version (3.12.0 - 3.12.x) and install if needed
- Create and activate a virtual environment
- Install required Python packages
- Start Docker containers using Docker Compose

### Suggested Setup Usage
The simplest way to get started is to just double-click `setup.bat` or run it from the command prompt. Wait for the script to complete all installations and verifications. The script will show progress information for each step.

## Usage

### 1. Running the Crawler

⚠️ **Important Crawling Time and Data Size Information:**
- Without images (`crawler.bat`): 
  - Crawling time: ~15 minutes
  - Output file size: ~100MB
- With images (`crawler.bat -i`): 
  - Crawling time: 25-30 minutes
  - Output file size: ~600MB
- Quick test option (`crawler.bat -s seed2small.txt`):
  - Crawling time: ~5 minutes
  - Perfect for testing the crawler functionality
  - Uses a smaller dataset

The crawler can be run in different modes using `crawler.bat`:

```bash
# Quick test with small dataset - 5min
crawler.bat -s seed2small.txt

# Basic usage (without images) - 15min, ~100MB
crawler.bat

# With image data - 25-30min, ~600MB
crawler.bat -i

# With custom output file
crawler.bat -o custom_output.jl

# Combining options
crawler.bat -i -o custom_output.jl -s seed.txt
```

Parameters:
- `-i`: Enable image data collection (increases crawling time and file size significantly)
- `-o`: Specify output file path (default: output.jl)
- `-s`: Specify seed file containing URLs to scrape (use seed2small.txt for quick testing)

### Suggested Crawler Usage
For most users, we recommend starting with:
```bash
# For testing (5 minutes)
crawler.bat -s seed2small.txt

# For full dataset without images (15 minutes)
crawler.bat

# For full dataset with images (25-30 minutes)
crawler.bat -i
```
Choose based on your needs:
- Use seed2small.txt for quick testing
- Run without -i flag for faster crawling and smaller file size
- Use -i flag only when images are necessary (significantly increases time and file size)

### 2. Building the Index

After collecting data, build the Elasticsearch index:
```bash
indexbuilder.bat [input_file]
```
- `input_file` is optional (defaults to output.jl)
- This script will load the scraped data into Elasticsearch

### Suggested Index Builder Usage (2min)
If you've used the default crawler settings, simply double-click `indexbuilder.bat` or run:
```bash
indexbuilder.bat
```
This will automatically index the data from output.jl into Elasticsearch.

### 3. Searching the Data

To search through the indexed data:
```bash
search.bat
```
This will launch an interactive search interface where you can query the collected data.

### Suggested Search Usage
Simply double-click `search.bat` or run:
```bash
search.bat
```
This will open an interactive console where you can type your search queries to find companies in the database.

## Troubleshooting

1. If setup.bat fails:
   - Ensure you have administrator privileges
   - Check your internet connection
   - Ensure Docker is running
   - Check if any antivirus is blocking installations
   - Verify you have enough disk space (at least 1GB free)

2. If crawler.bat fails:
   - Check internet connectivity
   - Verify Firefox is properly installed
   - Verify seed file format if using one
   - Check available disk space (600MB+ for image crawling)
   - Try the small seed file first to verify functionality

3. If indexbuilder.bat fails:
   - Ensure Elasticsearch container is running
   - Check if the input file exists
   - Verify Docker container health
   - Ensure enough memory is available for Elasticsearch

## System Requirements

- Minimum 4GB RAM (8GB recommended for image crawling)
- At least 1GB free disk space (2GB recommended for image crawling)
- Windows 10 or later
- Stable internet connection
- Administrator privileges

## Notes

- The crawler uses Firefox browser for web scraping
- Rate limiting is implemented to avoid overwhelming the target servers
- Images are stored in base64 format when using the -i flag
- Search functionality supports fuzzy matching and advanced query syntax
- All installations are performed with minimal user interaction
- Data is stored locally and can be reindexed as needed

## Clean Up

To stop all containers and clean up:
```bash
docker-compose down
```
This will stop and remove all Docker containers created by the project.

## Quick Start Guide

For the fastest way to get started, simply:

1. Ensure you have administrator privileges
2. Double-click `setup.bat` and wait for completion
3. Double-click `crawler.bat -s seed2small.txt` for a quick test (5 min)
4. Double-click `indexbuilder.bat` to index the collected data
5. Double-click `search.bat` to search through the data

This simple sequence will get you from installation to searching YC company data with minimal configuration required.

## Data Privacy and Usage

- This tool is for educational and research purposes
- Respect website terms of service and robots.txt rules
- Consider rate limiting when crawling large datasets
- Handle any collected data in accordance with applicable privacy laws

## Support

If you encounter any issues:
1. Check the troubleshooting section
2. Verify system requirements
3. Try the quick test option first
4. Check the logs in crawler_log.txt for detailed error messages