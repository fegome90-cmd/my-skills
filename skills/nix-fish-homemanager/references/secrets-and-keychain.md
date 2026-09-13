# Secrets & macOS Keychain Integration Pattern

## 1. The Threat Model: Secrets in `/nix/store`

In Nix, any variable, file, or string interpolated into a `.nix` expression becomes an immutable derivation output in `/nix/store/<hash>-<name>`.
* **Store Permissions:** `/nix/store` entries are world-readable (`0444`).
* **Source Exposure vs Store Exposure:** Committing a secret to Git creates *source exposure*; evaluating it with Nix creates *store exposure* (propagates across derivations and garbage-collection snapshots).
* **Golden Rule:** Nix configuration files must be 100% free of plaintext API keys, tokens, and private credentials.

---

## 2. The Non-Destructive macOS Keychain Loader Pattern

To inject secrets into environment variables at runtime without writing them to disk:

1. **Store credentials securely in macOS Keychain:**
   ```bash
   security add-generic-password -a "$USER" -s "ollama-api-key" -w "sk-..." -U
   security add-generic-password -a "$USER" -s "api-service-token" -w "token-..." -U
   ```

2. **Load dynamically in `conf.d/<name>-keychain.fish`:**
   ```fish
   # File: ~/.config/fish/conf.d/ollama-keychain.fish
   if test (uname) = Darwin
       # Query Keychain silently; suppress errors if not found
       set -l key (security find-generic-password -a "$USER" -s "ollama-api-key" -w 2>/dev/null)
       if test $status -eq 0; and test -n "$key"
           set -gx OLLAMA_API_KEY $key
       end
   end
   ```

---

## 3. Safe Verification Protocol (Zero Log Exposure)

Never print full secret tokens to terminal logs or AI transcripts. Verify existence and length safely:

```fish
# Check if variable is loaded in memory
test -n "$OLLAMA_API_KEY" && echo "✅ OLLAMA_API_KEY is loaded" || echo "❌ Missing"

# Check Keychain generic password status without printing password
security find-generic-password -a "$USER" -s "ollama-api-key" >/dev/null 2>&1 && echo "✅ Keychain entry exists"
```
