# kind: on-demand
# trigger: explicitly invoked by the chatgpt-idea-handoff skill for authorized HTML
"""Export user-facing shared-chat text from a local HTML download. No network."""
import argparse
import json
from pathlib import Path
import re
import sys


ENQUEUE = re.compile(r'streamController\.enqueue\(("(?:\\.|[^"\\])*")\)')


def extract(html):
    """Return source title and visible text messages, never hidden channel content."""
    for match in ENQUEUE.finditer(html):
        try:
            pool = json.loads(json.loads(match.group(1)))
        except (ValueError, TypeError):
            continue
        if not isinstance(pool, list):
            continue

        def value(ref):
            if not isinstance(ref, int) or isinstance(ref, bool):
                raise ValueError('Unsupported reference type in shared-page schema')
            if ref < 0:
                return None
            if ref >= len(pool):
                raise ValueError('Out-of-range reference in shared-page schema')
            return pool[ref]

        def fields(ref):
            obj = value(ref)
            if obj is None:
                return {}
            if not isinstance(obj, dict):
                raise ValueError('Expected referenced object in shared-page schema')
            result = {}
            for key, target in obj.items():
                if not re.fullmatch(r'_\d+', key):
                    raise ValueError('Unsupported object key in shared-page schema')
                result[value(int(key[1:]))] = target
            return result

        def get(obj, key):
            return value(obj[key]) if key in obj else None

        root = None
        for i, obj in enumerate(pool):
            if isinstance(obj, dict) and all(re.fullmatch(r'_\d+', k) for k in obj):
                candidate = fields(i)
                if 'linear_conversation' in candidate:
                    root = candidate
                    break
        if root is None:
            continue
        sequence = get(root, 'linear_conversation')
        if not isinstance(sequence, list):
            raise ValueError('Shared-page conversation sequence is not a list')
        messages = []
        seen = set()
        for node_ref in sequence:
            node = fields(node_ref)
            if 'message' not in node:
                continue
            msg = fields(node['message'])
            if not msg:
                continue
            meta = fields(msg['metadata']) if 'metadata' in msg else {}
            if get(meta, 'is_visually_hidden_from_conversation'):
                continue
            author = fields(msg['author']) if 'author' in msg else {}
            role = get(author, 'role')
            if role != 'user' and not (
                role == 'assistant' and get(msg, 'channel') == 'final'
                and get(msg, 'recipient') == 'all'
            ):
                continue
            content = fields(msg['content']) if 'content' in msg else {}
            if get(content, 'content_type') != 'text':
                raise ValueError('Visible message has unsupported non-text content; use browser/export fallback')
            part_refs = get(content, 'parts')
            if not isinstance(part_refs, list):
                raise ValueError('Visible text message lacks a parts list')
            parts = [value(ref) for ref in part_refs]
            if not all(isinstance(part, str) for part in parts):
                raise ValueError('Visible text contains unsupported structured parts')
            text = '\n\n'.join(parts)
            if not text.strip() or text.lstrip().startswith('::chatgpt-content-reference{'):
                raise ValueError('Empty text or unresolved reply reference; extraction incomplete')
            message_id = get(msg, 'id')
            if not isinstance(message_id, str):
                raise ValueError('Visible message lacks a string ID')
            if message_id in seen:
                continue
            seen.add(message_id)
            messages.append({'id': message_id, 'role': role, 'text': text})
        if not any(m['role'] == 'user' for m in messages) or not any(m['role'] == 'assistant' for m in messages):
            raise ValueError('Conversation lacks readable user messages or assistant replies')
        return get(root, 'title') or 'ChatGPT conversation', messages
    raise ValueError('No supported shared-chat data found; page may require login or use a changed schema')


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-url', required=True)
    parser.add_argument('--import-date', required=True, help='Client-local YYYY-MM-DD date')
    parser.add_argument('--expected-users', type=int)
    parser.add_argument('--expected-assistants', type=int)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args(argv)
    try:
        title, messages = extract(args.input.read_text(encoding='utf-8-sig'))
        counts = {role: sum(m['role'] == role for m in messages) for role in ('user', 'assistant')}
        for role, expected in [('user', args.expected_users), ('assistant', args.expected_assistants)]:
            if expected is not None and counts[role] != expected:
                raise ValueError(f'{role} count mismatch: expected {expected}, extracted {counts[role]}')
        if args.input.resolve() == args.output.resolve():
            raise ValueError('Input and output must be different files')
        header = (f'# {title}: conversation transcript\n\nImported: {args.import_date}.\n\n'
                  f'Source: {args.source_url}\n\nCoverage: shared snapshot; {counts["user"]} user messages '
                  f'and {counts["assistant"]} visible assistant text replies. Later changes to the original '
                  'chat are not established. Hidden/internal messages and duplicate fragments are excluded. '
                  'Non-text assets, including generated images and internal tool results, are not archived; '
                  'inspect the source and add descriptive markers when relevant. Original interactive '
                  'illustration markup is retained where present.\n')
        blocks = [header]
        for i, msg in enumerate(messages, 1):
            blocks.append(f'\n## {i}. {msg["role"].title()}\n\n<!-- message-id: {msg["id"]} -->\n\n{msg["text"]}\n')
        output = '\n'.join(blocks)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('w' if args.overwrite else 'x', encoding='utf-8', newline='\n') as stream:
            stream.write(output)
        if args.output.read_text(encoding='utf-8') != output:
            raise OSError('Output read-back verification failed')
        print(f'Saved {args.output}: {counts["user"]} user messages, {counts["assistant"]} assistant text replies.')
        return 0
    except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
        print(f'{type(exc).__name__}: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
