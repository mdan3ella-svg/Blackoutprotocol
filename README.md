# OPERATION BLACKOUT PROTOCOL — VERTASCAN | GitHub deployment edition v6

## What changed
The HTML no longer uses CDNs for Three.js or Google Fonts. Exact Three.js version **0.170.0** is a build-time dependency, vendored by a GitHub Actions workflow into `vendor/three` before publication. After deployment, game runtime references only local assets and local JS modules. The first build requires network access on GitHub Actions to install the pinned package.

**Important:** This source ZIP does NOT contain the downloaded Three.js module files; it becomes an entirely local-dependency site only *after* the workflow has run. For a local offline build run `npm install && npm run build`, then serve it through `http://localhost` (ES modules and WebGL asset loading do not reliably run via `file://`). After vendor generation, you may copy the complete published site to an offline local server. The soundtrack, JPG, and supplied original GLB files are included.

## GitHub Pages
1. Upload contents of this folder (including hidden `.github` folder) to the repository **root** on branch `main`.
2. Repository Settings → Pages → Build and deployment → **Source: GitHub Actions**.
3. Push/commit changes, then check Actions → **Publish BLACKOUT PROTOCOL** for the deployment.
4. Load the published URL. No external runtime requests are required by the game.

If using a different default branch, adjust `.github/workflows/pages.yml`.

## Original assets
`blue.glb` (Sentinel), `mantaray-XHD.glb` (Manta), `blackoutprotocol.jpg` (splash), and `blackoutprotocol.mp3` (soundtrack) are preserved.

## Desktop controls
WASD: thrust; mouse: aim; Space/X: ascend/descend; Shift: surge; C: cloak; F: null-drop; mouse left: fire; right hold: rail charge; E: EMP; 1/2: weapons; P/Escape: pause. Touch controls are included for mobile.

## Checks and limits
The CI script verifies vendored module presence, local imports, original asset inventory, and GLB 2.0 headers. JS syntax is checked separately during packaging. This is not a substitute for real GPU gameplay regression tests across all five missions and desktop/mobile devices. SSAO/SSR fidelity and framerate depend on the browser GPU; the game supports quality presets and a limited Ultra fallback. Not a certified 5A+ commercial release.
