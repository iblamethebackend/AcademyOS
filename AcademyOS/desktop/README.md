# AcademyOS desktop

Next.js App Router + TypeScript, with local Inter fonts, the supplied green branding, an SVG open-book identity and responsive glass surfaces. All current records and authentication flows are demonstrations. No database or external application is connected.

## Local development

```powershell
npm ci
npm run dev -- --port 3000
```

Open **http://localhost:3000**. The app starts at `/login`.

- `/login` — shared school sign-in, validation, password visibility, recovery preview, optional remembered demo session.
- `/signup` — school-invitation sign-up: invitation check → account details → confirmation preview. Roles and invited email come from the invitation, not a privilege selector.
- `/dashboard` — School Admin dashboard with campus selection, chart period, announcements, search, schedule details and local quick-action previews.
- `/setup` — school onboarding: school/campuses, academic foundations, people/imports, branding, launch checks and lifecycle previews.

Both authentication pages are designed to occupy one viewport. Shorter screens use tighter vertical spacing and fewer decorative elements; sign-up is split into two steps. Help dialogs can scroll independently when necessary.

## Demo sign-in and sign-up

On login, click **Fill demo account**, then **Sign in**:

- School: `greenfield`
- Email: `ananya@greenfield.example`
- Password: `Academy@2026`

On sign-up, click **Use demo invitation**, then **Continue**. The public demo code is `GF-TEACHER-26`; it previews a Teacher invitation for `new.teacher@greenfield.example`. `GF-EXPIRED-26` demonstrates the expired-invitation state. Fill a name, password and confirmation to review the completion state. No real account, session or email is created by sign-up; it does not grant School Admin access.

Sign-in stores a mock navigation session in sessionStorage, or localStorage when remembering the demo. Passwords are never persisted. The session lasts eight hours, or seven days for a remembered demo. The client gate is solely a UI flow, **not production authentication or an authorization boundary**. The public demo password is intentionally present in the client bundle. Backend authentication must replace this module before real school data is introduced.

Account recovery shows an explicit no-email preview. Sign out through the dashboard profile or setup profile. Browser storage failures fall back to the current tab's in-memory sign-in; setup changes may then be session-only.

## Data and implemented scope

`src/lib/model.ts` supplies typed school fixtures. `src/lib/dashboard-data.ts` supplies illustrative campus aggregates, schedules and announcements. The dashboard totals illustrate a whole campus; editable sample rosters contain only a few records. Browser storage keys are versioned and separate for setup, dashboard and demo navigation sessions.

Setup includes validated editable forms, campus management, academic calendar, CSV review with error and duplicate detection, local demo invitations, document previews, launch dependencies, JSON export and reversible lifecycle states. Dashboard quick actions create local records or previews only. No messages, payments, DNS changes or actual account deletions occur.

## Validation

```powershell
npm run build
npm run check
```

Browser scripts require Playwright and Microsoft Edge. Install `playwright` as a development dependency, or set `PLAYWRIGHT_MODULE` to an existing local installation, then run with the local server active:

```powershell
node scripts/login-review.mjs
node scripts/signup-review.mjs
node scripts/auth-layout-review.mjs
node scripts/dashboard-review.mjs
node scripts/review.mjs
```

Results and screenshots are written to the ignored `test-results/` directory. The login checks cover demo sessions, redirects, recovery, visibility, persistence, sign-out, and disabled browser storage. The sign-up checks cover invitation states, immutable invited email, password validation, no password persistence and no automatic privilege grant. Layout checks verify viewport dimensions and visible controls through validation states at desktop, tablet and phone sizes.

## Assets

- `public/brand/book-mark.svg` and `src/components/brand.tsx`: code-native interpretation of the supplied open-book brand mark; `src/app/icon.svg` is the favicon.
- `public/fonts/InterVariable.woff2`: locally served Inter from the upstream rsms/inter repository, with license in `public/fonts/OFL.txt`.
- `public/images/campus.png`: original campus image generated with the built-in image-generation tool. The image is a fictional campus, not a photograph of a particular school. The original is retained in the image-generation output directory.

Final campus image prompt:

> Photorealistic architectural photograph for a school software dashboard welcome banner. A beautiful contemporary K-12 school campus in India, elegant cream-white three-storey building with large glass windows and subtle stone panels, lush landscaped green lawn and small trees, gently blurred green leaves in upper right foreground, sunny soft morning daylight, calm pale blue white sky. Horizontal wide composition, main school building on the right two thirds, open soft sky and pale garden on left suitable to fade into white UI. No people, no signs, no lettering, no logos, no watermarks. Natural understated premium architecture photography, realistic, gently muted sage-green colors, not futuristic, no dark shadows.


## Register your school

