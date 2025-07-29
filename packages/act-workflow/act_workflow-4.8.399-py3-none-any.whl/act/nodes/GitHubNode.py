import logging
import json
import asyncio
import time
import os
import base64
from typing import Dict, Any, List, Optional, Union, Tuple
import httpx

from .base_node import (
    BaseNode, NodeSchema, NodeParameter, NodeParameterType,
    NodeValidationError
)

# Configure logging
logger = logging.getLogger(__name__)

class GitHubOperation:
    """Operations available on GitHub API."""
    # Repository operations
    GET_REPO = "get_repo"
    CREATE_REPO = "create_repo"
    UPDATE_REPO = "update_repo"
    DELETE_REPO = "delete_repo"
    LIST_REPOS = "list_repos"
    LIST_BRANCHES = "list_branches"
    CREATE_BRANCH = "create_branch"
    GET_BRANCH_PROTECTION = "get_branch_protection"
    UPDATE_BRANCH_PROTECTION = "update_branch_protection"
    
    # File operations
    GET_FILE_CONTENT = "get_file_content"
    CREATE_FILE = "create_file"
    UPDATE_FILE = "update_file"
    DELETE_FILE = "delete_file"
    
    # Pull request operations
    CREATE_PULL_REQUEST = "create_pull_request"
    GET_PULL_REQUEST = "get_pull_request"
    LIST_PULL_REQUESTS = "list_pull_requests"
    UPDATE_PULL_REQUEST = "update_pull_request"
    MERGE_PULL_REQUEST = "merge_pull_request"
    
    # Issues operations
    CREATE_ISSUE = "create_issue"
    GET_ISSUE = "get_issue"
    LIST_ISSUES = "list_issues"
    UPDATE_ISSUE = "update_issue"
    CLOSE_ISSUE = "close_issue"
    
    # Comments operations
    CREATE_COMMENT = "create_comment"
    LIST_COMMENTS = "list_comments"
    
    # Commit operations
    GET_COMMIT = "get_commit"
    LIST_COMMITS = "list_commits"
    
    # Releases operations
    CREATE_RELEASE = "create_release"
    GET_RELEASE = "get_release"
    LIST_RELEASES = "list_releases"
    UPDATE_RELEASE = "update_release"
    DELETE_RELEASE = "delete_release"
    
    # User operations
    GET_USER = "get_user"
    GET_AUTHENTICATED_USER = "get_authenticated_user"
    LIST_USER_REPOS = "list_user_repos"
    
    # Webhooks operations
    CREATE_WEBHOOK = "create_webhook"
    LIST_WEBHOOKS = "list_webhooks"
    DELETE_WEBHOOK = "delete_webhook"
    
    # Organization operations
    GET_ORGANIZATION = "get_organization"
    LIST_ORGANIZATION_REPOS = "list_organization_repos"
    LIST_ORGANIZATION_MEMBERS = "list_organization_members"
    
    # Teams operations
    GET_TEAM = "get_team"
    LIST_TEAMS = "list_teams"
    CREATE_TEAM = "create_team"
    
    # Actions operations
    LIST_WORKFLOWS = "list_workflows"
    GET_WORKFLOW = "get_workflow"
    TRIGGER_WORKFLOW = "trigger_workflow"
    LIST_WORKFLOW_RUNS = "list_workflow_runs"
    GET_WORKFLOW_RUN = "get_workflow_run"
    
    # Gist operations
    CREATE_GIST = "create_gist"
    GET_GIST = "get_gist"
    LIST_GISTS = "list_gists"
    UPDATE_GIST = "update_gist"
    DELETE_GIST = "delete_gist"

