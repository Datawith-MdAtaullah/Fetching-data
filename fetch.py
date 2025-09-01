import requests
import json

response = requests.get("https://php.enigmagenomics.com/api/gene.php?search=AAAS")
print(response.status_code)  # getting status code = 200 means everything is OK 

API = "https://php.enigmagenomics.com/api/gene.php?search="
genes = ["AAAS","ATM","BRCA1"]
results = []

for i in genes:
    url = API + i
    print("Fetching data from:", url)
    
    x = requests.get(url,timeout=20)
    
    if x.status_code != 200:
        print('Error')
        continue
    data = x.json()
    gene_name = data.get("name",i)
    
    conditions=[]
    for j in data.get("details",{}).get("conditions",[]):
        y = j.get("name")
        if y:
            conditions.append(y)          
    HPO = []
    for h in data.get("hpoAssociations", []):
        HPO_id = h.get("ontologyId")
        if HPO_id:
            HPO.append(HPO_id)
    results.append({
        "gene": gene_name,
        "conditions": conditions,
        "hpoOntologyIds": HPO
    })

            
output_file = "gene_condition_datax.json"
with open (output_file,"w",encoding="utf-8") as f:
    json.dump(results,f,indent = 2)
    