#!/usr/bin/env python3

import argparse
import time

from block import Block
from node import Node
from server import Server
from gevent import monkey

def main():
    monkey.patch_all()

    parser = argparse.ArgumentParser()
    parser.add_argument('node_id', nargs='?')
    parser.add_argument('nonce_type', nargs='?')
    
    node_id = int(parser.parse_args().node_id)
    nonce_type = parser.parse_args().nonce_type

    node = Node(node_id=node_id, nonce_type=nonce_type)
    server = Server(node=node)
    server.start()

if __name__ == '__main__':
    main()
