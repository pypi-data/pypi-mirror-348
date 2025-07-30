import os
import json

from jupyter_server.base.handlers import APIHandler

class TokenHandler(APIHandler):
    """Handler to provide the JovyanAI token from environment variables."""
    def get(self):
        token = os.environ.get("JOVYAN_AI_TOKEN")
        if token:
            self.log.info("[JovyanAI] Providing token from JOVYAN_AI_TOKEN environment variable.")
            self.finish(json.dumps({"token": token}))
        else:
            self.log.info("[JovyanAI] JOVYAN_AI_TOKEN environment variable not set.")
            # Return an empty token or null if preferred
            self.finish(json.dumps({"token": None})) 