---
name: job-scouting
description: Aggressive web job-scouting methodology for finding fresh software engineering / Python / AI roles. Use whenever searching for job postings, evaluating listings, or compiling a job dossier.
metadata:
  author: job-scout
  version: "1.0"
---

# Aggressive Job-Scouting Methodology

You are sourcing real, live job postings for a real candidate. The candidate's
full resume is available as crew knowledge (`knowledge/user_resume.txt`) —
ground every fit judgement in what the resume actually says, not assumptions.

## 1. Never stop early

An empty result is ONLY acceptable after you have completed the FULL effort
plan below. Stopping early is a failure, not a valid outcome.

Minimum effort before you may conclude a run:
- At least **12 distinct search queries** executed across your search tools
  (rotate: role keywords x source patterns). Reuse a query only if it returns
  new results after a filter change.
- At least **2 neural (Exa) queries** per technology keyword.
- Scrape (Firecrawl / ScrapeWebsiteTool) at least **8 candidate pages in
  full**, following at least **2 pages of pagination** on any job-board search
  you run.
- Open the careers pages of **every** target company named in the manifest
  before giving up on Tier 1.
- Try at least one alternate phrasing per failed query (title variants:
  "backend engineer", "software engineer", "python developer", "SWE",
  "platform engineer", "ML engineer").

## 2. Query construction

- Combine **one keyword axis** with **one source axis** per query:
  (python | django | fastapi | "software engineer" | "AI engineer" | "ML
  engineer") x (greenhouse.io | lever.co | ashbyhq.com | workable.com |
  seek.co.nz | wttj.com | weworkremotely.com | remoteok.com | linkedin.com |
  indeed.com | <company>/careers).
- Add recency operators where the engine supports them ("posted in last 14
  days", "past week", date-after:...).
- If a board offers URL search parameters for sorting by date (e.g. SEEK's
  date sorting, LinkedIn's f_TPR=r604800), scrape the sorted URL directly.

## 3. Freshness evidence (relaxed, evidence-tiered)

Accept a listing as fresh when ANY of these is observed in live tool output:
1. The listing page itself shows a posting date within the last 14 days.
2. The board shows relative recency ("posted 3 days ago", "new", "2d") within
   the last 14 days.
3. You reached the listing through a board URL that is date-filtered to the
   last 14 days (record the URL as your evidence).
Only reject for staleness when the page positively shows a date OLDER than 14
days.

## 4. Diversity mandate

Every run's output must include listings from at least 2 different sources,
and no source may contribute more than half the listings, unless fewer than 3
listings were found. Prefer the employer's own URL over aggregator copies.

## 5. Novelty

The previously-seen ledger injected in the task description is the ONLY
novelty authority. Memories from `search_memory` describe PAST runs — never
use them to reject a listing as a duplicate.

## 6. Reporting

When you return listings, tag each with its source tier and quote the
freshness evidence. When nothing passes after the full effort plan, return
empty output followed by a final section `SEARCH EFFORT LOG` listing the
queries executed and pages scraped, so the orchestrator can verify the run
was thorough.
