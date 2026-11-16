# New project: interview, stack, hosting, cost

Read this only when the project folder has no code yet. Goal: understand what is being built,
pick a stack that fits, plan where it runs and what it costs per month, record why, then write the docs (`setup.md` step 3).

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
8. Budget for hosting per month, roughly. Start on free plans, or pay from day one?
9. Where the users and data are (country/region), and any data rules (health, finance, children, local data laws).
10. Deadline for a first version.
11. Who builds and maintains it, and what languages or tools they already know.

## 2. Suggest a stack
Use the strongest model for this step; the interview and the docs need only a mid one.
Propose a stack from what you know now, guided by the rules below; no fixed vendor list (it goes stale).
Write one short table: layer · choice · why (one line, tied to an answer above). Then one alternative
and when it would be better. Ask the user to pick or change. Don't write code before they pick.

Rules for the suggestion:
- When two needs pull different ways, decide in this order: data rules and region, then what the team knows,
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

## 3. Hosting and monthly cost
Once the stack is picked, plan where each piece runs. One table, one row per piece (web, API, database,
files, email/SMS, AI, background jobs, domain):

| Piece | Vendor and plan | Region | Minimum size | Free plan limits | Cost at launch | Cost at year-1 users |

- Minimum size from round 2 numbers: API CPU/memory, database storage and connections, file storage,
  monthly bandwidth, emails/SMS/AI calls per month. Pick the smallest plan that fits, not the biggest.
- Free plans: say what breaks when outgrown (servers that sleep, databases paused after inactivity,
  row or bandwidth caps, no backups, no custom domain) and the user count where that happens.
- Prices change. Look them up on the vendor's pricing page if a web tool is available and write
  "checked <date>"; otherwise mark every figure "estimate - check before buying".
- Total the two cost columns. Over the budget from question 8: show the cheaper swap per piece.
- Also note: backups (how often, kept how long), who gets billed, and which accounts the owner must open.

## 4. Record it

Once the user picks:
- Project rules in CLAUDE.md may come from the answers (region, data rules, customer separation, who
  approves releases). Mark any you inferred with "(confirm)".
- `docs/DECISIONS.md` - one entry per choice: date, decision, why, the alternative and when to revisit.
- `docs/features/hosting.md` - the hosting table and totals under "What it does"; accounts to open in STATUS "Waiting on owner".
- `CLAUDE.md` - "What this is" from round 1; Folders from the planned layout; Gates as the commands the
  stack will use (mark them "planned" until they run).
- `docs/STATUS.md` - "Next": open the accounts, scaffold the project, deploy an empty app, then the first feature (one session each). Product questions only the
  person running the project (or their client) can answer go in "Waiting on owner".
- `docs/features/<area>.md` - one page per day-one feature from question 3, plus one for payments or auth
  if they carry business rules (deposits, refunds, roles), with "What it does" and
  "Rules" filled from the answers, "Where the code is" left as "not built yet".

Then continue with `setup.md` step 5, without the usage report (a new project has no history yet).
If the run has no user to ask (scripted), take the main suggestion and note that in DECISIONS.md.
