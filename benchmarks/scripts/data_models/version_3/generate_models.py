import yaml
import os

data = []
folder_path = "./"

# Remove all yaml files from the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".yml"):
        file_path = os.path.join(folder_path, filename)
        os.remove(file_path)

n_models = 1000
n_metrics = int(1000000 / n_models)
for n in range(n_models):
    cube = {
        "name": f"Orders_{n}",
        "sql": f"SELECT * FROM public.orders",
        "joins": [],
        "refresh_key": {"every": "5 hours"},
        "dimensions": [
            {"name": "id", "sql": "id", "type": "number", "primary_key": True},
            {"name": "createdAt", "sql": "created_at", "type": "time"},
        ],
        "measures": [],
    }

    for i in range(n_metrics):
        cube["measures"].append({"name": f"measure_{i}", "type": "count"})

    data.append({"cubes": [cube]})


for i in range(n_models):
    with open(f"models_{i}.yml", "w") as file:
        file.truncate(0)  # Clear the file before writing
        yaml.dump(data[i], file)
