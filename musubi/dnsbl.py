
"""
Copyright (c) 2012, Rob Cakebread
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
    "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
    TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
    PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS
    OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
    EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
    PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
    LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
    NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
    SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


Based on dnsbl.py by Vincent Carney (c) 2012

https://github.com/vincecarney/dnsbl/blob/master/dnsbl.py

Rewriting to do an additional TXT lookup of reason for blacklisting from DNSBL
using dnspython because gevent's socket can't lookup TXT records, apparently
it only does common types like A and CNAMEs etc.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

"""

import logging

import gevent
from gevent import socket


class Base(object):

    """DNSBL checker using gevent for super speed"""

    log = logging.getLogger(__name__)

    def __init__(self, ip=None, dnsbls=[], timeout=2):
        #TODO: Make timeout an --option
        self.ip = ip
        self.dnsbls = dnsbls
        self.timeout = timeout
        Base.log.debug('Checking IP %s' % ip)

    def build_query(self, dnsbl):
        '''Reverse the ip and append the name server'''
        reverse = '.'.join(reversed(self.ip.split('.')))
        return '{reverse}.{dnsbl}.'.format(reverse=reverse,
                                           dnsbl=dnsbl)

    def query(self, dnsbl):
        '''Perform query using gevent'''
        try:
            result = socket.gethostbyname(self.build_query(dnsbl))
        except socket.gaierror as err:
            result = False
            err = str(err)
            if not 'Errno 3' in err:
                Base.log.debug('Base.query.exception: %s %s' % (dnsbl, err))
        return dnsbl, result

    def check(self):
        '''Check results of all gevent jobs'''
        results = []
        jobs = [gevent.spawn(self.query, dnsbl)
                for dnsbl in self.dnsbls]
        gevent.joinall(jobs, self.timeout)
        for job in jobs:
            if job.successful():
                results.append(job.value)
            else:
                results.append((job.args[0], None))
        return results
