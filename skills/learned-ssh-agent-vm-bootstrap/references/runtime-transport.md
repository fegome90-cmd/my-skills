# Runtime Transport

Read this reference before executable discovery, listener/tunnel, HTTP/WebSocket/authenticated protocol, UI/backend identity, or authorized mutation, snapshot, or rollback work. Apply the parent skill's hard rules, decision gates, and output contract.

## Procedure

1. Discover the remote executable with a quoted non-interactive SSH command whose only lookup is `command -v <name>`; preserve its exit status. Probe the exact configured path safely, without sourcing startup files or printing PATH.
2. Discover endpoint and protocol from the consumer configuration/runtime; do not guess a health path. Verify local listener ownership and the SSH forward's remote target. Use bounded HTTP, for example:

   ```bash
   curl --fail --silent --show-error --connect-timeout 2 --max-time 5 -- "$health_url"
   ```

   Require a minimal authenticated exchange using the consumer's credential source. Record only status/safe metadata; stop if auth is unavailable. If the protocol is WebSocket, prove its authenticated upgrade, not merely TCP/HTTP reachability; finish with UI/backend identity.
3. After authorized changes, compare fresh state with the snapshot, rerun all applicable layers, report unrelated dirty state, and roll back on regression. Never claim success from a partial layer.
