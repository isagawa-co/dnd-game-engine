# X Bookmark Scanner

Scan X bookmarks for competitive intelligence relevant to Isagawa products.

## Pipeline

1. **Fetch** — Retrieve bookmarks (mock mode for testing, real mode needs credentials)
2. **Filter** — Keep only AI/agent-relevant posts using keyword matching
3. **Analyze** — Compare against Isagawa products, generate assessments
4. **Backlog** — Generate backlog items for borrowable ideas
5. **Notify** — Send report via configured method (console default)
6. **State** — Mark processed posts to enable idempotent re-runs

## Usage

### Mock Mode (Testing)

```python
from scanner.config import ScannerConfig
from scanner.fetcher import BookmarkFetcher
from scanner.analyzer import filter_relevant
from scanner.backlog_gen import generate_backlog_item, should_generate_backlog
from scanner.notifier import format_report, send_notification
from scanner.state import BookmarkState

config = ScannerConfig(mock_mode=True)
state = BookmarkState()
fetcher = BookmarkFetcher(config)

# Fetch and filter
bookmarks = fetcher.fetch_bookmarks()
new_bookmarks = [b for b in bookmarks if not state.is_processed(b["post_id"])]
analyses = filter_relevant(new_bookmarks, config)

# Generate backlog items for borrowable posts
for analysis in analyses:
    if should_generate_backlog(analysis):
        backlog_md = generate_backlog_item(analysis)
        # Write to backlog directory as needed

# Report and notify
report = format_report(analyses)
send_notification(report, config.notification_method)

# Update state
for analysis in analyses:
    state.mark_processed(analysis["post_id"], analysis["summary"])
state.set_last_scan_date()
```

### Real Mode (Production)

Requires:
- `X_USERNAME` and `X_PASSWORD` environment variables
- Playwright browser automation (not yet implemented)
- Set `mock_mode=False` in config

## Modules

| Module | Purpose |
|--------|---------|
| `scanner/config.py` | ScannerConfig dataclass, product lists, AI keywords |
| `scanner/state.py` | BookmarkState — tracks processed post IDs (JSON persistence) |
| `scanner/fetcher.py` | BookmarkFetcher — mock bookmarks or browser fetch |
| `scanner/analyzer.py` | analyze_post, filter_relevant, generate_assessment |
| `scanner/backlog_gen.py` | generate_backlog_item, should_generate_backlog |
| `scanner/notifier.py` | format_report, send_notification (console/email/sms) |
