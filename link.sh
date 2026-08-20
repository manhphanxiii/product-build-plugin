#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="$SCRIPT_DIR/skills"
LAVISH_DIR="$SCRIPT_DIR/lavish-axi/skills/lavish"
DESTINATIONS=("${HOME}/.claude/skills" "${HOME}/.agents/skills")
SOURCES=()

while IFS= read -r -d '' skill_file; do
  SOURCES+=("$(dirname "$skill_file")")
done < <(find "$SKILLS_DIR" -mindepth 2 -maxdepth 2 -name SKILL.md -print0)
SOURCES+=("$LAVISH_DIR")

if [[ ${#SOURCES[@]} -ne 10 ]]; then
  echo "Expected 10 skills, found ${#SOURCES[@]}."
  exit 1
fi

echo "Plan:"
for destination in "${DESTINATIONS[@]}"; do
  for source in "${SOURCES[@]}"; do
    name="$(basename "$source")"
    target="$destination/$name"
    echo "  $target -> $source"
    if [[ "$name" == "prototype" || "$name" == "implement" ]] && [[ -e "$target" || -L "$target" ]]; then
      echo "  WARNING: $target already exists and will be replaced."
    fi
  done
done

read -r -p "Continue? [y/N] " answer
if [[ ! "$answer" =~ ^[Yy]$ ]]; then
  echo "Cancelled."
  exit 0
fi

for destination in "${DESTINATIONS[@]}"; do
  mkdir -p "$destination"
  if [[ -L "$destination" ]]; then
    resolved="$(cd "$destination" && pwd -P)"
    case "$resolved/" in
      "$SCRIPT_DIR"/*)
        echo "Refusing destination that points back into this package: $destination"
        exit 1
        ;;
    esac
  fi
  for source in "${SOURCES[@]}"; do
    name="$(basename "$source")"
    target="$destination/$name"
    if [[ -e "$target" || -L "$target" ]]; then
      rm -rf "$target"
    fi
    ln -s "$source" "$target"
  done
done

echo "Linked 10 skills into each destination."