class GitHubNode(BaseNode):
    """
    Node for interacting with GitHub API.
    Provides functionality for repositories, issues, pull requests, and more.
    """
    
    # Define operation-parameter mapping as a class attribute
    _operation_parameters = {
        # Repository operations
        "get_repo": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo"
        ],
        "create_repo": [
            "operation", "auth_type", "token", "username", "password", "name", "description", 
            "private", "has_issues", "has_projects", "has_wiki", "auto_init", "gitignore_template", 
            "license_template"
        ],
        "update_repo": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "name", "description", "private", "has_issues", "has_projects", "has_wiki",
            "default_branch", "allow_squash_merge", "allow_merge_commit", "allow_rebase_merge"
        ],
        "delete_repo": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo"
        ],
        "list_repos": [
            "operation", "auth_type", "token", "username", "password", "type", "sort", "direction", 
            "per_page", "page"
        ],
        "list_branches": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "protected", "per_page", "page"
        ],
        "create_branch": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "branch_name", "sha"
        ],
        "get_branch_protection": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "branch"
        ],
        "update_branch_protection": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "branch", "required_status_checks", "enforce_admins", "required_pull_request_reviews", 
            "restrictions"
        ],
        
        # File operations
        "get_file_content": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "path", "ref"
        ],
        "create_file": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "path", "message", "content", "branch", "committer", "author"
        ],
        "update_file": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "path", "message", "content", "sha", "branch", "committer", "author"
        ],
        "delete_file": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "path", "message", "sha", "branch", "committer", "author"
        ],
        
        # Pull request operations
        "create_pull_request": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "title", "head", "base", "body", "draft", "maintainer_can_modify"
        ],
        "get_pull_request": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "pull_number"
        ],
        "list_pull_requests": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "state", "head", "base", "sort", "direction", "per_page", "page"
        ],
        "update_pull_request": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "pull_number", "title", "body", "state", "base", "maintainer_can_modify"
        ],
        "merge_pull_request": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "pull_number", "commit_title", "commit_message", "merge_method", "sha"
        ],
        
        # Issues operations
        "create_issue": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "title", "body", "assignees", "milestone", "labels", "assignee"
        ],
        "get_issue": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "issue_number"
        ],
        "list_issues": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "milestone", "state", "assignee", "creator", "mentioned", "labels", "sort", 
            "direction", "since", "per_page", "page"
        ],
        "update_issue": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "issue_number", "title", "body", "state", "milestone", "labels", "assignees", "assignee"
        ],
        "close_issue": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "issue_number"
        ],
        
        # Comments operations
        "create_comment": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "issue_number", "body"
        ],
        "list_comments": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "issue_number", "since", "per_page", "page"
        ],
        
        # Commit operations
        "get_commit": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "sha"
        ],
        "list_commits": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "sha", "path", "author", "since", "until", "per_page", "page"
        ],
        
        # Releases operations
        "create_release": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "tag_name", "target_commitish", "name", "body", "draft", "prerelease"
        ],
        "get_release": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "release_id"
        ],
        "list_releases": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "per_page", "page"
        ],
        "update_release": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "release_id", "tag_name", "target_commitish", "name", "body", "draft", "prerelease"
        ],
        "delete_release": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "release_id"
        ],
        
        # User operations
        "get_user": [
            "operation", "auth_type", "token", "username", "password", "username_to_get"
        ],
        "get_authenticated_user": [
            "operation", "auth_type", "token", "username", "password"
        ],
        "list_user_repos": [
            "operation", "auth_type", "token", "username", "password", "username_to_list", 
            "type", "sort", "direction", "per_page", "page"
        ],
        
        # Webhooks operations
        "create_webhook": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "hook_config", "events", "active"
        ],
        "list_webhooks": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "per_page", "page"
        ],
        "delete_webhook": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "hook_id"
        ],
        
        # Organization operations
        "get_organization": [
            "operation", "auth_type", "token", "username", "password", "org"
        ],
        "list_organization_repos": [
            "operation", "auth_type", "token", "username", "password", "org", 
            "type", "sort", "direction", "per_page", "page"
        ],
        "list_organization_members": [
            "operation", "auth_type", "token", "username", "password", "org", 
            "filter", "role", "per_page", "page"
        ],
        
        # Teams operations
        "get_team": [
            "operation", "auth_type", "token", "username", "password", "org", "team_slug"
        ],
        "list_teams": [
            "operation", "auth_type", "token", "username", "password", "org", 
            "per_page", "page"
        ],
        "create_team": [
            "operation", "auth_type", "token", "username", "password", "org", 
            "name", "description", "maintainers", "repo_names", "privacy", "permission"
        ],
        
        # Actions operations
        "list_workflows": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "per_page", "page"
        ],
        "get_workflow": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "workflow_id"
        ],
        "trigger_workflow": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "workflow_id", "ref", "inputs"
        ],
        "list_workflow_runs": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "workflow_id", "actor", "branch", "event", "status", "per_page", "page"
        ],
        "get_workflow_run": [
            "operation", "auth_type", "token", "username", "password", "owner", "repo", 
            "run_id"
        ],
        
        # Gist operations
        "create_gist": [
            "operation", "auth_type", "token", "username", "password", 
            "files", "description", "public"
        ],
        "get_gist": [
            "operation", "auth_type", "token", "username", "password", "gist_id"
        ],
        "list_gists": [
            "operation", "auth_type", "token", "username", "password", 
            "since", "per_page", "page"
        ],
        "update_gist": [
            "operation", "auth_type", "token", "username", "password", 
            "gist_id", "files", "description"
        ],
        "delete_gist": [
            "operation", "auth_type", "token", "username", "password", "gist_id"
        ],
    }
    
    def __init__(self, sandbox_timeout: Optional[int] = None):
        super().__init__(sandbox_timeout=sandbox_timeout)
        self.client = None
        
    def get_schema(self) -> NodeSchema:
        """Return the schema definition for the GitHub node."""
        return NodeSchema(
            node_type="github",
            version="1.0.0",
            description="Interacts with GitHub API for repository management, issues, pull requests, and more",
            parameters=[
                # Basic parameters
                NodeParameter(
                    name="operation",
                    type=NodeParameterType.STRING,
                    description="Operation to perform with GitHub API",
                    required=True,
                    enum=[
                        # Repository operations
                        GitHubOperation.GET_REPO,
                        GitHubOperation.CREATE_REPO,
                        GitHubOperation.UPDATE_REPO,
                        GitHubOperation.DELETE_REPO,
                        GitHubOperation.LIST_REPOS,
                        GitHubOperation.LIST_BRANCHES,
                        GitHubOperation.CREATE_BRANCH,
                        GitHubOperation.GET_BRANCH_PROTECTION,
                        GitHubOperation.UPDATE_BRANCH_PROTECTION,
                        
                        # File operations
                        GitHubOperation.GET_FILE_CONTENT,
                        GitHubOperation.CREATE_FILE,
                        GitHubOperation.UPDATE_FILE,
                        GitHubOperation.DELETE_FILE,
                        
                        # Pull request operations
                        GitHubOperation.CREATE_PULL_REQUEST,
                        GitHubOperation.GET_PULL_REQUEST,
                        GitHubOperation.LIST_PULL_REQUESTS,
                        GitHubOperation.UPDATE_PULL_REQUEST,
                        GitHubOperation.MERGE_PULL_REQUEST,
                        
                        # Issues operations
                        GitHubOperation.CREATE_ISSUE,
                        GitHubOperation.GET_ISSUE,
                        GitHubOperation.LIST_ISSUES,
                        GitHubOperation.UPDATE_ISSUE,
                        GitHubOperation.CLOSE_ISSUE,
                        
                        # Comments operations
                        GitHubOperation.CREATE_COMMENT,
                        GitHubOperation.LIST_COMMENTS,
                        
                        # Commit operations
                        GitHubOperation.GET_COMMIT,
                        GitHubOperation.LIST_COMMITS,
                        
                        # Releases operations
                        GitHubOperation.CREATE_RELEASE,
                        GitHubOperation.GET_RELEASE,
                        GitHubOperation.LIST_RELEASES,
                        GitHubOperation.UPDATE_RELEASE,
                        GitHubOperation.DELETE_RELEASE,
                        
                        # User operations
                        GitHubOperation.GET_USER,
                        GitHubOperation.GET_AUTHENTICATED_USER,
                        GitHubOperation.LIST_USER_REPOS,
                        
                        # Webhooks operations
                        GitHubOperation.CREATE_WEBHOOK,
                        GitHubOperation.LIST_WEBHOOKS,
                        GitHubOperation.DELETE_WEBHOOK,
                        
                        # Organization operations
                        GitHubOperation.GET_ORGANIZATION,
                        GitHubOperation.LIST_ORGANIZATION_REPOS,
                        GitHubOperation.LIST_ORGANIZATION_MEMBERS,
                        
                        # Teams operations
                        GitHubOperation.GET_TEAM,
                        GitHubOperation.LIST_TEAMS,
                        GitHubOperation.CREATE_TEAM,
                        
                        # Actions operations
                        GitHubOperation.LIST_WORKFLOWS,
                        GitHubOperation.GET_WORKFLOW,
                        GitHubOperation.TRIGGER_WORKFLOW,
                        GitHubOperation.LIST_WORKFLOW_RUNS,
                        GitHubOperation.GET_WORKFLOW_RUN,
                        
                        # Gist operations
                        GitHubOperation.CREATE_GIST,
                        GitHubOperation.GET_GIST,
                        GitHubOperation.LIST_GISTS,
                        GitHubOperation.UPDATE_GIST,
                        GitHubOperation.DELETE_GIST,
                    ]
                ),
                
                # Authentication parameters
                NodeParameter(
                    name="auth_type",
                    type=NodeParameterType.STRING,
                    description="Type of authentication to use",
                    required=True,
                    enum=["token", "basic"],
                    default="token"
                ),
                NodeParameter(
                    name="token",
                    type=NodeParameterType.STRING,
                    description="GitHub personal access token (for token auth)",
                    required=False
                ),
                NodeParameter(
                    name="username",
                    type=NodeParameterType.STRING,
                    description="GitHub username (for basic auth)",
                    required=False
                ),
                NodeParameter(
                    name="password",
                    type=NodeParameterType.STRING,
                    description="GitHub password or token (for basic auth)",
                    required=False
                ),
                
                # Repository parameters
                NodeParameter(
                    name="owner",
                    type=NodeParameterType.STRING,
                    description="Repository owner (username or organization)",
                    required=False
                ),
                NodeParameter(
                    name="repo",
                    type=NodeParameterType.STRING,
                    description="Repository name",
                    required=False
                ),
                NodeParameter(
                    name="name",
                    type=NodeParameterType.STRING,
                    description="Name for repository operations",
                    required=False
                ),
                NodeParameter(
                    name="description",
                    type=NodeParameterType.STRING,
                    description="Description of a repository",
                    required=False
                ),
                NodeParameter(
                    name="private",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether the repository is private",
                    required=False,
                    default=False
                ),
                NodeParameter(
                    name="has_issues",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to enable issues for the repository",
                    required=False,
                    default=True
                ),
                NodeParameter(
                    name="has_projects",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to enable projects for the repository",
                    required=False,
                    default=True
                ),
                NodeParameter(
                    name="has_wiki",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to enable wiki for the repository",
                    required=False,
                    default=True
                ),
                NodeParameter(
                    name="auto_init",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether to create an initial commit with empty README",
                    required=False,
                    default=False
                ),
                NodeParameter(
                    name="gitignore_template",
                    type=NodeParameterType.STRING,
                    description="Gitignore template to apply",
                    required=False
                ),
                NodeParameter(
                    name="license_template",
                    type=NodeParameterType.STRING,
                    description="License template to apply",
                    required=False
                ),
                NodeParameter(
                    name="default_branch",
                    type=NodeParameterType.STRING,
                    description="Default branch of the repository",
                    required=False
                ),
                NodeParameter(
                    name="allow_squash_merge",
                    type=NodeParameterType.BOOLEAN,
                    description="Allow squash merges for pull requests",
                    required=False
                ),
                NodeParameter(
                    name="allow_merge_commit",
                    type=NodeParameterType.BOOLEAN,
                    description="Allow merge commits for pull requests",
                    required=False
                ),
                NodeParameter(
                    name="allow_rebase_merge",
                    type=NodeParameterType.BOOLEAN,
                    description="Allow rebase merges for pull requests",
                    required=False
                ),
                
                # Branch parameters
                NodeParameter(
                    name="branch",
                    type=NodeParameterType.STRING,
                    description="Branch name",
                    required=False
                ),
                NodeParameter(
                    name="branch_name",
                    type=NodeParameterType.STRING,
                    description="Name for the new branch to create",
                    required=False
                ),
                NodeParameter(
                    name="sha",
                    type=NodeParameterType.STRING,
                    description="SHA of the commit to branch from",
                    required=False
                ),
                NodeParameter(
                    name="protected",
                    type=NodeParameterType.BOOLEAN,
                    description="Filter branches by protected status",
                    required=False
                ),
                
                # Branch protection parameters
                NodeParameter(
                    name="required_status_checks",
                    type=NodeParameterType.OBJECT,
                    description="Required status checks for branch protection",
                    required=False
                ),
                NodeParameter(
                    name="enforce_admins",
                    type=NodeParameterType.BOOLEAN,
                    description="Enforce branch protection for administrators",
                    required=False
                ),
                NodeParameter(
                    name="required_pull_request_reviews",
                    type=NodeParameterType.OBJECT,
                    description="Required pull request reviews for branch protection",
                    required=False
                ),
                NodeParameter(
                    name="restrictions",
                    type=NodeParameterType.OBJECT,
                    description="Branch restrictions for branch protection",
                    required=False
                ),
                
                # File parameters
                NodeParameter(
                    name="path",
                    type=NodeParameterType.STRING,
                    description="Path to file in repository",
                    required=False
                ),
                NodeParameter(
                    name="content",
                    type=NodeParameterType.STRING,
                    description="Content for file operations",
                    required=False
                ),
                NodeParameter(
                    name="message",
                    type=NodeParameterType.STRING,
                    description="Commit message for file operations",
                    required=False
                ),
                NodeParameter(
                    name="committer",
                    type=NodeParameterType.OBJECT,
                    description="Committer information for commit operations",
                    required=False
                ),
                NodeParameter(
                    name="author",
                    type=NodeParameterType.OBJECT,
                    description="Author information for commit operations",
                    required=False
                ),
                
                # Pull request parameters
                NodeParameter(
                    name="title",
                    type=NodeParameterType.STRING,
                    description="Title for pull request or issue",
                    required=False
                ),
                NodeParameter(
                    name="body",
                    type=NodeParameterType.STRING,
                    description="Body for pull request, issue, or comment",
                    required=False
                ),
                NodeParameter(
                    name="head",
                    type=NodeParameterType.STRING,
                    description="Head branch for pull request",
                    required=False
                ),
                NodeParameter(
                    name="base",
                    type=NodeParameterType.STRING,
                    description="Base branch for pull request",
                    required=False
                ),
                NodeParameter(
                    name="draft",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether the pull request is a draft",
                    required=False,
                    default=False
                ),
                NodeParameter(
                    name="maintainer_can_modify",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether maintainers can modify the pull request",
                    required=False,
                    default=True
                ),
                NodeParameter(
                    name="pull_number",
                    type=NodeParameterType.NUMBER,
                    description="Number of pull request",
                    required=False
                ),
                NodeParameter(
                    name="commit_title",
                    type=NodeParameterType.STRING,
                    description="Title for the merge commit",
                    required=False
                ),
                NodeParameter(
                    name="commit_message",
                    type=NodeParameterType.STRING,
                    description="Message for the merge commit",
                    required=False
                ),
                NodeParameter(
                    name="merge_method",
                    type=NodeParameterType.STRING,
                    description="Method to use for merging pull request",
                    required=False,
                    enum=["merge", "squash", "rebase"],
                    default="merge"
                ),
                
                # Issue parameters
                NodeParameter(
                    name="issue_number",
                    type=NodeParameterType.NUMBER,
                    description="Number of issue",
                    required=False
                ),
                NodeParameter(
                    name="assignees",
                    type=NodeParameterType.ARRAY,
                    description="Assignees for issue",
                    required=False
                ),
                NodeParameter(
                    name="milestone",
                    type=NodeParameterType.NUMBER,
                    description="Milestone ID for issue",
                    required=False
                ),
                NodeParameter(
                    name="labels",
                    type=NodeParameterType.ARRAY,
                    description="Labels for issue",
                    required=False
                ),
                NodeParameter(
                    name="assignee",
                    type=NodeParameterType.STRING,
                    description="Single assignee for issue",
                    required=False
                ),
                
                # Common list parameters
                NodeParameter(
                    name="state",
                    type=NodeParameterType.STRING,
                    description="State filter for issues or pull requests",
                    required=False,
                    enum=["open", "closed", "all"],
                    default="open"
                ),
                NodeParameter(
                    name="sort",
                    type=NodeParameterType.STRING,
                    description="Sort field for listings",
                    required=False
                ),
                NodeParameter(
                    name="direction",
                    type=NodeParameterType.STRING,
                    description="Sort direction",
                    required=False,
                    enum=["asc", "desc"],
                    default="desc"
                ),
                NodeParameter(
                    name="per_page",
                    type=NodeParameterType.NUMBER,
                    description="Number of results per page",
                    required=False,
                    default=30
                ),
                NodeParameter(
                    name="page",
                    type=NodeParameterType.NUMBER,
                    description="Page number",
                    required=False,
                    default=1
                ),
                
                # Additional issue list parameters
                NodeParameter(
                    name="creator",
                    type=NodeParameterType.STRING,
                    description="Creator username for issue filtering",
                    required=False
                ),
                NodeParameter(
                    name="mentioned",
                    type=NodeParameterType.STRING,
                    description="Username mentioned in issues",
                    required=False
                ),
                NodeParameter(
                    name="since",
                    type=NodeParameterType.STRING,
                    description="Only issues updated after this time (ISO 8601)",
                    required=False
                ),
                
                # Commit parameters
                NodeParameter(
                    name="until",
                    type=NodeParameterType.STRING,
                    description="Only commits before this time (ISO 8601)",
                    required=False
                ),
                
                # Release parameters
                NodeParameter(
                    name="tag_name",
                    type=NodeParameterType.STRING,
                    description="Tag name for release",
                    required=False
                ),
                NodeParameter(
                    name="target_commitish",
                    type=NodeParameterType.STRING,
                    description="Commitish value for release tag",
                    required=False
                ),
                NodeParameter(
                    name="prerelease",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether the release is a prerelease",
                    required=False,
                    default=False
                ),
                NodeParameter(
                    name="release_id",
                    type=NodeParameterType.NUMBER,
                    description="ID of release",
                    required=False
                ),
                
                # User parameters
                NodeParameter(
                    name="username_to_get",
                    type=NodeParameterType.STRING,
                    description="Username to get information for",
                    required=False
                ),
                NodeParameter(
                    name="username_to_list",
                    type=NodeParameterType.STRING,
                    description="Username to list repositories for",
                    required=False
                ),
                NodeParameter(
                    name="type",
                    type=NodeParameterType.STRING,
                    description="Type filter for repository listings",
                    required=False,
                    enum=["all", "owner", "public", "private", "member"],
                    default="all"
                ),
                
                # Webhook parameters
                # Webhook parameters
                NodeParameter(
                    name="hook_config",
                    type=NodeParameterType.OBJECT,
                    description="Configuration for webhook",
                    required=False
                ),
                NodeParameter(
                    name="events",
                    type=NodeParameterType.ARRAY,
                    description="Events that trigger the webhook",
                    required=False,
                    default=["push"]
                ),
                NodeParameter(
                    name="active",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether the webhook is active",
                    required=False,
                    default=True
                ),
                NodeParameter(
                    name="hook_id",
                    type=NodeParameterType.NUMBER,
                    description="ID of webhook",
                    required=False
                ),
                
                # Organization parameters
                NodeParameter(
                    name="org",
                    type=NodeParameterType.STRING,
                    description="Organization name",
                    required=False
                ),
                NodeParameter(
                    name="filter",
                    type=NodeParameterType.STRING,
                    description="Filter organization members by role",
                    required=False,
                    enum=["all", "2fa_disabled"],
                    default="all"
                ),
                NodeParameter(
                    name="role",
                    type=NodeParameterType.STRING,
                    description="Filter organization members by role",
                    required=False,
                    enum=["all", "admin", "member"],
                    default="all"
                ),
                
                # Team parameters
                NodeParameter(
                    name="team_slug",
                    type=NodeParameterType.STRING,
                    description="Slug of team",
                    required=False
                ),
                NodeParameter(
                    name="maintainers",
                    type=NodeParameterType.ARRAY,
                    description="Usernames of team maintainers",
                    required=False
                ),
                NodeParameter(
                    name="repo_names",
                    type=NodeParameterType.ARRAY,
                    description="Repository names for team access",
                    required=False
                ),
                NodeParameter(
                    name="privacy",
                    type=NodeParameterType.STRING,
                    description="Privacy level of team",
                    required=False,
                    enum=["secret", "closed"],
                    default="secret"
                ),
                NodeParameter(
                    name="permission",
                    type=NodeParameterType.STRING,
                    description="Permission level for team",
                    required=False,
                    enum=["pull", "push", "admin"],
                    default="pull"
                ),
                
                # Actions parameters
                NodeParameter(
                    name="workflow_id",
                    type=NodeParameterType.STRING,
                    description="ID or file name of workflow",
                    required=False
                ),
                NodeParameter(
                    name="ref",
                    type=NodeParameterType.STRING,
                    description="Reference for workflow dispatch",
                    required=False
                ),
                NodeParameter(
                    name="inputs",
                    type=NodeParameterType.OBJECT,
                    description="Inputs for workflow dispatch",
                    required=False
                ),
                NodeParameter(
                    name="actor",
                    type=NodeParameterType.STRING,
                    description="Username for filtering workflow runs",
                    required=False
                ),
                NodeParameter(
                    name="status",
                    type=NodeParameterType.STRING,
                    description="Status for filtering workflow runs",
                    required=False,
                    enum=["queued", "in_progress", "completed"],
                    default="completed"
                ),
                NodeParameter(
                    name="run_id",
                    type=NodeParameterType.NUMBER,
                    description="ID of workflow run",
                    required=False
                ),
                
                # Gist parameters
                NodeParameter(
                    name="files",
                    type=NodeParameterType.OBJECT,
                    description="Files object for gist operations",
                    required=False
                ),
                NodeParameter(
                    name="public",
                    type=NodeParameterType.BOOLEAN,
                    description="Whether the gist is public",
                    required=False,
                    default=True
                ),
                NodeParameter(
                    name="gist_id",
                    type=NodeParameterType.STRING,
                    description="ID of gist",
                    required=False
                ),
            ],
            
            # Define outputs for the node
            outputs={
                "status": NodeParameterType.STRING,
                "result": NodeParameterType.ANY,
                "error": NodeParameterType.STRING,
                "headers": NodeParameterType.OBJECT,
                "rate_limit": NodeParameterType.OBJECT
            },
            
            # Add metadata
            tags=["github", "git", "repository", "issues", "pull requests", "actions"],
            author="System"
        )
    
    def get_operation_parameters(self, operation: str) -> List[Dict[str, Any]]:
        """
        Get parameters relevant to a specific operation.
        
        Args:
            operation: The operation name (e.g., GET_REPO)
            
        Returns:
            List of parameter dictionaries for the operation
        """
        # Remove the prefix if present (e.g., GitHubOperation.GET_REPO -> GET_REPO)
        if "." in operation:
            operation = operation.split(".")[-1]
            
        # Convert to lowercase for lookup
        operation_key = operation.lower()
        
        # Get the parameter names for this operation
        param_names = self._operation_parameters.get(operation_key, [])
        
        # Get all parameters from the schema
        all_params = self.get_schema().parameters
        
        # Filter parameters based on the names
        operation_params = []
        for param in all_params:
            if param.name in param_names:
                # Convert to dictionary for the API
                param_dict = {
                    "name": param.name,
                    "type": param.type.value if hasattr(param.type, 'value') else str(param.type),
                    "description": param.description,
                    "required": param.required
                }
                
                # Add optional attributes if present
                if hasattr(param, 'default') and param.default is not None:
                    param_dict["default"] = param.default
                if hasattr(param, 'enum') and param.enum:
                    param_dict["enum"] = param.enum
                
                operation_params.append(param_dict)
        
        return operation_params
    
    def validate_custom(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """Custom validation based on the operation type."""
        operation = params.get("operation")
        
        if not operation:
            raise NodeValidationError("Operation is required")
            
        # Validate authentication parameters
        auth_type = params.get("auth_type", "token")
        if auth_type == "token":
            if not params.get("token"):
                raise NodeValidationError("Token is required for token authentication")
        elif auth_type == "basic":
            if not params.get("username") or not params.get("password"):
                raise NodeValidationError("Username and password are required for basic authentication")
        else:
            raise NodeValidationError(f"Invalid authentication type: {auth_type}")
            
        # Validate repository operations
        if operation in [
            GitHubOperation.GET_REPO, 
            GitHubOperation.UPDATE_REPO, 
            GitHubOperation.DELETE_REPO,
            GitHubOperation.LIST_BRANCHES,
            GitHubOperation.GET_BRANCH_PROTECTION,
            GitHubOperation.UPDATE_BRANCH_PROTECTION,
            GitHubOperation.CREATE_BRANCH
        ]:
            if not params.get("owner") or not params.get("repo"):
                raise NodeValidationError("Owner and repo are required for repository operations")
                
        # Validate create repository operation
        if operation == GitHubOperation.CREATE_REPO:
            if not params.get("name"):
                raise NodeValidationError("Repository name is required for creating a repository")
                
        # Validate branch operations
        if operation == GitHubOperation.CREATE_BRANCH:
            if not params.get("branch_name"):
                raise NodeValidationError("Branch name is required for creating a branch")
            if not params.get("sha"):
                raise NodeValidationError("SHA is required for creating a branch")
                
        if operation in [GitHubOperation.GET_BRANCH_PROTECTION, GitHubOperation.UPDATE_BRANCH_PROTECTION]:
            if not params.get("branch"):
                raise NodeValidationError("Branch is required for branch protection operations")
                
        # Validate file operations
        if operation in [
            GitHubOperation.GET_FILE_CONTENT, 
            GitHubOperation.CREATE_FILE, 
            GitHubOperation.UPDATE_FILE,
            GitHubOperation.DELETE_FILE
        ]:
            if not params.get("owner") or not params.get("repo") or not params.get("path"):
                raise NodeValidationError("Owner, repo, and path are required for file operations")
                
        if operation in [GitHubOperation.CREATE_FILE, GitHubOperation.UPDATE_FILE, GitHubOperation.DELETE_FILE]:
            if not params.get("message"):
                raise NodeValidationError("Commit message is required for file operations")
                
        if operation in [GitHubOperation.CREATE_FILE, GitHubOperation.UPDATE_FILE]:
            if not params.get("content"):
                raise NodeValidationError("Content is required for file creation/update")
                
        if operation in [GitHubOperation.UPDATE_FILE, GitHubOperation.DELETE_FILE]:
            if not params.get("sha"):
                raise NodeValidationError("SHA is required for file update/delete")
                
        # Validate pull request operations
        if operation == GitHubOperation.CREATE_PULL_REQUEST:
            if not params.get("owner") or not params.get("repo") or not params.get("title") or not params.get("head") or not params.get("base"):
                raise NodeValidationError("Owner, repo, title, head, and base are required for creating pull requests")
                
        if operation in [
            GitHubOperation.GET_PULL_REQUEST, 
            GitHubOperation.UPDATE_PULL_REQUEST,
            GitHubOperation.MERGE_PULL_REQUEST
        ]:
            if not params.get("owner") or not params.get("repo") or not params.get("pull_number"):
                raise NodeValidationError("Owner, repo, and pull_number are required for pull request operations")
                
        # Validate issue operations
        if operation == GitHubOperation.CREATE_ISSUE:
            if not params.get("owner") or not params.get("repo") or not params.get("title"):
                raise NodeValidationError("Owner, repo, and title are required for creating issues")
                
        if operation in [
            GitHubOperation.GET_ISSUE, 
            GitHubOperation.UPDATE_ISSUE,
            GitHubOperation.CLOSE_ISSUE
        ]:
            if not params.get("owner") or not params.get("repo") or not params.get("issue_number"):
                raise NodeValidationError("Owner, repo, and issue_number are required for issue operations")
                
        # Validate comment operations
        if operation == GitHubOperation.CREATE_COMMENT:
            if not params.get("owner") or not params.get("repo") or not params.get("issue_number") or not params.get("body"):
                raise NodeValidationError("Owner, repo, issue_number, and body are required for creating comments")
                
        if operation == GitHubOperation.LIST_COMMENTS:
            if not params.get("owner") or not params.get("repo") or not params.get("issue_number"):
                raise NodeValidationError("Owner, repo, and issue_number are required for listing comments")
                
        # Validate commit operations
        if operation == GitHubOperation.GET_COMMIT:
            if not params.get("owner") or not params.get("repo") or not params.get("sha"):
                raise NodeValidationError("Owner, repo, and sha are required for getting commits")
                
        # Validate release operations
        if operation == GitHubOperation.CREATE_RELEASE:
            if not params.get("owner") or not params.get("repo") or not params.get("tag_name"):
                raise NodeValidationError("Owner, repo, and tag_name are required for creating releases")
                
        if operation in [
            GitHubOperation.GET_RELEASE, 
            GitHubOperation.UPDATE_RELEASE,
            GitHubOperation.DELETE_RELEASE
        ]:
            if not params.get("owner") or not params.get("repo") or not params.get("release_id"):
                raise NodeValidationError("Owner, repo, and release_id are required for release operations")
                
        # Validate user operations
        if operation == GitHubOperation.GET_USER:
            if not params.get("username_to_get"):
                raise NodeValidationError("Username_to_get is required for getting user information")
                
        if operation == GitHubOperation.LIST_USER_REPOS:
            if not params.get("username_to_list"):
                raise NodeValidationError("Username_to_list is required for listing user repositories")
                
        # Validate webhook operations
        if operation == GitHubOperation.CREATE_WEBHOOK:
            if not params.get("owner") or not params.get("repo") or not params.get("hook_config"):
                raise NodeValidationError("Owner, repo, and hook_config are required for creating webhooks")
                
        if operation == GitHubOperation.DELETE_WEBHOOK:
            if not params.get("owner") or not params.get("repo") or not params.get("hook_id"):
                raise NodeValidationError("Owner, repo, and hook_id are required for deleting webhooks")
                
        # Validate organization operations
        if operation in [
            GitHubOperation.GET_ORGANIZATION, 
            GitHubOperation.LIST_ORGANIZATION_REPOS,
            GitHubOperation.LIST_ORGANIZATION_MEMBERS
        ]:
            if not params.get("org"):
                raise NodeValidationError("Organization name (org) is required for organization operations")
                
        # Validate team operations
        if operation == GitHubOperation.GET_TEAM:
            if not params.get("org") or not params.get("team_slug"):
                raise NodeValidationError("Organization name (org) and team_slug are required for getting team")
                
        if operation == GitHubOperation.CREATE_TEAM:
            if not params.get("org") or not params.get("name"):
                raise NodeValidationError("Organization name (org) and team name are required for creating team")
                
        # Validate actions operations
        if operation in [
            GitHubOperation.GET_WORKFLOW, 
            GitHubOperation.TRIGGER_WORKFLOW,
            GitHubOperation.LIST_WORKFLOW_RUNS
        ]:
            if not params.get("owner") or not params.get("repo") or not params.get("workflow_id"):
                raise NodeValidationError("Owner, repo, and workflow_id are required for workflow operations")
                
        if operation == GitHubOperation.TRIGGER_WORKFLOW:
            if not params.get("ref"):
                raise NodeValidationError("Reference (ref) is required for triggering workflows")
                
        if operation == GitHubOperation.GET_WORKFLOW_RUN:
            if not params.get("owner") or not params.get("repo") or not params.get("run_id"):
                raise NodeValidationError("Owner, repo, and run_id are required for getting workflow runs")
                
        # Validate gist operations
        if operation == GitHubOperation.CREATE_GIST:
            if not params.get("files"):
                raise NodeValidationError("Files are required for creating gists")
                
        if operation in [
            GitHubOperation.GET_GIST, 
            GitHubOperation.UPDATE_GIST,
            GitHubOperation.DELETE_GIST
        ]:
            if not params.get("gist_id"):
                raise NodeValidationError("Gist ID is required for gist operations")
                
        return {}
    
    async def execute(self, node_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the GitHub node."""
        try:
            # Extract params from node_data
            params = node_data.get("params", {})
            
            # Validate params
            self.validate_custom(params)
            
            # Get operation type
            operation = params.get("operation")
            
            # Setup HTTP client with auth
            await self._setup_client(params)
            
            try:
                # Execute the appropriate operation
                if operation == GitHubOperation.GET_REPO:
                    return await self._operation_get_repo(params)
                elif operation == GitHubOperation.CREATE_REPO:
                    return await self._operation_create_repo(params)
                elif operation == GitHubOperation.UPDATE_REPO:
                    return await self._operation_update_repo(params)
                elif operation == GitHubOperation.DELETE_REPO:
                    return await self._operation_delete_repo(params)
                elif operation == GitHubOperation.LIST_REPOS:
                    return await self._operation_list_repos(params)
                elif operation == GitHubOperation.LIST_BRANCHES:
                    return await self._operation_list_branches(params)
                elif operation == GitHubOperation.CREATE_BRANCH:
                    return await self._operation_create_branch(params)
                elif operation == GitHubOperation.GET_BRANCH_PROTECTION:
                    return await self._operation_get_branch_protection(params)
                elif operation == GitHubOperation.UPDATE_BRANCH_PROTECTION:
                    return await self._operation_update_branch_protection(params)
                elif operation == GitHubOperation.GET_FILE_CONTENT:
                    return await self._operation_get_file_content(params)
                elif operation == GitHubOperation.CREATE_FILE:
                    return await self._operation_create_file(params)
                elif operation == GitHubOperation.UPDATE_FILE:
                    return await self._operation_update_file(params)
                elif operation == GitHubOperation.DELETE_FILE:
                    return await self._operation_delete_file(params)
                elif operation == GitHubOperation.CREATE_PULL_REQUEST:
                    return await self._operation_create_pull_request(params)
                elif operation == GitHubOperation.GET_PULL_REQUEST:
                    return await self._operation_get_pull_request(params)
                elif operation == GitHubOperation.LIST_PULL_REQUESTS:
                    return await self._operation_list_pull_requests(params)
                elif operation == GitHubOperation.UPDATE_PULL_REQUEST:
                    return await self._operation_update_pull_request(params)
                elif operation == GitHubOperation.MERGE_PULL_REQUEST:
                    return await self._operation_merge_pull_request(params)
                elif operation == GitHubOperation.CREATE_ISSUE:
                    return await self._operation_create_issue(params)
                elif operation == GitHubOperation.GET_ISSUE:
                    return await self._operation_get_issue(params)
                elif operation == GitHubOperation.LIST_ISSUES:
                    return await self._operation_list_issues(params)
                elif operation == GitHubOperation.UPDATE_ISSUE:
                    return await self._operation_update_issue(params)
                elif operation == GitHubOperation.CLOSE_ISSUE:
                    return await self._operation_close_issue(params)
                elif operation == GitHubOperation.CREATE_COMMENT:
                    return await self._operation_create_comment(params)
                elif operation == GitHubOperation.LIST_COMMENTS:
                    return await self._operation_list_comments(params)
                elif operation == GitHubOperation.GET_COMMIT:
                    return await self._operation_get_commit(params)
                elif operation == GitHubOperation.LIST_COMMITS:
                    return await self._operation_list_commits(params)
                elif operation == GitHubOperation.CREATE_RELEASE:
                    return await self._operation_create_release(params)
                elif operation == GitHubOperation.GET_RELEASE:
                    return await self._operation_get_release(params)
                elif operation == GitHubOperation.LIST_RELEASES:
                    return await self._operation_list_releases(params)
                elif operation == GitHubOperation.UPDATE_RELEASE:
                    return await self._operation_update_release(params)
                elif operation == GitHubOperation.DELETE_RELEASE:
                    return await self._operation_delete_release(params)
                elif operation == GitHubOperation.GET_USER:
                    return await self._operation_get_user(params)
                elif operation == GitHubOperation.GET_AUTHENTICATED_USER:
                    return await self._operation_get_authenticated_user(params)
                elif operation == GitHubOperation.LIST_USER_REPOS:
                    return await self._operation_list_user_repos(params)
                elif operation == GitHubOperation.CREATE_WEBHOOK:
                    return await self._operation_create_webhook(params)
                elif operation == GitHubOperation.LIST_WEBHOOKS:
                    return await self._operation_list_webhooks(params)
                elif operation == GitHubOperation.DELETE_WEBHOOK:
                    return await self._operation_delete_webhook(params)
                elif operation == GitHubOperation.GET_ORGANIZATION:
                    return await self._operation_get_organization(params)
                elif operation == GitHubOperation.LIST_ORGANIZATION_REPOS:
                    return await self._operation_list_organization_repos(params)
                elif operation == GitHubOperation.LIST_ORGANIZATION_MEMBERS:
                    return await self._operation_list_organization_members(params)
                elif operation == GitHubOperation.GET_TEAM:
                    return await self._operation_get_team(params)
                elif operation == GitHubOperation.LIST_TEAMS:
                    return await self._operation_list_teams(params)
                elif operation == GitHubOperation.CREATE_TEAM:
                    return await self._operation_create_team(params)
                elif operation == GitHubOperation.LIST_WORKFLOWS:
                    return await self._operation_list_workflows(params)
                elif operation == GitHubOperation.GET_WORKFLOW:
                    return await self._operation_get_workflow(params)
                elif operation == GitHubOperation.TRIGGER_WORKFLOW:
                    return await self._operation_trigger_workflow(params)
                elif operation == GitHubOperation.LIST_WORKFLOW_RUNS:
                    return await self._operation_list_workflow_runs(params)
                elif operation == GitHubOperation.GET_WORKFLOW_RUN:
                    return await self._operation_get_workflow_run(params)
                elif operation == GitHubOperation.CREATE_GIST:
                    return await self._operation_create_gist(params)
                elif operation == GitHubOperation.GET_GIST:
                    return await self._operation_get_gist(params)
                elif operation == GitHubOperation.LIST_GISTS:
                    return await self._operation_list_gists(params)
                elif operation == GitHubOperation.UPDATE_GIST:
                    return await self._operation_update_gist(params)
                elif operation == GitHubOperation.DELETE_GIST:
                    return await self._operation_delete_gist(params)
                else:
                    error_message = f"Unknown operation: {operation}"
                    logger.error(error_message)
                    return {
                        "status": "error",
                        "result": None,
                        "error": error_message,
                        "headers": None,
                        "rate_limit": None
                    }
            finally:
                # Close HTTP client
                if self.client:
                    await self.client.aclose()
                
        except Exception as e:
            error_message = f"Error in GitHub node: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": None,
                "rate_limit": None
            }
    async def _setup_client(self, params: Dict[str, Any]) -> None:
        """
        Set up HTTP client with appropriate authentication.
        
        Args:
            params: Authentication parameters
        """
        # Base headers for GitHub API
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Node-Client"
        }
        
        # Add authentication
        auth_type = params.get("auth_type", "token")
        if auth_type == "token":
            token = params.get("token")
            headers["Authorization"] = f"token {token}"
            auth = None
        else:  # basic auth
            username = params.get("username")
            password = params.get("password")
            auth = (username, password)
        
        # Create HTTP client
        self.client = httpx.AsyncClient(
            base_url="https://api.github.com",
            headers=headers,
            auth=auth,
            timeout=60.0
        )
    
    async def _extract_rate_limit(self, response: httpx.Response) -> Dict[str, Any]:
        """Extract rate limit information from response headers."""
        rate_limit = {}
        if "X-RateLimit-Limit" in response.headers:
            rate_limit["limit"] = int(response.headers.get("X-RateLimit-Limit", "0"))
        if "X-RateLimit-Remaining" in response.headers:
            rate_limit["remaining"] = int(response.headers.get("X-RateLimit-Remaining", "0"))
        if "X-RateLimit-Reset" in response.headers:
            rate_limit["reset"] = int(response.headers.get("X-RateLimit-Reset", "0"))
        return rate_limit
    
    async def _format_response(self, response: httpx.Response) -> Dict[str, Any]:
        """
        Format API response for the node output.
        
        Args:
            response: The HTTP response from GitHub API
            
        Returns:
            Formatted response for node output
        """
        try:
            response.raise_for_status()
            
            # Extract rate limit from headers
            rate_limit = await self._extract_rate_limit(response)
            
            # Parse response body as JSON if present, otherwise return empty dict
            result = response.json() if response.content else {}
            
            return {
                "status": "success",
                "result": result,
                "error": None,
                "headers": dict(response.headers),
                "rate_limit": rate_limit
            }
        except httpx.HTTPStatusError as e:
            # Handle API errors
            error_json = e.response.json() if e.response.content else {"message": str(e)}
            error_message = error_json.get("message", str(e))
            
            # Extract rate limit even in case of error
            rate_limit = await self._extract_rate_limit(e.response)
            
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": dict(e.response.headers) if e.response else {},
                "rate_limit": rate_limit
            }
        except Exception as e:
            # Handle other errors
            return {
                "status": "error",
                "result": None,
                "error": str(e),
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Repository Operations
    # -------------------------
    
    async def _operation_get_repo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get repository information.
        
        Args:
            params: Repository parameters
            
        Returns:
            Repository information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting repository: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_create_repo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new repository.
        
        Args:
            params: Repository creation parameters
            
        Returns:
            New repository information
        """
        # Extract parameters for repository creation
        name = params.get("name")
        description = params.get("description")
        private = params.get("private", False)
        has_issues = params.get("has_issues", True)
        has_projects = params.get("has_projects", True)
        has_wiki = params.get("has_wiki", True)
        auto_init = params.get("auto_init", False)
        gitignore_template = params.get("gitignore_template")
        license_template = params.get("license_template")
        
        # Prepare request body
        body = {
            "name": name,
            "private": private,
            "has_issues": has_issues,
            "has_projects": has_projects,
            "has_wiki": has_wiki,
            "auto_init": auto_init
        }
        
        # Add optional parameters
        if description:
            body["description"] = description
        if gitignore_template:
            body["gitignore_template"] = gitignore_template
        if license_template:
            body["license_template"] = license_template
        
        try:
            response = await self.client.post("/user/repos", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating repository: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_update_repo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update repository information.
        
        Args:
            params: Repository update parameters
            
        Returns:
            Updated repository information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        
        # Extract parameters for repository update
        name = params.get("name")
        description = params.get("description")
        private = params.get("private")
        has_issues = params.get("has_issues")
        has_projects = params.get("has_projects")
        has_wiki = params.get("has_wiki")
        default_branch = params.get("default_branch")
        allow_squash_merge = params.get("allow_squash_merge")
        allow_merge_commit = params.get("allow_merge_commit")
        allow_rebase_merge = params.get("allow_rebase_merge")
        
        # Prepare request body with only provided parameters
        body = {}
        if name:
            body["name"] = name
        if description is not None:
            body["description"] = description
        if private is not None:
            body["private"] = private
        if has_issues is not None:
            body["has_issues"] = has_issues
        if has_projects is not None:
            body["has_projects"] = has_projects
        if has_wiki is not None:
            body["has_wiki"] = has_wiki
        if default_branch:
            body["default_branch"] = default_branch
        if allow_squash_merge is not None:
            body["allow_squash_merge"] = allow_squash_merge
        if allow_merge_commit is not None:
            body["allow_merge_commit"] = allow_merge_commit
        if allow_rebase_merge is not None:
            body["allow_rebase_merge"] = allow_rebase_merge
        
        try:
            response = await self.client.patch(f"/repos/{owner}/{repo}", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error updating repository: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_delete_repo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a repository.
        
        Args:
            params: Repository deletion parameters
            
        Returns:
            Status of deletion operation
        """
        owner = params.get("owner")
        repo = params.get("repo")
        
        try:
            response = await self.client.delete(f"/repos/{owner}/{repo}")
            
            # Special handling for successful deletion (204 No Content)
            if response.status_code == 204:
                rate_limit = await self._extract_rate_limit(response)
                return {
                    "status": "success",
                    "result": {"message": "Repository deleted successfully"},
                    "error": None,
                    "headers": dict(response.headers),
                    "rate_limit": rate_limit
                }
            
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error deleting repository: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_repos(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List repositories for the authenticated user.
        
        Args:
            params: Repository listing parameters
            
        Returns:
            List of repositories
        """
        # Extract filter parameters
        repo_type = params.get("type", "all")
        sort = params.get("sort", "full_name")
        direction = params.get("direction", "asc")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "type": repo_type,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get("/user/repos", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing repositories: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_branches(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List branches for a repository.
        
        Args:
            params: Branch listing parameters
            
        Returns:
            List of branches
        """
        owner = params.get("owner")
        repo = params.get("repo")
        protected = params.get("protected")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        if protected is not None:
            query_params["protected"] = "true" if protected else "false"
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/branches", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing branches: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_create_branch(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new branch in a repository.
        
        Args:
            params: Branch creation parameters
            
        Returns:
            New branch information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        branch_name = params.get("branch_name")
        sha = params.get("sha")
        
        # Creating a branch is done by creating a reference
        ref = f"refs/heads/{branch_name}"
        
        # Prepare request body
        body = {
            "ref": ref,
            "sha": sha
        }
        
        try:
            response = await self.client.post(f"/repos/{owner}/{repo}/git/refs", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating branch: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_branch_protection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get branch protection settings.
        
        Args:
            params: Branch protection parameters
            
        Returns:
            Branch protection settings
        """
        owner = params.get("owner")
        repo = params.get("repo")
        branch = params.get("branch")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/branches/{branch}/protection")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting branch protection: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_update_branch_protection(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update branch protection settings.
        
        Args:
            params: Branch protection update parameters
            
        Returns:
            Updated branch protection settings
        """
        owner = params.get("owner")
        repo = params.get("repo")
        branch = params.get("branch")
        
        # Extract protection parameters
        required_status_checks = params.get("required_status_checks")
        enforce_admins = params.get("enforce_admins", False)
        required_pull_request_reviews = params.get("required_pull_request_reviews")
        restrictions = params.get("restrictions")
        
        # Prepare request body
        body = {
            "required_status_checks": required_status_checks,
            "enforce_admins": enforce_admins,
            "required_pull_request_reviews": required_pull_request_reviews,
            "restrictions": restrictions
        }
        
        try:
            response = await self.client.put(f"/repos/{owner}/{repo}/branches/{branch}/protection", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error updating branch protection: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # File Operations
    # -------------------------
    
    async def _operation_get_file_content(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get file content from a repository.
        
        Args:
            params: File content parameters
            
        Returns:
            File content and metadata
        """
        owner = params.get("owner")
        repo = params.get("repo")
        path = params.get("path")
        ref = params.get("ref")
        
        # Prepare query parameters
        query_params = {}
        if ref:
            query_params["ref"] = ref
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/contents/{path}", params=query_params)
            result = await self._format_response(response)
            
            # If successful, decode the content for convenience
            if result["status"] == "success" and result["result"] and "content" in result["result"]:
                try:
                    # If result is a list, it's a directory listing
                    if isinstance(result["result"], list):
                        pass  # Keep as is for directory listings
                    else:
                        # For files, decode base64 content
                        encoded_content = result["result"]["content"]
                        decoded_content = base64.b64decode(encoded_content.replace('\n', '')).decode('utf-8')
                        result["result"]["decoded_content"] = decoded_content
                except Exception as decode_error:
                    # If decoding fails, just include a note
                    result["result"]["decoded_content_error"] = str(decode_error)
            
            return result
        except Exception as e:
            error_message = f"Error getting file content: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_create_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a file in a repository.
        
        Args:
            params: File creation parameters
            
        Returns:
            File creation result
        """
        owner = params.get("owner")
        repo = params.get("repo")
        path = params.get("path")
        message = params.get("message")
        content = params.get("content")
        branch = params.get("branch")
        committer = params.get("committer")
        author = params.get("author")
        
        # Encode content to base64
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        # Prepare request body
        body = {
            "message": message,
            "content": encoded_content
        }
        
        # Add optional parameters
        if branch:
            body["branch"] = branch
        if committer:
            body["committer"] = committer
        if author:
            body["author"] = author
        
        try:
            response = await self.client.put(f"/repos/{owner}/{repo}/contents/{path}", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating file: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    async def _operation_update_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a file in a repository.
        
        Args:
            params: File update parameters
            
        Returns:
            File update result
        """
        owner = params.get("owner")
        repo = params.get("repo")
        path = params.get("path")
        message = params.get("message")
        content = params.get("content")
        sha = params.get("sha")
        branch = params.get("branch")
        committer = params.get("committer")
        author = params.get("author")
        
        # Encode content to base64
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        
        # Prepare request body
        body = {
            "message": message,
            "content": encoded_content,
            "sha": sha
        }
        
        # Add optional parameters
        if branch:
            body["branch"] = branch
        if committer:
            body["committer"] = committer
        if author:
            body["author"] = author
        
        try:
            response = await self.client.put(f"/repos/{owner}/{repo}/contents/{path}", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error updating file: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_delete_file(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a file from a repository.
        
        Args:
            params: File deletion parameters
            
        Returns:
            File deletion result
        """
        owner = params.get("owner")
        repo = params.get("repo")
        path = params.get("path")
        message = params.get("message")
        sha = params.get("sha")
        branch = params.get("branch")
        committer = params.get("committer")
        author = params.get("author")
        
        # Prepare request body
        body = {
            "message": message,
            "sha": sha
        }
        
        # Add optional parameters
        if branch:
            body["branch"] = branch
        if committer:
            body["committer"] = committer
        if author:
            body["author"] = author
        
        try:
            response = await self.client.delete(f"/repos/{owner}/{repo}/contents/{path}", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error deleting file: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Pull Request Operations
    # -------------------------
    
    async def _operation_create_pull_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new pull request.
        
        Args:
            params: Pull request creation parameters
            
        Returns:
            New pull request information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        title = params.get("title")
        head = params.get("head")
        base = params.get("base")
        body = params.get("body")
        draft = params.get("draft", False)
        maintainer_can_modify = params.get("maintainer_can_modify", True)
        
        # Prepare request body
        pr_body = {
            "title": title,
            "head": head,
            "base": base,
            "draft": draft,
            "maintainer_can_modify": maintainer_can_modify
        }
        
        # Add optional parameters
        if body:
            pr_body["body"] = body
        
        try:
            response = await self.client.post(f"/repos/{owner}/{repo}/pulls", json=pr_body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating pull request: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_pull_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get pull request information.
        
        Args:
            params: Pull request parameters
            
        Returns:
            Pull request information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        pull_number = params.get("pull_number")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/pulls/{pull_number}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting pull request: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_pull_requests(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List pull requests for a repository.
        
        Args:
            params: Pull request listing parameters
            
        Returns:
            List of pull requests
        """
        owner = params.get("owner")
        repo = params.get("repo")
        state = params.get("state", "open")
        head = params.get("head")
        base = params.get("base")
        sort = params.get("sort", "created")
        direction = params.get("direction", "desc")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "state": state,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page
        }
        
        # Add optional filters
        if head:
            query_params["head"] = head
        if base:
            query_params["base"] = base
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/pulls", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing pull requests: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_update_pull_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a pull request.
        
        Args:
            params: Pull request update parameters
            
        Returns:
            Updated pull request information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        pull_number = params.get("pull_number")
        title = params.get("title")
        body = params.get("body")
        state = params.get("state")
        base = params.get("base")
        maintainer_can_modify = params.get("maintainer_can_modify")
        
        # Prepare request body with only provided parameters
        pr_body = {}
        if title:
            pr_body["title"] = title
        if body is not None:
            pr_body["body"] = body
        if state:
            pr_body["state"] = state
        if base:
            pr_body["base"] = base
        if maintainer_can_modify is not None:
            pr_body["maintainer_can_modify"] = maintainer_can_modify
        
        try:
            response = await self.client.patch(f"/repos/{owner}/{repo}/pulls/{pull_number}", json=pr_body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error updating pull request: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_merge_pull_request(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Merge a pull request.
        
        Args:
            params: Pull request merge parameters
            
        Returns:
            Merge result
        """
        owner = params.get("owner")
        repo = params.get("repo")
        pull_number = params.get("pull_number")
        commit_title = params.get("commit_title")
        commit_message = params.get("commit_message")
        merge_method = params.get("merge_method", "merge")
        sha = params.get("sha")
        
        # Prepare request body
        body = {
            "merge_method": merge_method
        }
        
        # Add optional parameters
        if commit_title:
            body["commit_title"] = commit_title
        if commit_message:
            body["commit_message"] = commit_message
        if sha:
            body["sha"] = sha
        
        try:
            response = await self.client.put(f"/repos/{owner}/{repo}/pulls/{pull_number}/merge", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error merging pull request: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Issues Operations
    # -------------------------
    
    async def _operation_create_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new issue.
        
        Args:
            params: Issue creation parameters
            
        Returns:
            New issue information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        title = params.get("title")
        body = params.get("body")
        assignees = params.get("assignees")
        milestone = params.get("milestone")
        labels = params.get("labels")
        assignee = params.get("assignee")
        
        # Prepare request body
        issue_body = {
            "title": title
        }
        
        # Add optional parameters
        if body:
            issue_body["body"] = body
        if assignees:
            issue_body["assignees"] = assignees
        if milestone:
            issue_body["milestone"] = milestone
        if labels:
            issue_body["labels"] = labels
        if assignee:
            issue_body["assignee"] = assignee
        
        try:
            response = await self.client.post(f"/repos/{owner}/{repo}/issues", json=issue_body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating issue: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get issue information.
        
        Args:
            params: Issue parameters
            
        Returns:
            Issue information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        issue_number = params.get("issue_number")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/issues/{issue_number}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting issue: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_issues(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List issues for a repository.
        
        Args:
            params: Issue listing parameters
            
        Returns:
            List of issues
        """
        owner = params.get("owner")
        repo = params.get("repo")
        milestone = params.get("milestone")
        state = params.get("state", "open")
        assignee = params.get("assignee")
        creator = params.get("creator")
        mentioned = params.get("mentioned")
        labels = params.get("labels")
        sort = params.get("sort", "created")
        direction = params.get("direction", "desc")
        since = params.get("since")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "state": state,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page
        }
        
        # Add optional filters
        if milestone:
            query_params["milestone"] = milestone
        if assignee:
            query_params["assignee"] = assignee
        if creator:
            query_params["creator"] = creator
        if mentioned:
            query_params["mentioned"] = mentioned
        if labels:
            query_params["labels"] = ",".join(labels) if isinstance(labels, list) else labels
        if since:
            query_params["since"] = since
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/issues", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing issues: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_update_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an issue.
        
        Args:
            params: Issue update parameters
            
        Returns:
            Updated issue information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        issue_number = params.get("issue_number")
        title = params.get("title")
        body = params.get("body")
        state = params.get("state")
        milestone = params.get("milestone")
        labels = params.get("labels")
        assignees = params.get("assignees")
        assignee = params.get("assignee")
        
        # Prepare request body with only provided parameters
        issue_body = {}
        if title:
            issue_body["title"] = title
        if body is not None:
            issue_body["body"] = body
        if state:
            issue_body["state"] = state
        if milestone is not None:
            issue_body["milestone"] = milestone
        if labels is not None:
            issue_body["labels"] = labels
        if assignees is not None:
            issue_body["assignees"] = assignees
        if assignee is not None:
            issue_body["assignee"] = assignee
        
        try:
            response = await self.client.patch(f"/repos/{owner}/{repo}/issues/{issue_number}", json=issue_body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error updating issue: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_close_issue(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Close an issue.
        
        Args:
            params: Issue closure parameters
            
        Returns:
            Closed issue information
        """
        # This is a special case of update_issue with state=closed
        params["state"] = "closed"
        return await self._operation_update_issue(params)
    
    # -------------------------
    # Comments Operations
    # -------------------------
    
    async def _operation_create_comment(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a comment on an issue or pull request.
        
        Args:
            params: Comment creation parameters
            
        Returns:
            New comment information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        issue_number = params.get("issue_number")
        body = params.get("body")
        
        # Prepare request body
        comment_body = {
            "body": body
        }
        
        try:
            response = await self.client.post(f"/repos/{owner}/{repo}/issues/{issue_number}/comments", json=comment_body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating comment: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_comments(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List comments on an issue or pull request.
        
        Args:
            params: Comment listing parameters
            
        Returns:
            List of comments
        """
        owner = params.get("owner")
        repo = params.get("repo")
        issue_number = params.get("issue_number")
        since = params.get("since")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        if since:
            query_params["since"] = since
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/issues/{issue_number}/comments", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing comments: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    # -------------------------
    # Commit Operations
    # -------------------------
    
    async def _operation_get_commit(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a commit.
        
        Args:
            params: Commit parameters
            
        Returns:
            Commit information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        sha = params.get("sha")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/commits/{sha}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting commit: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_commits(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List commits for a repository.
        
        Args:
            params: Commit listing parameters
            
        Returns:
            List of commits
        """
        owner = params.get("owner")
        repo = params.get("repo")
        sha = params.get("sha")
        path = params.get("path")
        author = params.get("author")
        since = params.get("since")
        until = params.get("until")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        # Add optional filters
        if sha:
            query_params["sha"] = sha
        if path:
            query_params["path"] = path
        if author:
            query_params["author"] = author
        if since:
            query_params["since"] = since
        if until:
            query_params["until"] = until
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/commits", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing commits: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Releases Operations
    # -------------------------
    
    async def _operation_create_release(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new release.
        
        Args:
            params: Release creation parameters
            
        Returns:
            New release information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        tag_name = params.get("tag_name")
        target_commitish = params.get("target_commitish")
        name = params.get("name")
        body = params.get("body")
        draft = params.get("draft", False)
        prerelease = params.get("prerelease", False)
        
        # Prepare request body
        release_body = {
            "tag_name": tag_name,
            "draft": draft,
            "prerelease": prerelease
        }
        
        # Add optional parameters
        if target_commitish:
            release_body["target_commitish"] = target_commitish
        if name:
            release_body["name"] = name
        if body:
            release_body["body"] = body
        
        try:
            response = await self.client.post(f"/repos/{owner}/{repo}/releases", json=release_body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating release: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_release(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get release information.
        
        Args:
            params: Release parameters
            
        Returns:
            Release information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        release_id = params.get("release_id")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/releases/{release_id}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting release: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_releases(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List releases for a repository.
        
        Args:
            params: Release listing parameters
            
        Returns:
            List of releases
        """
        owner = params.get("owner")
        repo = params.get("repo")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/releases", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing releases: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_update_release(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a release.
        
        Args:
            params: Release update parameters
            
        Returns:
            Updated release information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        release_id = params.get("release_id")
        tag_name = params.get("tag_name")
        target_commitish = params.get("target_commitish")
        name = params.get("name")
        body = params.get("body")
        draft = params.get("draft")
        prerelease = params.get("prerelease")
        
        # Prepare request body with only provided parameters
        release_body = {}
        if tag_name:
            release_body["tag_name"] = tag_name
        if target_commitish:
            release_body["target_commitish"] = target_commitish
        if name:
            release_body["name"] = name
        if body is not None:
            release_body["body"] = body
        if draft is not None:
            release_body["draft"] = draft
        if prerelease is not None:
            release_body["prerelease"] = prerelease
        
        try:
            response = await self.client.patch(f"/repos/{owner}/{repo}/releases/{release_id}", json=release_body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error updating release: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_delete_release(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a release.
        
        Args:
            params: Release deletion parameters
            
        Returns:
            Status of deletion operation
        """
        owner = params.get("owner")
        repo = params.get("repo")
        release_id = params.get("release_id")
        
        try:
            response = await self.client.delete(f"/repos/{owner}/{repo}/releases/{release_id}")
            
            # Special handling for successful deletion (204 No Content)
            if response.status_code == 204:
                rate_limit = await self._extract_rate_limit(response)
                return {
                    "status": "success",
                    "result": {"message": "Release deleted successfully"},
                    "error": None,
                    "headers": dict(response.headers),
                    "rate_limit": rate_limit
                }
            
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error deleting release: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # User Operations
    # -------------------------
    
    async def _operation_get_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a user.
        
        Args:
            params: User parameters
            
        Returns:
            User information
        """
        username = params.get("username_to_get")
        
        try:
            response = await self.client.get(f"/users/{username}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting user: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_authenticated_user(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about the authenticated user.
        
        Args:
            params: Not used
            
        Returns:
            Authenticated user information
        """
        try:
            response = await self.client.get("/user")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting authenticated user: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_user_repos(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List repositories for a user.
        
        Args:
            params: User repository listing parameters
            
        Returns:
            List of user repositories
        """
        username = params.get("username_to_list")
        repo_type = params.get("type", "owner")
        sort = params.get("sort", "updated")
        direction = params.get("direction", "desc")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "type": repo_type,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get(f"/users/{username}/repos", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing user repositories: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Webhooks Operations
    # -------------------------
    
    async def _operation_create_webhook(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a webhook for a repository.
        
        Args:
            params: Webhook creation parameters
            
        Returns:
            New webhook information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        hook_config = params.get("hook_config")
        events = params.get("events", ["push"])
        active = params.get("active", True)
        
        # Prepare request body
        body = {
            "config": hook_config,
            "events": events,
            "active": active
        }
        
        try:
            response = await self.client.post(f"/repos/{owner}/{repo}/hooks", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating webhook: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_webhooks(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List webhooks for a repository.
        
        Args:
            params: Webhook listing parameters
            
        Returns:
            List of webhooks
        """
        owner = params.get("owner")
        repo = params.get("repo")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/hooks", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing webhooks: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_delete_webhook(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a webhook.
        
        Args:
            params: Webhook deletion parameters
            
        Returns:
            Status of deletion operation
        """
        owner = params.get("owner")
        repo = params.get("repo")
        hook_id = params.get("hook_id")
        
        try:
            response = await self.client.delete(f"/repos/{owner}/{repo}/hooks/{hook_id}")
            
            # Special handling for successful deletion (204 No Content)
            if response.status_code == 204:
                rate_limit = await self._extract_rate_limit(response)
                return {
                    "status": "success",
                    "result": {"message": "Webhook deleted successfully"},
                    "error": None,
                    "headers": dict(response.headers),
                    "rate_limit": rate_limit
                }
            
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error deleting webhook: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Organization Operations
    # -------------------------
    
    async def _operation_get_organization(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about an organization.
        
        Args:
            params: Organization parameters
            
        Returns:
            Organization information
        """
        org = params.get("org")
        
        try:
            response = await self.client.get(f"/orgs/{org}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting organization: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_organization_repos(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List repositories for an organization.
        
        Args:
            params: Organization repository listing parameters
            
        Returns:
            List of organization repositories
        """
        org = params.get("org")
        repo_type = params.get("type", "all")
        sort = params.get("sort", "updated")
        direction = params.get("direction", "desc")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "type": repo_type,
            "sort": sort,
            "direction": direction,
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get(f"/orgs/{org}/repos", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing organization repositories: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_organization_members(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List members of an organization.
        
        Args:
            params: Organization members listing parameters
            
        Returns:
            List of organization members
        """
        org = params.get("org")
        filter_param = params.get("filter", "all")
        role = params.get("role", "all")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "filter": filter_param,
            "role": role,
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get(f"/orgs/{org}/members", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing organization members: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Teams Operations
    # -------------------------
    
    async def _operation_get_team(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a team.
        
        Args:
            params: Team parameters
            
        Returns:
            Team information
        """
        org = params.get("org")
        team_slug = params.get("team_slug")
        
        try:
            response = await self.client.get(f"/orgs/{org}/teams/{team_slug}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting team: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_teams(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List teams for an organization.
        
        Args:
            params: Team listing parameters
            
        Returns:
            List of teams
        """
        org = params.get("org")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get(f"/orgs/{org}/teams", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing teams: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_create_team(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a team in an organization.
        
        Args:
            params: Team creation parameters
            
        Returns:
            New team information
        """
        org = params.get("org")
        name = params.get("name")
        description = params.get("description")
        maintainers = params.get("maintainers")
        repo_names = params.get("repo_names")
        privacy = params.get("privacy", "secret")
        permission = params.get("permission", "pull")
        
        # Prepare request body
        body = {
            "name": name,
            "privacy": privacy,
            "permission": permission
        }
        
        # Add optional parameters
        if description:
            body["description"] = description
        if maintainers:
            body["maintainers"] = maintainers
        if repo_names:
            body["repo_names"] = repo_names
        
        try:
            response = await self.client.post(f"/orgs/{org}/teams", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating team: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # GitHub Actions Operations
    # -------------------------
    
    async def _operation_list_workflows(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List workflows for a repository.
        
        Args:
            params: Workflow listing parameters
            
        Returns:
            List of workflows
        """
        owner = params.get("owner")
        repo = params.get("repo")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/actions/workflows", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing workflows: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a workflow.
        
        Args:
            params: Workflow parameters
            
        Returns:
            Workflow information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        workflow_id = params.get("workflow_id")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting workflow: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_trigger_workflow(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Trigger a workflow run.
        
        Args:
            params: Workflow dispatch parameters
            
        Returns:
            Workflow dispatch result
        """
        owner = params.get("owner")
        repo = params.get("repo")
        workflow_id = params.get("workflow_id")
        ref = params.get("ref")
        inputs = params.get("inputs")
        
        # Prepare request body
        body = {
            "ref": ref
        }
        
        # Add optional parameters
        if inputs:
            body["inputs"] = inputs
        
        try:
            response = await self.client.post(f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/dispatches", json=body)
            
            # Special handling for successful dispatch (204 No Content)
            if response.status_code == 204:
                rate_limit = await self._extract_rate_limit(response)
                return {
                    "status": "success",
                    "result": {"message": "Workflow triggered successfully"},
                    "error": None,
                    "headers": dict(response.headers),
                    "rate_limit": rate_limit
                }
            
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error triggering workflow: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_workflow_runs(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List runs for a workflow.
        
        Args:
            params: Workflow run listing parameters
            
        Returns:
            List of workflow runs
        """
        owner = params.get("owner")
        repo = params.get("repo")
        workflow_id = params.get("workflow_id")
        actor = params.get("actor")
        branch = params.get("branch")
        event = params.get("event")
        status = params.get("status")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        # Add optional filters
        if actor:
            query_params["actor"] = actor
        if branch:
            query_params["branch"] = branch
        if event:
            query_params["event"] = event
        if status:
            query_params["status"] = status
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/actions/workflows/{workflow_id}/runs", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing workflow runs: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_workflow_run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a workflow run.
        
        Args:
            params: Workflow run parameters
            
        Returns:
            Workflow run information
        """
        owner = params.get("owner")
        repo = params.get("repo")
        run_id = params.get("run_id")
        
        try:
            response = await self.client.get(f"/repos/{owner}/{repo}/actions/runs/{run_id}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting workflow run: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    # -------------------------
    # Gist Operations
    # -------------------------
    
    async def _operation_create_gist(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a gist.
        
        Args:
            params: Gist creation parameters
            
        Returns:
            New gist information
        """
        files = params.get("files")
        description = params.get("description")
        public = params.get("public", True)
        
        # Prepare request body
        body = {
            "files": files,
            "public": public
        }
        
        # Add optional parameters
        if description:
            body["description"] = description
        
        try:
            response = await self.client.post("/gists", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error creating gist: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_get_gist(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get information about a gist.
        
        Args:
            params: Gist parameters
            
        Returns:
            Gist information
        """
        gist_id = params.get("gist_id")
        
        try:
            response = await self.client.get(f"/gists/{gist_id}")
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error getting gist: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_list_gists(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        List gists for the authenticated user.
        
        Args:
            params: Gist listing parameters
            
        Returns:
            List of gists
        """
        since = params.get("since")
        per_page = params.get("per_page", 30)
        page = params.get("page", 1)
        
        # Prepare query parameters
        query_params = {
            "per_page": per_page,
            "page": page
        }
        
        if since:
            query_params["since"] = since
        
        try:
            response = await self.client.get("/gists", params=query_params)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error listing gists: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_update_gist(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update a gist.
        
        Args:
            params: Gist update parameters
            
        Returns:
            Updated gist information
        """
        gist_id = params.get("gist_id")
        files = params.get("files")
        description = params.get("description")
        
        # Prepare request body with only provided parameters
        body = {}
        if files:
            body["files"] = files
        if description is not None:
            body["description"] = description
        
        try:
            response = await self.client.patch(f"/gists/{gist_id}", json=body)
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error updating gist: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }
    
    async def _operation_delete_gist(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a gist.
        
        Args:
            params: Gist deletion parameters
            
        Returns:
            Status of deletion operation
        """
        gist_id = params.get("gist_id")
        
        try:
            response = await self.client.delete(f"/gists/{gist_id}")
            
            # Special handling for successful deletion (204 No Content)
            if response.status_code == 204:
                rate_limit = await self._extract_rate_limit(response)
                return {
                    "status": "success",
                    "result": {"message": "Gist deleted successfully"},
                    "error": None,
                    "headers": dict(response.headers),
                    "rate_limit": rate_limit
                }
            
            return await self._format_response(response)
        except Exception as e:
            error_message = f"Error deleting gist: {str(e)}"
            logger.error(error_message)
            return {
                "status": "error",
                "result": None,
                "error": error_message,
                "headers": {},
                "rate_limit": {}
            }

# Register with NodeRegistry
try:
    from base_node import NodeRegistry
    NodeRegistry.register("github", GitHubNode)
    logger.info("Registered node type: github")
except Exception as e:
    logger.error(f"Error registering GitHub node: {str(e)}")