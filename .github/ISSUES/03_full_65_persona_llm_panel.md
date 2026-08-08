# Issue: Full 65-Persona Individual LLM Agent Simulation Engine

## Description
Touchgrass currently uses a 7-faction multi-investor quantitative scoring model (Value, Growth, Macro, Technical, Quant, China Value, Youzi/Momentum). This issue tracks extending the bridge to optionally spawn individual LLM subagents for each of the 65 investor personas defined in `uzi-skill` (e.g., Warren Buffett, Stanley Druckenmiller, Mark Minervini, Jim Simons, Zhang Lei).

## Proposed Architecture
- Use `investor-panel` subagent spawning mechanism from `uzi-skill` (`/Users/tiancheng/.gemini/config/plugins/uzi-skill/skills/investor-panel/SKILL.md`).
- Run subagent persona evaluation asynchronously and aggregate individual votes and rationale comments.

## Tasks
- [ ] Implement `UziBridge.run_full_65_llm_panel(symbol)` async loader.
- [ ] Store individual persona rationale commentary in daily report JSON/Markdown.
- [ ] Add caching for LLM persona responses to reduce token costs.
