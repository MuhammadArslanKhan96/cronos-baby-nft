from IPython.display import display 
from PIL import Image
import random
import json
import os

os.system('cls' if os.name=='nt' else 'clear')

def create_new_image(all_images, config):
    new_image = {}
    for layer in config["layers"]:
      new_image[layer["name"]] = random.choices(layer["values"], layer["weights"])[0]
    
    

    if new_image in all_images:
      return create_new_image(all_images, config)
    else:
      return new_image

def generate_unique_images(amount, config):
  print("Generating {} unique NFTs...".format(amount))
  pad_amount = len(str(amount))
  trait_files = {
  }
  for trait in config["layers"]:
    trait_files[trait["name"]] = {}
    for x, key in enumerate(trait["values"]):
      trait_files[trait["name"]][key] = trait["filename"][x]
  
  all_images = []
  for i in range(amount): 
    new_trait_image = create_new_image(all_images, config)
    all_images.append(new_trait_image)

  i = 0
  for item in all_images:
      item["tokenId"] = i
      i += 1

  for i, token in enumerate(all_images):
    attributes = []
    for key in token:
      if key != "tokenId":
        attributes.append({"trait_type": key, "value": token[key]})
    token_metadata = {
        "image": config["baseURI"] + "/" + str(token["tokenId"]) + '.png',
        "tokenId": token["tokenId"],
        "name":  config["name"] + str(token["tokenId"]).zfill(pad_amount),
        "description": config["description"],
        "attributes": attributes
    }
    with open('./metadata/' + str(token["tokenId"]) + '.json', 'w') as outfile:
        json.dump(token_metadata, outfile, indent=4)

  with open('./metadata/all-objects.json', 'w') as outfile:
    json.dump(all_images, outfile, indent=4)
  
  for item in all_images:
    layers = []
    for index, attr in enumerate(item):
      if attr != 'tokenId':
        layers.append([])
        layers[index] = Image.open(f'{config["layers"][index]["trait_path"]}/{trait_files[attr][item[attr]]}.png').convert('RGBA')

    if len(layers) == 1:
      rgb_im = layers[0].convert('RGBA')
      file_name = str(item["tokenId"]) + ".png"
      # rgb_im.save("./images/test/" + file_name)
    elif len(layers) == 2:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      rgb_im = main_composite.convert('RGBA')
      file_name = str(item["tokenId"]) + ".png"
      # rgb_im.save("./images/test/" + file_name)
    elif len(layers) >= 3:
      main_composite = Image.alpha_composite(layers[0], layers[1])
      layers.pop(0)
      layers.pop(0)
      for index, remaining in enumerate(layers):
        main_composite = Image.alpha_composite(main_composite, remaining)
      rgb_im = main_composite.convert('RGBA')
      file_name =str(item["tokenId"]) + ".png"
      # if item["tokenId"] > 99:
      #   file_name = str(item["tokenId"]) + ".png"
      # elif item["tokenId"] > 999:
      #   file_name = str(item["tokenId"]) + ".png"
      rgb_im.save("./images/test/" + file_name)
  
  # v1.0.2 addition
  print("\nUnique NFT's generated. After uploading images to IPFS, please paste the CID below.\nYou may hit ENTER or CTRL+C to quit.")
  cid = input("IPFS Image CID (): ")
  if len(cid) > 0:
    if not cid.startswith("ipfs://"):
      cid = "https://gateway.pinata.cloud/ipfs/{}".format(cid)
    if cid.endswith("/"):
      cid = cid[:-1]
    for i, item in enumerate(all_images):
      with open('./metadata/' + str(item["tokenId"]) + '.json', 'r') as infile:
        original_json = json.loads(infile.read())
        original_json["image"] = original_json["image"].replace(config["baseURI"]+"/", cid+"/")
        with open('./metadata/' + str(item["tokenId"]) + '.json', 'w') as outfile:
          json.dump(original_json, outfile, indent=4)

