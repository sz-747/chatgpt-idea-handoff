# Verification

From the repository root, run `python -B -m unittest discover -s tests` (Python 3, standard library only).

Four offline tests cover chronological user/assistant extraction, expected-count checks, malformed/missing source handling, and safe output replacement. The fixtures are synthetic and require no account or network.

On 2026-10-24, four tests passed. An authorized real shared-snapshot import recovered 18 user messages, 17 assistant text replies and an image marker from one source, and five user/assistant exchanges from another. The private source files are not distributed. These counts are evidence, never defaults for other chats.

An earlier signed-in search attempt stopped at a login dialog. A later authorized live test on 2026-10-24 succeeded through the signed-in ChatGPT UI: keyword search found both intended original chats, scrolling/expansion exposed their current available text, and comparison found no additional substantive context gaps against the existing project archives. Private source identities and payloads remain in the destination project, not this repository. This verifies one real two-chat handoff check, not exhaustive account discovery or alternate conversation branches. Live account/browser checks are opt-in under the current handoff request; the user performs authentication directly. Recheck coverage for each source, especially virtualized pages and changed HTML schemas.
