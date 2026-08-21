#!/usr/bin/env bash

set -euo pipefail

PLUGIN_NAME="build"
MODE="symlink"
ACTION="install"
DRY_RUN=0
ALLOW_PLUGIN_DUPLICATE=0
REQUESTED_REF=""
SOURCE_OVERRIDE=""
DEST_OVERRIDE=""

usage() {
  printf '%s\n' \
    "Usage: install-codex.sh [options]" \
    "" \
    "Install the build skills as standalone Codex skills." \
    "This is a fallback for development and pre-publication cloud testing." \
    "" \
    "Options:" \
    "  --copy                    Copy skills instead of creating symlinks." \
    "  --dry-run                 Print actions without changing files." \
    "  --source PATH             Use an explicit plugin checkout." \
    "  --dest PATH               Override the Codex skill directory." \
    "  --ref TAG_OR_COMMIT       Require source HEAD to match a Git ref." \
    "  --uninstall               Remove only installer-managed entries." \
    "  --allow-plugin-duplicate  Permit duplicates for isolated tests." \
    "  --help                    Show this help."
}

# Install the build skills as standalone Codex skills.
#
# This is a fallback for development and pre-publication Codex Cloud testing.
# Production users should install the universal build plugin instead.
#
# Usage:
#   install-codex.sh [--copy] [--dry-run] [--source PATH] [--dest PATH]
#                    [--ref TAG_OR_COMMIT] [--uninstall]
#
# Options:
#   --copy       Copy managed skill folders instead of creating symlinks.
#   --dry-run    Print the complete action set without changing files.
#   --source     Use an explicit product-build-plugin checkout.
#   --dest       Override the Codex skill directory.
#   --ref        Require the source checkout HEAD to match this Git ref.
#   --uninstall  Remove only entries previously managed by this installer.
#   --allow-plugin-duplicate
#                Permit standalone installation when the build plugin appears
#                in `codex plugin list`. Intended only for isolated tests.
#   --help       Show this help.

while [ "$#" -gt 0 ]; do
  case "$1" in
    --copy)
      MODE="copy"
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --source)
      [ "$#" -ge 2 ] || { echo "error: --source requires a path" >&2; exit 2; }
      SOURCE_OVERRIDE="$2"
      shift 2
      ;;
    --dest)
      [ "$#" -ge 2 ] || { echo "error: --dest requires a path" >&2; exit 2; }
      DEST_OVERRIDE="$2"
      shift 2
      ;;
    --ref)
      [ "$#" -ge 2 ] || { echo "error: --ref requires a tag or commit" >&2; exit 2; }
      REQUESTED_REF="$2"
      shift 2
      ;;
    --uninstall)
      ACTION="uninstall"
      shift
      ;;
    --allow-plugin-duplicate)
      ALLOW_PLUGIN_DUPLICATE=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      echo "error: unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)
DEFAULT_SOURCE=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd -P)
SOURCE_ROOT=${SOURCE_OVERRIDE:-$DEFAULT_SOURCE}

if [ ! -d "$SOURCE_ROOT" ]; then
  echo "error: source checkout does not exist: $SOURCE_ROOT" >&2
  exit 1
fi
SOURCE_ROOT=$(CDPATH= cd -- "$SOURCE_ROOT" && pwd -P)

if [ -n "$DEST_OVERRIDE" ]; then
  DEST_ROOT="$DEST_OVERRIDE"
else
  : "${HOME:?HOME must be set when --dest is omitted}"
  DEST_ROOT="$HOME/.agents/skills"
fi

MANIFEST_PATH="$DEST_ROOT/.${PLUGIN_NAME}-managed"
MARKER_NAME=".${PLUGIN_NAME}-plugin-owner"
TEMP_ROOT=$(mktemp -d "${TMPDIR:-/tmp}/${PLUGIN_NAME}-install.XXXXXX")
SKILL_LIST="$TEMP_ROOT/skills"
OLD_SKILL_LIST="$TEMP_ROOT/old-skills"
STALE_LIST="$TEMP_ROOT/stale-skills"
COLLISION_LIST="$TEMP_ROOT/collisions"
BACKUP_ROOT="$TEMP_ROOT/backup"
STAGE_ROOT="$TEMP_ROOT/stage"
CHANGED_LIST="$TEMP_ROOT/changed"

: > "$SKILL_LIST"
: > "$OLD_SKILL_LIST"
: > "$STALE_LIST"
: > "$COLLISION_LIST"
: > "$CHANGED_LIST"

cleanup() {
  rm -rf -- "$TEMP_ROOT"
}
trap cleanup EXIT

is_managed_copy() {
  local destination=$1
  local skill_name=$2
  local marker="$destination/$MARKER_NAME"
  [ -f "$marker" ] || return 1
  grep -Fxq "plugin=$PLUGIN_NAME" "$marker" || return 1
  grep -Fxq "source=$SOURCE_ROOT" "$marker" || return 1
  grep -Fxq "skill=$skill_name" "$marker"
}

