# Template: Non-destructive macOS Keychain Secret Loader
# Place in: ~/.config/fish/conf.d/<service_name>-keychain.fish

if test (uname) = Darwin
    # 1. Silently extract secret from macOS Keychain
    set -l secret_val (security find-generic-password -a "$USER" -s "<KEYCHAIN_SERVICE_NAME>" -w 2>/dev/null)
    
    # 2. Only export if query succeeded and key is non-empty
    if test $status -eq 0; and test -n "$secret_val"
        set -gx <ENV_VAR_NAME> $secret_val
    end
end