`/signup` now offers two entries: **Register your school** and **Join your school**. Existing invitation sign-up is at `/signup/join`. School registration is at `/register-school`.

The school registration preview has four steps: owner account details, simulated email verification, school identity/contact/workspace address, and review. Use the visible verification code `246810`; no email is sent. Codes expire after five minutes in the UI and can be renewed. Passwords are checked in memory and then discarded.

Creation saves a separate browser-local school workspace with the owner as its only staff member, one main campus, no students, and no completed setup steps. It then opens `/setup`. The previous Greenfield fixture and other registered schools remain separate. A workspace address must be unique within this browser. Real global uniqueness and email verification need a backend.

To return after signing out, use the registered school code and owner email with the public UI-preview password `Academy@2026`. This deliberately remains a mock sign-in; the owner password entered during registration is never saved. Resetting a registered school's demo keeps its original identity while restoring its empty onboarding state.

Run `node scripts/registration-review.mjs` with the local server running to verify the owner-to-setup flow, isolation, duplicate addresses, password non-persistence, returning sign-in, and one-screen layouts through validation states.


## Unified school workspace and Supabase preparation

School management now lives at `/workspace`, with horizontal navigation and glass panels. `/dashboard` and legacy `/setup` routes redirect to the appropriate workspace page. There is no separate Campus dashboard entry or traditional left navigation panel. Registration and owner sign-in lead to the School Workspace.

Workspace pages: overview, school profile, campuses, academic year, people/invitations, departments, branding, launch and settings. Counts use the current local roster, and newly registered schools begin empty.

Supabase integration is prepared behind `NEXT_PUBLIC_SUPABASE_ENABLED`. See `supabase/README.md` for exact status and activation steps. Live mode remains disabled until the intended project is accessible, the schema is applied, and authentication and RLS are tested. The supplied service-role key is not part of the app.


## Stable local development

`npm run dev` explicitly uses Webpack. The previous Turbopack dev session repeatedly emitted `HMR hash mismatch` and forced full login-page reloads. A running server must be restarted to pick up the changed dev command. Browser verification with `scripts/login-stability.mjs` confirmed a single document load, retained email input for 12 seconds, working recovery navigation, and no runtime errors.

For isolated browser checks, `ACADEMYOS_ISOLATED_PREVIEW=1` uses `.next-preview` instead of the active server cache. This directory is ignored by Git.

New school registration requires a physical school address in the School step. The address appears in review and in the school profile, and is saved in local and cloud school configuration. Timezone is not requested or displayed; an address does not infer the school timezone. Run `node scripts/registration-location-review.cjs` for validation and persistence checks.

## Staff activity and assigned work

The overview includes staff submission counts and links to `/workspace/staff-activity`. School owners can assign tasks to active roster members with a due date and instructions, record received work as notes and/or files, review submissions, complete tasks, and reopen them. Filters cover member, status, overdue work and search. Staff activity means a recorded submission in the last seven days, not online presence. Each record explicitly identifies the school owner as its recorder. No notifications or staff self-service access are created.

Task records use the existing school configuration persistence and are optional for older workspaces. Daily overdue status uses the school's selected timezone. Attachments accept PDF, CSV, TXT, DOCX, XLSX, PNG and JPEG, up to 10 MB. In local preview, actual files live in IndexedDB and are available only in that browser; JSON configuration exports include attachment metadata, not file bytes. Browser data cleanup removes local files. Live uploads use a private Supabase Storage bucket with school-owner policies; apply `supabase/staff-task-storage.sql` to enable them. Upload errors remain visible and do not create a submitted task. That storage migration has not been applied or verified remotely in this session.

Validation: `node scripts/staff-tasks-review.cjs` covers old workspace compatibility, task/submission validation, completion evidence, staff activity windows, overdue status, school timezones and upload limits.

## School achievements and certificates

School profile includes Achievements & certificates above the campus list. Owners can add or edit achievements and certificate entries with a title, issuer, date and description. Certificate entries require a PDF, PNG or JPEG file (up to 10 MB); achievement entries may omit the file. Cards support search, a details/certificate preview and download. Replacing a file while editing does not discard the existing reference if upload fails.

Records persist inside the school configuration, with optional-field compatibility for older workspaces and validation on workspace saves. Files use the existing private school-owner storage configured by `supabase/staff-task-storage.sql`. Apply that migration once if the shared file bucket is not yet configured. Preview mode stores file bytes in IndexedDB; JSON exports contain metadata only. Live bucket setup, remote upload and cross-owner policies remain unverified in this environment. Existing files are retained when a record's file is replaced; file deletion is not exposed.

Run `node scripts/school-achievements-review.cjs` for metadata, file type/size, date, duplicate and compatibility checks.
