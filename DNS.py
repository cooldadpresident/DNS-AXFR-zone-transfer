#!/bin/python3
import dns.resolver # module to query nameservers

nameservers = dns.resolver.query('inlanefreight.com', 'NS')
for ns in nameservers:
        print('NS:', ns)