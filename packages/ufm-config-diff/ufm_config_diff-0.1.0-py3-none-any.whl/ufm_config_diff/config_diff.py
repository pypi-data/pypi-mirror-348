import paramiko
import os
import re
import logging
import argparse
from io import StringIO
import sys
from datetime import datetime
from bs4 import BeautifulSoup


# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Helper function to compare version strings without external dependencies
def compare_versions(version1, version2):
    """Compare two version strings, returns True if version2 > version1"""
    try:
        # Split versions by dots and compare numerically
        v1_parts = re.split(r'[.-]', version1.lower().replace('build', '').strip())
        v2_parts = re.split(r'[.-]', version2.lower().replace('build', '').strip())
        
        # Convert to integers where possible
        v1_cleaned = []
        v2_cleaned = []
        
        for part in v1_parts:
            try:
                v1_cleaned.append(int(part))
            except ValueError:
                v1_cleaned.append(part)
                
        for part in v2_parts:
            try:
                v2_cleaned.append(int(part))
            except ValueError:
                v2_cleaned.append(part)
        
        # Compare each part
        for i in range(min(len(v1_cleaned), len(v2_cleaned))):
            # If both parts are integers, compare numerically
            if isinstance(v1_cleaned[i], int) and isinstance(v2_cleaned[i], int):
                if v1_cleaned[i] < v2_cleaned[i]:
                    return True
                elif v1_cleaned[i] > v2_cleaned[i]:
                    return False
            # Otherwise compare as strings
            else:
                if str(v1_cleaned[i]) < str(v2_cleaned[i]):
                    return True
                elif str(v1_cleaned[i]) > str(v2_cleaned[i]):
                    return False
                    
        # If we've compared all parts and they're equal so far,
        # the longer version is considered greater
        return len(v1_cleaned) < len(v2_cleaned)
    except Exception as e:
        logger.warning(f"Error comparing versions, falling back to string comparison: {e}")
        # If all else fails, fall back to lexicographical comparison
        return version2 > version1

# SSH Helper Function
def ssh_connect(host, username, password):
    try:
        logger.info(f"Connecting to {host}...")
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host, username=username, password=password)
        return ssh
    except Exception as e:
        logger.error(f"SSH connection failed for {host}: {e}")
        raise

# Function to fetch files with .cfg and .conf extensions
def fetch_config_files(ssh, path="/opt/ufm/"):
    try:
        files = []
        stdin, stdout, stderr = ssh.exec_command('find {} -type f \\( -name "*.cfg" -o -name "*.conf" \\)'.format(path))
        files = stdout.read().decode().splitlines()
        logger.info(f"Found {len(files)} configuration files.")
        return files
    except Exception as e:
        logger.error(f"Failed to fetch configuration files: {e}")
        raise

# Function to fetch UFM version
def fetch_ufm_version(ssh, path="/opt/ufm/files/ufm_version"):
    try:
        stdin, stdout, stderr = ssh.exec_command(f"cat {path}")
        version = stdout.read().decode().strip()
        if version:
            logger.info(f"UFM Version: {version}")
            return version
        else:
            logger.error("UFM version file not found or empty.")
            return None
    except Exception as e:
        logger.error(f"Failed to fetch UFM version: {e}")
        raise

# Function to get UFM version
def get_ufm_version(ssh, host=None):
    try:
        # Execute the command and get the output
        stdin, stdout, stderr = ssh.exec_command("cat /opt/ufm/files/ufm_version")
        version = stdout.read().decode('utf-8').strip()
        
        # Add error logging
        error = stderr.read().decode('utf-8').strip()
        if error:
            logger.error(f"Error reading UFM version on {host}: {error}")
        
        # Add debug logging
        logger.debug(f"UFM version read: {version}")
        
        if not version:
            logger.warning(f"UFM version file is empty on {host}")
            return "Unknown"
            
        return version
    except Exception as e:
        if host:
            logger.error(f"Error reading UFM version on {host}: {e}")
        else:
            logger.error(f"Error reading UFM version: {e}")
        return "Unknown"

