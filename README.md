# dhcproutegen
Python script for generating DHCP opt 121 (249 for Windows) in HEX notation

# usage
`dhcproutegen network/mask,gateway`

Example:

`dhcproutegen 192.168.20.0/24,10.20.20.1`

`dhcproutegen 172.16.30.20/32,192.168.1.1 10.10.0.0/255.255.0.0,172.168.0.1`
