import asyncio
import os
from typing import Any

import yaml
from langfuse import Langfuse


class LangfuseProvider:
    def __init__(self):
        self.client = Langfuse(
            public_key=os.environ.get("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.environ.get("LANGFUSE_SECRET_KEY"),
            host=os.environ.get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
        )

    async def get_trace(self, trace_id: str) -> str:
        """
        Fetches a trace from Langfuse and returns its YAML string representation.
        """
        fetch_response = await asyncio.to_thread(self.client.fetch_trace, trace_id)
        return self.normalize_trace(fetch_response.data)

    def normalize_trace(self, trace_data: Any) -> str:
        trace_as_dict = trace_data.dict()
        return yaml.dump(
            trace_as_dict,
            sort_keys=False,
            indent=2,
            default_flow_style=False,
            allow_unicode=True,
        )
