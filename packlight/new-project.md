# New project: interview and stack

Read this only when the project folder has no code yet. Goal: understand what is being built,
pick a stack that fits, record why, then write the docs (SKILL.md step 3).

## 1. Interview - three short rounds, a few questions each

Ask one round, wait, then the next. Skip anything already answered. Offer examples so answers are quick.

**Round 1 - the product**
1. What are you building, in one or two sentences? Its working name?
2. Who uses it? One kind of user, or several (for example customers and an admin)?
3. The main features - the 3-6 things it must do on day one.
4. What already exists: designs, a brand, an old system, data to import?

**Round 2 - size and platforms**
5. Where do people use it: web, iPhone, Android, desktop? Which first?
6. How many users at launch, and in a year (10s, 1,000s, 100,000s)?
7. Does it need: logins, payments, file or photo uploads, real-time updates, notifications,
   maps, search, AI features, offline use?

**Round 3 - limits**
8. Budget for hosting per month, roughly.
9. Where the users and data are (country/region), and any data rules (health, finance, children, local data laws).
10. Deadline for a first version.
11. Who builds and maintains it, and what languages or tools they already know.

## 2. Suggest a stack

Write one short table: layer · choice · why (one line, tied to an answer above). Then one alternative
and when it would be better. Ask the user to pick or change. Don't write code before they pick.

Defaults - start here, change only when an answer says so:

| Need | Default | Change when |
|---|---|---|
| Web app | Next.js (React, TypeScript) | Mostly static content: Astro. Every page behind a login (staff/admin tool): Vite + React, plus a separate Astro site if a public marketing page is needed. |
| Mobile | Expo (React Native, TypeScript) - one codebase for iPhone and Android | Heavy graphics, AR, deep OS features: native Swift / Kotlin. |
| Backend / API | Node + TypeScript (NestJS or Fastify) | Team knows Python, or heavy data/AI work: Python + FastAPI. |
| Small app, small team, fast launch | Hosted backend: Supabase (Postgres, auth, storage) | Strict data rules or region not offered: own backend. |
| Database | PostgreSQL | Pure key-value or huge write volume: pick for that need. |
| Vector search (AI over documents) | pgvector in the same Postgres | Tens of millions of chunks or heavy filtering: a vector database. |
| Reading PDFs, Word, web pages | A parsing library (e.g. Unstructured, Docling); OCR for scans | High volume or complex layouts: a hosted parser. |
| Auth | The platform's auth (Supabase, Clerk, Cognito, Firebase) | Unusual login rules or local law: own auth with a vetted library. |
| Business customers' own login (Google/Microsoft SSO, SAML) | WorkOS or Auth0 Organizations | Few customers, Google/Microsoft only: the platform's social login. |
| Payments | Stripe | Country not supported: the local provider. |
| Files | S3-compatible object storage | - |
| Real-time | Supabase Realtime or WebSockets | - |
| Email | Resend or Postmark | - |
| SMS | Twilio | Cheaper local provider in the user's country. |
| Push notifications | Expo Notifications (mobile), web push for web | - |
| Scheduled jobs (reminders, reports) | The host's cron (Supabase cron, Vercel cron) | Many or long jobs: a queue worker. |
| Hosting | Vercel (web) + a managed container or serverless host (API) | Data must stay in a region: a cloud with a region there. |
| AI features | A hosted model API behind your own backend; never call it from the app with a key. Stream answers to the browser (server-sent events). | Data must stay in a region: the model provider's endpoint in that region, on a cloud the rest of the stack already uses. |

Rules for the suggestion:
- When two rows pull different ways, decide in this order: data rules and region, then what the team knows,
  then managed over self-run, then cost.
- Data that must stay in a region: list every place data lands - database, files, backups, logs, email,
  AI provider, analytics, error tracking - and pick each one in that region. Note which need a data
  processing agreement.
- Software sold to companies (several customers in one system): every query is scoped by customer id;
  write that as a project rule.
- One language across the stack when the team is small (TypeScript is the usual pick).
- Prefer managed services for anything under ~10,000 users; say the monthly cost range.
- Fewer moving parts beats the newest tool. Name nothing the answers don't need.
- Say plainly what would make you change the choice later.

## 3. Record it

Once the user picks:
- Project rules in CLAUDE.md may come from the answers (region, data rules, customer separation, who
  approves releases). Mark any you inferred with "(confirm)".
- `docs/DECISIONS.md` - one entry per choice: date, decision, why, the alternative and when to revisit.
- `CLAUDE.md` - "What this is" from round 1; Folders from the planned layout; Gates as the commands the
  stack will use (mark them "planned" until they run).
- `docs/STATUS.md` - "Next": scaffold the project, then the first feature. Product questions only the
  person running the project (or their client) can answer go in "Waiting on owner".
- `docs/features/<area>.md` - one page per day-one feature from question 3, plus one for payments or auth
  if they carry business rules (deposits, refunds, roles), with "What it does" and
  "Rules" filled from the answers, "Where the code is" left as "not built yet".

Then continue with SKILL.md step 5, without the usage report (a new project has no history yet).
If the run has no user to ask (scripted), take the main suggestion and note that in DECISIONS.md.