def strip_ansi_codes(text):
    """Remove ANSI escape sequences from text"""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

# Function to compare parameters between two configuration files
def compare_files(ssh1, ssh2, file_path):
    try:
        # Read content from both servers
        stdin1, stdout1, stderr1 = ssh1.exec_command(f"cat {file_path}")
        stdin2, stdout2, stderr2 = ssh2.exec_command(f"cat {file_path}")
        
        # Read raw bytes instead of trying to decode as UTF-8
        file1_content = stdout1.read()
        file2_content = stdout2.read()

        try:
            # Try to decode as UTF-8 first
            file1_lines = [strip_ansi_codes(line) for line in file1_content.decode('utf-8').splitlines()]
            file2_lines = [strip_ansi_codes(line) for line in file2_content.decode('utf-8').splitlines()]
        except UnicodeDecodeError:
            # If UTF-8 fails, treat as binary and compare raw bytes
            if file1_content != file2_content:
                return [("Binary file differs", "Binary file differs")]
            return []

        # Parse parameters from both files
        def parse_config(lines):
            params = {}
            for line in lines:
                line = line.strip()
                # Skip empty lines, comments, and UFM version lines
                if (not line or 
                    line.startswith('#') or 
                    line.startswith(';') or 
                    'UFM Version' in line):  # Skip UFM Version lines
                    continue
                # Try to split on common parameter separators (=, :, space)
                for separator in ['=', ':', ' ']:
                    if separator in line:
                        key, value = line.split(separator, 1)
                        key = key.strip()
                        value = value.strip()
                        params[key] = value
                        break
            return params

        params1 = parse_config(file1_lines)
        params2 = parse_config(file2_lines)

        # Compare parameters
        diff = []
        # Check all keys from first file
        for key in params1:
            if key in params2:
                if params1[key] != params2[key]:
                    diff.append((
                        f"{key}: {params1[key]}",
                        f"{key}: {params2[key]}"
                    ))
            else:
                diff.append((f"{key}: {params1[key]}", "Parameter not found"))

        # Check for parameters only in second file
        for key in params2:
            if key not in params1:
                diff.append(("Parameter not found", f"{key}: {params2[key]}"))

        return diff

    except Exception as e:
        logger.error(f"Error comparing file {file_path} between servers: {e}")
        raise

