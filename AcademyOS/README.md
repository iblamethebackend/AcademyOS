# AcademyOS

Desktop redesign and React Native / Expo UI prototype · 11 November 2026.

## Start here

- **AcademyOS-Design-Review.pdf** — 23-page visual review: desktop direction, mobile welcome, 18 role workspaces and design foundations. Screens are captured from the running Expo web prototype.
- **AcademyOS-Mobile-Gallery.jpg** — welcome, parent, student, teaching, finance and transport at a glance.
- **AcademyOS-School-SaaS-Blueprint.pdf** — refreshed 71-page blueprint retaining 23 original screen concepts, 24 domains and 144 requirements.
- **screens/** and **AcademyOS-Screen-Gallery.jpg** — refreshed original concepts.
- **previews/** — rendered Expo screenshots, including desktop and 320 px phone views.
- **mobile/** — React Native / Expo TypeScript source, lockfile and built browser preview in `dist/`.

The original CampusOS files remain unchanged in the sibling `deliverables/` directory. AcademyOS is the new product name. The design review and prototype establish the refined direction; the blueprint preserves the detailed operational specification.

## Design and scope

Warm ivory, botanical green, sage, sand and lilac. Light desktop navigation, expressive summary panels, quiet white surfaces and a floating mobile dock. iOS uses Expo BlurView with a Reduced Transparency fallback. Android and web use a near-opaque surface for legibility. This is Apple-inspired glass styling, not native Apple Liquid Glass. Desktop navigation appears from 1000 px.

Mobile workspaces: Parent, Student, Teaching, Admissions, Student office, Academics, Examinations, Finance, People & HR, Communications, Transport, Library, Inventory, Health & wellbeing, Front office, Hostel & meals, School leadership and School IT.

There is no platform operator or control-panel entry in mobile. School leadership is a school role. School IT exposes school task navigation, not tenant administration or platform secrets. The desktop blueprint retains its separate platform-operations specification.

Workspace selection is a demo selector, not authentication. Production sign-in must derive assigned workspaces from the server; choosing a role must never grant permissions. Guardian relationships, class assignments, campus scope and sensitive record access require backend enforcement.

## Run

From `AcademyOS/mobile`:

```powershell
npm ci
npm start
```

Use `npm run web` for browser preview. To view the included static build from the workspace root:

```powershell
python -m http.server 8765 --bind 127.0.0.1 --directory AcademyOS/mobile/dist
```

Visit http://127.0.0.1:8765. A server is required; opening `dist/index.html` directly is unsupported.

## Working UI and remaining implementation

Working locally: welcome, 18 workspace variants, role switching, tabs, module filtering and empty state, task detail sheets, marking tasks reviewed, message details/read state, profile and return to welcome. State resets on workspace change and does not persist between sessions.

Module sheets are navigation concepts. Real sign-in, school records, child switching, payments, uploads, live transport, message delivery, approvals and detailed module forms are not implemented. All data and charts are fictional. Reviewing a task does not complete a real school action. The blueprint specifies the deeper workflows.

## Verification

- Blueprint: 71 pages, 144 unique requirements, 23 concepts; bookmarks, links, bounds and paragraph fit passed.
- Design review: 23 pages, 18 workspaces; no out-of-page text.
- TypeScript passed (`npm run check`).
- Expo web, iOS and Android bundle exports passed. These are bundling checks, not native app builds or device tests.
- Browser checks passed at 390, 320 and 1440 px: role switching, task review, module opening, search empty state, inbox read state and horizontal overflow. See `ui-verification.json`.
- Native blur, device safe areas, screen readers and Android runtime still require hardware review.

Expo SDK 55 currently recommends React Native 0.83.10; this installation uses 0.83.2. Updating that patch was blocked by registry access. Before native distribution, run `npx expo install --fix` with network access, rebuild and test on devices. The lockfile reproduces the tested dependencies.

To rerun screenshots, install `playwright` as a dev dependency, use local Edge, start the preview server, then run `node review.mjs` from `mobile/`. This session used an existing local Playwright package through `PLAYWRIGHT_MODULE` because downloading the review dependency was unavailable.

## Rebuild documents

Python dependencies: `source/requirements.txt`. Generators reference locally installed Windows Segoe UI fonts; fonts are not bundled.

```powershell
python AcademyOS/source/build_blueprint.py
python AcademyOS/source/verify_and_export.py
python AcademyOS/source/build_design_book.py
python AcademyOS/source/package.py
```

The design review requires `previews/` screenshots. `redesign.py` recreates the refreshed blueprint source from the preserved original files and is unnecessary for routine builds.

Implementation references: [Expo BlurView](https://docs.expo.dev/versions/v55.0.0/sdk/blur-view/), [Expo LinearGradient](https://docs.expo.dev/versions/v55.0.0/sdk/linear-gradient/).
