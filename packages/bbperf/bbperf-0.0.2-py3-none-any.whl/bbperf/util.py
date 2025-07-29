# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import socket
import ipaddress

from .exceptions import PeerDisconnectedException


def validate_args(args):
    if args.server and args.client:
        raise Exception("ERROR: cannot be both client and server")

    if args.client:
        # this is server IP address
        # allow any exception here to propogate up
        ipaddress.ip_address(args.client)

    if args.port > 65535:
        raise Exception("ERROR: invalid server port {}".format(args.port))

    if args.time <= 0:
        raise Exception("ERROR: argument time must be positive")

    if args.time < 10:
        raise Exception("ERROR: time must be at least 10 seconds")

    if args.udp and not args.bandwidth:
        raise Exception("ERROR: bandwidth option must be specified for UDP mode")


def convert_bandwidth_str_to_int(arg_str):
    # input string:
    # n[kmgKMG] | n[kmgKMG]pps

    idx = arg_str.find("pps")
    if idx > -1:
        # found, so pps
        is_pps = True
        human_num_str = arg_str[:idx]
    else:
        # bps
        is_pps = False
        human_num_str = arg_str

    last_char = human_num_str[-1:]

    if last_char in [ "k", "K" ]:
        ret_val = int(human_num_str[0:-1]) * (10 ** 3)

    elif last_char in [ "m", "M" ]:
        ret_val = int(human_num_str[0:-1]) * (10 ** 6)

    elif last_char in [ "g", "G" ]:
        ret_val = int(human_num_str[0:-1]) * (10 ** 9)

    else:
        ret_val = int(human_num_str)

    return is_pps, ret_val


def done_with_socket(mysock):
    try:
        mysock.shutdown(socket.SHUT_RDWR)
    except:
        pass

    try:
        mysock.close()
    except:
        pass


def threads_are_running(thread_list):
    any_running = False

    for t in thread_list:
        if t.is_alive():
            any_running = True

    return any_running


def recv_exact_num_bytes_tcp(client_sock, total_num_bytes_to_read):
    payload_bytes = bytearray()
    num_bytes_read = 0

    while num_bytes_read < total_num_bytes_to_read:

        num_bytes_remaining = total_num_bytes_to_read - num_bytes_read

        # blocking
        recv_bytes = client_sock.recv(num_bytes_remaining)

        num_bytes_received = len(recv_bytes)

        if num_bytes_received == 0:
            raise PeerDisconnectedException()

        num_bytes_read += num_bytes_received

        payload_bytes.extend(recv_bytes)

    return payload_bytes
