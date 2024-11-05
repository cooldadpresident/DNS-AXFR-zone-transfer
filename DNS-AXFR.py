#!/usr/bin/env python3
# DNS AXFR - authoritative zone transfer
#/home/pres/github/htb/Ipython/venv/bin/activate


# Dependencies
# python3-dnspython

# Used Modules
import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse

# Initialize Resolver-Class from dns.resolver as "NS"
NS = dr.Resolver()

# list of found subdomains
Subdomains = []

# Define the AXFR Function 
def AXFR(domain, nameserver):
        # try zone transfer for given domain and nameserver
        try:
                # perform the zone transfer
                # Initiates a zone transfer request to the specified nameserver for the given domain.
                axfr = dz.from_xfr(dq.xfr(nameserver, domain))

                # if zone transfer was successful
                if axfr:
                        print('[*] Successful Zone transfer from {}'.format(nameserver))
                        
                        # add found subdomains to global 'subdomains' list
                        for record in axfr:
                                Subdomains.append('{}.{}'.format(record.to_text(), domain))


        # if zone transfer fails
        except Exception as error:
                print(error)
                pass

# Main
if __name__ == '__main__':

        # Argument Parser - define usage
        parser = argparse.ArgumentParser(prog='DNS-AXFR.py', epilog='DNS Zone transfer Script', usage="DNS-AXFR.py [options] -d <DOMAIN>", prefix_chars='-', add_help=True)

        # Positional arguments
        parser.add_argument('-d', action='store', metavar='Domain', type=str, help='Target Domain.\tExample: inlanefreight.htb', required=True)
        parser.add_argument('-n', action='store', metavar='Nameserver', type=str, help='Nameserver seperated by comma.\tExample: ns1.inlanefreight.com,ns2.inlanefreight.com', required=True) 
        parser.add_argument('-v', action='version', version='DNS-AXFR.py - v1.0', help='Prints the version of DNS-AXFR.py')

        # Assign given arguments
        args = parser.parse_args()

        # Variables
        Domain = args.d
        NS.nameservers = list(args.n.split(","))

        # Check if url is given
        if not args.d:
                print("[!] You must specify target Domain.\n")
                print(parser.print_help())
                exit()
        if not args.n:
                print("[!] You must specify target nameservers.\n")
                print(parser.print_help())
                exit()
                
        # for each nameserver
        for nameserver in NS.nameservers:
                # Try AXFR
                AXFR(Domain, nameserver)
        # print the results 
        if Subdomains is not None:
                print('========= Found Subdomains  =========')

                # print each subdomain
                for subdomain in Subdomains:
                        print('{}'.format(subdomain))
        else:
                print('No subdomains found.') 
                exit()