is_managed_symlink() {
  local destination=$1
  local source_skill=$2
  local raw_target target_dir target_base resolved_target
  [ -L "$destination" ] || return 1
  raw_target=$(readlink "$destination")
  if [[ "$raw_target" = /* ]]; then
    target_dir=$(dirname -- "$raw_target")
    target_base=$(basename -- "$raw_target")
  else
    target_dir=$(dirname -- "$destination")/$(dirname -- "$raw_target")
    target_base=$(basename -- "$raw_target")
  fi
  [ -d "$target_dir" ] || return 1
  resolved_target=$(CDPATH= cd -- "$target_dir" && printf '%s/%s\n' "$(pwd -P)" "$target_base")
  [ "$resolved_target" = "$source_skill" ]
}

is_safe_managed_entry() {
  local destination=$1
  local skill_name=$2
  local source_skill="$SOURCE_ROOT/skills/$skill_name"
  is_managed_symlink "$destination" "$source_skill" || is_managed_copy "$destination" "$skill_name"
}

read_manifest() {
  [ -f "$MANIFEST_PATH" ] || return 0
  sed -n 's/^skill=//p' "$MANIFEST_PATH" | LC_ALL=C sort -u > "$OLD_SKILL_LIST"
}

if [ "$ACTION" = "uninstall" ]; then
  read_manifest
  if [ ! -s "$OLD_SKILL_LIST" ]; then
    echo "skipped: no managed standalone skills found in $DEST_ROOT"
    exit 0
  fi
  while IFS= read -r skill_name; do
    destination="$DEST_ROOT/$skill_name"
    if { [ -e "$destination" ] || [ -L "$destination" ]; } && \
      ! is_safe_managed_entry "$destination" "$skill_name"; then
      printf '%s\n' "$destination" >> "$COLLISION_LIST"
    fi
  done < "$OLD_SKILL_LIST"
  if [ -s "$COLLISION_LIST" ]; then
    echo "error: refusing to remove entries whose ownership cannot be verified:" >&2
    sed 's/^/  - /' "$COLLISION_LIST" >&2
    echo "No changes were made." >&2
    exit 1
  fi
  while IFS= read -r skill_name; do
    destination="$DEST_ROOT/$skill_name"
    if [ ! -e "$destination" ] && [ ! -L "$destination" ]; then
      echo "skipped: $skill_name (already absent)"
    elif is_safe_managed_entry "$destination" "$skill_name"; then
      if [ "$DRY_RUN" -eq 1 ]; then
        echo "would remove: $destination"
      else
        rm -rf -- "$destination"
        echo "removed: $destination"
      fi
    fi
  done < "$OLD_SKILL_LIST"
  if [ "$DRY_RUN" -eq 1 ]; then
    echo "would remove manifest: $MANIFEST_PATH"
  else
    rm -f -- "$MANIFEST_PATH"
  fi
  exit 0
fi

if [ ! -d "$SOURCE_ROOT/skills" ] || [ ! -f "$SOURCE_ROOT/.codex-plugin/plugin.json" ]; then
  echo "error: source is not a dual-host build plugin checkout: $SOURCE_ROOT" >&2
  exit 1
fi

if [ -n "$REQUESTED_REF" ]; then
  if ! git -C "$SOURCE_ROOT" rev-parse --verify "$REQUESTED_REF^{commit}" >/dev/null 2>&1; then
    echo "error: Git ref does not exist in source checkout: $REQUESTED_REF" >&2
    exit 1
  fi
  REQUESTED_COMMIT=$(git -C "$SOURCE_ROOT" rev-parse "$REQUESTED_REF^{commit}")
  SOURCE_COMMIT=$(git -C "$SOURCE_ROOT" rev-parse HEAD)
  if [ "$REQUESTED_COMMIT" != "$SOURCE_COMMIT" ]; then
    echo "error: source HEAD $SOURCE_COMMIT does not match requested ref $REQUESTED_REF ($REQUESTED_COMMIT)" >&2
    exit 1
  fi
fi

if [ "$ALLOW_PLUGIN_DUPLICATE" -eq 0 ] && command -v codex >/dev/null 2>&1; then
  if codex plugin list 2>/dev/null | grep -Eq '(^|[[:space:]])build(@|[[:space:]]|$)'; then
    echo "error: the build universal plugin is already installed; standalone fallback would create duplicate skills" >&2
    exit 1
  fi
fi

find "$SOURCE_ROOT/skills" -mindepth 2 -maxdepth 2 -type f -name SKILL.md -print \
  | sed 's#/SKILL.md$##' \
  | sed 's#^.*/##' \
  | LC_ALL=C sort -u > "$SKILL_LIST"

if [ "$(wc -l < "$SKILL_LIST" | tr -d ' ')" -ne 10 ]; then
  echo "error: expected 10 skills in $SOURCE_ROOT/skills" >&2
  exit 1
fi

read_manifest
comm -23 "$OLD_SKILL_LIST" "$SKILL_LIST" > "$STALE_LIST"

while IFS= read -r skill_name; do
  destination="$DEST_ROOT/$skill_name"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    if ! is_safe_managed_entry "$destination" "$skill_name"; then
      printf '%s\n' "$destination" >> "$COLLISION_LIST"
    fi
  fi
done < "$SKILL_LIST"

while IFS= read -r skill_name; do
  [ -n "$skill_name" ] || continue
  destination="$DEST_ROOT/$skill_name"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    if ! is_safe_managed_entry "$destination" "$skill_name"; then
      printf '%s\n' "$destination" >> "$COLLISION_LIST"
    fi
  fi
done < "$STALE_LIST"

if [ -s "$COLLISION_LIST" ]; then
  echo "error: refusing to overwrite unmanaged Codex skill entries:" >&2
  sed 's/^/  - /' "$COLLISION_LIST" >&2
  echo "No changes were made." >&2
  exit 1
fi

if [ "$DRY_RUN" -eq 1 ]; then
  while IFS= read -r skill_name; do
    destination="$DEST_ROOT/$skill_name"
    if [ -e "$destination" ] || [ -L "$destination" ]; then
      echo "would update: $destination ($MODE)"
    else
      echo "would install: $destination ($MODE)"
    fi
  done < "$SKILL_LIST"
  while IFS= read -r skill_name; do
    [ -n "$skill_name" ] && echo "would remove stale: $DEST_ROOT/$skill_name"
  done < "$STALE_LIST"
  echo "would write manifest: $MANIFEST_PATH"
  exit 0
fi

mkdir -p -- "$STAGE_ROOT" "$BACKUP_ROOT" "$DEST_ROOT"

while IFS= read -r skill_name; do
  source_skill="$SOURCE_ROOT/skills/$skill_name"
  if [ "$MODE" = "symlink" ]; then
    ln -s -- "$source_skill" "$STAGE_ROOT/$skill_name"
  else
    cp -R -- "$source_skill" "$STAGE_ROOT/$skill_name"
    {
      printf 'plugin=%s\n' "$PLUGIN_NAME"
      printf 'source=%s\n' "$SOURCE_ROOT"
      printf 'skill=%s\n' "$skill_name"
    } > "$STAGE_ROOT/$skill_name/$MARKER_NAME"
  fi
done < "$SKILL_LIST"

rollback() {
  local skill_name destination
  while IFS= read -r skill_name; do
    [ -n "$skill_name" ] || continue
    destination="$DEST_ROOT/$skill_name"
    rm -rf -- "$destination"
    if [ -e "$BACKUP_ROOT/$skill_name" ] || [ -L "$BACKUP_ROOT/$skill_name" ]; then
      mv -- "$BACKUP_ROOT/$skill_name" "$destination"
    fi
  done < "$CHANGED_LIST"
  if [ -f "$BACKUP_ROOT/manifest" ]; then
    mv -- "$BACKUP_ROOT/manifest" "$MANIFEST_PATH"
  else
    rm -f -- "$MANIFEST_PATH"
  fi
}
trap 'rollback; cleanup' ERR

if [ -f "$MANIFEST_PATH" ]; then
  mv -- "$MANIFEST_PATH" "$BACKUP_ROOT/manifest"
fi

while IFS= read -r skill_name; do
  destination="$DEST_ROOT/$skill_name"
  if [ "$MODE" = "symlink" ] && is_managed_symlink "$destination" "$SOURCE_ROOT/skills/$skill_name"; then
    rm -rf -- "$STAGE_ROOT/$skill_name"
    echo "skipped: $destination (already linked)"
    continue
  fi
  printf '%s\n' "$skill_name" >> "$CHANGED_LIST"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    mv -- "$destination" "$BACKUP_ROOT/$skill_name"
    status="updated"
  else
    status="installed"
  fi
  mv -- "$STAGE_ROOT/$skill_name" "$destination"
  echo "$status: $destination ($MODE)"
done < "$SKILL_LIST"

while IFS= read -r skill_name; do
  [ -n "$skill_name" ] || continue
  destination="$DEST_ROOT/$skill_name"
  printf '%s\n' "$skill_name" >> "$CHANGED_LIST"
  mv -- "$destination" "$BACKUP_ROOT/$skill_name"
  echo "removed stale: $destination"
done < "$STALE_LIST"

{
  printf 'plugin=%s\n' "$PLUGIN_NAME"
  printf 'source=%s\n' "$SOURCE_ROOT"
  printf 'mode=%s\n' "$MODE"
  while IFS= read -r skill_name; do
    printf 'skill=%s\n' "$skill_name"
  done < "$SKILL_LIST"
} > "$MANIFEST_PATH"

trap cleanup EXIT
echo "complete: 10 standalone fallback skills managed in $DEST_ROOT"
