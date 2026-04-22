# 🏭 Industrial RAG Agent for Documents

A conversational AI agent designed to extract, analyze, and answer precise technical questions based on complex industrial documentation (Siemens S7-1500 TM NPU manuals).

## 💡 The Problem

In industrial automation, engineers waste valuable hours searching for specific configuration parameters, voltage specs, or safety procedures buried inside PDF manuals hundreds of pages long.

## 🚀 The Solution

This project implements a local **RAG (Retrieval-Augmented Generation)** architecture. It allows users to ask questions in natural language and receive immediate technical answers, citing exactly the **document and page number** where the information was retrieved — ensuring full traceability and eliminating hallucinations.

## ⚙️ Technical Architecture

The system is built with a modular and scalable approach:

* **Orchestration:** LangGraph and LangChain for agent state management and tool handling.
* **Reasoning Engine (LLM):** Claude 3.5 Haiku (via Anthropic API) configured with `ToolStrategy` for strict structured outputs.
* **Local Vectorization:** HuggingFace models (`all-MiniLM-L6-v2`) running on CPU to guarantee the privacy of industrial documents.
* **Vector Database:** FAISS (Facebook AI Similarity Search) in-memory for ultra-low latency retrieval.

## 🛠️ Installation & Usage

1. Clone this repository:
```bash
git clone https://github.com/CristhianTechAIHub/Industrial-Agent-AI.git
```
