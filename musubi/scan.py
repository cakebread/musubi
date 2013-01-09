
"""

Scan multiple DNSBLs for IP addresss or domain.

Copyright (c) 2012, 2013 Rob Cakebread
All rights reserved.


If you give the domain, musubi will try to find all your IP addresses
for each mail server by querying MX DNS records and then doing a lookup
for the IPs. If your mail server uses round-robin DNS, this of course
won't find all the IPs. You must find out the IP CIDR range and then
give that, e.g.

   musubi scan 192.0.64.0/24


"""

import sys
import logging

import dns
from cliff.lister import Lister
from IPy import IP
import requests

from .dnsbl import Base
from .netdns import get_mx_hosts, ips_from_domains, get_txt, build_query, \
    net_calc, verify_domain

requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)


DNSBL_LIST = 'http://musubi.cakebread.info/dnsbl.txt'

# Try to get list of working DNSBLs checked hourly, experimental.
# TODO Add options to use local list, pipe in, etc.
req = requests.get(DNSBL_LIST)
if req.status_code == 200:
    BASE_DNSBLS = req.text.split()
else:
    from .dnsbllist import BASE_DNSBLS


class Scan(Lister):

    """Scan multiple DNSBLs by IP or domain"""

    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Scan, self).get_parser(prog_name)
        parser.add_argument('scan', nargs='?', default=None)
        return parser

    def dnsbl_check(self, ip):
        backend = Base(ip=ip, dnsbls=BASE_DNSBLS)
        return backend.check()

    def dnsbl_scanner(self, rdata, ip):
        for dnsbl, blacklisted in self.dnsbl_check(ip):
            # Scan.log.debug('Testing: %s' % dnsbl)
            if blacklisted:
                Scan.log.debug('blacklisted: %s' % dnsbl)
                try:
                    query = build_query(ip, dnsbl)
                    txt = get_txt(query)[0]
                except dns.resolver.NoAnswer:
                    Scan.log.debug("No TXT record for %s" % query)
                rdata.append(
                    (ip,
                     dnsbl,
                     blacklisted,
                     txt,)
                )
        return rdata

    def take_action(self, parsed_args):
        """This could be a lot prettier if I used these as arguments
        instead of trying to detect input type --IP --domain --range
        It's just easier to use without them, hmm.
        """
        arg = parsed_args.scan
        rdata = []
        if "/" in arg:
            # CIDR notation
            ips = net_calc(arg)
        else:
            try:
                # Throw exception if it's not an IP and then try domain name
                ip = IP(arg)
                ips = [ip]
            except ValueError:
                if verify_domain(arg):
                    hosts = get_mx_hosts(arg)
                    ips = ips_from_domains(hosts)
                else:
                    raise RuntimeError('Can not lookup domain: %s' % arg)
        for ip in ips:
            ip = str(ip)
            rdata = self.dnsbl_scanner(rdata, ip)

        if not len(rdata):
            Scan.log.debug("Not found on any DNSBL lists.")
            sys.exit(0)
        Scan.log.debug(rdata)
        return (('IP', 'DNSBL Host', 'Response Code', 'DNS TXT Record'), rdata)
