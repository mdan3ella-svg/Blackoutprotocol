# BLACKOUT PROTOCOL v6 — Regression Audit (2026-10-30)

## Verdict: NOT RELEASE-CERTIFIED / FULL GPU REGRESSION BLOCKED

The requested end-to-end GPU regression was **not** completed. The unzipped source distribution contains no `vendor/three` directory. It is a **CI build-input package**, not directly bootable as-is. The environment could not download the pinned npm package because DNS/network access was unavailable. Consequently neither full gameplay nor visual/performance claims can be certified.

## Executed checks

- **PASS:** `node --check` on the module script and both build/test scripts.
- **PASS:** Existing assets physically present and readable, including Sentinel and Manta GLBs, soundtrack, and title art.
- **PASS:** GLB headers indicate valid v2 containers with exact length fields. (This does not prove geometry, animation or skinning quality.)
- **PASS (static only):** The source defines five mission records. No mission was actually played or cleared.
- **PASS (DOM only):** Desktop 1440×900, mobile 390×844 and tablet 820×1180 exposed core menu/control elements and did not horizontally overflow when the DOM was loaded in browser isolation.
- **BLOCKED:** Chromium software WebGL context creation did not succeed in the current runtime.
- **BLOCKED:** Full Three.js import/boot and all 5 mission runtime paths. Loading HTML in browser isolation produces an import-map/module resolution error; the missing `vendor/three` folder also blocks direct hosting of extracted ZIP.
- **NOT TESTED:** Mission objectives/transition and completion, enemy AI and attack collisions, all weapons, HUD changes, saved progress, mouse/keyboard/touch controls in-game, SSAO/SSR/bloom rendering, GPU frame time, long-session leaks, Android/iOS hardware FPS.

## Production acceptance test matrix (still outstanding)

| Area | Procedure | Acceptance |
|---|---|---|
| Boot | Build with `npm ci`/`npm install` followed by `npm run build`, deploy to HTTP server | No network/CDN fetches and no console errors; both models rendered |
| Five missions | Enter and complete missions 01–05 with scripted objectives; retry and resume | Objectives, timer, transitions, unlocks and finale correct |
| Controls | Desktop keyboard/mouse pointer lock, firing, cloak, surge, freefall, EMP, pause; touch modes | Every control fires exactly once, no stuck input after pause |
| Rendering | PERFORMANCE/HIGH/ULTRA, SSAO, SSR, bloom, device loss/recovery, resize | No black viewport, shader errors or divergent display |
| Frame pacing | Record 1% low/median FPS, p95 GPU frame time after 5-minute run per mission/profile | Meet device-specific budgets after measured baseline; no unbounded growth |
| Mobile | Real Android Chrome and iOS Safari portrait/landscape, rotation, tilt permission | Layout accessible, input responsive, stable sustained frame pacing |
| Persistence | Reload after each mission and mute/quality changes | Unlocked missions and settings restored correctly |

## Deployment note

GitHub Pages workflow references `npm install`, `npm run build`, and copies the resulting `vendor` directory into `dist`. This can produce a no-runtime-CDN hosted site if CI completes successfully. Do not label an extracted source ZIP 'fully offline' without the dependency files already present. For deterministic releases, commit `package-lock.json` and use `npm ci`.
