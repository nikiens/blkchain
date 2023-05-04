import logging
import json
import grequests
import time

from threading import Thread
from flask import Flask, request
from node import Node

class Server():

    def __init__(self, node: Node):
        self.node = node

        self.host = 'localhost'
        self.urls = [f'http://{self.host}:{3000 + offset}/' for offset in range(3)]
        self.curr_port = 3000 + self.node.node_id - 1

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
            block = json.loads(block_json)
            
            if self.node.handle_block(block):
                self.logger.info(str(block))
            else:
                return "Error occured during block processing"
            
            return "Block processed"
    
        server_thread = Thread(target=srv.run, args=(self.host, self.current_port), daemon=False)
        blocks_generation_thread = Thread(target=self.blocks_generator, daemon=False)

        server_thread.start()
        blocks_generation_thread.start()