# from langchain_google_genai import ChatGoogleGenerativeAI
from crewai import Agent, Task, Crew, Process 
from crewai_tools import CSVSearchTool,JSONSearchTool
from langchain_openai import ChatOpenAI

import os

# os.environ["OPENAI_API_BASE"] ='https://integrate.api.nvidia.com/v1'
os.environ["OPENAI_API_BASE"] ='http://localhost:11443'
os.environ["OPENAI_API_KEY"] =""
os.environ["NVIDIA_API_KEY"] =""

js_tool = CSVSearchTool(
            json_path='D:\\agents\\complete_data.json', 
            config={
            "llm": {
                "provider": "openai",  # Other options include google, openai, anthropic, llama2, etc.
                "config": {
                    "model": "llama3:instruct",
                    # "base_url": "http://localhost:11443",
                    # Additional optional configurations can be specified here.
                    # temperature=0.5,
                    # top_p=1,
                    # stream=true,
                },
            },
            "embedder": {
                "provider": "nvidia", # or openai, ollama, ...
                "config": {
                    "model": "nvidia/nv-embed-v1",
                    # "task_type": "retrieval_document",
                    # Further customization options can be added here.
                },
            },
    })

#llm = ChatOllama(model="llama3:70b",base_url="http://localhost:11443")
llm = ChatOpenAI(model="meta/llama3-70b-instruct",base_url = "https://integrate.api.nvidia.com/v1",api_key="")
# llm = ChatOpenAI(model="llama3:instruct",base_url = "https://integrate.api.nvidia.com/v1",api_key="")
#llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest",api_key="")

geo_analyst = Agent(
    role = 'Geo-Spatial Analyst',
    goal = 'Get the relevant categories and layers data for the user query {query} from the json file.',
    backstory = """You are an expert in geo-spatial analysis, 
    with a deep understanding of spatial data and its applications.
    You can quickly parse user queries and identify the relevant layers and categories.""",
    llm = llm,
    tools = [js_tool],
    verbrose = True
)

task_layer = Task(
    description = """Analyze the user's query {query} and identify which categories and layers are to be activated based on the user's query.
    Only return the layers that are relevant for answering the user's query.
    """,
    expected_output = "Use the exact category and layers names and in the same format as they are in the json file.",
    agent = geo_analyst,
    tools = [js_tool]    
)

crew = Crew(
    agents = [geo_analyst],
    tasks = [task_layer],
    # process = Process.sequential
)

result = crew.kickoff(inputs={'query':'ctivate final roads district and railway lines as well as lithology'})
print(result)