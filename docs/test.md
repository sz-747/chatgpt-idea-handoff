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

## Authorized background handoff (2026-10-28; recorded 2026-10-29)

A subsequent live test recovered 12 user messages and 12 assistant replies from one signed-in original conversation's current selected branch. A hidden in-app browser performed keyword search, loaded virtualized earlier/later turns using page-level Playwright events, and expanded a collapsed pasted table. Overlapping batches of message IDs established one chronological order; both beginning and end were reached. Direct chat reading had exposed only five recent exchanges despite reporting no further page.

Rendered message bodies were written directly to a local intermediate file and converted to UTF-8 Markdown. The handoff included a chronological transcript, implementation context and a verification receipt. Code-block content, rendered linked URLs, message IDs, file read-back, transcript hash and local handoff links were checked. No desktop mouse/keyboard injection, clipboard access, editor, file manager or save dialog was used. No share link or source message was created.

The external browser provider rejected an explicit hidden-tab visibility option. The supported hidden in-app tab then loaded the signed-in session after normal page loading, without authentication changes or challenge intervention. Prefer that separate hidden surface before interacting with user-owned tabs. Private source identities, transcripts and account data are excluded from this repository.

This is one host/session and selected-branch result, not proof of exhaustive account discovery, alternate branches, deleted content or cross-client reliability. Citation links exposed in the rendered text were retained; secondary sources in citation popovers and non-text asset downloads were outside the test. Citation favicons were omitted. A console encoding error during reporting was corrected by using UTF-8 output. The earlier instruction-only review above remains historical; it did not itself perform this live test.
