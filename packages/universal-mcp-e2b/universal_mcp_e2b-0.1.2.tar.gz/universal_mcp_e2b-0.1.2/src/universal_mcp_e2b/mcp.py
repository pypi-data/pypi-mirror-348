
from universal_mcp.servers.server import SingleMCPServer
from universal_mcp.integrations.integration import ApiKeyIntegration
from universal_mcp.stores.store import EnvironmentStore

from universal_mcp_e2b.app import E2bApp

env_store = EnvironmentStore()
integration_instance = ApiKeyIntegration(name="E2B_API_KEY", store=env_store)
app_instance = E2bApp(integration=integration_instance)

mcp = SingleMCPServer(
    app_instance=app_instance,
)

if __name__ == "__main__":
    mcp.run()


