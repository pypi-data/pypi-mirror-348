from mcp.server.fastmcp import FastMCP
from datetime import datetime
from typing import Any, Dict
import requests 
import logging
import os 
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PROXIES = {
    "http": "http://genproxy.corp.amdocs.com:8080", 
    "https": "http://genproxy.corp.amdocs.com:8080",
}

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("mistfs_mcp_server.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("mistfs_mcp_server")

mcp = FastMCP("mistfs_tools")


@mcp.tool()
async def Get_Project_Repositories(project_name: str) -> str:
    """Get project repositories from Microsoft Visual Studio Team Foundation Server.
    
    Args:
        project_name: Name of the project in Microsoft Visual Studio Team Foundation Server
        
    Returns:
        List of repositories in the specified project
    """
    try:
        # Validate input
        if not project_name:
            return "Error: Project name is required"
        
        logger.info(f"Fetching repositories for project: {project_name}")
        TFS_PAT = os.getenv("TFS_PAT")
        if not TFS_PAT:
            logger.error("TFS_PAT is not set. It requires a PAT to access Microsoft Visual Studio Team Foundation Server.")
            return "Error: TFS_PAT is not set. It requires a PAT to access Microsoft Visual Studio Team Foundation Server."

        os.environ['HTTP_PROXY'] = ''
        os.environ['HTTPS_PROXY'] = ''

        REPOSITORY_URL = f"https://mistfs/misamdocs/{project_name}/_apis/git/repositories"
        repository_response = requests.get(
                REPOSITORY_URL,
                auth=("", TFS_PAT),
                verify=False
        )
        repository_response.raise_for_status()
        repository_data = repository_response.json()
          
        if repository_data and "value" in repository_data:
            repositories = repository_data.get('value', [])
            repositorynames = [repository['name'] for repository in repositories]
            logger.info(f"Successfully fetched repositories for project: {project_name}")
            return repositorynames
        else:
            logger.warning(f"No repositories found for project: {project_name}")
            return "No repositories found or error occurred"
    
    except Exception as e:
        logger.exception(f"Error fetching repositories for {project_name}: {str(e)}")
        return f"Error fetching repositories: {str(e)}"

@mcp.tool()
async def Get_Repository_Checkins(project_name: str, repository_name: str, userupn: str) -> str:
    """Get the all check-in (commit) from a repository using the Microsoft Visual Studio Team Foundation Server REST API.
    
    Args:
        project_name: Name of the project in Microsoft Visual Studio Team Foundation Server
        repository_name: Name of the repository
        userupn: userupn to filter commits
        
    Returns:
        All check-in (commit) details
    """
    
    # Validate input
    if not project_name or not repository_name or not userupn:
        return "Error: Project Name, Repository Name, and User UPN are required"

    logger.info(f"Fetching all check-ins for project: {project_name}, repository: {repository_name}, user: {userupn}")
    TFS_PAT = os.getenv("TFS_PAT")
    if not TFS_PAT:
        logger.error("TFS_PAT is not set. It requires a PAT to access Microsoft Visual Studio Team Foundation Server.")
        return "Error: TFS_PAT is not set. It requires a PAT to access Microsoft Visual Studio Team Foundation Server."

    os.environ['HTTP_PROXY'] = ''
    os.environ['HTTPS_PROXY'] = ''

    CHECKIN_URL = f"https://mistfs/misamdocs/{project_name}/_apis/git/repositories/{repository_name}/commits?searchCriteria.author={userupn}"

    checkin_response = requests.get(
            CHECKIN_URL,
            auth=("", TFS_PAT),
            verify=False
    )
    checkin_response.raise_for_status()
    checkin_data = checkin_response.json()
        
    if checkin_data and "value" in checkin_data:
        commits = checkin_data.get('value', [])
        #get all commits
        all_commits = []
        for commit in commits:
            commit_info = {
                "commit_id": commit.get('commitId'),
                "author": commit.get('author', {}).get('name'),
                "date": commit.get('committer', {}).get('date'),
                "comment": commit.get('comment')
            }
            all_commits.append(commit_info)

        if all_commits:
            logger.info(f"Successfully fetched commits for project: {project_name}, repository: {repository_name}, user: {userupn}")
            return all_commits
        else:
            logger.warning(f"No commits found for project: {project_name}, repository: {repository_name}, user: {userupn}")
            return "No commits found"
    else:
        logger.error(f"Error fetching commits for project: {project_name}, repository: {repository_name}, user: {userupn}")
        return "Error fetching commits"




