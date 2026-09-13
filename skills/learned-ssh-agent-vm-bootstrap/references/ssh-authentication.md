# SSH Authentication

Read this reference before SSH configuration, key, fingerprint, path/stat, or fresh-auth work. Apply the parent skill's hard rules, decision gates, and output contract.

## Procedure

1. Record the local account with `id -un`. Inspect the exact consumer SSH executable, arguments, config file, target, remote user, `known_hosts`, and key paths without printing environment values. Resolve named executables only with `command -v`; preserve nonzero results. Run `ssh -G` with the consumer's actual options/config and inspect every effective `identityfile`. Check agent accessibility with `ssh-add -l` (status/fingerprint only); verify each key is readable and its public/private fingerprints match without emitting key material.
2. Inventory actual paths before metadata checks. Report missing config, key, or public key explicitly. If an existing path is available, detect `stat` capability separately (BSD `-f` versus GNU `-c`) on that path, then collect permissions; never infer the platform from a missing-file error.
3. Verify the trusted host fingerprint against `known_hosts`. Run the exact consumer SSH executable with its exact arguments/config as one test, separately from this fresh-auth proof:

   ```bash
   "$ssh_bin" -F "$ssh_config" -o ControlPath=none -o ControlMaster=no -o BatchMode=yes -o StrictHostKeyChecking=yes "$target" 'id -un'
   ```

   Include `-F` only when it is the consumer's actual config. Do not replace either result with an interactive command or stale control connection.
