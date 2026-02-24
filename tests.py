import json
with open("exampledata.json") as f:
    Database = json.load(f)

Database["Entries"].append("siso")

with open("exampledata.json","w") as f:
    json.dump(Database, f, indent=2)