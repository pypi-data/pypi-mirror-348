# UFM Configuration Differentiator Tool

A powerful tool to compare UFM (Unified Fabric Manager) configurations between two NVIDIA servers.

## Features

- Compare UFM, SHARP, MFT, and OpenSM versions
- Identify differences between configuration files
- Generate HTML reports with highlighted differences
- Automatically sort higher versions for easier comparison
- Filter and search capabilities in the HTML report

## Installation

```bash
pip install ufm-config-diff
```

## Usage

```bash
# Basic usage
ufm-config-diff server1 server2 username password

# With optional output file
ufm-config-diff server1 server2 username password output_report.html

# Fast mode - only compare critical configuration files
ufm-config-diff server1 server2 username password --fast
```

## Requirements

- Python 3.6+
- SSH access to the servers
- UFM installed on both servers

## HTML Report

The tool generates an interactive HTML report that:

- Shows version differences between servers
- Lists all configuration differences
- Provides filtering and sorting capabilities
- Highlights missing parameters and differences
- Includes a table of contents for quick navigation

## License

MIT License 