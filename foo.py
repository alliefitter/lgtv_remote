from getmac import get_mac_address
from wakeonlan import send_magic_packet

send_magic_packet(get_mac_address(ip='192.168.0.44'))