import os
import json
import glob
import shutil
from utils import Utils

class Nexo:
    def __init__(self):
        self.armors_rendering = {}
        self.furnace_data = {"items": {}}

    def get_armor_type(self, material):
        return next((armor for armor in ["HELMET", "CHESTPLATE", "LEGGINGS", "BOOTS"] if armor in material), "UNKNOWN")

    def extract(self):
        os.makedirs("output/nexo", exist_ok=True)
        datas = [Utils.load_yaml(file) for file in glob.glob("pack/Nexo/items/**/*.yml", recursive=True)]
        #print(json.dumps(datas, indent=4))

        for data in datas:
            for item_name, item_data in data.items():
                material = item_data.get("material")
                if not any(armor in material for armor in ["HELMET", "CHESTPLATE", "LEGGINGS", "BOOTS"]): 
                    continue

                textures = item_data.get("Pack", {}).get("textures", [])
                model_id = item_data.get("Pack", {}).get("custom_model_data", "")

                for texture in textures:
                    texture_path = glob.glob(f"J:/Data/Tin/ArmorExtract/pack/Nexo/pack/Nexo/pack/asset/minecraft/texture/{texture}.png")
                    #if os.path.exists(texture_path):
                    os.makedirs(os.path.dirname(f"output/nexo/textures/models/{texture}.png"), exist_ok=True)
                    shutil.copy(texture_path, f"output/nexo/textures/models/{texture}.png")
                    armor_type = self.get_armor_type(material)
                    self.furnace_data["items"].setdefault(f"minecraft:{material}".lower(), {}).setdefault("custom_model_data", {})[model_id] = {
                            "armor_layer": {
                                "type": armor_type.lower(),
                                "texture": f"textures/models/{texture}",
                                "auto_copy_texture": False
                            }
                        }
                    #else:
                        #print(f"Texture not found: {texture_path}")

        Utils.save_json("output/nexo/furnace.json", self.furnace_data)