#!/usr/bin/env python3
"""
Test suite for GitHub Node with improved pull request handling
"""

import logging
import asyncio
import os
import time
import json
from typing import Dict, Any, List

# Import the GitHub Node
from GitHubNode import GitHubNode, GitHubOperation

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test repository settings - will be created and used for all tests
TEST_REPO_NAME = "node-test-repo"
TEST_REPO_DESCRIPTION = "Test repository for GitHub Node"

async def run_tests():
    """Run test suite for GitHub node."""
    print("=== GitHub Node Test Suite ===")
    
    # Get GitHub token from environment or user input
    github_token = os.environ.get("GITHUB_TOKEN")
    if not github_token:
        github_token = input("Enter GitHub Personal Access Token: ")
        if not github_token:
            print("GitHub token is required for testing")
            return
    
    # Get GitHub username for tests
    github_username = os.environ.get("GITHUB_USERNAME")
    if not github_username:
        github_username = input("Enter your GitHub username: ")
        if not github_username:
            print("GitHub username is required for testing")
            return
    
    # Create an instance of the GitHub Node
    node = GitHubNode()
    
    # Track created resources for cleanup
    created_repo = None
    created_gist_id = None
    
    # Test cases - organized by category
    repository_tests = [
        {
            "name": "Create Repository",
            "params": {
                "operation": GitHubOperation.CREATE_REPO,
                "auth_type": "token",
                "token": github_token,
                "name": TEST_REPO_NAME,
                "description": TEST_REPO_DESCRIPTION,
                "private": True,
                "auto_init": True
            },
            "expected_status": "success",
            "save_result_key": "created_repo"  # Save full repo info for later cleanup
        },
        {
            "name": "Get Repository",
            "params": {
                "operation": GitHubOperation.GET_REPO,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME
            },
            "expected_status": "success",
            "save_result_key": "repo_details"  # Save repo details including default branch
        },
        {
            "name": "Update Repository",
            "params": {
                "operation": GitHubOperation.UPDATE_REPO,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "description": f"{TEST_REPO_DESCRIPTION} - Updated"
            },
            "expected_status": "success"
        },
        {
            "name": "List Repositories",
            "params": {
                "operation": GitHubOperation.LIST_REPOS,
                "auth_type": "token",
                "token": github_token
            },
            "expected_status": "success"
        }
    ]
    
    branch_and_file_setup = [
        {
            "name": "Get Default Branch Commit",
            "params": {
                "operation": GitHubOperation.LIST_COMMITS,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME
            },
            "expected_status": "success",
            "save_result_key": "default_branch_commits"  # Save for branch creation test
        },
        {
            "name": "Create Test Branch",
            "params": {
                "operation": GitHubOperation.CREATE_BRANCH,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "branch_name": "test-branch",
                "sha": "{default_branch_sha}"  # Will be replaced with actual SHA
            },
            "expected_status": "success"
        },
        {
            "name": "Create File on Main Branch",
            "params": {
                "operation": GitHubOperation.CREATE_FILE,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "path": "main-branch-file.md",
                "message": "Create file on main branch",
                "content": "# Main Branch File\nThis file was created on the main branch."
            },
            "expected_status": "success"
        },
        {
            "name": "Create File on Test Branch",
            "params": {
                "operation": GitHubOperation.CREATE_FILE,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "path": "test-branch-file.md",
                "message": "Create file on test branch",
                "content": "# Test Branch File\nThis file was created on the test branch.",
                "branch": "test-branch"
            },
            "expected_status": "success",
            "save_result_key": "test_branch_file"  # Save for PR testing
        }
    ]
    
    pull_request_tests = [
        {
            "name": "Create Pull Request",
            "params": {
                "operation": GitHubOperation.CREATE_PULL_REQUEST,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "title": "Test Pull Request",
                "body": "This is a test pull request created by the GitHub Node test suite.",
                "head": "test-branch",
                "base": "{default_branch_name}"  # Will be replaced with actual default branch
            },
            "expected_status": "success",
            "save_result_key": "created_pr"  # Save for update and merge tests
        },
        {
            "name": "Get Pull Request",
            "params": {
                "operation": GitHubOperation.GET_PULL_REQUEST,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "pull_number": "{pr_number}"  # Will be replaced with actual PR number
            },
            "expected_status": "success"
        },
        {
            "name": "Update Pull Request",
            "params": {
                "operation": GitHubOperation.UPDATE_PULL_REQUEST,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "pull_number": "{pr_number}",  # Will be replaced with actual PR number
                "title": "Updated Test Pull Request"
            },
            "expected_status": "success"
        },
        {
            "name": "Merge Pull Request",
            "params": {
                "operation": GitHubOperation.MERGE_PULL_REQUEST,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "pull_number": "{pr_number}",  # Will be replaced with actual PR number
                "commit_title": "Merge test pull request"
            },
            "expected_status": "success"
        }
    ]
    
    issue_tests = [
        {
            "name": "Create Issue",
            "params": {
                "operation": GitHubOperation.CREATE_ISSUE,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "title": "Test Issue",
                "body": "This is a test issue created by the GitHub Node test suite."
            },
            "expected_status": "success",
            "save_result_key": "created_issue"  # Save for comment and update tests
        },
        {
            "name": "Get Issue",
            "params": {
                "operation": GitHubOperation.GET_ISSUE,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "issue_number": "{issue_number}"  # Will be replaced with actual issue number
            },
            "expected_status": "success"
        },
        {
            "name": "Create Comment",
            "params": {
                "operation": GitHubOperation.CREATE_COMMENT,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "issue_number": "{issue_number}",  # Will be replaced with actual issue number
                "body": "This is a test comment created by the GitHub Node test suite."
            },
            "expected_status": "success"
        },
        {
            "name": "List Comments",
            "params": {
                "operation": GitHubOperation.LIST_COMMENTS,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "issue_number": "{issue_number}"  # Will be replaced with actual issue number
            },
            "expected_status": "success"
        },
        {
            "name": "Update Issue",
            "params": {
                "operation": GitHubOperation.UPDATE_ISSUE,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "issue_number": "{issue_number}",  # Will be replaced with actual issue number
                "title": "Updated Test Issue"
            },
            "expected_status": "success"
        },
        {
            "name": "Close Issue",
            "params": {
                "operation": GitHubOperation.CLOSE_ISSUE,
                "auth_type": "token",
                "token": github_token,
                "owner": github_username,
                "repo": TEST_REPO_NAME,
                "issue_number": "{issue_number}"  # Will be replaced with actual issue number
            },
            "expected_status": "success"
        }
    ]
    
    gist_tests = [
        {
            "name": "Create Gist",
            "params": {
                "operation": GitHubOperation.CREATE_GIST,
                "auth_type": "token",
                "token": github_token,
                "files": {
                    "test-file.md": {
                        "content": "# Test Gist\nThis is a test gist created by the GitHub Node test suite."
                    }
                },
                "description": "Test Gist",
                "public": False
            },
            "expected_status": "success",
            "save_result_key": "created_gist"  # Save for update and delete tests
        },
        {
            "name": "Get Gist",
            "params": {
                "operation": GitHubOperation.GET_GIST,
                "auth_type": "token",
                "token": github_token,
                "gist_id": "{gist_id}"  # Will be replaced with actual gist ID
            },
            "expected_status": "success"
        },
        {
            "name": "Update Gist",
            "params": {
                "operation": GitHubOperation.UPDATE_GIST,
                "auth_type": "token",
                "token": github_token,
                "gist_id": "{gist_id}",  # Will be replaced with actual gist ID
                "files": {
                    "test-file.md": {
                        "content": "# Updated Test Gist\nThis gist was updated by the GitHub Node test suite."
                    }
                },
                "description": "Updated Test Gist"
            },
            "expected_status": "success"
        },
        {
            "name": "List Gists",
            "params": {
                "operation": GitHubOperation.LIST_GISTS,
                "auth_type": "token",
                "token": github_token
            },
            "expected_status": "success"
        }
    ]
    
    # Combine all test categories
    all_tests = (
        repository_tests +
        branch_and_file_setup +
        pull_request_tests +
        issue_tests +
        gist_tests
    )
    
    # Run all test cases with a delay between tests
    total_tests = len(all_tests)
    passed_tests = 0
    saved_values = {}
    
    print(f"\nRunning {total_tests} tests across all GitHub API categories...")
    
    for idx, test_case in enumerate(all_tests):
        test_name = test_case["name"]
        test_category = test_name.split()[0].lower()
        
        print(f"\nRunning test {idx+1}/{total_tests}: {test_name}")
        
        try:
            # Replace placeholders in params with saved values
            params = test_case["params"].copy()
            
            # Special handling for certain tests that need data from previous tests
            if test_name == "Create Test Branch" and "default_branch_commits" in saved_values:
                # Extract SHA from the first commit
                commits = saved_values["default_branch_commits"]
                if commits and len(commits) > 0:
                    default_branch_sha = commits[0].get("sha")
                    if default_branch_sha:
                        params["sha"] = default_branch_sha
            
            # Get default branch name from repo details
            if "repo_details" in saved_values:
                default_branch_name = saved_values["repo_details"].get("default_branch", "main")
                # Replace placeholder in any parameter
                for key, value in params.items():
                    if isinstance(value, str) and value == "{default_branch_name}":
                        params[key] = default_branch_name
            
            # Replace placeholders in parameter values
            for key, value in params.items():
                if isinstance(value, str) and value.startswith("{") and value.endswith("}"):
                    placeholder = value[1:-1]
                    if placeholder == "issue_number" and "created_issue" in saved_values:
                        params[key] = saved_values["created_issue"].get("number")
                    elif placeholder == "pr_number" and "created_pr" in saved_values:
                        params[key] = saved_values["created_pr"].get("number")
                    elif placeholder == "release_id" and "created_release" in saved_values:
                        params[key] = saved_values["created_release"].get("id")
                    elif placeholder == "gist_id" and "created_gist" in saved_values:
                        params[key] = saved_values["created_gist"].get("id")
                    elif placeholder in saved_values:
                        params[key] = saved_values[placeholder]
            
            # Prepare node data
            node_data = {
                "params": params
            }
            
            # Execute the node
            result = await node.execute(node_data)
            
            # Check if the result status matches expected status
            if result["status"] == test_case["expected_status"]:
                print(f"✅ PASS: {test_name}")
                
                # Save result value if specified
                if "save_result_key" in test_case and result["result"]:
                    key = test_case["save_result_key"]
                    saved_values[key] = result["result"]
                    
                    # Save specific values for cleanup
                    if key == "created_repo":
                        created_repo = result["result"]
                    elif key == "created_gist":
                        created_gist_id = result["result"].get("id")
                    
                    print(f"   Saved result as '{key}'")
                    
                    # Print important information for debugging
                    if key == "created_pr":
                        print(f"   Created PR #{result['result'].get('number')} from {params['head']} to {params['base']}")
                
                # Show rate limit info
                if result.get("rate_limit"):
                    remaining = result["rate_limit"].get("remaining", "unknown")
                    limit = result["rate_limit"].get("limit", "unknown")
                    print(f"   Rate limit: {remaining}/{limit} remaining")
                
                passed_tests += 1
            else:
                print(f"❌ FAIL: {test_name}")
                print(f"   Expected status '{test_case['expected_status']}', got '{result['status']}'")
                print(f"   Error: {result.get('error')}")
                
                # Print response details for debugging
                print(f"   Response body: {str(result.get('result'))[:300]}")
                
            # Add a delay between tests to avoid rate limiting
            await asyncio.sleep(1.0)
            
        except Exception as e:
            print(f"❌ FAIL: {test_name}")
            print(f"   Exception: {str(e)}")
    
    # Add cleanup tests for gists
    cleanup_tests = []
    
    # Only add gist deletion if we created a gist
    if created_gist_id:
        cleanup_tests.append({
            "name": "Delete Gist",
            "params": {
                "operation": GitHubOperation.DELETE_GIST,
                "auth_type": "token",
                "token": github_token,
                "gist_id": created_gist_id
            },
            "expected_status": "success"
        })
    
    # Run cleanup tests
    cleanup_total = len(cleanup_tests)
    cleanup_passed = 0
    
    if cleanup_tests:
        print("\n=== Running Cleanup Tests ===")
        
        for idx, test_case in enumerate(cleanup_tests):
            print(f"\nRunning cleanup test {idx+1}/{cleanup_total}: {test_case['name']}")
            
            try:
                # Prepare node data
                node_data = {
                    "params": test_case["params"]
                }
                
                # Execute the node
                result = await node.execute(node_data)
                
                # Check if the result status matches expected status
                if result["status"] == test_case["expected_status"]:
                    print(f"✅ PASS: {test_case['name']}")
                    cleanup_passed += 1
                else:
                    print(f"❌ FAIL: {test_case['name']}")
                    print(f"   Expected status '{test_case['expected_status']}', got '{result['status']}'")
                    print(f"   Error: {result.get('error')}")
                
                # Add a delay between tests
                await asyncio.sleep(1.0)
                
            except Exception as e:
                print(f"❌ FAIL: {test_case['name']}")
                print(f"   Exception: {str(e)}")
    
    # Print summary
    print(f"\n=== Test Summary ===")
    print(f"Total tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success rate: {passed_tests / total_tests * 100:.1f}%")
    
    if cleanup_tests:
        print(f"\nCleanup tests: {cleanup_total}")
        print(f"Passed: {cleanup_passed}")
        print(f"Failed: {cleanup_total - cleanup_passed}")
    
    # Final repository cleanup
    cleanup_repo = input("\nDelete test repository? (y/n): ").lower() == 'y'
    if cleanup_repo and created_repo:
        try:
            print(f"Deleting test repository: {github_username}/{TEST_REPO_NAME}")
            delete_result = await node.execute({
                "params": {
                    "operation": GitHubOperation.DELETE_REPO,
                    "auth_type": "token",
                    "token": github_token,
                    "owner": github_username,
                    "repo": TEST_REPO_NAME
                }
            })
            
            if delete_result["status"] == "success":
                print("✅ Repository deleted successfully")
            else:
                print(f"❌ Failed to delete repository: {delete_result.get('error')}")
        except Exception as e:
            print(f"❌ Failed to delete repository: {str(e)}")
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    # Run the async tests
    asyncio.run(run_tests())