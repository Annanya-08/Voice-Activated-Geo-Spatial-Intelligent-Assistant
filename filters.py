# import required libraries
from crewai import Agent, Task, Crew, Process 
from langchain_openai import ChatOpenAI

# define llm

# define the tool
from crewai_tools import ScrapeWebsiteTool

# To enable scrapping any website it finds during it's execution
WebScrapper = ScrapeWebsiteTool()

# Initialize the tool with the website URL, so the agent can only scrap the content of the specified website
# tool = ScrapeWebsiteTool(website_url='https://www.example.com')

# Extract the text from the site
# text = tool.run()
# print(text)

# define a agent for legend
geo_assistant = Agent(
    role = 'Geo-Spatial Assistant',
    goal = 'Get the relevant legend data for the user query {query} from the specified URLs.',
    backstory = """You are an expert in geo-spatial analysis, 
    with a deep understanding of spatial data and its applications.
    You can quickly parse user queries and identify the relevant layers and legend.""",
    llm = llm,
    tools = [WebScrapper],
    verbrose = True
)

task_legend = Task(
    description = """Analyze the user's query {query} and identify which legends are to be activated based on the user's query.

    Only return the layers that are relevant for answering the user's query.
    """,
    expected_output = "Use the exact category and layers names and in the same format as they are in the json file.",
    agent = geo_assistant,
    tools = [WebScrapper],
    context = [task_layers]    
)