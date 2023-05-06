import logging
import json
import grequests
import time
import sys
import os

from types import SimpleNamespace
from threading import Thread
from flask import Flask, request
from node import Node
from block import Block

class Server():

    def __init__(self, node: Node):
        self.node = node

        self.start_port = os.environ['START_PORT']
        self.host = f'node{self.node.node_id}'
        self.neighbour_ids = os.environ['NEIGHBOUR_IDS']
        self.curr_port = int(self.start_port) + self.node.node_id

        self.urls = [f'http://{self.host}:{self.curr_port}']
        for i in self.neighbour_ids.split(', '):
            self.urls.append(f'http://node{i}:{int(self.start_port) + int(i)}')
        
        logging.basicConfig(stream=sys.stdout, level=logging.INFO)
        logging.getLogger('werkzeug').disabled = True
        self.logger = logging.getLogger(f'Node {self.node.node_id}')

    def block_generation(self):
        while True:
            if self.node.blocks:
                block = self.node.generate_block()
                
                if block.index > self.node.block_index:
                    grequests.map((grequests.post(i, json=block.to_json()) for i in self.urls))

            time.sleep(0.5)

    def start(self):
        srv = Flask(__name__)

        @srv.route('/', methods=['POST'])
        def srv_handler():
            block_json = request.get_json()
            block = json.loads(block_json, object_hook=lambda o: SimpleNamespace(**o))
            
            if self.node.handle_block(block):
                self.logger.info(str(block))
            else:
                return "Error occured during block processing"
            
            return "Block processed"
    
        server_thread = Thread(target=srv.run, args=(self.host, self.curr_port), daemon=False)
        blocks_generation_thread = Thread(target=self.block_generation, daemon=False)

        server_thread.start()
        blocks_generation_thread.start()

        if self.node.node_id == 1:
            time.sleep(2)

            genesis = Block(0, 'GENESIS', nonce_type='1to10', node_id=-1)
            grequests.map((grequests.post(i, json=genesis.to_json()) for i in self.urls))
        