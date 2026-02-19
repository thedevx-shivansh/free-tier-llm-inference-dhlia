# Decentralized Hybrid LLM Inference on Free-Tier GPUs

> **A systems-level feasibility study of running modern open-weight LLMs  
> on free-tier GPU infrastructure.**

---

## Overview

This repository contains a **reproducible deployment** of open-weight large language model (LLM) inference running entirely on **free-tier GPU infrastructure**.

The objective of this project is **not** to build a product, framework, or hosted service.

Instead, it answers a narrower and more practical question:

> **What kinds of modern reasoning-capable LLMs actually run under strict hardware and cost constraints?**

All experiments were executed on the **Kaggle free tier**, with no paid APIs and no persistent infrastructure.

This repository serves as the **executable artifact** for an accompanying **student research paper** focused on *system-level feasibility*, not model training or benchmark competition.
**Research Paper Link:**
**https://zenodo.org/records/18466177**
**Kaggle Logs:**
**https://www.kaggle.com/code/shivanshdevx/free-tier-llm-inference-validation**

---

## What Was Built

A local inference stack was deployed using **open-weight LLMs** on a free-tier NVIDIA GPU and validated through direct execution.

The system demonstrates that:

- Quantized **7B–8B reasoning models** can run reliably  
- Inference remains usable after cold start  
- GPU memory usage stays within free-tier limits  
- **Time-to-first-token (TTFT)** and throughput are observable and repeatable  
- The setup tolerates common free-tier constraints  
  (ephemeral sessions, restarts, session limits)

All claims are based on **observed behavior**, not estimates.

---

## System Architecture

**Deployment characteristics**

- **Inference engine:** Ollama  
- **User interface:** Open WebUI  
- **Topology:** Single-node (no distributed inference)  
- **APIs:** None (fully local execution)  

This project prioritizes **what runs in practice**, not architectural abstraction.

---

## Hardware & Runtime Environment

| Component | Details |
|--------|--------|
| Platform | Kaggle Notebooks (Free Tier) |
| GPU | NVIDIA Tesla T4 (16 GB VRAM) |
| Session Type | Ephemeral (≈12-hour limit) |
| Cost | `$0` |

> [!NOTE]  
> Exact runtime proof (GPU allocation, backend status, UI, and inference output)  
> is included in the `screenshots/` directory.

---

## Repository Layout

```text
deployment/
 └─ kaggle_ollama_webui.py
    → Full deployment script

notebooks/
 └─ kaggle_inference_validation.ipynb
    → Minimal execution log used for validation

screenshots/
 ├─ nvidia-smi.png        → GPU allocation proof
 ├─ ollama-running.png    → Backend running
 ├─ open-webui-ui.png     → UI confirmation
 └─ model-response.png   → Inference output

README.md
LICENSE

