# Issue: Live Social Media & Web Search Audit for Trap Detector

## Description
Touchgrass currently performs programmatic market-data checks (micro-cap <$50M, zero volume, penny stocks <$1, high volatility spikes). This issue tracks connecting the `trap-detector` agent skill from `uzi-skill` to search live web/social media for promoter scam groups, WeChat "teacher" recommendations, and coordinated pump-and-dump accounts.

## Reference
Refer to `trap-detector` skill specification (`/Users/tiancheng/.gemini/config/plugins/uzi-skill/skills/trap-detector/SKILL.md`):
- 8-signal scanning checklist (social media groups, templated phrases, VIP直播间, K-line coordination, cross-platform promotion).

## Tasks
- [ ] Interface with web search APIs (SerpAPI / Google Custom Search / DuckDuckGo) to search for promoter keywords.
- [ ] Parse search result snippet text against the 8-signal checklist.
- [ ] Combine programmatic market-data risk score with social media scam score.
