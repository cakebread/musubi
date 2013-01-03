

"""

Testing various DNS related utility functions

Copyright (c) 2012, 2013 Rob Cakebread
All rights reserved.

"""



from musubi.netdns import build_query

def test_build_query():
    '''Reverse the ip and append the name server
    reverse = '.'.join(reversed(ip.split('.')))
    query = '{reverse}.{dnsbl}.'.format(reverse=reverse, dnsbl=dnsbl)
    '''

    assert build_query('127.0.0.1', 'domain.com') == '1.0.0.127.domain.com.'
    assert build_query('127.0.0.1', 'domain.com.') != '1.0.0.127.domain.com.'
    assert build_query('1.1.1.1', 'domain.com') != '1.0.0.127.domain.com.'
    assert build_query('2.2.2.2', 'domain.com') == '2.2.2.2.domain.com.'
    assert (build_query('foobar', 'domain.com') != '2.2.2.2.domain.com.')
    

