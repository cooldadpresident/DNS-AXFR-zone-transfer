#!/usr/bin/env python3
# Dependencies
# python3-dnspython

import dns.zone as dz
import dns.query as dq
import dns.resolver as dr
import argparse

# Inicializace třídy Resolver z dns.resovler jako "NS"
NS = dr.Resolver()

# Seznam nalezených subdomén
Subdomains = []

# Definice funkce AXFR pro přenos zóny
def AXFR(domain, nameserver):
        # Pokus o přenos zóny pro danou doménu a nameserver 
        try:
                # Zahájení požadavku pro přenos zóny k určenému namserveru pro danou doménu
                # Funkce dq.xfr iniciuje přenos a dz.from_xfr zpracovává vásledky 
                axfr = dz.from_xfr(dq.xfr(nameserver, domain))

                # Pokud je přenos zóny úspěšný
                if axfr:
                        print('[*] Úspššný přenos zóny {}'.format(nameserver))
                        
                        # Přidání nalezených subdomén do seznamu 'Subdomains'
                        for record in axfr:
                                Subdomains.append('{}.{}'.format(record.to_text(), domain))


        # Pokud přenos zóny selže 
        except Exception as error:
                print(error)
                pass

# Main
if __name__ == '__main__':

        # Argument Parser
        parser = argparse.ArgumentParser(prog='DNS-AXFR.py', epilog='DNS Zone transfer Script', usage="DNS-AXFR.py [options] -d <DOMAIN>", prefix_chars='-', add_help=True)

        # Argumenty 
        parser.add_argument('-d', action='store', metavar='Domain', type=str, help='Domain.\tExample: example.htb', required=True)
        parser.add_argument('-n', action='store', metavar='Nameserver', type=str, help='Nameserver .\tExample: ns1.example.com,ns2.example.com', required=True) 
        parser.add_argument('-v', action='version', version='DNS-AXFR.py - v1.0', help='Prints the version of DNS-AXFR.py')

        # Argumenty pro pomoc
        args = parser.parse_args()

        # Nastavení proměnných 
        Domain = args.d
        NS.nameservers = list(args.n.split(","))

        # Kontrola argumentů
        if not args.d:
                print("[!] You must specify target Domain.\n")
                print(parser.print_help())
                exit()
        if not args.n:
                print("[!] You must specify target nameservers.\n")
                print(parser.print_help())
                exit()
                
        # pro každý nameserver
        for nameserver in NS.nameservers:
                # Zkus AXFR přenos
                AXFR(Domain, nameserver)
        # Výpis výsledků 
        if Subdomains is not None:
                print('========= Found Subdomains  =========')

                # Výpis každé subdomény 
                for subdomain in Subdomains:
                        print('{}'.format(subdomain))
        else:
                print('No subdomains found.') 
                exit()


