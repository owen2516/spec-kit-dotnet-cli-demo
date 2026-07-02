import sys
import click

# Custom exceptions and exit codes (T006)
class TZCLIError(click.ClickException):
    """Base exception for tz-cli errors."""
    exit_code = 1

class ArgumentError(TZCLIError):
    """Exception for command line argument or format validation errors."""
    exit_code = 1

class ResolutionError(TZCLIError):
    """Exception for timezone IANA search or Nominatim geocoding API errors."""
    exit_code = 2


@click.group()
def cli():
    """Timezone Scheduler CLI tool.
    
    Allows querying timezone offsets, converting datetimes, and scheduling meetings.
    """
    pass


@cli.command()
@click.argument("location", required=True)
@click.option("-f", "--format", "output_format", type=click.Choice(["text", "json"]), default="text", help="Output format.")
def query(location, output_format):
    """Queries the current time and offset of a location."""
    click.echo(f"Querying location: {location} (stub)")


@cli.command()
@click.option("-t", "--time", "dt_str", required=True, help="Datetime to convert (YYYY-MM-DD HH:MM).")
@click.option("-f", "--from", "from_loc", required=True, help="Source timezone/location.")
@click.option("-o", "--to", "to_locs", required=True, multiple=True, help="Target timezone/locations.")
@click.option("--json", "is_json", is_flag=True, help="Output in structured JSON.")
def convert(dt_str, from_loc, to_locs, is_json):
    """Converts a specific datetime to target locations."""
    click.echo(f"Converting time from {from_loc} to {to_locs} (stub)")


@cli.command()
@click.option("-l", "--locations", required=True, help="Comma-separated list of participant locations.")
@click.option("-d", "--date", "date_str", required=True, help="Target meeting date (YYYY-MM-DD).")
@click.option("-u", "--duration", default="1h", help="Meeting duration (e.g. 1h, 30m).")
@click.option("-r", "--range", "hours_range", default="08:00-21:00", help="Allowed meeting hours (HH:MM-HH:MM).")
@click.option("-x", "--export", "export_path", help="Filename to export the top recommended meeting to as an .ics file.")
@click.option("--json", "is_json", is_flag=True, help="Output in structured JSON.")
def schedule(locations, date_str, duration, hours_range, export_path, is_json):
    """Finds optimal overlapping meeting times across multiple timezones."""
    click.echo(f"Scheduling meeting for {locations} (stub)")


def main():
    try:
        cli()
    except TZCLIError as e:
        click.echo(f"Error: {e}", err=True)
        sys.exit(e.exit_code)
    except Exception as e:
        click.echo(f"Unexpected error: {e}", err=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
