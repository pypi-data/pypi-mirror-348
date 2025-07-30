import os
import subprocess
from typing import Optional
from urllib.parse import urlparse

class GitPushError(Exception):
    """Custom exception for Git operations"""
    pass

def push(
    username: str,
    email: str,
    repo_url: str,
    local_path: str,
    commit_message: str,
    branch_name: str = "main"
) -> None:
    """
    Push local directory contents to a Git repository.
    
    Args:
        username (str): Git username for configuration
        email (str): Git email for configuration
        repo_url (str): URL of the public repository
        local_path (str): Path to the local directory to push
        commit_message (str): Commit message for the push
        branch_name (str, optional): Branch name to push to. Defaults to "main".
    
    Raises:
        GitPushError: If any Git operation fails
        ValueError: If inputs are invalid
    """
    try:
        # Validate inputs
        if not all([username, email, repo_url, local_path, commit_message]):
            raise ValueError("All arguments except branch_name are required")
        
        if not os.path.exists(local_path):
            raise ValueError(f"Local path does not exist: {local_path}")
        
        # Parse repository URL
        parsed_url = urlparse(repo_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise ValueError("Invalid repository URL")
        
        # Change to the local directory
        os.chdir(local_path)
        
        # Configure Git
        subprocess.run(["git", "config", "--local", "user.name", username], check=True)
        subprocess.run(["git", "config", "--local", "user.email", email], check=True)
        
        # Initialize repository if not already initialized
        if not os.path.exists(".git"):
            subprocess.run(["git", "init"], check=True)
            subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
        
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        
        # Check if there are any changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            print("No changes to commit")
            return
        
        # Commit changes
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        
        # Check if branch exists
        branch_check = subprocess.run(
            ["git", "branch", "-a"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # Create and switch to branch if it doesn't exist
        if branch_name not in branch_check.stdout:
            subprocess.run(["git", "checkout", "-b", branch_name], check=True)
        else:
            subprocess.run(["git", "checkout", branch_name], check=True)
        
        # Push to remote
        subprocess.run(["git", "push", "-u", "origin", branch_name], check=True)
        print(f"Successfully pushed to {branch_name} branch")
        
    except subprocess.CalledProcessError as e:
        raise GitPushError(f"Git operation failed: {str(e)}")
    except Exception as e:
        raise GitPushError(f"An error occurred: {str(e)}")
    finally:
        # Reset Git config to global if it was set locally
        try:
            subprocess.run(["git", "config", "--local", "--unset", "user.name"], check=False)
            subprocess.run(["git", "config", "--local", "--unset", "user.email"], check=False)
        except:
            pass 