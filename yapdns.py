import dpkt
import socket
import struct

from dpkt.udp import UDP


def int2ip(int_ip):
    return socket.inet_ntoa(struct.pack("!I", int_ip))


def main():
    s = socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.SOCK_DGRAM)
    s.bind(('eth1', 0x0800))

    while True:
        data, addr = s.recvfrom(1024)
        eth = dpkt.ethernet.Ethernet(data)
        ip = eth.data
        if isinstance(ip, str):
            err_count += 1
            continue
        if type(ip.data) == UDP:
            udp = ip.data
            # print repr(udp)
            if udp.sport == 53:
                try:
                    dns = dpkt.dns.DNS(udp.data)
                    if dns.qr == 1:
                        for rr in dns.an:
                            if rr.type == 1:
                                print int2ip(struct.unpack('>I', rr.rdata)[0])
                            else:
                                print rr.type
                except Exception as e:
                    raise e
                else:
                    print dns.qd[0].name


if __name__ == '__main__':
    main()
