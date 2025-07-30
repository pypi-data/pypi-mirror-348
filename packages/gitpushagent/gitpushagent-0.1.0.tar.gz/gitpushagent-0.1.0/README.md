# GitPushAgent

A simple Python package that automates Git push operations with a single function call. Perfect for automating Git workflows and CI/CD pipelines.

## Features

- Simple one-function interface
- Automatic Git configuration
- Branch management (create/switch)
- Repository initialization
- Error handling
- Local Git config management

## Installation

You can install GitPushAgent using pip:

```bash
pip install gitpushagent
```

## Usage

### Basic Usage

```python
from gitpushagent import push

# Push to main branch
push(
    username="your-username",
    email="your.email@example.com",
    repo_url="https://github.com/username/repo.git",
    local_path="/path/to/your/local/directory",
    commit_message="Your commit message"
)
```

### Using a Different Branch

```python
from gitpushagent import push

# Push to a specific branch
push(
    username="your-username",
    email="your.email@example.com",
    repo_url="https://github.com/username/repo.git",
    local_path="/path/to/your/local/directory",
    commit_message="Your commit message",
    branch_name="feature-branch"  # Optional, defaults to "main"
)
```

### Error Handling

```python
from gitpushagent import push, GitPushError

try:
    push(
        username="your-username",
        email="your.email@example.com",
        repo_url="https://github.com/username/repo.git",
        local_path="/path/to/your/local/directory",
        commit_message="Your commit message"
    )
except GitPushError as e:
    print(f"An error occurred: {e}")
except ValueError as e:
    print(f"Invalid input: {e}")
```

## Parameters

- `username` (str): Your Git username
- `email` (str): Your Git email
- `repo_url` (str): URL of the public repository
- `local_path` (str): Path to the local directory you want to push
- `commit_message` (str): Your commit message
- `branch_name` (str, optional): Branch name to push to (defaults to "main")

## Features in Detail

1. **Automatic Git Configuration**: Sets up Git user name and email locally for the operation
2. **Repository Management**: 
   - Initializes Git repository if not already initialized
   - Adds remote origin if not present
3. **Branch Handling**:
   - Creates new branch if it doesn't exist
   - Switches to existing branch if it exists
4. **Smart Push**:
   - Only commits if there are changes
   - Pushes to the specified branch
5. **Error Handling**:
   - Validates all inputs
   - Provides clear error messages
   - Cleans up local Git config after operation

## Requirements

- Python 3.7 or higher
- Git installed on your system

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 