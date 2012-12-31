
"""

Look up MX records for a domain, show IP addresses, PTRs

Copyright (c) 2012, Rob Cakebread
All rights reserved.

"""

import logging
import socket

from cliff.lister import Lister
import dns.resolver


class GetMX(Lister):

    """Show MX records for domain"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        """Set up parser options for this command"""
        parser = super(GetMX, self).get_parser(prog_name)
        parser.add_argument('getmx', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        """Take action for this command"""
        domain = parsed_args.getmx
        return (('Priority', 'Mail Server Domain Name', 'IP', 'PTR'),
               ((
                x.preference,
                str(x.exchange)[:-1],
                dns.resolver.query(str(x.exchange)[:-1], 'A')[0],
                socket.gethostbyaddr(
                str(dns.resolver.query(
                    str(x.exchange)[:-1], 'A')[0]))[0]
                ) for x in dns.resolver.query(domain, 'MX')))
