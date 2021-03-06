import socket
import struct
import textwrap




def main():
    conn = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(3))

    while True:
        raw_data , addr = conn.recvfrom(65536)
        dest_mac , src_mac , eth_proto , data = ethernet_frame(raw_data)
        print('\nEthernet  Frame:')
        print('Destination: {} , Source: {} , Protocol: {}'.format(dest_mac , src_mac, eth_proto))



# Unpack ethernet frame

def ethernet_frame(data):
    dest_mac , src_mac , proto = struct .unpack('! 6s 6s H', data[:14])
    return get_mac_addr(dest_mac) , get_mac_addr(src_mac) , socket.htons(proto) , data[14:]



# Return properly formatted MAC address (ie AA:BB:CC:DD:EE:FF)

def get_mac_addr(bytes_addr):
    bytes_str = map('{:02x}'.format , bytes_addr)
    return ':'.join(bytes_str).upper()


# Unpacks IPv4 packet
def ipv4_packet(data):
    version_header_length = data[0]
    version = version_header_length >> 4
    header_lenght = (version_header_length & 15) * 4
    ttl , proto , src , target = struct.unpack('! 8x B B 2x 4s 4s' , data[:20] )
    return version , header_lenght , ttl , proto , ipv4(src) , ipv4(target) , data[header_lenght:]


# Returns properly formatted IPv4 address

def ipv4(addr):
    return '.'.join(map(str,addr))



# Unpacks ICMP packet
def icmp_packet(data):
    icmp_type , code , checksum = struct.unpack('! B B H' , data[:4])
    return icmp_type , code , checksum , data[4:]


# Unpacks TCP segment

def tcp_segment(data):
    (src_port , dest_port , sequence , acknowledgement , offset_reserved_flags) = struct.unpack('! H H L L H' , data[:14])
    offset = (offset_reserved_flags >> 12) * 4
    flag_urg = (offset_reserved_flags & 32) >> 5
    flag_ack = (offset_reserved_flags & 16) >> 5
    flag_psh = (offset_reserved_flags & 8) >> 5
    flag_rst = (offset_reserved_flags & 4) >> 5
    flag_syn = (offset_reserved_flags & 2) >> 5
    flag_fin = (offset_reserved_flags & 1

    return src_port, dest_port , sequence , acknowledgement , flag_urg , flag_rst , flag_syn , flag_fin , data[offset:]


main()