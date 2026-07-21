# GitHub Pull Requests

Use this guide whenever creating, reviewing, updating, or merging a GitHub pull request.

## Before opening

- Review the complete diff and exclude unrelated changes.
- Follow the repository's pull-request template and local contribution instructions.
- Run the relevant local validation and document anything that could not be run.
- Open the pull request without auto-merge and keep it unmerged while automated or agent review is pending. Use draft state only when configured reviewers also run on drafts.

## Review gate

Opening a pull request starts review; it does not authorize merging it.

1. Wait for the configured Codex review to finish. No review yet means pending, not approved.
2. Inspect all review summaries, inline threads, checks, and requested changes.
3. Assess each comment on its technical merits.
4. Implement valid feedback and rerun the affected validation.
5. If feedback should not be implemented, reply in the original thread with a concise technical reason.
6. Reply to implemented feedback with what changed and where.
7. Resolve a thread only after its concern has been addressed or explicitly declined.
8. Recheck the pull request immediately before merge for late comments and check-state changes.

A thumbs-up or clean Codex review satisfies the agent-review step, but it does not replace any human approval required by the repository. Do not enable auto-merge before all review gates are satisfied.

## Merge requirements

Do not merge while any of the following is true:

- Codex review is still pending;
- an actionable review comment is unanswered;
- a review conversation is unresolved;
- a required check is pending or failing;
- the branch is out of date when the repository requires an up-to-date branch;
- required human approval or explicit owner authorization is missing.

If a review arrives after a premature merge, treat that as a process failure: assess the feedback, reply to every thread, and ship valid corrections through a follow-up pull request.

## Repository protection

Prefer GitHub rulesets or branch protection for the default branch. At minimum:

- require changes to arrive through a pull request;
- require conversations to be resolved before merging;
- require the repository's mandatory status checks;
- prevent bypass except for an intentional emergency path.

A formal one-approval rule works only when someone other than the pull-request author can submit an approving review. In a solo repository where the owner account also authors pull requests, use a bot or service account for authored changes before requiring owner approval; GitHub does not count self-approval. Until that separation exists, require explicit owner authorization operationally and keep conversation resolution enforced technically.
