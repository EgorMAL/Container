from python import Packer, Bin, Item, Painter
import time
import json


start = time.time()

packer = Packer()

json_file = open("../Data/Input/0/30_cl.json")
data_dict = json.load(json_file)

bin_id = data_dict['cargo_space']['id']
bin_ZYX = data_dict['cargo_space']['size']

# self, partno, ZYX, weight,put_type=1
bin = Bin(partno=bin_id, ZYX=bin_ZYX, put_type=0)
packer.addBin(bin)

for item_data in data_dict['cargo_groups']:
    for i in range(item_data['count']):
        item_id = item_data['group_id']
        item_ZYX = item_data['size']
        item_weight = item_data['mass']
        # self, partno,typeof, ZYX, weight, level, updown, color
        packer.addItem(Item(partno=item_id, typeof='cube', ZYX=item_ZYX, weight=item_weight, level=1, updown=True, color='red'))

packer.pack(bigger_first=True,distribute_items=False,fix_point=True,number_of_decimals=0)

b = packer.bins[0]
volume = b.width * b.height * b.length
print(":::::::::::", b.string())

print("FITTED ITEMS:")
volume_t = 0
volume_f = 0
unfitted_name = ''
for item in b.items:
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("position : ",item.position)
    print("rotation type : ",item.rotation_type)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.length))
    print("volume : ",float(item.width) * float(item.height) * float(item.length))
    print("weight : ",float(item.weight))
    volume_t += float(item.width) * float(item.height) * float(item.length)
    print("***************************************************")
print("***************************************************")
print("UNFITTED ITEMS:")
for item in b.unfitted_items:
    print("partno : ",item.partno)
    print("color : ",item.color)
    print("W*H*D : ",str(item.width) +'*'+ str(item.height) +'*'+ str(item.length))
    print("volume : ",float(item.width) * float(item.height) * float(item.length))
    print("weight : ",float(item.weight))
    volume_f += float(item.width) * float(item.height) * float(item.length)
    unfitted_name += '{},'.format(item.partno)
    print("***************************************************")
print("***************************************************")
print('space utilization : {}%'.format(round(volume_t / float(volume) * 100 ,2)))
print('residual volumn : ', float(volume) - volume_t )
print('unpack item : ',unfitted_name)
print('unpack item volume : ',volume_f)
print("gravity distribution : ",b.gravity)
stop = time.time()
print('used time : ',stop - start)

# draw results
painter = Painter(b)
painter.plotBoxAndItems()

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

with open("../Data/Output/30_cl.json", 'w') as fp:
    json.dump(output_dict, fp)
print(output_dict)