generate_unique_images(100, {
  "layers": [
    {
      "name": "dark-blue",
      "values": ["0_darker_blue_start"],
      "trait_path": "./trait-layers",
      "filename": ["0_darker_blue_start"],
      "weights": [100]
    },
    {
      "name": "Backgrounds",
      "values": ["Background_1", "Background_2", "Background_3", "Background_4", "Background_5", "Background_6", "Background_7", "Background_8", "Background_9", "Background_10", "Background_11", "Background_12", "Background_13", "Background_14", "Background_15", "Background_16"],
      "trait_path": "./trait-layers/Backgrounds",
      "filename": ["Background_1", "Background_2", "Background_3", "Background_4", "Background_5", "Background_6", "Background_7", "Background_8", "Background_9", "Background_10", "Background_11", "Background_12", "Background_13", "Background_14", "Background_15", "Background_16"],
      "weights": [100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]
    },
    {
      "name": "Manes",
      "values": ["Mane_1", "Mane_2", "Mane_3", "Mane_4", "Mane_5", "Mane_6", "Mane_7", "Mane_8", "Mane_9", "Mane_10", "Mane_11", "Mane_12", "Mane_13", "Mane_14", "Mane_15", "Mane_16"],
      "trait_path": "./trait-layers/Manes",
      "filename": ["Mane_1", "Mane_2", "Mane_3", "Mane_4", "Mane_5", "Mane_6", "Mane_7", "Mane_8", "Mane_9", "Mane_10", "Mane_11", "Mane_12", "Mane_13", "Mane_14", "Mane_15", "Mane_16"],
      "weights": [100,100,100,100,100,100,100,100,100,100,100,100,100,100,100,100]
    },
    {
      "name": "Heads",
      "values": ["Head_1", "Head_2", "Head_3", "Head_4", "Head_5", "Head_6", "Head_7", "Head_8", "Head_9", "Head_10", "Head_11", "Head_12"],
      "trait_path": "./trait-layers/Heads",
      "filename": ["Head_1", "Head_2", "Head_3", "Head_4", "Head_5", "Head_6", "Head_7", "Head_8", "Head_9", "Head_10", "Head_11", "Head_12"],
      "weights": [100,100,100,100,100,100,100,100,100,100,100,100]
    },
    {
      "name": "Earnings",
      "values": ["Earning_1", "Earning_2", "Earning_3", "Earning_4", "Earning_5", "Earning_6", "Earning_7", "Earning_8", "Earning_9", "Earning_10", "Earning_11"],
      "trait_path": "./trait-layers/Earnings",
      "filename": ["Earning_1", "Earning_2", "Earning_3", "Earning_4", "Earning_5", "Earning_6", "Earning_7", "Earning_8", "Earning_9", "Earning_10", "Earning_11"],
      "weights": [5,5,5,5,5,5,5,5,5,5,5]
    },
   {
      "name": "Glasses",
      "values": ["Glasses_1", "Glasses_2", "Glasses_3", "Glasses_4", "Glasses_5", "Glasses_6", "Glasses_7", "Glasses_8"],
      "trait_path": "./trait-layers/Glasses",
      "filename": ["Glasses_1", "Glasses_2", "Glasses_3", "Glasses_4", "Glasses_5", "Glasses_6", "Glasses_7", "Glasses_8"],
      "weights": [3,3,3,3,3,3,3,3]
    },
    {
      "name": "Hats",
      "values": ["Hat_1", "Hat_2", "Hat_3", "Hat_4", "Hat_5", "Hat_6", "Hat_7", "Hat_8", "Hat_9", "Hat_10", "Hat_11"],
      "trait_path": "./trait-layers/Hats",
      "filename": ["Hat_1", "Hat_2", "Hat_3", "Hat_4", "Hat_5", "Hat_6", "Hat_7", "Hat_8", "Hat_9", "Hat_10", "Hat_11"],
      "weights": [2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5,2.5]
    },
    {
      "name": "Costumes",
      "values": ["Costume_1", "Costume_2", "Costume_3", "Costume_4", "Costume_5", "Costume_6", "Costume_7", "Costume_8", "Costume_9", "Costume_10", "Costume_11", "Costume_12", "Costume_13", "Costume_14", "Costume_15", "Costume_16"],
      "trait_path": "./trait-layers/Costumes",
      "filename": ["Costume_1", "Costume_2", "Costume_3", "Costume_4", "Costume_5", "Costume_6", "Costume_7", "Costume_8", "Costume_9", "Costume_10", "Costume_11", "Costume_12", "Costume_13", "Costume_14", "Costume_15", "Costume_16"],
      "weights": [6,0.1,0.1,1,4,5,3,8,9.75,1,9,9.75,7,6.3,1,1]
    },
    {
      "name": "Animals",
      "values": ["Animal_1", "Animal_2", "Animal_3", "Animal_4", "Animal_5", "Animal_6"],
      "trait_path": "./trait-layers/Animals",
      "filename": ["Animal_1", "Animal_2", "Animal_3", "Animal_4", "Animal_5", "Animal_6"],
      "weights": [1,1,1,1,1,1]
    },
    {
      "name": "Specials",
      "values": ["Special_1", "Special_2", "Special_3", "Special_4", "Special_5", "Special_6", "Special_7", "Special_8", "Special_9", "Special_10", "Special_11", "Special_12"],
      "trait_path": "./trait-layers/Specials",
      "filename": ["Special_1", "Special_2", "Special_3", "Special_4", "Special_5", "Special_6", "Special_7", "Special_8", "Special_9", "Special_10", "Special_11", "Special_12"],
      "weights": [0.05,0.05,0.05,0.05,0.05,0.05, 0.05,0.05,0.05,0.05,0.05,0.05]
    },
  ],
  # "incompatibilities": [
  #   {
  #     "layer": "Backgrounds",
  #     "value": "2",
  #     "incompatible_with": ["11-01"]
  #   },  #  @dev : Blue backgrounds will never have the attribute "Python Logo 2".
  # ],
  "baseURI": "www.abcd.com",
  "name": "CRO BABY NFT Collection",
  "description": "CRO BABY GENESIS - ASLAN NFTs"
})

