"""Offline checks using synthetic data; no account or network access."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

script = Path(__file__).resolve().parents[1] / 'scripts' / 'extract_shared_chat.py'
spec = importlib.util.spec_from_file_location('extract_shared_chat', script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def fixture(reply='Use a local runtime.', include_reply=True):
    pool = []

    def add(value):
        if isinstance(value, dict):
            node = {'_' + str(add(k)): add(v) for k, v in value.items()}
        elif isinstance(value, list):
            node = [add(item) for item in value]
        else:
            node = value
        pool.append(node)
        return len(pool) - 1

    def message(mid, role, text, hidden=False, channel='final'):
        return {'message': {'id': mid, 'author': {'role': role}, 'metadata': {'is_visually_hidden_from_conversation': hidden},
                            'channel': channel, 'recipient': 'all', 'content': {'content_type': 'text', 'parts': [text]}}}

    seq = [message('system', 'system', 'INTERNAL SYSTEM'), message('user', 'user', 'Build my idea'),
           message('hidden', 'assistant', 'INTERNAL REASONING', channel='analysis'),
           message('fragment', 'assistant', 'DUPLICATE FRAGMENT', hidden=True)]
    if include_reply:
        seq += [message('reply', 'assistant', reply), message('reply', 'assistant', reply)]
    add({'title': 'Example idea', 'linear_conversation': seq})
    return '<script>window.__reactRouterContext.streamController.enqueue(' + json.dumps(json.dumps(pool)) + ')</script>'


class ExportChecks(unittest.TestCase):
    def test_order_replies_privacy_and_deduplication(self):
        title, messages = module.extract(fixture())
        self.assertEqual(title, 'Example idea')
        self.assertEqual([(m['role'], m['text']) for m in messages], [('user', 'Build my idea'), ('assistant', 'Use a local runtime.')])

    def test_missing_or_placeholder_reply_is_not_success(self):
        for html in [fixture(include_reply=False), fixture(reply='::chatgpt-content-reference{index="1"}'), '<html>Log in</html>']:
            with self.subTest(html=html[:40]), self.assertRaises(ValueError):
                module.extract(html)

    def test_counts_fail_before_output_is_written(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.html'
            output = Path(directory) / 'transcript.md'
            source.write_text(fixture(), encoding='utf-8')
            result = module.main(['--input', str(source), '--output', str(output), '--source-url', 'https://example.invalid/shared', '--import-date', '2026-10-24', '--expected-assistants', '2'])
            self.assertEqual(result, 1)
            self.assertFalse(output.exists())

    def test_existing_markdown_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'source.html'
            output = Path(directory) / 'transcript.md'
            source.write_text(fixture(), encoding='utf-8')
            output.write_text('Existing project notes', encoding='utf-8')
            self.assertEqual(module.main(['--input', str(source), '--output', str(output), '--source-url', 'https://example.invalid/shared', '--import-date', '2026-10-24']), 1)
            self.assertEqual(output.read_text(encoding='utf-8'), 'Existing project notes')


if __name__ == '__main__':
    unittest.main()
