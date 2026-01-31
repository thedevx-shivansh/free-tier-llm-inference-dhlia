Decentralized Hybrid LLM Inference on Free-Tier GPUs

This repository contains a reproducible deployment of open-weight large language model (LLM) inference running on free-tier GPU infrastructure.

The goal of this project is not to build a product or a framework.
It is to verify, in practice, what kinds of modern reasoning models can actually run under strict hardware and cost constraints (Kaggle free tier).

This repository is linked to a student research paper focused on system-level feasibility, not model training or benchmark competition.

What I built:
I deployed a local inference stack using open-weight LLMs on a free-tier NVIDIA GPU (Kaggle), and validated that:
7B–8B quantized reasoning models can run reliably
Inference is usable after cold start
VRAM usage stays within free-tier limits
Time-to-first-token and throughput are observable and repeatable
The system survives typical free-tier issues (ephemeral sessions, restarts)

The deployment uses:
Ollama for local model execution
Open WebUI for interaction
A single-node setup (no distributed inference)
No paid APIs

Hardware & environment:
Platform: Kaggle Notebooks (Free Tier)
GPU: NVIDIA Tesla T4 (16GB VRAM)
Session type: Ephemeral (12-hour limit)
Cost: $0

Exact environment proof is included in the screenshots folder.

Repository structure
deployment/
  kaggle_ollama_webui.py   → full deployment script

notebooks/
  kaggle_inference_validation.ipynb
  → minimal execution log used for validation

screenshots/
  nvidia-smi.png           → GPU allocation proof
  ollama-running.png       → backend running
  open-webui-ui.png        → UI confirmation
  model-response.png       → inference output

README.md
LICENSE


Nothing here is abstracted or hidden.
What ran is what you see.

What works:
7B–8B open-weight models (quantized)
Stable inference once models are loaded
TTFT in the few-seconds range
Tokens/sec in the tens (hardware dependent)
Repeatable execution across sessions

What does NOT work well:
Long context (>16k tokens) on free tier
Large models (30B+) without aggressive offloading
Production reliability or uptime guarantees
Anything requiring SLAs
This is a research deployment, not a service.

Reproducibility
To reproduce:
Open a Kaggle notebook with GPU enabled
Run the deployment script in deployment/
Verify GPU allocation with nvidia-smi

Run a basic inference prompt:
The notebook in notebooks/ is provided as an execution log, not a tutorial.
The deployment script is the authoritative reference.

Relation to the paper:
This repository is the executable artifact referenced in the accompanying research paper on decentralized / hybrid LLM inference under free-tier constraints.
The paper explains why the system is designed this way.
This repository shows that it actually runs.

Notes:
The code prioritizes reproducibility over elegance
Some steps are intentionally explicit
No optimization beyond what was required to run on free tier
This is intentional.

Author
Shivansh Arora
High School Student (India)
Systems-focused research project
Built and validated through direct experimentation
