#!/usr/bin/env python3
import os
import json
import requests
import time
import argparse
import sys
import random
import string
import textwrap
from datetime import datetime

# Handle collections.Iterable deprecation for Python 3.10+
try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable

# Now import tabulate
try:
    from tabulate import tabulate
except ImportError as e:
    if "cannot import name 'Iterable' from 'collections'" in str(e):
        # Monkey patch collections.Iterable for tabulate
        import collections
        if not hasattr(collections, 'Iterable'):
            collections.Iterable = Iterable
        # Try import again
        from tabulate import tabulate

BASE_URL = "https://api.mail.tm"
HEADERS = {"Content-Type": "application/json"}
CONFIG_DIR = os.path.expanduser("~/.tempmail")
ACCOUNTS_FILE = os.path.join(CONFIG_DIR, "accounts.json")
CURRENT_ACCOUNT_FILE = os.path.join(CONFIG_DIR, "current_account.json")

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

def generate_password(length=16):
    """Generate a random secure password."""
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return ''.join(random.choice(chars) for _ in range(length))

def save_accounts(accounts):
    """Save all accounts to the accounts file."""
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=2)

def load_accounts():
    """Load all accounts from the accounts file."""
    if os.path.exists(ACCOUNTS_FILE):
        with open(ACCOUNTS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_current_account(account_id):
    """Save the current active account ID."""
    with open(CURRENT_ACCOUNT_FILE, "w") as f:
        json.dump({"current": account_id}, f)

def get_current_account_id():
    """Get the current active account ID."""
    if os.path.exists(CURRENT_ACCOUNT_FILE):
        with open(CURRENT_ACCOUNT_FILE, "r") as f:
            data = json.load(f)
            return data.get("current")
    return None

def create_account(alias=None, password=None):
    """Create a new temporary email account."""
    try:
        # Get available domains
        domain_res = requests.get(f"{BASE_URL}/domains")
        if domain_res.status_code != 200:
            print(f"Error fetching domains: {domain_res.text}")
            return None
            
        domain = domain_res.json()["hydra:member"][0]["domain"]
        
        # Generate username if not provided
        if not alias:
            alias = f"user{int(time.time())}"
        
        email = f"{alias}@{domain}"
        
        # Generate password if not provided
        if not password:
            password = generate_password()
        
        # Create account
        res = requests.post(
            f"{BASE_URL}/accounts", 
            json={"address": email, "password": password}, 
            headers=HEADERS
        )
        
        if res.status_code != 201:
            print(f"Failed to create account: {res.text}")
            return None
            
        # Get authentication token
        token_res = requests.post(
            f"{BASE_URL}/token", 
            json={"address": email, "password": password}, 
            headers=HEADERS
        )
        
        if token_res.status_code != 200:
            print(f"Failed to get token: {token_res.text}")
            return None
            
        token_data = token_res.json()
        
        # Create account data
        account = {
            "id": alias,
            "email": email,
            "password": password,
            "token": token_data["token"],
            "created_at": datetime.now().isoformat()
        }
        
        # Save to accounts list
        accounts = load_accounts()
        accounts[alias] = account
        save_accounts(accounts)
        
        # Always set newly created account as the current one
        save_current_account(alias)
            
        return account
        
    except Exception as e:
        print(f"Error creating account: {str(e)}")
        return None

def get_account(account_id=None):
    """Get account details by ID or current account if no ID provided."""
    accounts = load_accounts()
    
    if not account_id:
        account_id = get_current_account_id()
        
    if not account_id:
        print("No account selected. Create or select an account first.")
        return None
        
    if account_id not in accounts:
        print(f"Account '{account_id}' not found.")
        return None
        
    return accounts[account_id]

def refresh_token(account):
    """Refresh the authentication token for an account."""
    try:
        token_res = requests.post(
            f"{BASE_URL}/token", 
            json={"address": account["email"], "password": account["password"]}, 
            headers=HEADERS
        )
        
        if token_res.status_code != 200:
            print(f"Failed to refresh token: {token_res.text}")
            return False
            
        token_data = token_res.json()
        account["token"] = token_data["token"]
        
        # Update account in storage
        accounts = load_accounts()
        accounts[account["id"]] = account
        save_accounts(accounts)
        
        return True
        
    except Exception as e:
        print(f"Error refreshing token: {str(e)}")
        return False

def get_messages(account, page=1, limit=10):
    """Get messages for an account with pagination."""
    try:
        token = account["token"]
        res = requests.get(
            f"{BASE_URL}/messages?page={page}&itemsPerPage={limit}", 
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if res.status_code == 401:
            # Token expired, try to refresh
            if refresh_token(account):
                # Retry with new token
                return get_messages(account, page, limit)
            return None
            
        if res.status_code != 200:
            print(f"Failed to get messages: {res.text}")
            return None
            
        return res.json()
        
    except Exception as e:
        print(f"Error getting messages: {str(e)}")
        return None

def get_message_content(account, message_id):
    """Get the full content of a specific message."""
    try:
        token = account["token"]
        res = requests.get(
            f"{BASE_URL}/messages/{message_id}", 
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if res.status_code == 401:
            # Token expired, try to refresh
            if refresh_token(account):
                # Retry with new token
                return get_message_content(account, message_id)
            return None
            
        if res.status_code != 200:
            print(f"Failed to get message content: {res.text}")
            return None
            
        return res.json()
        
    except Exception as e:
        print(f"Error getting message content: {str(e)}")
        return None

def delete_message(account, message_id):
    """Delete a specific message."""
    try:
        token = account["token"]
        res = requests.delete(
            f"{BASE_URL}/messages/{message_id}", 
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
        )
        
        if res.status_code == 401:
            # Token expired, try to refresh
            if refresh_token(account):
                # Retry with new token
                return delete_message(account, message_id)
            return False
            
        if res.status_code != 204:
            print(f"Failed to delete message: {res.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error deleting message: {str(e)}")
        return False

def delete_account(account_id):
    """Delete an account from local storage."""
    accounts = load_accounts()
    
    if account_id not in accounts:
        print(f"Account '{account_id}' not found.")
        return False
        
    # Delete account
    del accounts[account_id]
    save_accounts(accounts)
    
    # Update current account if needed
    current = get_current_account_id()
    if current == account_id:
        if accounts:
            # Set first available account as current
            save_current_account(next(iter(accounts)))
        else:
            # No accounts left, remove current account file
            if os.path.exists(CURRENT_ACCOUNT_FILE):
                os.remove(CURRENT_ACCOUNT_FILE)
                
    return True

def mark_as_read(account, message_id):
    """Mark a message as read."""
    try:
        token = account["token"]
        res = requests.patch(
            f"{BASE_URL}/messages/{message_id}", 
            json={"seen": True},
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/merge-patch+json"
            }
        )
        
        if res.status_code == 401:
            # Token expired, try to refresh
            if refresh_token(account):
                # Retry with new token
                return mark_as_read(account, message_id)
            return False
            
        if res.status_code != 200:
            print(f"Failed to mark message as read: {res.text}")
            return False
            
        return True
        
    except Exception as e:
        print(f"Error marking message as read: {str(e)}")
        return False

def display_message(message, detailed=False):
    """Display a message in a formatted way."""
    if detailed:
        print("\n" + "="*80)
        print(f"From: {message['from']['address']}")
        print(f"Subject: {message['subject']}")
        print(f"Date: {message['createdAt']}")
        print(f"ID: {message['id']}")
        print("="*80)
        
        # Display HTML content as plain text
        if 'html' in message:
            print("\nContent:")
            print("-"*80)
            print(message['html'])
        elif 'text' in message:
            print("\nContent:")
            print("-"*80)
            print(message['text'])
        else:
            print("\nNo content available.")
            
        print("="*80 + "\n")
    else:
        seen = "✓" if message.get("seen", False) else " "
        date = message["createdAt"].split("T")[0]
        subject = message["subject"] if len(message["subject"]) <= 50 else message["subject"][:47] + "..."
        sender = message["from"]["address"]
        return [seen, message["id"][:8], date, sender, subject]

def list_accounts():
    """List all accounts."""
    accounts = load_accounts()
    current = get_current_account_id()
    
    if not accounts:
        print("No accounts found. Create one with 'tempmail create'.")
        return
    
    table_data = []
    for alias, account in accounts.items():
        active = "✓" if alias == current else " "
        created = account["created_at"].split("T")[0] if "created_at" in account else "N/A"
        table_data.append([active, alias, account["email"], created])
    
    print(tabulate(table_data, headers=["Current", "Alias", "Email", "Created"], tablefmt="pretty"))

def monitor_inbox(account, interval=10, limit=5):
    """Monitor inbox for new messages."""
    print(f"Monitoring inbox for {account['email']}...")
    print(f"Press Ctrl+C to stop monitoring.")
    
    try:
        last_check = []
        while True:
            messages_data = get_messages(account, page=1, limit=limit)
            
            if not messages_data:
                print("Failed to fetch messages. Retrying...")
                time.sleep(interval)
                continue
                
            messages = messages_data.get("hydra:member", [])
            
            # Check for new messages
            current_ids = [msg["id"] for msg in messages]
            if last_check and set(current_ids) != set(last_check):
                new_ids = set(current_ids) - set(last_check)
                if new_ids:
                    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] New message(s) received!")
                    
                    # Display new messages
                    table_data = []
                    for msg in messages:
                        if msg["id"] in new_ids:
                            table_data.append(display_message(msg))
                    
                    print(tabulate(table_data, headers=["Read", "ID", "Date", "From", "Subject"], tablefmt="pretty"))
            
            last_check = current_ids
            sys.stdout.write(f"\r[{datetime.now().strftime('%H:%M:%S')}] Checking for new messages... ")
            sys.stdout.flush()
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

def interactive_mode(account):
    """Start an interactive session for managing emails."""
    if not account:
        print("No account selected. Create or select an account first.")
        return
        
    print(f"\nInteractive mode for {account['email']}")
    print("Type 'help' for available commands.")
    
    while True:
        try:
            cmd = input("\n> ").strip().lower()
            
            if cmd in ["exit", "quit", "q"]:
                break
                
            elif cmd in ["help", "h", "?"]:
                print("\nAvailable commands:")
                print("  list, ls       - List recent messages")
                print("  list-full, lf  - List recent messages with full content")
                print("  read <id>      - Read a message by ID")
                print("  delete <id>    - Delete a message by ID")
                print("  mark <id>      - Mark a message as read")
                print("  refresh, r     - Refresh message list")
                print("  monitor, m     - Monitor inbox for new messages")
                print("  info, i        - Show account information")
                print("  exit, quit, q  - Exit interactive mode")
                
            elif cmd in ["list", "ls"]:
                messages_data = get_messages(account, limit=10)
                if not messages_data:
                    print("No messages found or failed to fetch messages.")
                    continue
                    
                messages = messages_data.get("hydra:member", [])
                if not messages:
                    print("No messages in inbox.")
                    continue
                    
                table_data = []
                for msg in messages:
                    table_data.append(display_message(msg))
                
                print(tabulate(table_data, headers=["Read", "ID", "Date", "From", "Subject"], tablefmt="pretty"))
                
            elif cmd in ["list-full", "lf"]:
                messages_data = get_messages(account, limit=5)  # Limit to 5 for full view
                if not messages_data:
                    print("No messages found or failed to fetch messages.")
                    continue
                    
                messages = messages_data.get("hydra:member", [])
                if not messages:
                    print("No messages in inbox.")
                    continue
                
                # Show full message content for each message
                for i, msg in enumerate(messages):
                    # Get full message content
                    full_msg = get_message_content(account, msg["id"])
                    if full_msg:
                        print(f"\n--- Message {i+1}/{len(messages)} ---")
                        display_message(full_msg, detailed=True)
                    else:
                        print(f"\n--- Message {i+1}/{len(messages)} ---")
                        print(f"Failed to fetch full content for message ID: {msg['id']}")
                        display_message(msg, detailed=True)
                
            elif cmd.startswith("read "):
                msg_id = cmd.split(" ", 1)[1].strip()
                
                # Find full ID if partial
                messages_data = get_messages(account, limit=20)
                if not messages_data:
                    print("Failed to fetch messages.")
                    continue
                    
                messages = messages_data.get("hydra:member", [])
                full_id = None
                
                for msg in messages:
                    if msg["id"].startswith(msg_id):
                        full_id = msg["id"]
                        break
                
                if not full_id:
                    print(f"No message found with ID starting with '{msg_id}'.")
                    continue
                
                message = get_message_content(account, full_id)
                if message:
                    display_message(message, detailed=True)
                    mark_as_read(account, full_id)
                else:
                    print(f"Failed to fetch message with ID '{full_id}'.")
                    
            elif cmd.startswith("delete "):
                msg_id = cmd.split(" ", 1)[1].strip()
                
                # Find full ID if partial
                messages_data = get_messages(account, limit=20)
                if not messages_data:
                    print("Failed to fetch messages.")
                    continue
                    
                messages = messages_data.get("hydra:member", [])
                full_id = None
                
                for msg in messages:
                    if msg["id"].startswith(msg_id):
                        full_id = msg["id"]
                        break
                
                if not full_id:
                    print(f"No message found with ID starting with '{msg_id}'.")
                    continue
                
                if delete_message(account, full_id):
                    print(f"Message deleted successfully.")
                else:
                    print(f"Failed to delete message.")
                    
            elif cmd.startswith("mark "):
                msg_id = cmd.split(" ", 1)[1].strip()
                
                # Find full ID if partial
                messages_data = get_messages(account, limit=20)
                if not messages_data:
                    print("Failed to fetch messages.")
                    continue
                    
                messages = messages_data.get("hydra:member", [])
                full_id = None
                
                for msg in messages:
                    if msg["id"].startswith(msg_id):
                        full_id = msg["id"]
                        break
                
                if not full_id:
                    print(f"No message found with ID starting with '{msg_id}'.")
                    continue
                
                if mark_as_read(account, full_id):
                    print(f"Message marked as read.")
                else:
                    print(f"Failed to mark message as read.")
                    
            elif cmd in ["refresh", "r"]:
                print("Refreshing messages...")
                messages_data = get_messages(account, limit=10)
                if not messages_data:
                    print("Failed to fetch messages.")
                    continue
                    
                messages = messages_data.get("hydra:member", [])
                if not messages:
                    print("No messages in inbox.")
                    continue
                    
                table_data = []
                for msg in messages:
                    table_data.append(display_message(msg))
                
                print(tabulate(table_data, headers=["Read", "ID", "Date", "From", "Subject"], tablefmt="pretty"))
                
            elif cmd in ["monitor", "m"]:
                monitor_inbox(account)
                
            elif cmd in ["info", "i"]:
                print(f"\nAccount Information:")
                print(f"  Alias: {account['id']}")
                print(f"  Email: {account['email']}")
                print(f"  Created: {account['created_at']}")
                
            else:
                print(f"Unknown command: {cmd}")
                print("Type 'help' for available commands.")
                
        except KeyboardInterrupt:
            print("\nExiting interactive mode.")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    parser = argparse.ArgumentParser(
        description="Temporary Email CLI Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
        Examples:
          tempmail create                     # Create a new email account
          tempmail create --alias myemail     # Create with custom alias
          tempmail list                       # List all accounts
          tempmail use myemail                # Switch to a specific account
          tempmail inbox                      # Check inbox of current account
          tempmail read MESSAGE_ID            # Read a specific message
          tempmail monitor                    # Monitor inbox for new messages
          tempmail interactive                # Start interactive mode
        ''')
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")
    
    # Create account command
    create_parser = subparsers.add_parser("create", help="Create a new email account")
    create_parser.add_argument("--alias", help="Custom alias for the account")
    create_parser.add_argument("--password", help="Custom password for the account")
    
    # List accounts command
    subparsers.add_parser("list", help="List all accounts")
    
    # Use account command
    use_parser = subparsers.add_parser("use", help="Switch to a specific account")
    use_parser.add_argument("alias", help="Alias of the account to use")
    
    # Delete account command
    delete_parser = subparsers.add_parser("delete", help="Delete an account")
    delete_parser.add_argument("alias", help="Alias of the account to delete")
    
    # Check inbox command
    inbox_parser = subparsers.add_parser("inbox", help="Check inbox of current account")
    inbox_parser.add_argument("--limit", type=int, default=10, help="Number of messages to show")
    inbox_parser.add_argument("--full", action="store_true", help="Show full message content")
    
    # Read message command
    read_parser = subparsers.add_parser("read", help="Read a specific message")
    read_parser.add_argument("message_id", help="ID of the message to read")
    
    # Delete message command
    delete_msg_parser = subparsers.add_parser("delete-message", help="Delete a specific message")
    delete_msg_parser.add_argument("message_id", help="ID of the message to delete")
    
    # Monitor inbox command
    monitor_parser = subparsers.add_parser("monitor", help="Monitor inbox for new messages")
    monitor_parser.add_argument("--interval", type=int, default=10, help="Check interval in seconds")
    
    # Interactive mode command
    subparsers.add_parser("interactive", help="Start interactive mode")
    
    # Current account info command
    subparsers.add_parser("info", help="Show current account information")
    
    args = parser.parse_args()
    
    # Handle commands
    if args.command == "create":
        account = create_account(args.alias, args.password)
        if account:
            print(f"Account created successfully:")
            print(f"  Email: {account['email']}")
            print(f"  Password: {account['password']}")
            print(f"  Alias: {account['id']}")
            print("\nThis account is now set as your current account.")
        else:
            print("Failed to create account.")
            
    elif args.command == "list":
        list_accounts()
        
    elif args.command == "use":
        accounts = load_accounts()
        if args.alias in accounts:
            save_current_account(args.alias)
            print(f"Switched to account: {accounts[args.alias]['email']}")
        else:
            print(f"Account '{args.alias}' not found.")
            
    elif args.command == "delete":
        if delete_account(args.alias):
            print(f"Account '{args.alias}' deleted successfully.")
        else:
            print(f"Failed to delete account '{args.alias}'.")
            
    elif args.command == "inbox":
        account = get_account()
        if account:
            messages_data = get_messages(account, limit=args.limit)
            if not messages_data:
                print("No messages found or failed to fetch messages.")
                return
                
            messages = messages_data.get("hydra:member", [])
            if not messages:
                print("No messages in inbox.")
                return
            
            print(f"Inbox for {account['email']}:")
            
            if args.full:
                # Show full message content for each message
                for i, msg in enumerate(messages):
                    # Get full message content
                    full_msg = get_message_content(account, msg["id"])
                    if full_msg:
                        print(f"\n--- Message {i+1}/{len(messages)} ---")
                        display_message(full_msg, detailed=True)
                    else:
                        print(f"\n--- Message {i+1}/{len(messages)} ---")
                        print(f"Failed to fetch full content for message ID: {msg['id']}")
                        display_message(msg, detailed=True)
            else:
                # Show message summary in table format
                table_data = []
                for msg in messages:
                    table_data.append(display_message(msg))
                
                print(tabulate(table_data, headers=["Read", "ID", "Date", "From", "Subject"], tablefmt="pretty"))
        
    elif args.command == "read":
        account = get_account()
        if account:
            # Find full ID if partial
            messages_data = get_messages(account, limit=20)
            if not messages_data:
                print("Failed to fetch messages.")
                return
                
            messages = messages_data.get("hydra:member", [])
            full_id = None
            
            for msg in messages:
                if msg["id"].startswith(args.message_id):
                    full_id = msg["id"]
                    break
            
            if not full_id:
                print(f"No message found with ID starting with '{args.message_id}'.")
                return
            
            message = get_message_content(account, full_id)
            if message:
                display_message(message, detailed=True)
                mark_as_read(account, full_id)
            else:
                print(f"Failed to fetch message with ID '{full_id}'.")
                
    elif args.command == "delete-message":
        account = get_account()
        if account:
            # Find full ID if partial
            messages_data = get_messages(account, limit=20)
            if not messages_data:
                print("Failed to fetch messages.")
                return
                
            messages = messages_data.get("hydra:member", [])
            full_id = None
            
            for msg in messages:
                if msg["id"].startswith(args.message_id):
                    full_id = msg["id"]
                    break
            
            if not full_id:
                print(f"No message found with ID starting with '{args.message_id}'.")
                return
            
            if delete_message(account, full_id):
                print(f"Message deleted successfully.")
            else:
                print(f"Failed to delete message.")
                
    elif args.command == "monitor":
        account = get_account()
        if account:
            monitor_inbox(account, interval=args.interval)
            
    elif args.command == "interactive":
        account = get_account()
        interactive_mode(account)
        
    elif args.command == "info":
        account = get_account()
        if account:
            print(f"\nCurrent Account Information:")
            print(f"  Alias: {account['id']}")
            print(f"  Email: {account['email']}")
            print(f"  Created: {account['created_at']}")
        
    else:
        # No command or invalid command
        parser.print_help()

if __name__ == "__main__":
    main()