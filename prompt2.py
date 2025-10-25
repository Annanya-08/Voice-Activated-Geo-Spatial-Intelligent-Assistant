# Import the required libraries
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json

def extract_layer(query: str):
    def execute_query(query: str):
        with open('complete_data.json') as f:
            metadata = json.load(f)

        llm = ChatOpenAI(model="meta/llama3-70b-instruct", base_url="https://integrate.api.nvidia.com/v1", api_key="")

        # Example data dictionary (replace with actual metadata processing logic)
        data = {"Land Resources": ["Champawat:champawat_lulc2005_06","Champawat:champawat_lulc2011_12","Champawat:champawat_lulc2015_16","Champawat:champawat_lulc_2021_22"]}

        # Example URL (replace with actual URL construction logic)
        URL = "https://<ip>:<port>/geoserver/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=application/json&LAYER={layer_name}"

        prompt1 = f"""
        You're a versatile data analyst tasked with processing dictionary data:{data} in a structured manner. Your main objective is to read 
        the dictionary data, extract values for each key, pass that value in place of layer_name in the URL: {URL},
        retrieve the legend titles from that URL and store it in a list.
        Again understand the user query and check if the user is asking for any specific legend, if yes then return that specific legend
        else return all legend titles for that specific layer. 

        Task:

        Given a dictionary dataset with keys and corresponding lists of values, your task is to process this information. For each
        value in the list of values corresponding to a key, you are to access a URL: {URL},
        where the value is passed and value stores the layer name.
        From the URL, extract the legend title associated with that particular value.
        When a user query is received, determine the legend name being requested and return it. If no specific legend is mentioned,
        return all legend names.
        Remember to handle the data processing efficiently, retrieve the correct legend titles based on the values, and provide a 
        user-friendly response according to the user query, ensuring all possible legend names are covered.

        Example: When the dictionary data contains:
        {json.dumps(data)}

        After completing the above tasks you have to return an output in the form:

        Example:

        User Query: "Provide me information about Water Resources, focusing on drainage and tubewells."
        Categories - Water Resources
                    Layers - drainage_corrected
                            Legend - Distributary Canal
                                    River
                                    Main Canal
                            champawat_tubewells
                            Legend - champawat_tubewells
                
        Output Dictionary Format:

        {{
            "Water Resources": {{
                "drainage_corrected": ["Distributary Canal", "River", "Main Canal"],
                "champawat_tubewells": ["champawat_tubewells"]
            }}
        }}

        Always ensure that the responses are accurate, concise, and formatted appropriately to meet the user's specific request 
        or general query regarding legend names associated with different layers.
        """

        output = ChatPromptTemplate.from_template(prompt1)
        chain = output | llm | StrOutputParser()
        result = chain.invoke({"query": query, "metadata": metadata,"data":data,"URL":URL})
        return result

    return execute_query(query)

if __name__ == "__main__":
    x = extract_layer("activate lulc. ")
    print(x)
