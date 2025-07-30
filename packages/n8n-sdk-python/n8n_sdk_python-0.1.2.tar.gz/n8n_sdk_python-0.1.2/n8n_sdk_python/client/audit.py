"""
n8n Audit API Client.
"""

from typing import Optional, Any

from ..client.base import BaseClient
from ..models.audit import AuditAdditionalOptions, AuditResponse


class AuditClient(BaseClient):
    """
    Client for interacting with n8n Audit APIs.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def generate_audit_report(
        self,
        options: Optional[AuditAdditionalOptions | dict[str, Any]] = None
    ) -> AuditResponse:
        """
        Generate a security audit for your n8n instance.
        API Docs: https://docs.n8n.io/api/v1/audit/#generate-an-audit
        """
        _options: Optional[AuditAdditionalOptions] = None
        if options is not None:
            if isinstance(options, dict):
                _options = AuditAdditionalOptions(**options)
            elif isinstance(options, AuditAdditionalOptions):
                _options = options
            else:
                raise TypeError(
                    "Parameter 'options' must be of type AuditAdditionalOptions or dict, "
                    f"got {type(options).__name__}"
                )

        payload: Optional[dict[str, Any]] = None
        if _options:
            # The N8N-API.md example payload is: { "additionalOptions": { "daysAbandonedWorkflow": 0, ... } }
            # So we need to wrap the options model.
            payload = {"additionalOptions": _options.model_dump(exclude_none=True)}
        
        response_data = await self.post(endpoint="/v1/audit", json=payload)
        return AuditResponse(**response_data) 