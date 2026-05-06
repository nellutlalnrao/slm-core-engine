# slm-core-engine
slm-core-engine is a CPU-first, disk-native Smart AI engine that combines Retrieval-Augmented Generation (RAG) with conversational memory, enabling small language models like Microsoft Phi-3-mini to reason accurately over large local datasets without GPUs or cloud dependency.

## Why slm-core-engine exists?

Small language models are fast, efficient, and affordable — but they suffer from:

- Limited context windows
- Hallucinations without grounding
- No long-term conversational memory
- Heavy dependence on GPUs or cloud APIs

**slm-core-engine solves these problems** by shifting intelligence from the model to the architecture.

## Key Benefits

- Runs on Low-End Hardware (Designed for 8 GB RAM systems)
- Breaks Context Window Limits
- Reduced Hallucinations
- Fully Offline & Private
- Modular (Swap SLMs without redesign) & Extensible (Add tools (SQL, APIs, OS) / Extend memory and ranking policies independently)