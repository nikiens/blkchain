from block import Block

class Node():

    def __init__(self, node_id, nonce_type):
        self.node_id = node_id
        self.block_index = None
        self.nonce_type = nonce_type
        self.blocks = []

    def handle_block(self, block):
        if block.index == 0:
            self.block_index = 0
            self.blocks.append(block)

            return True

        if not self.blocks:
            return False    
        
        if block.index > self.blocks[-1].index:
            self.block_index = block.index
            self.blocks.append(block)

            return True
        
        return False

    def generate_block(self):
        if self.blocks:
            return Block(
                index=self.block_index + 1,
                prev_hash=self.blocks[-1].hash,
                node_id=self.node_id,
                nonce_type=self.nonce_type
            )