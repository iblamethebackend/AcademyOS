# Supabase connection

Intended project: `gbmnaunmwczatheeqjil`.

The project URL and supplied public anon key are configured in ignored `.env.local`. The provided service-role key was not saved or used by application code. It is not needed for the owner-scoped integration.

## Current verification status

- Official `@supabase/supabase-js` 2.119.0 and `@supabase/ssr` 0.12.7 installed and pinned; registry archive integrity verified.
- Next.js production build and TypeScript checks pass.
- The project's HTTP gateway responds to an unauthenticated health request with the expected missing-key response.
- The connected Supabase account does **not** have permission to inspect this project. No schema changes have been made remotely.
- Public-key Auth settings requests could not be completed from this environment. Live signup, token refresh, password recovery and database isolation have not been verified against the target.
- `NEXT_PUBLIC_SUPABASE_ENABLED=false` preserves the working local preview until the schema and Auth configuration can be verified. Setting the flag alone does not create the database tables.

## Prepared integration

- Browser and per-request server clients; Next.js 16 proxy with Auth-server user verification, cookie refresh and private cache headers.
- Live owner signup, confirmation code / confirmation-link callback, password sign-in, recovery and reset screen.
- Server-side workspace routes with authenticated identity, same-origin mutation checks and an HttpOnly workspace selector cookie.
- Owner-scoped workspace configuration persistence with revision checks to detect concurrent updates. Failed saves remain visible and stop further writes until reload.
- Public keys only in browser code; no service-role client.

`schema.sql` creates one additive foundation table, `public.academyos_workspaces`. Configuration contains the existing typed school state as JSONB. Rosters currently remain configuration records; these are not separate authenticated student/staff memberships. Normalized operational tables and live invitation delivery are later modules. Live access is school-owner-only at this stage.

RLS allows a signed-in user to create/read/update only workspaces whose `owner_id` is their verified Auth user ID. No permissions are derived from editable user metadata. The application also requires confirmed email before school creation. Owner identity and workspace address cannot be changed through UPDATE grants. Actual deletion is not exposed.

## Complete the live connection

1. Connect the Supabase account that owns this project. Alternatively, run `schema.sql` in this project's SQL editor.
2. Confirm email/password sign-in and email confirmation are configured in Supabase Auth.
3. Add `http://localhost:3000/auth/callback` to the Auth redirect URL allow list. Include the final deployment's callback when deploying. Keep URL allow lists restricted to intended origins.
4. Default confirmation-link emails work with `/auth/callback`. Code entry requires the confirmation email template to include the email token. A six-digit demo code is never accepted in live mode.
5. Verify the table, policies and grants with `verify.sql`, run Auth signup/confirmation/sign-in, then check two separate school owners cannot access each other's rows.
6. Run Supabase security advisors. Only after these pass, set `NEXT_PUBLIC_SUPABASE_ENABLED=true` and restart the local Next.js server.

Do not upload the Greenfield demo dataset automatically. A new live owner begins with a new, empty school configuration. Existing browser-local preview records remain local when switching modes.

The service-role key shared in chat should be rotated in Supabase before production use. Updating it is unnecessary for this integration because the app does not use it.

Implementation references: [Supabase SSR clients](https://supabase.com/docs/guides/auth/server-side/creating-a-client), [Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security).


## Schema applied by project owner

The project owner ran `schema.sql` successfully in the target SQL Editor. Live Supabase mode is now enabled in the local environment. The migration result was reported by the owner; direct remote schema/RLS verification is still pending.

This agent's execution environment returns `EACCES` for outbound Supabase requests, and the plugin connection is currently unavailable. Run the Next.js dev server from your own terminal to allow its server-side Supabase calls. Open `/api/connection` to inspect Auth reachability and anonymous table restrictions. A successful status check is a prerequisite to testing real signup, but does not replace a two-user RLS test.

Add `http://localhost:3000/auth/callback` to Supabase Auth redirect URLs before using confirmation and recovery links. The shared demo password is not accepted in live mode. Use the password you enter during real registration.

## Confirmation email delivery

A successful signup or resend response acknowledges the request; it does not prove inbox delivery. The registration page states this explicitly. Confirmation emails may contain a link only. Code entry works only when the confirmation template includes `{{ .Token }}`.

If no email arrives, inspect Authentication logs and the mail provider delivery logs. Check whether the address already has a confirmed account, in which case the owner should sign in. Verify custom SMTP configuration: Supabase's built-in mail service only delivers to project team addresses and is rate limited. Configure custom SMTP to send to other school owners. Do not disable email verification to work around delivery failures.

See [SMTP configuration](https://supabase.com/docs/guides/auth/auth-smtp) and [email templates](https://supabase.com/docs/guides/auth/auth-email-templates).
