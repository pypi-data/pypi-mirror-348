# Copyright (c) 2024 Cloudflare, Inc.
# Licensed under the Apache 2.0 license found in the LICENSE file or at https://www.apache.org/licenses/LICENSE-2.0

import time

from .exceptions import PeerDisconnectedException


# falling off the end of this method terminates the process
def run_recv_term_queue(args, stdout_queue, control_conn, results_queue):
    if args.verbosity:
        stdout_queue.put("starting control receiver process: run_recv_term_queue")

    while True:

        try:
            # blocking
            bytes_read = control_conn.recv_a_c_block()

        except ConnectionResetError:
            if args.verbosity:
                stdout_queue.put("connection reset error")
            # exit process
            break

        except PeerDisconnectedException:
            if args.verbosity:
                stdout_queue.put("peer disconnected (control socket)")
            # exit process
            break

        received_str = bytes_read.decode()
        curr_time_str = str(time.time())
        new_str = received_str + curr_time_str + " d "

        results_queue.put(new_str)

    control_conn.close()

    if args.verbosity:
        stdout_queue.put("exiting control receiver process: run_recv_term_queue")


# falling off the end of this method terminates the process
def run_recv_term_send(args, stdout_queue, control_conn):
    if args.verbosity:
        stdout_queue.put("starting control receiver process: run_recv_term_send")

    while True:

        try:
            # blocking
            bytes_read = control_conn.recv_a_c_block()

        except ConnectionResetError:
            if args.verbosity:
                stdout_queue.put("connection reset error")
            # exit process
            break

        except PeerDisconnectedException:
            if args.verbosity:
                stdout_queue.put("peer disconnected (control socket)")
            # exit process
            break

        received_str = bytes_read.decode()
        curr_time_str = str(time.time())
        new_str = received_str + curr_time_str + " d "

        control_conn.send(new_str.encode())

    control_conn.close()

    if args.verbosity:
        stdout_queue.put("exiting control receiver process: run_recv_term_send")


# falling off the end of this method terminates the process
def run_recv_queue(args, stdout_queue, control_conn, results_queue):
    if args.verbosity:
        stdout_queue.put("starting control receiver process: run_recv_queue")

    while True:
        try:
            # blocking
            bytes_read = control_conn.recv_a_d_block()

        except ConnectionResetError:
            if args.verbosity:
                stdout_queue.put("connection reset error")
            # exit process
            break

        except PeerDisconnectedException:
            if args.verbosity:
                stdout_queue.put("peer disconnected (control socket)")
            # exit process
            break

        received_str = bytes_read.decode()

        # passthru as is
        results_queue.put(received_str)

    control_conn.close()

    if args.verbosity:
        stdout_queue.put("exiting control receiver process: run_recv_queue")
