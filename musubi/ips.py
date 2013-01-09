
"""

Look up IP addresses for all mail servers in MX records

Copyright (c) 2012, 2013 Rob Cakebread
All rights reserved.

"""

import logging

from cliff.lister import Lister
from .netdns import get_mx_hosts, ips_from_domains


class GetIPs(Lister):

    """Show IP addresses for all servers in MX records for given domain"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Get parser options"""
        parser = super(GetIPs, self).get_parser(prog_name)
        parser.add_argument('ips', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        """Take action on args"""
        hosts = get_mx_hosts(parsed_args.ips)
        return (('IPs for MX Servers',),
               ((ip,) for ip in ips_from_domains(hosts)))
