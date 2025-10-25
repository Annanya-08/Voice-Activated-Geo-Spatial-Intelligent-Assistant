import requests
def extract_legend_name(data: dict):
    def extract_layer_name(data: dict):
        layername = []
        for key, value in data.items():
            for i in value:
                layername.append(i)
        return layername

    def get_legend_names(layer_name):
        url = f"http://<ip>:<port>/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=application/json&LAYER={layer_name}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            legend_names = [rule["name"] for rule in data["Legend"][0]["rules"]]
            return legend_names
        else:
            return None


    layer_names = extract_layer_name(data)

    legends_dict = {}
    for layer_name in layer_names:
        legend = get_legend_names(layer_name)
        if legend:
            legends_dict[layer_name] = legend
        else:
            legends_dict[layer_name] = "No legends present"

    return legends_dict


print(extract_legend_name({'Transport': ['Champawat:final_roads_district', 'Champawat:railway_line_champ'], 'Geology': ['Champawat:champa_lithology']}))
