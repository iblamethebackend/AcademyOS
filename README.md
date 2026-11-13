# AcademyOS

School workspace application, mobile prototype, design assets, and product documentation.

- [Desktop application](AcademyOS/desktop): Next.js and TypeScript school workspace with Supabase integration.
- [Mobile prototype](AcademyOS/mobile): React Native / Expo application.
- [Design and product documentation](AcademyOS/README.md): blueprints, requirements, screen galleries, and generators.
- [Original deliverables](deliverables/README.md): preserved CampusOS reference materials.

## Run the desktop application

```powershell
cd AcademyOS/desktop
npm ci
Copy-Item .env.example .env.local
npm run dev -- --port 3000
```

Configure the public Supabase settings in `.env.local` for your project. See the [Supabase setup notes](AcademyOS/desktop/supabase/README.md) and the [desktop README](AcademyOS/desktop/README.md) for setup and current implementation scope. Open http://localhost:3000.

Local environment files, credentials, dependency folders, build output, verification screenshots, and generated ZIP packs are excluded from Git. No management token is required in the application or its browser bundle.
