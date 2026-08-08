import urllib.request
import json
import os
import subprocess

def get_git_token():
    try:
        proc = subprocess.run(
            ["git", "credential", "fill"],
            input=b"url=https://github.com/tianchengc/touchgrass.git\n",
            capture_output=True,
            check=True
        )
        for line in proc.stdout.decode('utf-8').splitlines():
            if line.startswith("password="):
                return line.split("=", 1)[1]
    except Exception as e:
        print(f"Error fetching git credential: {e}")
    return None

token = get_git_token()
if not token:
    print("Could not retrieve GitHub token.")
    exit(1)

url = "https://api.github.com/repos/tianchengc/touchgrass/issues"

issues_to_create = [
    {
        "title": "Add Remote Discord Webhook and Email Notification Delivery",
        "body": """## Description
Currently, Touchgrass Trader generates formatted markdown market reports for console output and local file persistence. To provide unattended remote digests, we need to implement Discord Webhook and Email alert delivery.

## Implementation Reference
We can reference the implementation in `BreakoutAnalysis` (`BreakoutAnalysis/src/notifications/discord_notifier.py` and `email_notifier.py`):
- **Discord Webhooks**: HTTP POST requests delivering Discord embeds (`DISCORD_WEBHOOK_URL`).
- **Email Alerts**: SMTP/SendGrid digest delivery to configured subscriber email lists (`SMTP_SERVER`, `SENDER_EMAIL`).

## Tasks
- [ ] Port/adapt `DiscordNotifier` from `BreakoutAnalysis/src/notifications/discord_notifier.py`.
- [ ] Implement `EmailNotifier` supporting HTML/Markdown email templates.
- [ ] Wire channel auto-detection in `Notifier.__init__()` based on environment variables (`DISCORD_WEBHOOK_URL`, `SMTP_HOST`).
- [ ] Add unit tests verifying mock dispatching to Discord and Email."""
    },
    {
        "title": "Automated Broker Integration for Direct Position Rebalancing Execution",
        "body": """## Description
Touchgrass Trader currently evaluates portfolio health and outputs position rebalancing recommendations (e.g. `BUY`, `SELL / AVOID`, `HOLD`). To enable zero-touch portfolio management, we need an optional broker execution layer.

## Proposed Architecture
- Interface with popular open APIs: **Alpaca Trading API** (US stocks) and **Interactive Brokers API (ib_insync)**.
- Guard executions with strict risk controls (max position sizing limits, stop-loss order attachment, manual approval confirmation flag).

## Tasks
- [ ] Create `touchgrass/src/broker/` interface module.
- [ ] Implement `AlpacaBroker` adapter for order placement and position querying.
- [ ] Add explicit dry-run mode (`--dry-run`) to preview trades before sending to broker.
- [ ] Provide user configuration flag `EXECUTE_AUTOMATED_TRADES=true`."""
    },
    {
        "title": "Full 65-Persona Individual LLM Agent Simulation Engine",
        "body": """## Description
Touchgrass currently uses a 7-faction multi-investor quantitative scoring model (Value, Growth, Macro, Technical, Quant, China Value, Youzi/Momentum). This issue tracks extending the bridge to optionally spawn individual LLM subagents for each of the 65 investor personas defined in `uzi-skill` (e.g., Warren Buffett, Stanley Druckenmiller, Mark Minervini, Jim Simons, Zhang Lei).

## Proposed Architecture
- Use `investor-panel` subagent spawning mechanism from `uzi-skill` (`/Users/tiancheng/.gemini/config/plugins/uzi-skill/skills/investor-panel/SKILL.md`).
- Run subagent persona evaluation asynchronously and aggregate individual votes and rationale comments.

## Tasks
- [ ] Implement `UziBridge.run_full_65_llm_panel(symbol)` async loader.
- [ ] Store individual persona rationale commentary in daily report JSON/Markdown.
- [ ] Add caching for LLM persona responses to reduce token costs."""
    },
    {
        "title": "Live Social Media & Web Search Audit for Trap Detector",
        "body": """## Description
Touchgrass currently performs programmatic market-data checks (micro-cap <$50M, zero volume, penny stocks <$1, high volatility spikes). This issue tracks connecting the `trap-detector` agent skill from `uzi-skill` to search live web/social media for promoter scam groups, WeChat "teacher" recommendations, and coordinated pump-and-dump accounts.

## Reference
Refer to `trap-detector` skill specification (`/Users/tiancheng/.gemini/config/plugins/uzi-skill/skills/trap-detector/SKILL.md`):
- 8-signal scanning checklist (social media groups, templated phrases, VIP直播间, K-line coordination, cross-platform promotion).

## Tasks
- [ ] Interface with web search APIs (SerpAPI / Google Custom Search / DuckDuckGo) to search for promoter keywords.
- [ ] Parse search result snippet text against the 8-signal checklist.
- [ ] Combine programmatic market-data risk score with social media scam score."""
    }
]

for issue in issues_to_create:
    data = json.dumps(issue).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "User-Agent": "Python",
        "Authorization": f"token {token}",
        "Content-Type": "application/json",
        "Accept": "application/vnd.github.v3+json"
    })
    try:
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode("utf-8"))
            print(f"CREATED: Issue #{res['number']} - {res['title']} -> {res['html_url']}")
    except Exception as e:
        print(f"Error creating issue '{issue['title']}': {e}")
