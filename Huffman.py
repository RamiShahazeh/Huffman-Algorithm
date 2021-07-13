import os
import math
from functools import total_ordering

@total_ordering
# Huffman Tree ode
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
        self.code = None

    def __repr__(self):
        return "(" + self.char + "," + str(self.freq) + ")"

    def isLeaf(self):
        if (self.left is None) and (self.right is None):
            return True
        else:
            return False

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if other == None:
            return False

        if (not isinstance(other, Node)):
            return False
        return self.freq == other.freq


# Huffman coding
def convert_to_bytes(encoded_text):
    extra_bits = len(encoded_text) % 8
    b = bytearray()
    if extra_bits != 0:
        # zero padding
        zeros = 8 - extra_bits
        for i in range(zeros):
            encoded_text += "0"
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        b.append(int(byte, 2))
    return b


def save_binary_file(file_path, encoded_text):
    code_bytes = convert_to_bytes(encoded_text)
    f = open(file_path, "wb")
    f.write(bytes(code_bytes))
    f.close()


def read_binary_file( input_path):
    bits_string = ""
    f = open(input_path, 'rb')
    byte = f.read(1)
    while (len(byte) > 0):
        byte = ord(byte)
        bits = bin(byte)[2:].rjust(8, '0')
        bits_string += bits
        byte = f.read(1)
    f.close()
    return bits_string

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.root = None
        self.code = {}

    def __repr__(self):
        return "(" + self.path + "," + str(self.code) + ")"

    def compress(self):
        # read file part 2
        #text = read_binary_file(self.path)

        # read file part1
        f = open(self.path, "r")
        text = f.read()
        f.close()

        # calculate each character frequancy freq_table = {}
        freq_table = self.get_freq_table(text)
        print(freq_table)

        # calculate entropy
        print("entropy", self.calculate_entropy(freq_table))

        # create leaf nodes leafs = []
        leafs = self.create_leafs(freq_table)

        # create huffman tree
        self.root = self.create_huffman_tree(leafs)

        # create code table
        self.create_code_table(self.root, "")

        # encode text
        encoded_text = self.encode(text)


        # save file part 1
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        f = open(output_path, "w")
        text = f.write(encoded_text)
        f.close()

        # save file part 2
        #filename, file_extension = os.path.splitext(self.path)
        #output_path = filename + ".bin"
        #save_binary_file(output_path,encoded_text)


        # compression ratio
        print("finished compression >", output_path)
        print("compression ratio", self.get_compression_ratio())

    # compress functions
    def get_freq_table(self, text):
        freq_table = {}
        for character in text:
            if not character in freq_table:
                freq_table[character] = 0
            freq_table[character] += 1
        return freq_table

    def calculate_entropy(self, freq_table):
        values_sum = sum(freq_table.values())
        res = 0
        for key in freq_table:
            res = res + (-1 * (freq_table[key] / values_sum) * math.log2(freq_table[key] / values_sum))
        return res

    def create_leafs(self, freq_table):
        leafs = []
        for key in freq_table:
            leafs.append(Node(key, freq_table[key]))
        leafs.sort()
        print(leafs)
        return leafs

    def create_huffman_tree(self, nodes):
        root = None
        i = 65
        while len(nodes) > 1:
            c = chr(i)
            n1 = nodes.pop(0)
            n2 = nodes.pop(0)
            new_node = Node(c, n1.freq + n2.freq)
            i = i + 1
            new_node.left = n1
            new_node.right = n2
            nodes.append(new_node)
            nodes.sort()
            root = nodes[0]
            print(nodes)
        return root

    def create_code_table(self, node, code):
        if (node.isLeaf()):
            self.code[node.char] = code
        else:
            self.create_code_table(node.left, code + "0")
            self.create_code_table(node.right, code + "1")
        return True

    def encode(self, text):
        encoded_text = ""
        for c in text:
            encoded_text += self.code[c]

        return encoded_text

    def get_compression_ratio(self):
        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + ".bin"
        comp_ratio = os.path.getsize(self.path) / os.path.getsize(output_path)
        print(comp_ratio)
        return (comp_ratio)

    ##########################

    def decopmress(self):

        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_decompressed" + ".txt"
        input_path = filename + ".bin"

        # read  compressed file part 2
        #bits_string = read_binary_file(input_path)

        # read  compressed file part 1
        f = open(input_path, "r")
        bits_string = f.read()
        f.close()

        decoded_text = self.decode(self.root, bits_string)
        #part 2
       # save_binary_file(output_path, decoded_text)
        #part 1
        decoded_text = self.decode(self.root, bits_string)
        f = open(output_path, "w")
        f.write(decoded_text)
        f.close()
        print("finished decompression >", output_path)

    # decompress function
    def decode(self, root, bits_string):
        decoded_text = ""
        print(bits_string)
        for bit in bits_string:
            if bit == "0":
                root = root.left
            else:
                root = root.right
            if root.isLeaf():
                decoded_text += root.char
                root = self.root
        print(decoded_text)
        return decoded_text


