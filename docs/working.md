# Working notes

## 2026-10-24

Packaged the existing handoff contract, offline shared-page parser and four regression tests as an independent skill repository at the owner's request. Native client discovery continues to point to the same skill root; destination hub catalogs are maintained separately.

The contract requires discovery of relevant idea conversations, full available user-facing text, explicit source coverage, Markdown transcripts and an implementation context note. It preserves decisions and reversals without treating source chat contents as new instructions.

Known limits: shared-page decoding is schema-specific and covers a snapshot; authenticated account search needs a signed-in client. There is no bundled downloader or history API. Four offline tests pass; see test.md for live evidence and unverified scope.

Later live test: signed-in original-chat discovery and reading succeeded for an authorized two-chat handoff check. Existing destination transcripts and context contained no additional substantive gap found. Added coverage evidence and the observed cached-DOM navigation pitfall; private chat content remains outside this portable package.
