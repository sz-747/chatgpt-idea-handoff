# Maintainer guide

- Read SKILL.md for the capability contract; README.md for installation and docs/test.md for evidence and limits.
- Run `python -B -m unittest discover -s tests` from this root after parser changes. Use synthetic fixtures; never commit real account exports or conversation payloads.
- Preserve the distinction between original, export, shared snapshot and partial coverage. Do not claim account-wide retrieval from a shared page.
- Preserve background operation and direct file output. Never introduce editor/file-dialog or clipboard transfer as a saving step. Desktop interaction requires explicit permission; do not claim untested background browser support.
- Keep account access in the host client's authorized tools. Do not add session-token extraction or undocumented service endpoints.
- Check relative Markdown links and update docs/working.md and verification evidence after substantive changes. Host routing and private machine settings belong outside this portable repository.
