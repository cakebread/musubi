
"""

Look up MX records for a domain, show IP addresses, PTRs

Copyright (c) 2012, 2013, Rob Cakebread
All rights reserved.

"""

import logging
import socket

from cliff.lister import Lister
import dns.resolver

from .netdns import verify_domain


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
        if verify_domain(domain):
            return (('Priority', 'Mail Server Domain Name', 'IP', 'PTR'),
                   ((
                    x.preference,
                    str(x.exchange).lower(),
                    dns.resolver.query(str(x.exchange), 'A')[0],
                    socket.gethostbyaddr(
                    str(dns.resolver.query(
                        str(x.exchange), 'A')[0]))[0]
                    ) for x in dns.resolver.query(domain, 'MX')))
        else:
            raise RuntimeError('Can not lookup domain: %s' % domain)
