import json

def search(string, keys_list):
    string=string.replace(' -->',':').replace('[ ','{').replace(' ]','}').replace(' |',',')

    string='{'+string+'}'

    dict_obj = json.loads(string)

    print(dict_obj)

    value=dict_obj.copy()
    for k in keys_list:
        value = value[k]
    
    string=str(value).replace(':',' -->').replace('{','[ ').replace('}',' ]').replace(',',' |')
    return string



string = '"key2" --> [ "height" --> [ "name" --> "skax" | "street" --> "bsb" ] | "level" --> [ "level" --> 52 | "height" --> 44.42 | "street" --> "xtxo" ] | "street" --> [ "street" --> "bp" | "name" --> "xvtl" | "age" --> 34 | "level" --> 65 | "height" --> 31.75 ] ]'

list_of_keys=['key2','height']

print(search(string,list_of_keys))
