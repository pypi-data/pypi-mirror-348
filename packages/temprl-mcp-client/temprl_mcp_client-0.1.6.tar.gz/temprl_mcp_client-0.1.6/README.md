# Temprl MCP Client

A flexible Python library and CLI tool for interacting with Model Context Protocol (MCP) servers using any LLM model.


## Overview

Temprl MCP Client is both a Python library and a command-line tool that allows you to query and interact with MCP servers through natural language. It connects to any number of configured MCP servers, makes their tools available to language models (OpenAI, Anthropic, Ollama, LMStudio), and provides a conversational interface for accessing and manipulating data from these servers.

The project demonstrates how to:
- Connect to multiple MCP servers simultaneously
- List and call tools provided by these servers
- Use function calling capabilities to interact with external data sources
- Process and present results in a user-friendly way
- Create a reusable Python library with a clean API
- Build a command-line interface on top of the library

## Features

- **Multiple Provider Support**: Works with OpenAI, Anthropic, Ollama, and LMStudio models
- **Modular Architecture**: Clean separation of concerns with provider-specific modules
- **Dual Interface**: Use as a Python library or command-line tool
- **MCP Server Integration**: Connect to any number of MCP servers simultaneously
- **Tool Discovery**: Automatically discover and use tools provided by MCP servers
- **Flexible Configuration**: Configure models and servers through JSON configuration
- **Environment Variable Support**: Securely store API keys in environment variables
- **Comprehensive Documentation**: Detailed usage examples and API documentation
- **Installable Package**: Easy installation via pip with `temprl-mcp-client` command

## Prerequisites

Before installing Temprl MCP Client, ensure you have the following prerequisites installed:

1. **Python 3.8+**
2. **SQLite** - A lightweight database used by the demo
3. **uv/uvx** - A fast Python package installer and resolver

### Setting up Prerequisites

#### Windows