def compare_configurations(server1, server2, fast_mode=False):
    try:
        ssh1 = ssh_connect(server1['host'], server1['username'], server1['password'])
        ssh2 = ssh_connect(server2['host'], server2['username'], server2['password'])

        # Check UFM version files exist on both servers
        logger.info("Checking UFM installation on servers...")
        if not check_ufm_version(ssh1, server1['host']):
            print(f"\nError: UFM version file not found on {server1['host']}")
            print("Please ensure UFM is properly installed and the version file exists at /opt/ufm/files/ufm_version")
            sys.exit(1)
            
        if not check_ufm_version(ssh2, server2['host']):
            print(f"\nError: UFM version file not found on {server2['host']}")
            print("Please ensure UFM is properly installed and the version file exists at /opt/ufm/files/ufm_version")
            sys.exit(1)

        # If we get here, both servers have UFM version files
        logger.info("UFM installation verified on both servers")
        
        # Get UFM versions
        ufm_version1 = get_ufm_version(ssh1, server1['host'])
        ufm_version2 = get_ufm_version(ssh2, server2['host'])
        
        # Get SHARP versions
        sharp_version1 = get_sharp_version(ssh1, server1['host'])
        sharp_version2 = get_sharp_version(ssh2, server2['host'])

        # Get MFT versions
        mft_version1 = get_mft_version(ssh1, server1['host'])
        mft_version2 = get_mft_version(ssh2, server2['host'])

        # Get OpenSM versions
        opensm_version1 = get_opensm_version(ssh1, server1['host'])
        opensm_version2 = get_opensm_version(ssh2, server2['host'])

        base_path = "/opt/ufm/files/"
        
        if fast_mode:
            # In fast mode, only check specific files with their full paths
            critical_files = [
                '/opt/ufm/files/conf/gv.cfg',
                '/opt/ufm/files/conf/opensm/opensm.conf',
                '/opt/ufm/files/conf/sharp/sharp_am.cfg',
                '/opt/ufm/files/conf/ibutils2/ibdiagm.conf',
                '/etc/mft/mft.conf'
            ]
            files1 = critical_files
            files2 = critical_files
        else:
            # Get list of all files from both servers
            stdin1, stdout1, stderr1 = ssh1.exec_command(f"find {base_path} -type f")
            stdin2, stdout2, stderr2 = ssh2.exec_command(f"find {base_path} -type f")
            
            files1 = stdout1.read().decode('utf-8').splitlines()
            files2 = stdout2.read().decode('utf-8').splitlines()

        # Compare files and collect differences
        file_comparisons = []
        common_files = set(files1).intersection(set(files2))

        for file_path in common_files:
            file_diff = compare_files(ssh1, ssh2, file_path)
            if file_diff:
                file_comparisons.append({"file": file_path, "diff": file_diff})

        # Determine version order for display
        swap_servers = compare_versions(ufm_version1, ufm_version2)
        
        # If server2 has a higher version, we'll display it on the right as requested
        if swap_servers:
            # We're already good - server 2 has the higher version and will be on the right
            is_swapped = False
        else:
            # We need to swap to put the higher version on the right
            server1, server2 = server2, server1
            ufm_version1, ufm_version2 = ufm_version2, ufm_version1
            sharp_version1, sharp_version2 = sharp_version2, sharp_version1
            mft_version1, mft_version2 = mft_version2, mft_version1
            opensm_version1, opensm_version2 = opensm_version2, opensm_version1
            is_swapped = True
            
            # Also swap the diff data for display
            for file_comp in file_comparisons:
                swapped_diff = []
                for diff1, diff2 in file_comp['diff']:
                    swapped_diff.append((diff2, diff1))
                file_comp['diff'] = swapped_diff

        return {
            'ufm_version1': ufm_version1,
            'ufm_version2': ufm_version2,
            'sharp_version1': sharp_version1,
            'sharp_version2': sharp_version2,
            'mft_version1': mft_version1,
            'mft_version2': mft_version2,
            'opensm_version1': opensm_version1,
            'opensm_version2': opensm_version2,
            'files': file_comparisons,
            'server1': server1,
            'server2': server2,
            'is_swapped': is_swapped
        }

    except Exception as e:
        logger.error(f"Error comparing configurations: {e}")
        raise
    finally:
        ssh1.close()
        ssh2.close()

def check_ufm_version(ssh, host):
    """Check if UFM version file exists and is readable"""
    try:
        # First check if the file exists
        stdin, stdout, stderr = ssh.exec_command("test -f /opt/ufm/files/ufm_version && echo 'exists'")
        if not stdout.read().decode('utf-8').strip():
            logger.error(f"UFM version file not found on {host}")
            return False
        return True
    except Exception as e:
        logger.error(f"Error checking UFM version on {host}: {e}")
        return False

