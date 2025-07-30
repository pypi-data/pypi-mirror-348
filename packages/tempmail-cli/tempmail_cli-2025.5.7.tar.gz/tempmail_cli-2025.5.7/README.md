# TempMail CLI

A command-line tool for managing temporary email accounts using the mail.tm API.

## Features

- Create and manage multiple temporary email accounts
- Monitor inbox for new messages
- Read, delete, and mark messages as read
- Interactive mode for easier email management
- Persistent storage of accounts

## Installation

```bash
pip install tempmail-cli
```

Or install from source:

```bash
git clone https://github.com/yourusername/tempmail-cli.git
cd tempmail-cli
pip install -e .
```

## Usage

### Basic Commands

```bash
# Create a new email account
tempmail create

# Create with custom alias
tempmail create --alias myemail

# List all accounts
tempmail list

# Switch to a specific account
tempmail use myemail

# Check inbox of current account
tempmail inbox

# Check inbox with full message content
tempmail inbox --full

# Read a specific message (can use partial ID)
tempmail read abc123

# Delete a specific message
tempmail delete-message abc123

# Monitor inbox for new messages
tempmail monitor

# Start interactive mode
tempmail interactive

# Show current account information
tempmail info
```

### Interactive Mode

Interactive mode provides a shell-like interface for managing emails:

```
> help
Available commands:
  list, ls       - List recent messages
  read <id>      - Read a message by ID
  delete <id>    - Delete a message by ID
  mark <id>      - Mark a message as read
  refresh, r     - Refresh message list
  monitor, m     - Monitor inbox for new messages
  info, i        - Show account information
  exit, quit, q  - Exit interactive mode
```

## Configuration

All account data is stored in `~/.tempmail/` directory:
- `accounts.json`: Stores all account information
- `current_account.json`: Stores the currently selected account

## License

MIT