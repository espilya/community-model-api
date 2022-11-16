import json

# https://stackoverflow.com/questions/27189892/how-to-filter-json-array-in-python

filename = "data/Hecht_DEGARI_emotions.json"
filename = "data/1.json"

# Perspective (user attributes, artworks similarity features, emotion similarity on plutchik emotions similar artworks)
with open(filename, 'r', encoding='utf8') as f:
    data = json.load(f)#[0]


# Transform json input to python objects
#input_dict = json.loads(data)
input_dict = data
print (type(input_dict))

for x in input_dict:
    print(x['userid'])
    print(x.keys())
    print("\n")


# Filter python objects with list comprehensions
#output_dict = [x for x in input_dict if x['_doctype'] == 'SPICEUMProperty']
#output_dict = [x for x in input_dict if x["doctype"] == 'PH236328']
output_dict = [x for x in input_dict if 'SPICEUMProperty' in x['_id']]


# Transform python object back into json
output_json = json.dumps(output_dict)

print("\n")
print(output_dict)
print("\n")

filename = "data/Hecht_DEGARI_emotions SPICEUMProperty.json"
with open(filename, "w") as outfile:
    #json.dump(user_interactions.to_dict('records'), outfile, indent=4)
    json.dump(output_dict, outfile, indent=4)