#Additional layer objects can be added following the above formats. They will automatically be composed along with the rest of the layers as long as they are the same size as eachother.
#Objects are layered starting from 0 and increasing, meaning the front layer will be the last object. (Branding)

# long shrimp best keen canoe vendor pretty arm tide butter evidence miss
# pub key wallet Ft3qcmWAT92hd7Ta54eztrGXGwfhJnNd2EoNcjtGkbrL

# SPL-token for whitelist                            
# Creating token 8kYjKFHxUty5Lb3RWmRw2sKS3H5CsYhqopJjJmvu8XeC
# Signature: 3RA6jPaXMXLJNscHPACKLijsASp3x8PBtT4SyPnF38M6iZ9gMkt9LuPfmgbGk7nxezinZ9GpY3yGTFhUUgbMWejG

# Account for Spl token 
# E9sUhhP8DWn1fhx9y2EFcPmhVAr2N8nyTJfAsmBDLbJK

# Pinata Secrets
# // API Key: 80df0a854acc03d8b936
# //  API Secret: 01da84e1a5f54a5c26e362e1d345d6896e3e29f90ada50d61e7abef3023e5a6d
# //  JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJiN2MwMjJlMy1jZWUwLTQ5YzgtOGU1OC1mNGVhNDBhZmFlZmUiLCJlbWFpbCI6Im11aGFtbWFkc2FkaXFoYW5pZkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlfSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiODBkZjBhODU0YWNjMDNkOGI5MzYiLCJzY29wZWRLZXlTZWNyZXQiOiIwMWRhODRlMWE1ZjU0YTVjMjZlMzYyZTFkMzQ1ZDY4OTZlM2UyOWY5MGFkYTUwZDYxZTdhYmVmMzAyM2U1YTZkIiwiaWF0IjoxNjQ5Mjc5NDYwfQ.qPBZgn1lVZN-S02uG7386d1LgaMNyNsjlJ3pdKSzOUw