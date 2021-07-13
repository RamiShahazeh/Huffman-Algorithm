from Huffman import HuffmanCoding

path = "sample.txt"

h = HuffmanCoding(path)
h.compress()

h.decopmress()

"""""
my_list = []
for i in range(8):
    my_list.append(i)
print(my_list)

genre = ['pop', 'rock', 'jazz']
for i in range(len(genre)):
    print('i like', genre[i])

my_dict = dict()
my_dict = {"rami": 80, "anas": 80}
for key in my_dict:
    print(my_dict[key])


def check(data):
    res = sum(data.values()) / len(data)
    if (res > 60):
        return True, res
    else:
        return False, res


ok, res = check(my_dict)
if ok:
    print("avarage: ", res)
"""""