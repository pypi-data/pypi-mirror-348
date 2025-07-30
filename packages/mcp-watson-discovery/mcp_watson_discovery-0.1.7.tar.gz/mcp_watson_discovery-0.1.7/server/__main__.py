from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from ibm_watson import DiscoveryV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import httpx
load_dotenv()
import asyncio
import os
import json

mcp = FastMCP("mcp-watson-discovery")

USER_AGENT = "watson-app/1.0"

def get_projects() -> dict | None:
  authenticator = IAMAuthenticator( os.getenv('WATSONX_DISCOVERY_APIKEY') )
  discovery = DiscoveryV2(
      version=os.getenv('WATSONX_DISCOVERY_VERSION'),
      authenticator=authenticator
  )

  discovery.set_service_url( os.getenv('WATSONX_DISCOVERY_URL') )

  discovery_projects = discovery.list_projects().get_result()
  return discovery_projects

def get_collections(project_id: str) -> dict | None:
  authenticator = IAMAuthenticator( os.getenv('WATSONX_DISCOVERY_APIKEY') )
  discovery = DiscoveryV2(
      version=os.getenv('WATSONX_DISCOVERY_VERSION'),
      authenticator=authenticator
  )

  discovery.set_service_url( os.getenv('WATSONX_DISCOVERY_URL'))

  discovery_collections = discovery.list_collections(project_id).get_result()
  return discovery_collections


def get_query_results(project_id: str, collection_id: list, natural_language_query: str, limit: int = 2, filter: str = None ) -> dict | None:
  authenticator = IAMAuthenticator( os.getenv('WATSONX_DISCOVERY_APIKEY') )
  discovery = DiscoveryV2(
      version=os.getenv('WATSONX_DISCOVERY_VERSION'),
      authenticator=authenticator
  )

  discovery.set_service_url( os.getenv('WATSONX_DISCOVERY_URL') )

  query_results = discovery.query(project_id=project_id, collection_ids=collection_id, natural_language_query=natural_language_query,count=2).get_result()
  return query_results


@mcp.tool()  
async def get_projects() -> dict | None:
  """
  # Watson Discovery Get Projects

  ## Description
  The Watson Discovery Get Projects tool provides access to IBM Watson Discovery's projects, allowing you to retrieve a list of all available projects in your Watson Discovery instance. This tool returns both the human-readable project names and their corresponding unique identifiers (UUIDs) for use in subsequent operations.

  ## Function
  This tool connects to your IBM Watson Discovery instance using your provided authentication credentials, queries the available projects, and returns structured information about each project.
  
  ## Use Cases
  - Inventory management of Watson Discovery projects
  - Project selection for further operations, such as querying or collection management
  - Pre-processing step before performing operations on specific projects
  - Integration with automated workflows that require project UUIDs

  ## Authentication
  This tool requires valid IBM Cloud IAM API credentials to access your Watson Discovery instance. Ensure your service account has appropriate permissions to list projects.

  ## Output Format
  Results are returned as a structured array of project objects, each containing:
  - `name`: The project name (string)
  - `project_id`: The project's UUID (string in UUID format)
  - `type`: The type of project Possible values: [intelligent_document_processing,document_retrieval,conversational_search,content_mining,content_intelligence,other] (string)
  - `collection_count`: The number of collections configured in this project (integer)
  """
  loop = asyncio.get_running_loop()
  projects = await loop.run_in_executor(None, get_projects)
  
  return projects


@mcp.tool()  
async def list_project_collections(project_id: str) -> dict | None:
  """
  # Watson Discovery List Project Collections

  ## Description
  The Watson Discovery List Project Collections return a lists of existing collections for the specified project and returns structured information about each collection

  ## Function
  This tool connects to your IBM Watson Discovery instance using your provided authentication credentials, listing the available collections of a project, and returns structured information about each collection.
  
  ## Use Cases
  - Inventory management of Watson Discovery collections
  - Collection selection for further operations, such as querying 
  - Pre-processing step before performing operations on specific projects and collections
  - Integration with automated workflows that require collection UUIDs

  ## Authentication
  This tool requires valid IBM Cloud IAM API credentials to access your Watson Discovery instance. Ensure your service account has appropriate permissions to list collections.

  ## Output Format
  Results are returned as a structured array of collections objects, each containing:
  - `name`: The collection name (string)
  - `collection_id`: The collection's UUID (string in UUID format)  
  """
  loop = asyncio.get_running_loop()
  collections = await loop.run_in_executor(None, get_collections, project_id)

  return collections


@mcp.tool()  
async def query_project(project_id: str, collection_id: list, natural_language_query: str, count: int = 2, filter: str = None) -> dict | None:
  """
   # Watson Discovery Query Project

  ## Description
  Search your data by submitting queries that are written in natural language for the specified project and collections. The query returns a list of documents that match the query criteria.

  ## Function
  This tool connects to your IBM Watson Discovery instance using your provided authentication credentials, listing the available documents of a project and collections, and returns structured information about each document.
  
  ## Use Cases
  - Search and retrieve documents from a specific project and collection
  - Integration with automated workflows that require document retrieval
  
  ## Authentication
  This tool requires valid IBM Cloud IAM API credentials to access your Watson Discovery instance. Ensure your service account has appropriate permissions to query projects.

  ## Output Format
  Results are returned as a structured array of result objects, each containing:
  - `document_id`: The unique identifier of the document (string)
  - `result_metadata`: Metadata of a query result (object)
  - `metadata`: Metadata of the document (object)
  - `document_passages`: Passages from the document that best matches the query (object)
  """
  loop = asyncio.get_running_loop()
  documents = await loop.run_in_executor(None, get_query_results, project_id, collection_id, natural_language_query, count, filter)

  return documents["results"]


def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()