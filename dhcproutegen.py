#!/usr/bin/env python

import sys


helpstring = """

    This script is generate hex string for DHCP option 121 (249 MS)
    Usage:
         dhcproutegen 192.168.22.0/24,10.20.20.1
         dhcproutegen 172.16.27.50/32,172.16.27.1 10.0.50.0/255.255.192.0,192.168.17.1

    github: 

"""


def check_ip_mask(addrmask: str) -> bool:
    """Validate the IP-address or network mask, return True if valid and exception otherwise
    Example: check_ip_mask('192.168.130.230')
    """
    try:
        if len(addrmask) in [1,2]:
            i = int(addrmask)
            if -1 > i < 33:
                return True
        for i in addrmask.split('.'):
            i = int(i)
            if i > 255 or i < 0:
                raise ValueError

    except ValueError:
        print("Error '", addrmask, "' is not a valid IP-address or network mask.", sep='')
        exit(1)

    return True


def ip_to_hex(ip: str) -> str:
    """Convert IP-address and return a HEX string w/o leading '0x'.
    Example: ip_to_hex("192.168.127.18")
    """

    if check_ip_mask(ip):

        if ip == "0.0.0.0":
            return "00"

        result = ""
        parts = ip.split('.')

        while parts[-1] == '0':
            parts.pop()

        for i in parts:
            temp_hex = format(int(i), "x")
            if len(temp_hex) < 2:
                temp_hex = '0' + temp_hex
            result += temp_hex

        return result


def mask_to_hex(mask) -> str:
    """Convert network mask to HEX string w/o leading '0x'.
    Example: mask_to_hex(8) or mask_to_hex("255.255.255.252")
    """

    mask = str(mask)

    if check_ip_mask(mask):

        if len(mask) in [1,2]:
            result = format(int(mask), "x")
            if len(result) < 2:
                result = "0" + result
        else:
            tmp = ''
            for i in mask.split('.'):
                tmp += format(int(i), 'b')
            result = format(int(tmp.count('1')), "x")
            if len(result) < 2:
                result = "0" + result

        return result


if __name__ == "__main__":

    concat_route = ''

    if len(sys.argv) < 2:
        print(helpstring)

    else:
        for param in sys.argv[1:]:

            print("Route:", param)
            hostnet_mask, gw = param.split(",")
            hostnet, netmask = hostnet_mask.split("/")

            hex_hostnet = ip_to_hex(hostnet)
            hex_mask = mask_to_hex(netmask)
            hex_gw = ip_to_hex(gw)
            concat_route += hex_mask + hex_hostnet + hex_gw
            print("HEX: 0x", hex_mask, hex_hostnet, hex_gw, sep='', end='\n\n')

        print('Concatenated route: 0x', concat_route, sep='')