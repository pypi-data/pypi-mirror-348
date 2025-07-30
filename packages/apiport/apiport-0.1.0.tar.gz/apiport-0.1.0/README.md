# APIPort

A command-line tool for securely managing API secrets.

## Features

- **Secure Storage**: All secrets are encrypted using Fernet symmetric encryption
- **Multiple Input Formats**: Add secrets individually or in bulk from files
- **AI-Powered Parsing**: Intelligently extract secrets from various text formats (with optional AI integration)
- **Environment File Integration**: Easily import secrets to your .env files
- **Simple Command-Line Interface**: Intuitive commands for managing your secrets

## Installation

```bash
# Basic installation
pip install apiport

# With AI-powered parsing capabilities
pip install apiport[ai]
```

## Usage

### Adding Secrets

```bash
# Add a single secret
apiport add API_KEY=your_secret_key

# Add multiple secrets at once
apiport add API_KEY=your_secret_key DB_PASSWORD=your_db_password

# Add secrets from a file
apiport add --file secrets.txt
```

### Listing Secrets

```bash
# List all secret names
apiport list

# List secrets with their values (debug mode)
apiport list --debug
```

### Deleting Secrets

```bash
# Delete a specific secret
apiport delete API_KEY

# Delete all secrets (reset the vault)
apiport delete
```

### Updating Secrets

```bash
# Update an existing secret
apiport update API_KEY new_secret_value
```

### Importing to .env File

```bash
# Import a specific secret to .env
apiport import API_KEY

# Import multiple secrets
apiport import API_KEY DB_PASSWORD

# Import all secrets
apiport import
```

## AI-Powered Parsing

When installed with the `[ai]` extra, APIPort can use Google's Generative AI to intelligently extract secrets from various text formats. This is especially useful for parsing complex or non-standard formats.

To use this feature:
1. Install with AI support: `pip install apiport[ai]`
2. Set your Gemini API key in your environment: `export GEMINI_API_KEY=your_key`
3. Use the file import feature: `apiport add --file your_complex_file.txt`

## Security

- All secrets are encrypted using Fernet symmetric encryption
- Encryption keys are stored locally in `~/.apiport_key`
- The encrypted vault is stored in `~/.apiport/vault.port`

## License

MIT
