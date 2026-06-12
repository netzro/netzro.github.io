Title: How LLMs Are Built — Inside The Architecture
Date: 2026-06-12
Author: Gifted
Category: Technology
Tags: ai, architecture
Slug: how-llms-are-built-inside-the-architecture
Summary: From tokenization to inference — a plain-language walk through how large language models are structured, trained, and named.

---

Every few months a new model drops. GPT-4o. Claude 3.5 Sonnet. Gemini 2.0 Flash. Qwen3. The names sound like car trims. The press releases sound like science fiction. But under the branding, the architecture is surprisingly consistent.

This post is what I wish someone had handed me before I started building agents on top of these systems. What is actually inside a large language model. How it gets built. And what the names mean.

## What An LLM Actually Is

A large language model is a function. You give it a sequence of tokens, it returns a probability distribution over the next token. That is it. Everything else — the persuasive essays, the code generation, the code-switching between languages — is emergent behavior from doing that one thing at scale.

The "large" part refers to parameters. A parameter is a weight in the neural network. GPT-3 had 175 billion parameters. Current top models are rumored to be in the trillions. Each parameter is a floating-point number that gets learned during training. More parameters generally means more capacity to store patterns, but also more cost to train and run.

The "language" part is a misnomer, by the way. These models do not understand language the way you and I do. They model statistical relationships between tokens. Whether that constitutes "understanding" is a philosophical question. For engineering purposes, it does not matter — the output is what matters.

## The Name Game

Let me decode the naming conventions, because they are more structured than they look.

**Company + Model Family + Variant + Size + Version**

Take `claude-sonnet-4` as an example:

