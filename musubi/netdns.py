
"""

Various DNS related utility functions

Copyright (c) 2012, 2013 Rob Cakebread
All rights reserved.

"""
import logging

import IPy
from dns import resolver, reversename

log = logging.getLogger(__name__)


def verify_domain(domain):
    '''Verify if host name exists'''
    try:
        hosts = get_mx_hosts(domain)
        if len(hosts):
            return True
    except resolver.NXDOMAIN:
        log.debug('NXDOMAIN: %s' % domain)
        return
    except resolver.NoAnswer:
        log.debug('NoAnswer: %s' % domain)
        return


def build_query(ip, dnsbl):
    '''Reverse the ip and append the name server'''
    reverse = '.'.join(reversed(ip.split('.')))
    query = '{reverse}.{dnsbl}.'.format(reverse=reverse, dnsbl=dnsbl)
    log.debug('Query: %s' % query)
    return query


def get_ips(domain):
    """Return all IPs (A records) for domain"""
    return [str(rdata) for rdata in resolver.query(domain, 'A')]


def get_mx_hosts(domain):
    """Get all domain names for servers in MX records"""
    return [x.exchange for x in resolver.query(domain, 'MX')]


def get_txt(domain):
    """Return all TXT records for a domain"""
    return [rdata.to_text() for rdata in resolver.query(domain, 'TXT')]


def get_spf(domain):
    """Return SPF TXT records for given domain"""
    txts = get_txt(domain)
    for txt in txts():
        test_txt = txt.lower()
        # TODO Need to look at SPF spec on this to check about spaces & quotes:
        if 'v=spf1' in test_txt[0:9]:
            yield txt


def ptr_from_ip(ip):
    """return PTR domain for given IP"""
    domain = reversename.from_address(ip)
    log.debug("domain ptr_from_ip: %s" % domain)
    return str(resolver.query(domain, "PTR")[0])


def ips_from_domains(domains):
    """
    Return unique set of all ips for all domains given.
    This is used to determine all the IPs we need to check
    for all mail servers we can find through MX records.

    Sometimes two or more servers have the same IP.

    $ musubi mx lancterprise.com

    +----------+-----------------------------+
    | priority | mail server domain name     |
    +----------+-----------------------------+
    | 10       | mailstore1.secureserver.net |
    | 0        | smtp.secureserver.net       |
    +----------+-----------------------------+

    $ musubi ips lancnterprise.com

    216.69.126.209

    """

    ips = []
    for host in domains:
        for ip in get_ips(host):
            if ip not in ips:
                ips.append(ip)
    return ips


def net_calc(iprange):
    """

    all_ips =IPy.IP('213.170.64.0/23')
    for ip in all_ips:
        print ip

    Note: We can get rid of IPy dependency when I figure out how to do
    this with pythondns.
    """
    return IPy.IP(iprange)