def get_sharp_version(ssh, host=None):
    """Extract SHARP version from sharp_am.cfg"""
    try:
        # First check if file exists
        stdin, stdout, stderr = ssh.exec_command("test -f /opt/ufm/files/conf/sharp/sharp_am.cfg && echo 'exists'")
        if not stdout.read().decode('utf-8').strip():
            if host:
                logger.warning(f"SHARP configuration file not found on {host}")
            else:
                logger.warning("SHARP configuration file not found")
            return "Unknown"
            
        cmd = "grep '# Version:' /opt/ufm/files/conf/sharp/sharp_am.cfg"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        version_line = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        
        if error:
            if host:
                logger.warning(f"Error reading SHARP version on {host}: {error}")
            else:
                logger.warning(f"Error reading SHARP version: {error}")
        
        if version_line:
            # Extract version number from "# Version: X.Y.Z"
            version = version_line.split(':')[1].strip()
            return version
        else:
            if host:
                logger.warning(f"Version line not found in SHARP config file on {host}")
            else:
                logger.warning("Version line not found in SHARP config file")
    except Exception as e:
        if host:
            logger.error(f"Error reading SHARP version on {host}: {e}")
        else:
            logger.error(f"Error reading SHARP version: {e}")
    return "Unknown"

def get_mft_version(ssh, host=None):
    """Extract MFT version from mst version command"""
    try:
        # First check if mst command exists
        stdin, stdout, stderr = ssh.exec_command("command -v mst || echo 'not found'")
        result = stdout.read().decode('utf-8').strip()
        if 'not found' in result:
            if host:
                logger.warning(f"MFT tools (mst) not installed on {host}")
            else:
                logger.warning("MFT tools (mst) not installed")
            return "Not Installed"
            
        cmd = "mst version"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        version_line = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        
        if error:
            if host:
                logger.warning(f"Error executing mst version on {host}: {error}")
            else:
                logger.warning(f"Error executing mst version: {error}")
        
        if version_line:
            # Try to find the part starting with "mft" and extract version until the comma
            if 'mft' in version_line:
                mft_part = version_line.split('mft')[1].strip()
                version = mft_part.split(',')[0]
                return version
            else:
                if host:
                    logger.warning(f"Unexpected format from mst version on {host}: {version_line}")
                else:
                    logger.warning(f"Unexpected format from mst version: {version_line}")
        else:
            if host:
                logger.warning(f"Empty output from mst version on {host}")
            else:
                logger.warning("Empty output from mst version")
    except Exception as e:
        if host:
            logger.error(f"Error reading MFT version on {host}: {e}")
        else:
            logger.error(f"Error reading MFT version: {e}")
    return "Unknown"

def get_opensm_version(ssh, host=None):
    """Extract OpenSM version from opensm.log"""
    try:
        # First check if log file exists
        stdin, stdout, stderr = ssh.exec_command("test -f /opt/ufm/files/log/opensm.log && echo 'exists'")
        if not stdout.read().decode('utf-8').strip():
            if host:
                logger.warning(f"OpenSM log file not found on {host}")
            else:
                logger.warning("OpenSM log file not found")
            return "Log Not Found"
            
        cmd = "cat /opt/ufm/files/log/opensm.log | grep OpenSM | head -1 | sed 's/.*\\(OpenSM [^ ]*\\).*/\\1/'"
        stdin, stdout, stderr = ssh.exec_command(cmd)
        version_line = stdout.read().decode('utf-8').strip()
        error = stderr.read().decode('utf-8').strip()
        
        if error:
            if host:
                logger.warning(f"Error parsing OpenSM log on {host}: {error}")
            else:
                logger.warning(f"Error parsing OpenSM log: {error}")
        
        if version_line:
            # The command already formats the output as "OpenSM X.Y.Z"
            if 'OpenSM' in version_line:
                return version_line.split('OpenSM ')[1]
            else:
                if host:
                    logger.warning(f"Unexpected format from OpenSM log on {host}: {version_line}")
                else:
                    logger.warning(f"Unexpected format from OpenSM log: {version_line}")
        else:
            if host:
                logger.warning(f"No OpenSM version found in log on {host}")
            else:
                logger.warning("No OpenSM version found in log")
    except Exception as e:
        if host:
            logger.error(f"Error reading OpenSM version on {host}: {e}")
        else:
            logger.error(f"Error reading OpenSM version: {e}")
    return "Unknown"

