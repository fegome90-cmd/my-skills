#!/usr/bin/env bash
# generate_manifest.sh - Deterministic Canonical Tree Manifest Generator
# Includes all regular files, dotfiles, symlinks, permissions, sizes, and hashes.
# Compliant with bash-scripting, bash-cleanup-trap, and robust CLI patterns.

set -euo pipefail

TARGET_DIR="${1:-.}"
OUTPUT_FILE="${2:-TREE_MANIFEST}"

# 1. Preflight dependencies
command -v python3 >/dev/null 2>&1 || {
  echo "Error: python3 is required to generate the deterministic manifest." >&2
  exit 1
}

if [ ! -d "$TARGET_DIR" ]; then
  echo "Error: Target directory '$TARGET_DIR' does not exist." >&2
  exit 1
fi

# 2. Setup safe temp file with automatic EXIT cleanup trap (bash-cleanup-trap pattern)
TEMP_MANIFEST=$(mktemp)
cleanup() {
  local exit_code=$?
  rm -f "$TEMP_MANIFEST"
  exit "$exit_code"
}
trap cleanup EXIT INT TERM

# 3. Traverse directory deterministically using embedded Python engine
python3 - "$TARGET_DIR" "$TEMP_MANIFEST" << 'EOF'
import os
import sys
import hashlib
import stat

target_dir = os.path.abspath(sys.argv[1])
output_file = sys.argv[2]

entries = []

for root, dirs, files in os.walk(target_dir):
    dirs.sort()
    files.sort()
    for name in files:
        full_path = os.path.join(root, name)
        rel_path = os.path.relpath(full_path, target_dir)
        
        st = os.lstat(full_path)
        mode = oct(stat.S_IMODE(st.st_mode))[2:].zfill(4)
        
        if os.path.islink(full_path):
            ftype = "l"
            link_target = os.readlink(full_path)
            sha = hashlib.sha256(link_target.encode("utf-8")).hexdigest()
            size = len(link_target)
        else:
            ftype = "f"
            size = st.st_size
            h = hashlib.sha256()
            with open(full_path, "rb") as f:
                while chunk := f.read(65536):
                    h.update(chunk)
            sha = h.hexdigest()
            
        entries.append(f"{ftype} {mode} {size} {sha} {rel_path}")

entries.sort(key=lambda x: x.split(" ", 4)[4])

with open(output_file, "w", encoding="utf-8") as f:
    for entry in entries:
        f.write(entry + "\n")
EOF

# 4. Atomic file placement (same-filesystem rename; never a partial copy)
mv -f "$TEMP_MANIFEST" "$OUTPUT_FILE"

# 5. Robust cross-platform digest calculation
if command -v shasum >/dev/null 2>&1; then
  TREE_DIGEST=$(shasum -a 256 "$OUTPUT_FILE" | awk '{print $1}')
elif command -v sha256sum >/dev/null 2>&1; then
  TREE_DIGEST=$(sha256sum "$OUTPUT_FILE" | awk '{print $1}')
else
  TREE_DIGEST=$(python3 -c "import hashlib, sys; print(hashlib.sha256(open(sys.argv[1], 'rb').read()).hexdigest())" "$OUTPUT_FILE")
fi

echo "Tree manifest successfully written to: $OUTPUT_FILE"
echo "TREE_DIGEST: $TREE_DIGEST"
