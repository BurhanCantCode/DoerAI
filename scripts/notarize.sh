#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VERSION="${ORANGE_VERSION:-0.9.0-beta.1}"
APP_NAME="${APP_NAME:-Orange}"
DMG_PATH="${NOTARIZE_TARGET_DMG:-$ROOT_DIR/dist/${APP_NAME}-${VERSION}.dmg}"
PKG_PATH="${NOTARIZE_TARGET_PKG:-$ROOT_DIR/dist/${APP_NAME}-${VERSION}.pkg}"

if [[ ! -f "$DMG_PATH" ]]; then
  echo "[notarize] DMG not found: $DMG_PATH"
  exit 1
fi

if ! command -v xcrun >/dev/null 2>&1; then
  echo "[notarize] xcrun not found. Install Xcode command line tools."
  exit 1
fi

submit_for_notarization() {
  local target="$1"
  echo "[notarize] Submitting $target"
  if [[ -n "${APPLE_NOTARY_PROFILE:-}" ]]; then
    xcrun notarytool submit "$target" \
      --keychain-profile "$APPLE_NOTARY_PROFILE" \
      --wait
  else
    : "${APPLE_ID:?APPLE_ID required when APPLE_NOTARY_PROFILE is not set}"
    : "${APPLE_TEAM_ID:?APPLE_TEAM_ID required when APPLE_NOTARY_PROFILE is not set}"
    : "${APPLE_APP_SPECIFIC_PASSWORD:?APPLE_APP_SPECIFIC_PASSWORD required when APPLE_NOTARY_PROFILE is not set}"
    xcrun notarytool submit "$target" \
      --apple-id "$APPLE_ID" \
      --team-id "$APPLE_TEAM_ID" \
      --password "$APPLE_APP_SPECIFIC_PASSWORD" \
      --wait
  fi
}

submit_for_notarization "$DMG_PATH"

echo "[notarize] Stapling DMG ticket..."
xcrun stapler staple "$DMG_PATH"

echo "[notarize] Verifying notarized DMG..."
spctl -a -vv -t open "$DMG_PATH"

if [[ -f "$PKG_PATH" ]]; then
  submit_for_notarization "$PKG_PATH"
  echo "[notarize] Stapling PKG ticket..."
  xcrun stapler staple "$PKG_PATH"
  echo "[notarize] Verifying notarized PKG..."
  spctl -a -vv -t install "$PKG_PATH"
else
  echo "[notarize] PKG not found, skipping: $PKG_PATH"
fi

echo "[notarize] Complete."