- `claude` — the model family (Anthropic's brand)
- `sonnet` — the tier (Anthropic names tiers after literary forms: Haiku < Sonnet < Opus, from light to heavy)
- `4` — the generation

Or `gpt-4o-mini`:

- `gpt` — the family (OpenAI's Generative Pre-trained Transformer)
- `4` — the generation
- `o` — "omni," meaning multimodal (text + image + audio input)
- `mini` — the size variant

Or `gemini-2.0-flash`:

- `gemini` — the family (Google)
- `2.0` — the generation
- `flash` — the size variant (speed-optimized, lighter than "pro" or "ultra")

OpenRouter, which is what I use to route models, follows this pattern in their model slugs: `provider/model-name`. So `anthropic/claude-sonnet-4` means "Anthropic's Claude, Sonnet tier, generation 4."

Some other patterns:

- **Parameter count in the name:** Llama 3.1 70B means "70 billion parameters." GPT-3 meant "3rd generation GPT," not 3 billion parameters.
- **Suffixes:** `-instruct`, `-chat`, `-turbo` — these distinguish base models from fine-tuned variants optimized for conversation. `llama-3.1-70b-instruct` is the instruct-tuned version. It has been further trained on dialogue data.
- **Context length:** Sometimes appended as `128k` or `200k`, indicating the number of tokens the model can process in a single request.

The names are not arbitrary. They encode the model's lineage, capability, and cost tier. Learn to read them and you can make better routing decisions before you spend a single token of inference.

## The Architecture

Nearly every modern LLM is a **transformer**. The transformer architecture was introduced in the 2017 paper "Attention Is All You Need" — arguably the most cited paper in modern AI. Before transformers, language models used recurrent neural networks (RNNs). RNNs processed text sequentially, one token at a time, which made them slow and bad at long-range dependencies.

The transformer changed everything with one mechanism: **self-attention**.

Self-attention lets every token in a sequence look at every other token simultaneously. If the sentence is "The bank was steep so I sat by the river bank," the word "bank" can attend to both "steep" and "river" to disambiguate. An RNN would have to process the whole sentence sequentially to get there. The transformer does it in one pass.

The transformer stack looks like this:

- **Input embeddings** — each token is converted to a high-dimensional vector (a list of numbers)
- **Positional encoding** — since the transformer has no notion of order, position information is added to each token's embedding
- **Multi-head self-attention** — each layer computes attention across the entire sequence, with multiple "heads" capturing different relationship types simultaneously
- **Feed-forward network** — a small two-layer network applied independently to each token
- **Layer normalization** — stabilizes training
- **Repeat** — this block is stacked. GPT-3 had 96 layers. Current models range from 32 to 120+. Each layer refines the representation

The output is passed through a final linear layer and softmax to produce probabilities over the entire vocabulary (typically 32,000 to 200,000+ tokens).

## The Training Pipeline

Training an LLM happens in three phases.

**Phase 1: Pre-training (language modeling)**

This is where 99% of the cost goes. The model is trained on a massive corpus of text — books, websites, code repositories, papers, conversations. The task is simple: given all previous tokens, predict the next one.

If the input is "The cat sat on the," the model should assign high probability to "mat," "floor," "couch" and low probability to "refrigerator." The loss function measures how wrong the model is, and gradient descent updates all those billions of parameters to make it less wrong.

This phase takes thousands of GPUs running for weeks or months. For GPT-4, estimates put the training cost above $100 million. For Llama 3 (405B parameters), Meta used 16,000 H100 GPUs for 54 days.

The result is a **base model**. It is good at predicting text but not at following instructions. If you ask a base model "Write me a poem about Lagos," it might instead continue with "Lagos is the most populous city in Nigeria with an estimated population of..." — because training data is heavy on Wikipedia-style completions.

**Phase 2: Supervised fine-tuning (SFT)**

Humans write ideal responses to prompts, and the model is trained to produce those responses instead of generic continuations. This teaches the model to be helpful, follow instructions, and format outputs correctly.

The dataset here is much smaller — tens of thousands of examples, not trillions of tokens. But the examples are high-quality, written by annotators with clear guidelines.

The result is an **instruct model** or **chat model**. This is what most APIs serve by default.

**Phase 3: Reinforcement learning from human feedback (RLHF) — or alternatives**

This is where the model is aligned with human preferences. Humans rank multiple outputs from the model (e.g., "Response A is better than Response B because it's more concise and accurate"). A reward model is trained on these rankings, and then the LLM is optimized to maximize reward.

Some systems use DPO (Direct Preference Optimization) or RLAIF (Reinforcement Learning from AI Feedback, where an AI does the ranking instead of humans). The goal is the same: shape the model's behavior beyond what SFT alone can achieve.

The final product is what you interact with when you call an API.

## The Inference Engine

When you send a prompt to an LLM, here is what happens:

- **Tokenization** — your text is split into tokens. Not words. Subwords. A tokenizer (usually Byte-Pair Encoding or SentencePiece) breaks text into pieces. "Unbelievable" might become ["Un", "believ", "able"]. Code and tokenization are separate concerns but deeply intertwined — the choice of tokenizer affects how well the model handles different languages, code, and special characters.
- **Prefill phase** — the model processes your entire prompt in one forward pass, building up the key-value cache for each layer. This is the expensive part for long prompts.
- **Decode phase** — the model generates output one token at a time, autoregressively. Each new token is appended to the input, and the model runs again. This is why generation feels slow — it is inherently sequential.
- **Sampling** — the raw probability distribution is adjusted by temperature and top-p/top-k sampling parameters before a token is selected. Temperature 0 means "always pick the most likely token." Higher values add randomness.

This is why context window matters. A model with a 128k token context must maintain key-value caches for all 128,000 positions, which explodes memory usage. This is where techniques like grouped-query attention, sliding window attention, and mixture-of-experts come in — architectural innovations to make long contexts practical.

## What Makes Models Different

If they all use transformers, why do models behave so differently?

- **Training data composition.** A model trained heavily on code will be better at coding. A model trained on multilingual data will handle multiple languages. The data diet defines the model.
- **Data quality and filtering.** More is not always better. Llama 3's team devoted enormous effort to data quality, deduplication, and filtering junk from the pre-training corpus.
- **Architecture tweaks.** Mixture of Experts (MoE) activates only a subset of parameters per token, allowing larger models without proportionally larger compute. Some models use different attention variants (GQA, MLA) to reduce memory.
- **Post-training.** Two models with identical pre-training can diverge dramatically based on SFT and RLHF. This is where Anthropic's safety focus, OpenAI's tool-use optimization, and Google's multimodal integration show up.
- **System prompt.** The invisible instructions prepended to every conversation shape how the model behaves. It is part of the product, not the architecture, but it is often the biggest differentiator in practice.

## Where This Is Going

The trend is toward efficiency. Qwen3 packs strong performance into a smaller parameter count through better training data and distillation. Ollama and llama.cpp make it possible to run quantized models on consumer hardware.

The other trend is specialization. General-purpose models are being complemented by purpose-built models — code generation, document processing, audio understanding. The era of one-model-does-everything gives way to model routing, where different tasks get routed to different models optimized for that task. This is the problem OmniRoute solves in my stack.

The architecture is not changing fundamentally. The transformer is still the backbone. But everything around it — training data quality, efficiency techniques, alignment methods, inference optimization — is evolving fast.

The models will get smaller, faster, smarter, and cheaper. The names will keep sounding like car trims. And under the hood, it will still be tokens going in and probabilities coming out.

---

*I run multiple LLMs through OmniRoute on a self-hosted infrastructure. If you are building on top of these models, understanding the architecture helps you choose the right tool and set realistic expectations.*