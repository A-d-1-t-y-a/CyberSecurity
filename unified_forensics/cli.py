import click
import json
import logging
import sys
import os
from pathlib import Path
from colorama import init, Fore, Style

from .core.framework import UnifiedForensicsFramework

init(autoreset=True)

@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.option('--debug', '-d', is_flag=True, help='Enable debug logging')
def cli(verbose, debug):
    """Unified Memory Forensics Framework"""
    if debug:
        logging.basicConfig(level=logging.DEBUG)
    elif verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARNING)

@cli.command()
@click.argument('memory_dump', type=click.Path(exists=True))
@click.option('--os', '-o', type=click.Choice(['windows', 'linux', 'macos']), help='Specify operating system')
@click.option('--output', '-f', type=click.Path(), help='Output file for results')
@click.option('--plugins', '-p', multiple=True, help='Enable specific plugins')
@click.option('--format', 'output_format', type=click.Choice(['json', 'table', 'summary']), default='json', help='Output format')
def analyze(memory_dump, os, output, plugins, output_format):
    """Analyze a memory dump file"""
    try:
        framework = UnifiedForensicsFramework()
        
        click.echo(f"{Fore.CYAN}Starting memory forensics analysis...")
        click.echo(f"{Fore.YELLOW}Memory dump: {memory_dump}")
        
        if os:
            click.echo(f"{Fore.YELLOW}OS specified: {os}")
        else:
            click.echo(f"{Fore.YELLOW}Auto-detecting OS...")
        
        if plugins:
            click.echo(f"{Fore.YELLOW}Plugins: {', '.join(plugins)}")
        
        results = framework.analyze(
            memory_dump_path=memory_dump,
            os_type=os,
            plugins=list(plugins) if plugins else None,
            output_file=output
        )
        
        if output_format == 'json':
            if output:
                click.echo(f"{Fore.GREEN}Results saved to {output}")
            else:
                click.echo(json.dumps(results, indent=2))
        elif output_format == 'table':
            _display_table_results(results)
        elif output_format == 'summary':
            _display_summary_results(results)
        
        click.echo(f"{Fore.GREEN}Analysis completed successfully!")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}", err=True)
        sys.exit(1)

@cli.command()
def info():
    """Display framework information"""
    framework = UnifiedForensicsFramework()
    
    click.echo(f"{Fore.CYAN}Unified Memory Forensics Framework")
    click.echo(f"{Fore.YELLOW}Version: 1.0.0")
    click.echo(f"{Fore.YELLOW}Author: Manoj Santhoju")
    click.echo()
    
    click.echo(f"{Fore.CYAN}Supported Operating Systems:")
    for os_type in framework.get_supported_os():
        click.echo(f"  - {os_type}")
    
    click.echo()
    click.echo(f"{Fore.CYAN}Available Tools:")
    for tool in framework.get_available_tools():
        click.echo(f"  - {tool}")
    
    click.echo()
    click.echo(f"{Fore.CYAN}Available Plugins:")
    for plugin in framework.get_available_plugins():
        click.echo(f"  - {plugin}")

@cli.command()
@click.argument('memory_dump', type=click.Path(exists=True))
def detect_os(memory_dump):
    """Detect operating system from memory dump"""
    try:
        framework = UnifiedForensicsFramework()
        os_type = framework.os_detector.detect_os(memory_dump)
        
        click.echo(f"{Fore.GREEN}Detected OS: {os_type}")
        
    except Exception as e:
        click.echo(f"{Fore.RED}Error: {str(e)}", err=True)
        sys.exit(1)

def _display_table_results(results):
    """Display results in table format"""
    click.echo(f"\n{Fore.CYAN}=== ANALYSIS RESULTS ===")
    
    metadata = results.get('metadata', {})
    click.echo(f"{Fore.YELLOW}OS Type: {metadata.get('os_type', 'Unknown')}")
    click.echo(f"{Fore.YELLOW}Analysis Time: {metadata.get('analysis_timestamp', 'Unknown')}")
    
    processes = results.get('processes', [])
    click.echo(f"\n{Fore.CYAN}Processes ({len(processes)}):")
    for proc in processes[:10]:
        status = f"{Fore.RED}[SUSPICIOUS]" if proc.get('suspicious') else f"{Fore.GREEN}[NORMAL]"
        click.echo(f"  {status} PID: {proc.get('pid', 'N/A')} | Name: {proc.get('name', 'N/A')}")
    
    if len(processes) > 10:
        click.echo(f"  ... and {len(processes) - 10} more processes")
    
    network = results.get('network_connections', [])
    click.echo(f"\n{Fore.CYAN}Network Connections ({len(network)}):")
    for conn in network[:10]:
        click.echo(f"  {conn.get('local_address', 'N/A')}:{conn.get('local_port', 'N/A')} -> {conn.get('remote_address', 'N/A')}:{conn.get('remote_port', 'N/A')}")
    
    if len(network) > 10:
        click.echo(f"  ... and {len(network) - 10} more connections")
    
    statistics = results.get('statistics', {})
    click.echo(f"\n{Fore.CYAN}Statistics:")
    click.echo(f"  Total Processes: {statistics.get('total_processes', 0)}")
    click.echo(f"  Total Connections: {statistics.get('total_network_connections', 0)}")
    click.echo(f"  Suspicious Processes: {statistics.get('suspicious_processes', 0)}")
    click.echo(f"  Active Connections: {statistics.get('active_connections', 0)}")

def _display_summary_results(results):
    """Display results in summary format"""
    click.echo(f"\n{Fore.CYAN}=== ANALYSIS SUMMARY ===")
    
    metadata = results.get('metadata', {})
    click.echo(f"{Fore.YELLOW}OS Type: {metadata.get('os_type', 'Unknown')}")
    
    statistics = results.get('statistics', {})
    click.echo(f"{Fore.YELLOW}Total Processes: {statistics.get('total_processes', 0)}")
    click.echo(f"{Fore.YELLOW}Total Connections: {statistics.get('total_network_connections', 0)}")
    click.echo(f"{Fore.YELLOW}Suspicious Processes: {statistics.get('suspicious_processes', 0)}")
    
    if statistics.get('suspicious_processes', 0) > 0:
        click.echo(f"{Fore.RED}⚠️  Suspicious activity detected!")
    else:
        click.echo(f"{Fore.GREEN}✅ No suspicious activity detected")

if __name__ == '__main__':
    cli()