def generate_html_report(server1, server2, comparisons, output_file):
    """Generate HTML report with enhanced UI/UX"""
    try:
        # Create a unique ID for each file for table of contents links
        file_ids = {}
        for i, file_comp in enumerate(comparisons['files']):
            file_path = file_comp['file']
            file_id = f"file-{i}"
            file_ids[file_path] = file_id
        
        # Determine which versions are different and need markers
        version_diff = {
            'ufm': comparisons['ufm_version1'] != comparisons['ufm_version2'],
            'sharp': comparisons['sharp_version1'] != comparisons['sharp_version2'],
            'mft': comparisons['mft_version1'] != comparisons['mft_version2'],
            'opensm': comparisons['opensm_version1'] != comparisons['opensm_version2']
        }
        
        # Define CSS separately to avoid issues with -- in CSS variables
        css = """
    <style>
        :root {
            --nvidia-green: #76b900;
            --nvidia-dark: #1a1a1a;
            --nvidia-light: #f2f2f2;
            --diff-color: #ffeb99;
            --missing-color: #ffcccc;
            --matching-color: #e6ffe6;
            --version-diff: #ff8c00;
        }
        
        body {
            font-family: 'DINPro', Arial, sans-serif;
            margin: 0;
            padding: 0;
            color: #333;
            background-color: #ffffff;
        }
        
        .container {
            width: 95%;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            background-color: var(--nvidia-dark);
            color: #fff;
            padding: 20px;
            margin-bottom: 30px;
        }
        
        h1, h2, h3, h4 {
            font-family: 'DINPro-Bold', Arial, sans-serif;
            margin-top: 0;
        }
        
        h1 {
            color: var(--nvidia-green);
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        h2 {
            color: var(--nvidia-dark);
            font-size: 1.8em;
            margin: 20px 0;
            border-bottom: 2px solid var(--nvidia-green);
            padding-bottom: 8px;
        }
        
        h3 {
            color: var(--nvidia-dark);
            font-size: 1.4em;
            margin: 15px 0;
        }
        
        table {
            width: 100%;
            table-layout: fixed; /* Fixed table layout to control column width */
            border-collapse: collapse;
            margin: 20px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        th {
            background-color: var(--nvidia-dark);
            color: white;
            padding: 12px 15px;
            text-align: left;
            overflow-wrap: break-word; /* Allow word breaking */
            word-wrap: break-word;
        }
        
        td {
            padding: 10px 15px;
            border: 1px solid #ddd;
            text-align: left;
            overflow-wrap: break-word; /* Allow word breaking */
            word-wrap: break-word;
            max-width: 50vw; /* Limit to half viewport width */
            white-space: normal; /* Allow wrapping */
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:hover {
            background-color: #f1f1f1;
        }
        
        .diff {
            background-color: var(--diff-color);
            font-weight: bold;
        }
        
        .missing {
            background-color: var(--missing-color);
            color: #cc0000;
            font-weight: bold;
        }
        
        .toc {
            background-color: var(--nvidia-light);
            padding: 20px;
            margin-bottom: 30px;
            border-left: 4px solid var(--nvidia-green);
        }
        
        .toc ul {
            list-style-type: none;
            padding-left: 0;
        }
        
        .toc li {
            margin: 8px 0;
        }
        
        .toc a {
            color: #0066cc; /* Hyperlink blue color */
            text-decoration: underline; /* Underline to make it look like a hyperlink */
            padding: 5px;
            display: block;
            transition: all 0.2s ease;
        }
        
        .toc a:hover {
            background-color: var(--nvidia-green);
            color: white;
            text-decoration: none; /* Remove underline on hover */
        }
        
        .server-info {
            display: flex;
            justify-content: space-between;
            flex-wrap: wrap;
            margin-bottom: 20px;
        }
        
        .server-card {
            flex: 1;
            min-width: 300px;
            background-color: var(--nvidia-light);
            margin: 0 10px 10px 0;
            padding: 15px;
            border-radius: 4px;
        }
        
        .server-card h3 {
            color: var(--nvidia-green);
            margin-top: 0;
        }
        
        .version-box {
            padding: 8px;
            margin: 5px 0;
            background-color: white;
            border-left: 3px solid var(--nvidia-green);
        }
        
        /* Version difference marker */
        .version-diff {
            position: relative;
            border-left: 3px solid var(--version-diff) !important;
        }
        
        footer {
            text-align: center;
            margin-top: 50px;
            padding: 20px;
            background-color: var(--nvidia-dark);
            color: white;
        }
        
        /* Scrollable TOC for many files */
        .toc-scroll {
            max-height: 300px;
            overflow-y: auto;
        }
        
        /* Style for the search filter in DataTables */
        .dataTables_filter input {
            padding: 5px;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        
        /* Style DataTables pagination */
        .dataTables_paginate .paginate_button {
            background-color: var(--nvidia-light);
            border: 1px solid #ddd;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
        }
        
        .dataTables_paginate .paginate_button.current {
            background-color: var(--nvidia-green);
            color: white;
            border: 1px solid var(--nvidia-green);
        }
        
        /* Bold for differing values */
        .diff-value {
            font-weight: bold;
        }
        
        /* Responsive tables */
        @media screen and (max-width: 1200px) {
            table {
                width: 100%;
                display: block;
                overflow-x: auto; /* Allow horizontal scrolling only if absolutely necessary */
            }
        }
    </style>
"""
        # JavaScript for DataTables
        js_code = """
    <script>
        $(document).ready(function() {
            // Initialize all tables with DataTables
            $('table.display').each(function() {
                $(this).DataTable({
                    responsive: true,
                    ordering: true,
                    paging: true,
                    searching: true,
                    lengthMenu: [[10, 25, 50, -1], [10, 25, 50, "All"]],
                    language: {
                        search: "Filter:",
                        lengthMenu: "Show _MENU_ entries",
                        info: "Showing _START_ to _END_ of _TOTAL_ entries"
                    },
                    columnDefs: [
                        { "width": "50%", "targets": 0 },
                        { "width": "50%", "targets": 1 }
                    ]
                });
            });
            
            // Smooth scrolling for TOC links
            $('.toc a').on('click', function(event) {
                if (this.hash !== '') {
                    event.preventDefault();
                    var hash = this.hash;
                    $('html, body').animate({
                        scrollTop: $(hash).offset().top - 100
                    }, 800);
                }
            });
        });
    </script>
"""

        # Build HTML without CSS/JS first
        html_head = f"""<!DOCTYPE html>
<html>
<head>
    <title>UFM Configuration Comparison Report</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- DataTables CSS and JS -->
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css">
    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/responsive/2.2.9/css/responsive.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.datatables.net/responsive/2.2.9/js/dataTables.responsive.min.js"></script>
    {css}
</head>
<body>
    <header>
        <div class="container">
            <h1>UFM Configuration Comparison Report</h1>
            <p>Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>
    </header>
    
    <div class="container">
        <div class="server-info">
            <div class="server-card">
                <h3>Server 1: {comparisons['server1']['host']}</h3>
                <div class="version-box{' version-diff' if version_diff['ufm'] else ''}">UFM Version: {comparisons['ufm_version1']}</div>
                <div class="version-box{' version-diff' if version_diff['sharp'] else ''}">SHARP Version: {comparisons['sharp_version1']}</div>
                <div class="version-box{' version-diff' if version_diff['mft'] else ''}">MFT Version: {comparisons['mft_version1']}</div>
                <div class="version-box{' version-diff' if version_diff['opensm'] else ''}">OpenSM Version: {comparisons['opensm_version1']}</div>
            </div>
            <div class="server-card">
                <h3>Server 2: {comparisons['server2']['host']}</h3>
                <div class="version-box{' version-diff' if version_diff['ufm'] else ''}">UFM Version: {comparisons['ufm_version2']}</div>
                <div class="version-box{' version-diff' if version_diff['sharp'] else ''}">SHARP Version: {comparisons['sharp_version2']}</div>
                <div class="version-box{' version-diff' if version_diff['mft'] else ''}">MFT Version: {comparisons['mft_version2']}</div>
                <div class="version-box{' version-diff' if version_diff['opensm'] else ''}">OpenSM Version: {comparisons['opensm_version2']}</div>
            </div>
        </div>
        
        <h2>Table of Contents</h2>
        <div class="toc">
            <div class="toc-scroll">
                <ul>
"""

        # Build table of contents
        toc = ""
        for file_path, file_id in file_ids.items():
            toc += f'                    <li><a href="#{file_id}">{file_path}</a></li>\n'

        # Middle part of HTML
        html_middle = """
                </ul>
            </div>
        </div>
        
        <h2>Configuration Differences</h2>
"""

        # Build tables for each file
        tables = ""
        for file_comp in comparisons['files']:
            file_path = file_comp['file']
            file_id = file_ids[file_path]
            
            # Table header with server info - note that we may have swapped the servers
            tables += f"""
        <h3 id="{file_id}">{file_path}</h3>
        <table id="table-{file_id}" class="display responsive nowrap">
            <thead>
                <tr>
                    <th>Server 1 ({comparisons['server1']['host']}: {comparisons['ufm_version1']})</th>
                    <th>Server 2 ({comparisons['server2']['host']}: {comparisons['ufm_version2']})</th>
                </tr>
            </thead>
            <tbody>
"""
            
            # Table rows
            for diff1, diff2 in file_comp['diff']:
                is_diff1_missing = 'not found' in diff1
                is_diff2_missing = 'not found' in diff2
                
                # Apply bold to differing values by wrapping in a span with a class
                if not is_diff1_missing and not is_diff2_missing:
                    diff1_display = f'<span class="diff-value">{diff1}</span>'
                    diff2_display = f'<span class="diff-value">{diff2}</span>'
                else:
                    diff1_display = diff1
                    diff2_display = diff2
                
                tables += f"""
                <tr>
                    <td class="{'missing' if is_diff1_missing else 'diff'}">{diff1_display}</td>
                    <td class="{'missing' if is_diff2_missing else 'diff'}">{diff2_display}</td>
                </tr>"""
            
            tables += """
            </tbody>
        </table>"""

        # Footer part
        footer = f"""
        {js_code}
        
        <footer>
            <p>NVIDIA UFM Configuration Comparison Tool</p>
            <p>&copy; {datetime.now().strftime("%Y")} NVIDIA Corporation. All rights reserved.</p>
        </footer>
    </div>
</body>
</html>
"""

        # Combine all parts
        html_content = html_head + toc + html_middle + tables + footer

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info(f"Enhanced HTML report generated: {output_file}")

    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise

def main():
    try:
        parser = argparse.ArgumentParser(description='Compare UFM configurations between two servers')
        parser.add_argument('host1', help='First server hostname/IP')
        parser.add_argument('host2', help='Second server hostname/IP')
        parser.add_argument('username', help='SSH username')
        parser.add_argument('password', help='SSH password')
        parser.add_argument('output_file', nargs='?', 
                          default=f'ufm_config_diff_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html',
                          help='Output HTML file path (optional)')
        parser.add_argument('--fast', action='store_true',
                          help='Fast mode: only compare critical configuration files')
        
        args = parser.parse_args()

        server1 = {
            'host': args.host1,
            'username': args.username,
            'password': args.password
        }
        
        server2 = {
            'host': args.host2,
            'username': args.username,
            'password': args.password
        }

        comparisons = compare_configurations(server1, server2, fast_mode=args.fast)
        generate_html_report(comparisons['server1'], comparisons['server2'], comparisons, args.output_file)
        logger.info(f"Report generated: {args.output_file}")
        print(f"Report generated: {args.output_file}")
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 