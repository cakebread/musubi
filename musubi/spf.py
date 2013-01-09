
"""

Look up SPF records for a domain

Copyright (c) 2012, 2013 Rob Cakebread
All rights reserved.

"""

import logging

from cliff.command import Command
import dns.resolver


class GetSPF(Command):

    """Show SPF records for domain"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(GetSPF, self).get_parser(prog_name)
        parser.add_argument('getspf', nargs='?', default=None)
        return parser

    def take_action(self, parsed_args):
        domain = parsed_args.getspf
        for x in dns.resolver.query(domain, 'TXT'):
            txt = x.to_text()
            test_txt = txt.lower()
            # There are many uses for TXT, we only want SPF records:
            if 'v=spf1' in test_txt[0:7]:
                print(txt)
