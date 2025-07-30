from jupyter_server.utils import url_path_join as ujoin
from jupyter_server.serverapp import ServerApp

# Use a relative import for the handler
from .handlers import TokenHandler

def _jupyter_server_extension_points():
    """Defines the server extension point."""
    return [{"module": "jovyanai_extension"}]

def _load_jupyter_server_extension(server_app: ServerApp):
    """Registers the API handler to receive HTTP requests from the frontend extension."""
    web_app = server_app.web_app
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]

    # Define the route for the token handler
    token_route_pattern = ujoin(base_url, "jovyanai_token")

    # Add the handler to the web app
    handlers = [(token_route_pattern, TokenHandler)]
    web_app.add_handlers(host_pattern, handlers)

    server_app.log.info(f"[JovyanAI] Registered token handler at URL path {token_route_pattern}")

# For backward compatibility with older versions of Jupyter server
load_jupyter_server_extension = _load_jupyter_server_extension 