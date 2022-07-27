import json
import os
from python import Packer, Bin, Item, Painter
import time

def Pack(filename):
    f = open(filename)
    d = json.load(f)
    
    packer = Packer()

    bin_id = d['cargo_space']['id']
    bin_ZYX = d['cargo_space']['size']

    # self, partno, WHD, put_type=1
    bin = Bin(partno=bin_id, ZYX=bin_ZYX, put_type=0)
    packer.addBin(bin)
    # self, partno,typeof, WHD, weight, level, updown, color
    for item in d['cargo_groups']:
        packer.addItem(Item(partno=item['group_id'], 
                            typeof='cube',
                            ZYX=item['size'],
                            weight=item['mass'],
                            level=1,
                            updown=item['turnover'],
                            color='red'))
       

    packer.pack(bigger_first=True,distribute_items=False,fix_point=True,number_of_decimals=0)

    b = packer.bins[0]

    packed_cargos_info = [] 
    count = 1
    for item in b.items:
        dimension = item.getDimension()
        item_info = {}
        item_info["calculated_size"] = {
            "width": round(float(item.width) * 0.001, 4),
            "length": round(float(item.length) * 0.001, 4), 
            "height": round(float(item.height) * 0.001, 4)}
        item_info["cargo_id"] = item.partno
        item_info["id"] = count
        item_info["mass"] = str(item.weight)
        item_info["position"] = {
            "x": round(float(item.position[2]) * 0.001 + round(float(dimension[2])) * 0.001 / 2, 4),
            "y": round(float(item.position[1]) * 0.001 + round(float(dimension[1])) * 0.001 / 2, 4),
            "z": round(float(item.position[0]) * 0.001 + round(float(dimension[0])) * 0.001 / 2, 4)}
        item_info["size"] = {
            "width": round(float(dimension[0]) * 0.001, 4), 
            "height": round(float(dimension[1]) * 0.001, 4),
            "length": round(float(dimension[2]) * 0.001, 4) 
            }
        item_info["sort"] = 1
        item_info["stacking"] = True
        item_info["turnover"] = True
        item_info["type"] = "box"
        count += 1
        packed_cargos_info.append(item_info)

    print(packed_cargos_info)
    unpacked_cargos_info = []

    for item in b.unfitted_items:
        item_info = {}
        item_info["group_id"] =  item.partno,
        item_info["id"] = 0,
        item_info["mass"] = str(item.weight),
        item_info["position"] = {"x": -100, "y": -100, "z": -100},
        item_info["size"] = {"height": float(item.height), "length": float(item.length), "width": float(item.width)},
        item_info["sort"] = 1
        item_info["stacking"] = True
        item_info["turnover"] = True
        unpacked_cargos_info.append(item_info)

    output_dict = {
    "cargoSpace": {
    "loading_size": {
    "length": bin_ZYX[0] * 0.001,
    "height": bin_ZYX[1] * 0.001,
    "width": bin_ZYX[2] * 0.001
    },
    "position": [
    bin_ZYX[0] * 0.001 / 2, #L
    bin_ZYX[1] * 0.001 / 2, #H
    bin_ZYX[2] * 0.001 / 2 #W
    ],
    "type": "pallet"
    },
    "cargos": packed_cargos_info,
    "unpacked": unpacked_cargos_info
    }

    with open("../Output/"+ filename.split('/')[-1], 'w') as fp:
        json.dump(output_dict, fp)
    print(output_dict)

    return b

dirname = '../Data/Input'
dirnames = []
filenames = []
for file in os.listdir(dirname):
    filename = dirname + '/' + file
    filenames.append(filename)

    start = time.time()

    b = Pack(filename)

    stop = time.time()
    print('used time : ',stop - start)

        # draw results
        # painter = Painter(b)
        # painter.plotBoxAndItems()

        

# print(*dirnames, sep='\n')
# print(*filenames, sep='\n')