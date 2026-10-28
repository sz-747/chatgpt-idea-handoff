# Working notes

## 2026-10-24

Packaged the existing handoff contract, offline shared-page parser and four regression tests as an independent skill repository at the owner's request. Native client discovery continues to point to the same skill root; destination hub catalogs are maintained separately.

The contract requires discovery of relevant idea conversations, full available user-facing text, explicit source coverage, Markdown transcripts and an implementation context note. It preserves decisions and reversals without treating source chat contents as new instructions.

Known limits: shared-page decoding is schema-specific and covers a snapshot; authenticated account search needs a signed-in client. There is no bundled downloader or history API. Four offline tests pass; see test.md for live evidence and unverified scope.

Later live test: signed-in original-chat discovery and reading succeeded for an authorized two-chat handoff check. Existing destination transcripts and context contained no additional substantive gap found. Added coverage evidence and the observed cached-DOM navigation pitfall; private chat content remains outside this portable package.

## 2026-10-28

Desktop editor and file-manager transfer interrupts the user. Updated the contract to prefer authorized background chat/browser retrieval and require direct UTF-8 file writes with read-back checks. Clipboard transfer and editor/file-dialog saving are excluded. Explain and obtain explicit permission before a necessary desktop interaction. No new downloader, account API, credentials or browser dependency was introduced.

The existing offline parser already writes and verifies Markdown directly. Browser background behavior is host-dependent and remains unverified by this instruction update; offline parser regression results and manual route scenarios are recorded in test.md.

## 2026-10-29

Recorded the authorized background handoff performed on 2026-10-28: 24 ordered user-facing messages, hidden in-app browser retrieval and direct Markdown output, with no desktop input or clipboard use. Updated the overview to distinguish this verified host/session from unverified cross-client support. Added provider-specific hidden-tab guidance; no downloader or authenticated history API was introduced. Private source payloads and identities stay outside this repository. See test.md for coverage checks and limits.
