# ChatGPT idea handoff

Bring an idea from ChatGPT web into an implementation workspace as full available user/assistant Markdown transcripts and a concise context note.

The agent entry point is [SKILL.md](SKILL.md). It covers signed-in search, conversation selection, coverage checks, project reconciliation and missing-access behavior. Direct access is preferred; existing shared snapshots are a fallback.

Install this folder in your client's skill discovery directory, or link it there. The host client supplies authorized chat/browser tools. The bundled offline shared-page parser requires Python 3 and no third-party packages. From this repository root:

```sh
python scripts/extract_shared_chat.py --help
python -B -m unittest discover -s tests
```

The parser reads a local downloaded HTML file and writes Markdown. It does not authenticate or download chats. Shared snapshots may omit later private changes; hidden reasoning and internal tool messages are excluded. Keep raw downloads, exports and transcripts in the destination project's private storage, outside this repository.

See [verification](docs/test.md) and [maintenance notes](docs/working.md).