1. **Python 3.8+**:
   - Download and install from [python.org](https://www.python.org/downloads/windows/)
   - Ensure you check "Add Python to PATH" during installation

2. **SQLite**:
   - Download the precompiled binaries from [SQLite website](https://www.sqlite.org/download.html)
   - Choose the "Precompiled Binaries for Windows" section and download the sqlite-tools zip file
   - Extract the files to a folder (e.g., `C:\sqlite`)
   - Add this folder to your PATH:
     - Open Control Panel > System > Advanced System Settings > Environment Variables
     - Edit the PATH variable and add the path to your SQLite folder
     - Verify installation by opening Command Prompt and typing `sqlite3 --version`

3. **uv/uvx**:
   - Open PowerShell as Administrator and run:
     ```
     powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
     ```
   - Restart your terminal and verify installation with `uv --version`

#### macOS

1. **Python 3.8+**:
   - Install using Homebrew:
     ```
     brew install python
     ```

2. **SQLite**:
   - SQLite comes pre-installed on macOS, but you can update it using Homebrew:
     ```
     brew install sqlite
     ```
   - Verify installation with `sqlite3 --version`

3. **uv/uvx**:
   - Install using Homebrew:
     ```
     brew install uv
     ```
   - Or use the official installer:
     ```
     curl -LsSf https://astral.sh/uv/install.sh | sh
     ```
   - Verify installation with `uv --version`

#### Linux (Ubuntu/Debian)

1. **Python 3.8+**:
   ```
   sudo apt update
   sudo apt install python3 python3-pip
   ```

2. **SQLite**:
   ```
   sudo apt update
   sudo apt install sqlite3
   ```
   - Verify installation with `sqlite3 --version`

3. **uv/uvx**:
   ```
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
   - Verify installation with `uv --version`

## Installation

### Option 1: Install from PyPI (Recommended)

```bash
pip install temprl-mcp-client
```

## Configuration

The project uses two main configuration files:

1. `.env` - Contains OpenAI API configuration:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL=gpt-4o
   # OPENAI_BASE_URL=https://api.openai.com/v1  # Uncomment and modify if using a custom base url
   ```

2. `mcp_config.json` - Defines MCP servers to connect to:
   ```json
   {
     "mcpServers": {
       "server1": {
         "command": "command-to-start-server",
         "args": ["arg1", "arg2"],
         "env": {
           "ENV_VAR1": "value1",
           "ENV_VAR2": "value2"
         }
       },
       "server2": {
         "command": "another-server-command",
         "args": ["--option", "value"]
       }
     }
   }
   ```

   You can add as many MCP servers as you need, and the client will connect to all of them and make their tools available.

## Usage

The Temprl MCP client now supports storing chat memories in a PostgreSQL database, which enables:

1. Persistent storage of conversations across sessions
2. Loading past conversations by ID
3. Continuing conversations from where they left off

### Using PostgreSQL for Chat Memory

The chat memory system can be configured to use PostgreSQL for storage, which provides better performance and scalability compared to SQLite.

#### PostgreSQL Configuration in Code

You can use PostgreSQL directly in your code by passing the appropriate configuration to the `ChatMemory` class or `initialize_mcp` function:

```python
from temprl_mcp_client.client import initialize_mcp, run_interaction

# PostgreSQL configuration
postgres_config = {
    "host": "localhost",
    "port": "5432",
    "database": "temprl_mcp",
    "user": "postgres",
    "password": "your_password"
}

# Initialize MCP with PostgreSQL storage
mcp_manager = await initialize_mcp(
    use_postgres=True,
    postgres_config=postgres_config
)

# Run interactions as usual
response = await run_interaction(
    user_query="Your question here",
    mcp_manager=mcp_manager
)
```

#### PostgreSQL Configuration via Command Line

You can also configure PostgreSQL from the command line using the provided scripts:

```bash
# Initialize a conversation with PostgreSQL storage
python init_conversation.py --use-postgres --pg-host localhost --pg-port 5432 --pg-db temprl_mcp --pg-user postgres --pg-password your_password

# Load an existing conversation from PostgreSQL
python chat_by_id.py --id your-chat-id --use-postgres --pg-host localhost --pg-db temprl_mcp

# Run the test script with PostgreSQL
python test.py --use-postgres --pg-host localhost --pg-user postgres
```

#### Using Environment Variables

If you don't provide explicit configuration, the system will look for these environment variables:

```
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=temprl_mcp
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
```

You can set these in your environment or in a `.env` file in your project root.

#### Setting Up PostgreSQL Database

Before using PostgreSQL, make sure to set up the database:

1. Install PostgreSQL on your system
2. Create a database for the Temprl MCP client
3. Run the setup script:

```bash
python setup_postgres.py
```

This script will create the necessary tables in your PostgreSQL database.

### Using Chat Memory

#### Starting a New Chat

When you start a conversation, the system automatically generates a unique ID for the chat:

```python
from temprl_mcp_client.client import initialize_mcp, run_interaction

# Initialize MCP with a new chat memory
mcp_manager = await initialize_mcp()

# Get the chat ID for later use
chat_id = mcp_manager.chat_memory.chat_id
print(f"New chat created with ID: {chat_id}")

# Run interactions
response = await run_interaction(
    user_query="Your question here",
    mcp_manager=mcp_manager
)
```

#### Loading a Chat by ID

To continue a previous conversation, use the chat ID:

```python
from temprl_mcp_client.client import initialize_mcp, run_interaction

# Load an existing chat by ID
chat_id = "your-previous-chat-id"
mcp_manager = await initialize_mcp(chat_id=chat_id)

# Check if the chat was found
if mcp_manager.chat_memory.is_new:
    print(f"No chat found with ID: {chat_id}")
else:
    print(f"Loaded chat: {mcp_manager.chat_memory.title}")
    
# Continue the conversation
response = await run_interaction(
    user_query="Your next question",
    mcp_manager=mcp_manager
)
```

#### Using the Chat ID Tool

The client comes with a convenient tool for managing chats by ID:

```bash
# List all available chats
python chat_by_id.py --list

# Start a new chat
python chat_by_id.py

# Load a chat by ID
python chat_by_id.py --id your-chat-id

# Load a chat and immediately send a query
python chat_by_id.py --id your-chat-id --query "Your question here"
```

### Using Specific MCP Servers

By default, all initialized MCP servers are available during the interaction. However, you can now selectively use only certain servers for specific interactions:

```python
from temprl_mcp_client.client import initialize_mcp, run_interaction

# Initialize all MCP servers first
mcp_manager = await initialize_mcp()

# Get list of available servers
available_servers = mcp_manager.get_available_servers()
print(f"Available servers: {available_servers}")  # e.g., ['zoom', 'gmail', 'business']

# Use only specific servers for this interaction
response = await run_interaction(
    user_query="Schedule a Zoom meeting for tomorrow",
    mcp_manager=mcp_manager,
    server_names=["zoom"]  # Only use the Zoom server for this interaction
)

# In another interaction, use different servers
response = await run_interaction(
    user_query="Check my unread emails",
    mcp_manager=mcp_manager,
    server_names=["gmail"]  # Only use the Gmail server for this interaction
)

# You can also use multiple servers in one interaction
response = await run_interaction(
    user_query="Create a meeting and send confirmation emails",
    mcp_manager=mcp_manager,
    server_names=["zoom", "gmail"]  # Use both Zoom and Gmail servers
)
```

This approach allows you to:
1. Initialize all servers once at the beginning
2. Selectively use only the servers needed for each specific interaction
3. Reduce the number of tools exposed to the model, improving its performance

### Using Custom System Prompts and User IDs

You can now provide a custom system prompt for each interaction and associate user IDs with interactions:

```python
from temprl_mcp_client.client import initialize_mcp, run_interaction

# Initialize MCP manager
mcp_manager = await initialize_mcp()

# Run an interaction with a custom system prompt
response = await run_interaction(
    user_query="What can you tell me about machine learning?",
    mcp_manager=mcp_manager,
    system_prompt="You are an AI expert specialized in machine learning and data science. Provide detailed, technical answers."
)

# Run an interaction with a user ID
response = await run_interaction(
    user_query="Schedule a meeting with my team",
    mcp_manager=mcp_manager,
    user_id="user123"  # This ID will be passed to MCP servers
)

# Combine all parameters
response = await run_interaction(
    user_query="Analyze my sales data and schedule a presentation",
    mcp_manager=mcp_manager,
    server_names=["analytics", "calendar"],  # Only use these specific servers
    system_prompt="You are a sales analyst assistant. Focus on business insights.",
    user_id="sales_manager_42"  # This ID will be passed to MCP servers
)
```

Benefits of these features:
1. **Custom System Prompts**: Override the default system prompt for specific interactions to tailor the model's behavior
2. **User ID Support**: Pass user identifiers to MCP servers for authentication, personalization, or tracking
3. **Flexible Integration**: Combine with server selection for highly customized interactions

From the command line, you can use these features with:

```bash
# Use a custom system prompt
python init_conversation.py --system-prompt "You are a specialized assistant for scientific research" --query "Explain quantum computing"

# Associate a user ID with the interaction
python init_conversation.py --user-id "researcher_42" --query "Search for recent papers on CRISPR"

# Combine all options
python init_conversation.py --servers "research,calendar" --system-prompt "You are a research assistant" --user-id "lab_director" --query "Schedule a lab meeting and find relevant papers"
```

### API Reference

The chat memory system provides the following features:

- `ChatMemory(chat_id=None)` - Create or load a chat memory
- `chat_memory.chat_id` - Get the unique ID for the current chat
- `ChatMemory.list_conversations()` - List all available chats
- `ChatMemory.delete_conversation(chat_id)` - Delete a chat by ID

The system automatically persists all messages to the database as you chat, so there's no need to manually save the state.
