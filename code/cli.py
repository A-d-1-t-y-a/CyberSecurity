import json
import sys
import click
from rich.console import Console
from rich.table import Table
from .core import analyze_memory

console = Console()

@click.group()
def cli():
	pass

@cli.command()
@click.option("--dump", required=True, type=click.Path(exists=True, dir_okay=False))
@click.option("--type", "analysis_type", default="full", type=click.Choice(["full","processes","network","malware","kernel"]))
@click.option("--format", "output_format", default="json", type=click.Choice(["json","table"]))
@click.option("--verbose", is_flag=True, default=False)
def analyze(dump, analysis_type, output_format, verbose):
	result = analyze_memory(dump, analysis_type, verbose)
	if output_format == "json":
		console.print_json(data=result)
		return
	table = Table(show_header=True, header_style="bold magenta")
	table.add_column("PID")
	table.add_column("Name")
	table.add_column("User")
	for p in result.get("processes", []):
		table.add_row(str(p.get("pid","")), p.get("name",""), p.get("user",""))
	console.print(table)

if __name__ == "__main__":
	try:
		cli()
	except KeyboardInterrupt:
		sys.exit(130)
