import xml.etree.ElementTree as ET

def extract_jsontags(xml_string):
    root = ET.fromstring(xml_string)
    categories_json = []
    
    for category_elem in root.findall('category'):
        category_json = {}
        
        categoryName_elem = category_elem.find('categoryName')
        if categoryName_elem is not None:
            category_json['categoryName'] = categoryName_elem.text.strip()
        
        layers_json = []
        layers_elem = category_elem.find('layers')
        if layers_elem is not None:
            for layer_elem in layers_elem.findall('layer'):
                layer_json = {}
                
                layerName_elem = layer_elem.find('layerName')
                if layerName_elem is not None:
                    layer_json['layerName'] = layerName_elem.text.strip()
                
                legends_json = []
                legends_elem = layer_elem.find('legends')
                if legends_elem is not None:
                    for legend_elem in legends_elem.findall('legend'):
                        legendname_elem = legend_elem.find('legendname')
                        if legendname_elem is not None:
                            legends_json.append({'legendname': legendname_elem.text.strip()})
                
                if legends_json:
                    layer_json['legends'] = legends_json
                
                layers_json.append(layer_json)
            
            category_json['layers'] = layers_json
        
        categories_json.append(category_json)
    
    return {'categories': categories_json}

# Example usage:
xml_string = """
<categories>
    <category>
        <categoryName>xyz</categoryName>
        <layers>
            <layer>
                <layerName>layer1</layerName>
                <legends>
                    <legend>
                        <legendname>legend1</legendname>
                    </legend>
                    <legend>
                        <legendname>legend2</legendname>
                    </legend>
                </legends>
            </layer>
            <layer>
                <layerName>layer2</layerName>
                <legends>
                    <legend>
                        <legendname>legend1</legendname>
                    </legend>
                    <legend>
                        <legendname>legend2</legendname>
                    </legend>
                </legends>
            </layer>
            <layer>
                <layerName>layer3</layerName>
            </layer>
        </layers>
    </category>
    <category>
        <categoryName>abc</categoryName>
        <layers>
            <layer>
                <layerName>layerz</layerName>
                <legends>
                    <legend>
                        <legendname>legendq</legendname>
                    </legend>
                    <legend>
                        <legendname>legendf</legendname>
                    </legend>
                    <legend>
                        <legendname>legendc</legendname>
                    </legend>
                </legends>
            </layer>
            <layer>
                <layerName>layery</layerName>
                <legends>
                    <legend>
                        <legendname>legenda</legendname>
                    </legend>
                    <legend>
                        <legendname>legendb</legendname>
                    </legend>
                </legends>
            </layer>
            <layer>
                <layerName>layerz</layerName>
            </layer>
        </layers>
    </category>
</categories>
"""

result = extract_jsontags(xml_string)
print(result)
