# Unpack
For a project already set up, when docs have grown or drifted. Cheap pass: line counts first, then read only
what fails. Run from the project root. Don't commit.
1. `wc -l CLAUDE.md docs/STATUS.md docs/features/*.md`.
2. CLAUDE.md over 80 lines: move state to STATUS.md and feature detail to feature pages; keep rules.
3. STATUS.md: rewrite to current state only, whatever its length. History means dated past events, version
   lists, commit hashes, "last updated" stamps and "done" items. Git already has commit detail: drop it.
   Keep current facts (what is live, what is unpushed) and future dates (deadlines) as plain state. A finished item with a
   reason worth keeping goes to its page's "Decisions (why)". Extra sections are fine if they hold state.
4. Feature pages: merge pages under ~10 lines into a neighbour. Split a page past ~150 lines at a top-level
   heading; leave a one-line pointer both ways and add the new page to the register. Make the register
   match the files.
5. Drift - check each path in "Where the code is":
   - Resolve it against the project root, then each repo root in CLAUDE.md "Folders"; a bare filename
     matches any file of that name (note this is loose).
   - Treat backticked tokens as paths; expand `{a,b}` braces; strip line numbers (`:120`), function names and
     anything after a `*` or `…`; skip prose. Check doc paths (docs/...) the pages cite too.
   - Check the branch the docs name, not the checked-out one: `git -C <repo> ls-tree -r --name-only <branch>`.
   - Fix a path that moved (find it by name); flag one that is gone in the page's "Open". Don't read code.
6. Old docs (any file under docs/, not only .md): list a doc as a candidate when the register or CLAUDE.md calls it history, or when no page,
   CLAUDE.md or the register links to it. Show the list; move to `docs/archive/` only what the user agrees
   to. Never delete. Also flag a second STATUS.md anywhere under docs/ - sessions may read the wrong one.
7. Report: before/after line counts for changed and new files plus the total, changes one per line,
   drift checked/missing, old-doc candidates.
   If nothing crossed a limit, say so in one line.
