"""
Commands module for the apiport CLI tool.
"""
import os
import sys

# Try to import Google AI libraries, but make them optional
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    
    load_dotenv()
    
    has_genai = True
    client = genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
except ImportError:
    has_genai = False
    print("[!] Google AI libraries not found. LLM-based parsing will be disabled.")
    print("[!] To enable LLM features, install required packages: pip install google-generativeai python-dotenv")

from .storage import load_vault, save_vault

def add(secret_name, secret_value=None, path_to_file=None):
    """Add secrets to the vault.
    
    Args:
        secret_name: Either a single secret name or a key=value string or a list of key=value strings
        secret_value: The value for the secret (if secret_name is just a name)
        path_to_file: Optional path to a file containing secrets
    """
    vault = load_vault()
    
    # Case 1: File path provided
    if path_to_file and os.path.exists(path_to_file):
        _add_from_file(path_to_file, vault)
        return
    
    # Case 2: Single key-value pair with separate arguments
    if secret_value is not None:
        vault[secret_name] = secret_value
        save_vault(vault)
        print(f"[+] Added secret: {secret_name}")
        return
    
    # Case 3: Key=value format in secret_name
    if isinstance(secret_name, str) and "=" in secret_name:
        key, value = secret_name.split("=", 1)
        vault[key] = value
        save_vault(vault)
        print(f"[+] Added secret: {key}")
        return
    
    # Case 4: List of key=value pairs
    if isinstance(secret_name, list):
        for item in secret_name:
            if "=" in item:
                key, value = item.split("=", 1)
                vault[key] = value
                print(f"[+] Added secret: {key}")
            else:
                print(f"[!] Invalid format for {item}. Use KEY=value format.")
        save_vault(vault)
        return
    
    # Invalid input
    print("[!] Invalid input format. Use 'add KEY VALUE' or 'add KEY=VALUE' or provide a file path.")

def _add_from_file(file_path, vault):
    """Parse and add secrets from a file.
    
    This function attempts to intelligently parse different file formats.
    """
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Try to parse as .env format first (most common)
    secrets_added = 0
    
    # Try LLM parsing first if available
    if has_genai:
        try:
            # Use Gemini to parse the content
            generation_config = {
                "temperature": 0,
                "top_p": 1,
                "top_k": 1,
                "max_output_tokens": 2048,
            }
            
            safety_settings = [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
            ]
            
            model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                generation_config=generation_config,
                safety_settings=safety_settings
            )
            
            prompt = f"""You are an expert at parsing API Keys from text files.
            Here is some text that contains API_KEYS. There could be some unnecessary information and comments (like email ids, or wrong api key names, incorrect format, todo list etc). Ignore the unnecessary information and extract only the API KEYs.
            Return the API_KEYS in the form KEY=VALUE, where the key is in all caps and snake_case, one per line. Make sure that the API KEY variable names is in the correct format according to the api companies guidelines. So, if you see [OPEN AIs api is sk34t-sag..., give back OPENAI_API_KEY=sk34t-sag...].
            
            {content}
            """
            
            response = model.generate_content(prompt)
            
            # Process LLM response
            if response.text:
                llm_extracted = response.text.strip().split('\n')
                for pair in llm_extracted:
                    if '=' in pair:
                        key, value = pair.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"\'')
                        
                        if key:
                            vault[key] = value
                            secrets_added += 1
                            print(f"[+] Added secret: {key}")
                
                # If we successfully extracted secrets with the LLM, save and return
                if secrets_added > 0:
                    save_vault(vault)
                    print(f"[*] Added {secrets_added} secrets from {file_path} using LLM parsing")
                    return
        except Exception as e:
            print(f"[!] Error using LLM for parsing: {str(e)}")
            print("[*] Falling back to manual parsing...")
    
    # Manual parsing as fallback
    secrets_added = 0
    for line in content.splitlines():
        line = line.strip()
        
        # Skip empty lines and comments
        if not line or line.startswith('#'):
            continue
            
        # Try to extract key-value pairs
        if '=' in line:
            # Handle KEY=VALUE format
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            
            if key:
                vault[key] = value
                secrets_added += 1
                print(f"[+] Added secret: {key}")
        elif ':' in line:
            # Handle KEY: VALUE format
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip().strip('"\'')
            
            if key:
                vault[key] = value
                secrets_added += 1
                print(f"[+] Added secret: {key}")
    
    # If we found secrets, save and return
    if secrets_added > 0:
        save_vault(vault)
        print(f"[*] Added {secrets_added} secrets from {file_path}")
        return
    
    # If no secrets were found with any parsing method
    print("[!] Could not parse secrets from the file. Please ensure it's in a supported format.")
    print("[*] Supported formats: KEY=VALUE or KEY: VALUE (one per line)")
    if not has_genai:
        print("[*] Install Google AI libraries for intelligent parsing of complex formats.")


def delete(secret_name=None):
    """Delete a secret from the vault.
    
    Args:
        secret_name: The name of the secret to delete. If None, delete all secrets.
    """
    vault = load_vault()
    
    # If no secret name provided, delete all secrets
    if secret_name is None:
        count = len(vault)
        if count > 0:
            vault.clear()
            save_vault(vault)
            print(f"[!] Deleted all {count} secrets from the vault")
        else:
            print("[*] No secrets to delete. Vault is already empty.")
        return
    
    # Delete a specific secret
    if secret_name in vault:
        del vault[secret_name]
        save_vault(vault)
        print(f"[x] Deleted secret: {secret_name}")
    else:
        print("[!] Secret not found")

def update(secret_name, new_value):
    vault = load_vault()
    if secret_name in vault:
        vault[secret_name] = new_value
        save_vault(vault)
        print(f"[~] Updated secret: {secret_name}")
    else:
        print("[!] Secret not found")

def list_secrets(debug=False):
    """List all secrets in the vault.
    
    Args:
        debug: If True, show the secret values as well as the names.
    """
    vault = load_vault()
    if not vault:
        print("[*] No secrets stored.")
    else:
        print("[*] Stored secrets:")
        for key, value in vault.items():
            if debug:
                # Show the secret value in debug mode
                # Truncate long values for better readability
                if len(value) > 30:
                    display_value = value[:27] + "..."
                else:
                    display_value = value
                print(f" - {key} = {display_value}")
            else:
                # Just show the secret name in normal mode
                print(f" - {key}")

def import_to_env(*secret_names):
    vault = load_vault()
    
    # If no arguments provided, import all secrets
    if not secret_names:
        if not vault:
            print("[!] No secrets found in vault")
            return
        
        secret_names = list(vault.keys())
        print(f"Importing all {len(secret_names)} secrets")
    
    imported_count = 0
    with open(".env", "a") as f:
        for secret_name in secret_names:
            if secret_name in vault:
                f.write(f"{secret_name}={vault[secret_name]}\n")
                print(f"[+] Imported {secret_name} to .env")
                imported_count += 1
            else:
                print(f"[!] Secret not found: {secret_name}")
    
    if imported_count > 0:
        print(f"[*] Successfully imported {imported_count} secret(s) to .env")
