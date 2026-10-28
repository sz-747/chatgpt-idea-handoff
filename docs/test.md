# Verification

From the repository root, run `python -B -m unittest discover -s tests` (Python 3, standard library only).

Four offline tests cover chronological user/assistant extraction, expected-count checks, malformed/missing source handling, and safe output replacement. The fixtures are synthetic and require no account or network.

On 2026-10-24, four tests passed. An authorized real shared-snapshot import recovered 18 user messages, 17 assistant text replies and an image marker from one source, and five user/assistant exchanges from another. The private source files are not distributed. These counts are evidence, never defaults for other chats.

An earlier signed-in search attempt stopped at a login dialog. A later authorized live test on 2026-10-24 succeeded through the signed-in ChatGPT UI: keyword search found both intended original chats, scrolling/expansion exposed their current available text, and comparison found no additional substantive context gaps against the existing project archives. Private source identities and payloads remain in the destination project, not this repository. This verifies one real two-chat handoff check, not exhaustive account discovery or alternate conversation branches. Live account/browser checks are opt-in under the current handoff request; the user performs authentication directly. Recheck coverage for each source, especially virtualized pages and changed HTML schemas.

## Background-operation contract review (2026-10-28)

Manual review scenarios for the updated instructions:

- Complete chat-tool output: write transcripts and context directly, then read back and check links; no desktop actions.
- Partial chat-tool output with authorized background browser support: verify source identity and load/check available messages before saving; no foreground fallback by assumption.
- Foreground-only browser or login requirement: explain the blocker, preserve partial work, and request permission for the specific desktop interaction or let the user authenticate directly. Do not open an editor or use the clipboard to save.
- Existing shared HTML or official export: parse locally and write directly; retain snapshot/export coverage labels and report missing messages.

These scenarios were reviewed against the contract, not executed as live browser tests. The four existing synthetic parser tests were rerun successfully after this documentation update. No authenticated background browser run or fresh-agent behavior test was performed.
