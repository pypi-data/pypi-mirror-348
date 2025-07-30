
from universal_mcp.servers import SingleMCPServer
from universal_mcp.integrations import ApiKeyIntegration
from universal_mcp.stores import EnvironmentStore

from universal_mcp_tavily.app import TavilyApp

env_store = EnvironmentStore()
integration_instance = ApiKeyIntegration(name="TAVILY_API_KEY", store=env_store)
app_instance = TavilyApp(integration=integration_instance)

mcp = SingleMCPServer(
    app_instance=app_instance,
)

if __name__ == "__main__":
    mcp.run()


