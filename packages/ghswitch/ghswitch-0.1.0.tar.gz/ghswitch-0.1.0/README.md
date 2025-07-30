# GitHub Account Manager (ghswitch)

A command-line tool for managing multiple GitHub accounts on a single device. Works on both macOS and Windows.

## Features

- Add multiple GitHub accounts with their configurations (username, email, SSH key, token)
- Switch between accounts globally or per repository
- Automatically handle SSH key switching and Git configuration updates
- List all configured accounts
- Set a primary account for new repositories
- Remove accounts when no longer needed

## Installation

```bash
pip install ghswitch
```

Or install from source:

```bash
git clone https://github.com/yourusername/ghswitch.git
cd ghswitch
pip install -e .
```

## Usage

### Adding a new account

```bash
ghswitch add --name work --username workuser --email work@example.com --ssh-key ~/.ssh/id_rsa_work
```

### Listing all accounts

```bash
ghswitch list
```

### Setting the primary account

```bash
ghswitch set-primary work
```

### Switching accounts for a specific repository

```bash
cd /path/to/your/repo
ghswitch use personal
```

### Switching the global account

```bash
ghswitch use work --global
```

### Removing an account

```bash
ghswitch remove personal
```

## Configuration

The configuration is stored in `~/.ghswitch/config.yaml` (macOS/Linux) or `%USERPROFILE%\.ghswitch\config.yaml` (Windows).

## License

MIT
