# Issue: Add Remote Discord Webhook and Email Notification Delivery

## Description
Currently, Touchgrass Trader generates formatted markdown market reports for console output and local file persistence. To provide unattended remote digests, we need to implement Discord Webhook and Email alert delivery.

## Implementation Reference
We can reference the implementation in `BreakoutAnalysis` (`BreakoutAnalysis/src/notifications/discord_notifier.py` and `email_notifier.py`):
- **Discord Webhooks**: HTTP POST requests delivering Discord embeds (`DISCORD_WEBHOOK_URL`).
- **Email Alerts**: SMTP/SendGrid digest delivery to configured subscriber email lists (`SMTP_SERVER`, `SENDER_EMAIL`).

## Tasks
- [ ] Port/adapt `DiscordNotifier` from `BreakoutAnalysis/src/notifications/discord_notifier.py`.
- [ ] Implement `EmailNotifier` supporting HTML/Markdown email templates.
- [ ] Wire channel auto-detection in `Notifier.__init__()` based on environment variables (`DISCORD_WEBHOOK_URL`, `SMTP_HOST`).
- [ ] Add unit tests verifying mock dispatching to Discord and Email.
