'''
Agent to extract categories and layers
'''
# Import the required libraries
from langchain_community.chat_models import ChatOllama, ChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import Graph
# from langchain_google_genai import ChatGoogleGenerativeAI

# Open JSON file
import json

# Access URLS
import requests

import ast

def extract_layer(query: str):
    def execute_query(query: str):
        with open('complete_data.json') as f:
            metadata = json.load(f)

        llm = ChatOpenAI(model="meta/llama3-70b-instruct",base_url = "https://integrate.api.nvidia.com/v1",api_key="")

        prompt1 = """
        You're an AI designed to assist a tech-savvy user in retrieving specific information from metadata:{metadata}. You excel at parsing through
        user queries to identify requested categories and layers within metadata efficiently.

        Task: I need you to read the user's query:{query}, comprehend it, extract the categories and layers mentioned, and organize them into a
        dictionary format. Each key in the dictionary should represent a category name, with the corresponding value being a list of 
        layer names related to that category.

        -For this specific task, make sure you pay attention to the context of the user's query:{query} and extract the categories accurately.
        -Also ensure the categories and layers name are same to the ones used in metadata:{metadata}.
        -User queries might vary in complexity, so adapt accordingly and provide a well-structured dictionary output.
        -only return the dictonary no additional information
        """

        output = ChatPromptTemplate.from_template(prompt1)
        chain = output | llm | StrOutputParser()
        result = chain.invoke({"query": query, "metadata": metadata})
        return result

    return execute_query(query)

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

if __name__ == "__main__":
    x = ast.literal_eval(extract_layer("activate lulc. "))
    y = extract_legend_name(x)
    print(y)





# # Define a Langchain graph
# workflow = Graph()

# workflow.add_node("Layer extracter", extract_layer)
# workflow.add_node("node_2", function_2)

# workflow.add_edge('Layer extracter', 'node_2')

# workflow.set_entry_point("Layer extracter")
# workflow.set_finish_point("node_2")

# app = workflow.compile()

# query = "activate lulc. "
# app.invoke(query)
