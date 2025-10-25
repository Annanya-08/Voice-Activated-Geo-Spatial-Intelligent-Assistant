import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

with open('complete_data.json') as f:
    metadata = json.load(f)
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",api_key="")
llm = ChatOpenAI(model="meta/llama3-70b-instruct",base_url = "https://integrate.api.nvidia.com/v1",api_key="")
example1 = """
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
            </layers>
    </category>
</categories>

"""
                    
prompt = """
        You're an AI designed to assist a tech-savvy user in retrieving specific information from data provided.
        You excel at parsing through user queries to identify requested categories, layers and legends within metadata and legends data efficiently.
        
        Task: I need you to read the user's query:{query}, comprehend it, extract the categories, layers and legends mentioned from metadata:{metadata} and legends data:{legend_data}, and organize them into a
        xml format which follows {example1} schema strictly.
 
        -For this specific task, make sure you pay attention to the context of the user's query.
        -Sometimes when user asks using legend name directly look the legend_data first and then search the metadata for the category name.
        -Do not return the legends under layers until asked specifically in the users query.
        -Also ensure the categories, layers and legends name are same to the ones used in metadata and legend data.
        -User queries might vary in complexity, so adapt accordingly and provide a well-structured xml output.
        -only return the xml structured response no additional information                    
"""

query = "activate National highway, railway lines as well as lithology."
legend_data = {'Champawat:final_roads_district': ['National Highway', 'O.D.R.', 'PMGSY', 'RCC Roads', 'RWD Parisampati', 'State Highway', 'Unmetalled Roads', 'Urban Roads', 'Village Roads'], 'Champawat:railway_line_champ': ['Broad Gauge Railway'], 'Champawat:champa_lithology': ['BASIC META-VOLCANICS', 'BIOTITE SCHIST,CHLORITE SCHIST,QTZT& GNEISS', 'BIOTITE SCHIST,GNEISS,QTZT., INTRUSIVE GRANITE', 'CARBONACEOUS PHYLLITE, QUARTZITE AND SCHIST', 'CHLORITE SCHIST WITH SCRICITE QUARTZITE BAND', 'CHLORITE/BIOTITE SCHIST WITH QUARTZITE &GNEISS', 'COBBLE,PEBBLE,GRAVEL & BOULDER IN SANDY MATRIX', 'CONGLOMERATE, SANDSTONE,SILT & CLAY', 'FINE TO MEDIUM LEUCOCRATIC GRANITE & GRANODIORITE', 'GAR. MICA & CHLORITESCHIST, QTZ WITH PHYLLITE', 'GNEISS', 'GRANITE GNEISS WITH RAFTS OF QUARTZITE, SCHIST', 'GRAVEL, INTER LAYERED SAND AND SILT', 'GRAVEL,BOULDER EMBEDDED IN OXIDISED SANDY MATRIX', 'GRAVEL,INTERLAYERED SAND,SILT & CLAY', 'GREY MICACEOUS SAND, SILT AND CLAY', 'GREY SAND, SILT AND CLAY', 'LEUCOCRATIC GRANITE AND GRANODIORITE', 'METAVOLCANICS', 'MUSCOVITE GNEISS WITH QUARTZITE BANDS', 'OXIDISED SILT-CLAY WITH KANKAR AND MICACEOUS SAND', 'PENECONTEMP.BASIC LAVA FLOW,DYKE & DOLERITE SILL', 'QUARTZITE WITH METAVOLC., CHL. SCHIST & PHYLLITE', 'QUARTZITE, BIOTITE SCHIST AND PARAGNEISS', 'QUARTZITE, SHALE, PHYLLITE AND CONGLOMERATE', 'QUARTZITE, SLATE, LENSOIDAL LIMESTONE AND TUFF', 'SANDSTONE WITH CLAY INTERCALATION', 'SANDSTONE WITH THIN INTERCALATION OF SANDY CLAY', 'SANDSTONE, SILTSTONE, CLAYSTONE WITH CONGLOMERATE', 'SHALE,QUARTZITE, LIMESTONE AND CONGLOMERATE', 'SILT,CLAY,SAND WITH GRAVEL AND PEBBLES', 'SLATE, QUARTZITE DOLOMITE WITH BASIC INTRUSIVES', 'SUB ANGULAR COBBLE, PEBBLE, SAND AND SILT', 'UNMAPPED']}
output = ChatPromptTemplate.from_template(prompt)
chain = output | llm | StrOutputParser()
result = chain.invoke({"query": query, "metadata": metadata,"legend_data":legend_data,"example1":example1})

print(result)
