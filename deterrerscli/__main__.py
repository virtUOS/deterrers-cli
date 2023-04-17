import click
import deterrersapi
import pathlib
import json
import yaml

deterrers = None

profiles = click.Choice(
        ('', 'HTTP', 'SSH', 'HTTP+SSH', 'Multipurpose'),
        case_sensitive=False)
host_firewalls = click.Choice(
        ('', 'UFW', 'FirewallD', 'nftables'),
        case_sensitive=False)


def print_format(data, format: str):
    if format == 'yaml':
        print(yaml.dump(data))
    else:
        print(json.dumps(data, indent=4))


@click.group()
def cli():
    global deterrers
    with open(pathlib.Path().home() / '.deterrers.yml', 'r') as f:
        config = yaml.safe_load(f)
    deterrers = deterrersapi.Deterrers(config['url'], config['token'])


@cli.command()
@click.option('--format', default='json', help='Output format (json or yaml)')
def hosts(format):
    '''List all IPs added to DETERRERS.
    '''
    data = deterrers.hosts()
    print_format(data, format)


@cli.command()
@click.option('--format', default='json', help='Output format (json or yaml)')
@click.argument('ipv4')
def get(format, ipv4):
    '''Get information about an IP address in DETERRERS.
    '''
    data = deterrers.get(ipv4)
    print_format(data, format)


@cli.command()
@click.argument('ipv4')
def delete(ipv4):
    '''Delete IP address from DETERRERS.
    '''
    deterrers.delete(ipv4)


@cli.command()
@click.option('--admin', '-a', multiple=True, required=True)
@click.option('--profile', '-p', default='', type=profiles)
@click.option('--firewall', '-f', default='', type=host_firewalls)
@click.argument('ipv4')
def add(ipv4, admin, profile, firewall):
    '''Add IP address to DETERRERS.
    '''
    deterrers.add(ipv4, admin, profile, firewall)


@cli.command()
@click.option('--profile', '-p', default='', type=profiles)
@click.option('--firewall', '-f', default='', type=host_firewalls)
@click.argument('ipv4')
def update(ipv4, profile, firewall):
    '''Update IP address in DETERRERS.
    '''
    deterrers.update(ipv4, profile, firewall)


@cli.group()
def action():
    '''Activate firewall profile or block IP address in perimeter firewall.
    '''
    pass


@action.command()
@click.argument('ipv4')
def register(ipv4):
    '''Activate profile in perimeter firewall.
    '''
    deterrers.action(ipv4, 'register')


@action.command()
@click.argument('ipv4')
def block(ipv4):
    '''Block IP address perimeter firewall.
    '''
    deterrers.action(ipv4, 'block')


if __name__ == '__main__':
    cli()
