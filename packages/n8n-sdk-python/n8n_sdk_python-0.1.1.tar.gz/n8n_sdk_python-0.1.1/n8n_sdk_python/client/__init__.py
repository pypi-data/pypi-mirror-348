"""
n8n API 客戶端模組。
這個模組包含與 n8n API 通信的客戶端類。
"""

from typing import Optional

from .base import BaseClient
from .audit import AuditClient
from .credentials import CredentialClient
from .executions import ExecutionClient
from .projects import ProjectClient
from .source_control import SourceControlClient
from .tags import TagClient
from .users import UserClient
from .variables import VariableClient
from .workflows import WorkflowClient

from .nodes import NodesClient
from .connections import ConnectionsClient


class N8nClient:
    """
    n8n API 完整客戶端類，整合所有API功能。
    """
    
    def __init__(self, base_url: Optional[str] = None, api_key: Optional[str] = None):
        """
        初始化 n8n API 客戶端
        
        Args:
            base_url: n8n API 的基礎 URL
            api_key: n8n API 金鑰
        """
        self.audit = AuditClient(base_url=base_url, api_key=api_key)
        self.credentials = CredentialClient(base_url=base_url, api_key=api_key)
        self.executions = ExecutionClient(base_url=base_url, api_key=api_key)
        self.projects = ProjectClient(base_url=base_url, api_key=api_key)
        self.source_control = SourceControlClient(base_url=base_url, api_key=api_key)
        self.tags = TagClient(base_url=base_url, api_key=api_key)
        self.users = UserClient(base_url=base_url, api_key=api_key)
        self.variables = VariableClient(base_url=base_url, api_key=api_key)
        self.workflows = WorkflowClient(base_url=base_url, api_key=api_key)

        # NOTE: unofficial API
        self.nodes = NodesClient(base_url=base_url, api_key=api_key)
        self.connections = ConnectionsClient(base_url=base_url, api_key=api_key)
        
        # audit
        self.generate_audit_report = self.audit.generate_audit_report
        
        # credentials
        self.create_credential = self.credentials.create_credential
        self.delete_credential = self.credentials.delete_credential
        self.get_credential_schema = self.credentials.get_credential_schema
        self.transfer_credential_to_project = self.credentials.transfer_credential_to_project

        # executions
        self.list_executions = self.executions.list_executions
        self.get_execution = self.executions.get_execution
        self.delete_execution = self.executions.delete_execution
        
        # projects
        self.create_project = self.projects.create_project
        self.list_projects = self.projects.list_projects
        self.delete_project = self.projects.delete_project
        self.update_project = self.projects.update_project

        # source control
        self.pull_from_source_control = self.source_control.pull_from_source_control

        # tags
        self.create_tag = self.tags.create_tag
        self.list_tags = self.tags.list_tags
        self.get_tag = self.tags.get_tag
        self.delete_tag = self.tags.delete_tag
        self.update_tag = self.tags.update_tag

        # users
        self.list_users = self.users.list_users
        self.create_users = self.users.create_users
        self.get_user = self.users.get_user
        self.delete_user = self.users.delete_user
        self.update_user_role = self.users.update_user_role

        # variables
        self.create_variable = self.variables.create_variable
        self.list_variables = self.variables.list_variables
        self.delete_variable = self.variables.delete_variable

        # workflows
        self.create_workflow = self.workflows.create_workflow
        self.list_workflows = self.workflows.list_workflows
        self.get_workflow = self.workflows.get_workflow
        self.delete_workflow = self.workflows.delete_workflow
        self.update_workflow = self.workflows.update_workflow
        self.activate_workflow = self.workflows.activate_workflow
        self.deactivate_workflow = self.workflows.deactivate_workflow
        self.transfer_workflow_to_project = self.workflows.transfer_workflow_to_project
        self.get_workflow_tags = self.workflows.get_workflow_tags
        self.update_workflow_tags = self.workflows.update_workflow_tags

        # NOTE: unofficial API
        # nodes
        self.get_node_types = self.nodes.get_node_types
        self.get_node_type = self.nodes.get_node_type
        
        # connections
        self.list_connections = self.connections.list_connections
        self.create_connection = self.connections.create_connection
        self.delete_connection = self.connections.delete_connection


__all__ = [
    'BaseClient',
    'UserClient',
    'AuditClient',
    'ExecutionClient',
    'WorkflowClient',
    'CredentialClient',
    'TagClient',
    'SourceControlClient',
    'VariableClient',
    'ProjectClient',
    'NodesClient',
    'ConnectionsClient',
    'N8nClient'
] 