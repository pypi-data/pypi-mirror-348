# How to Install `dtx`

Before you begin, choose **how you want to run `dtx`** depending on your environment and requirements.

---

## Option 1: Install `dtx` locally **with full dependencies (torch etc.)**

This is recommended if you plan to run **local models** (e.g., Hugging Face, Ollama) on your machine.

```bash
pip install dtx[torch]
```

Includes:
- Core CLI
- `torch`, `transformers` for local LLM and classifier execution
- Supports all datasets and local execution

---

## Option 2: Install `dtx` if **torch is already installed**

If your environment already has `torch` installed (for example, in a GPU-accelerated ML environment), you can skip extras:

```bash
pip install dtx
```

`dtx` will use your existing `torch` installation.

> Tip: Verify torch is installed:
> ```bash
> python -c "import torch; print(torch.__version__)"
> ```

---

## Option 3: Use `uv` for fast installation in a clean environment

If you're creating a new environment and want **fast dependency resolution** with `uv`:

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install `dtx` with full dependencies

```bash
uv pip install dtx[torch]
```

---

## Option 4: Use Docker wrapper (`ddtx`)

If you prefer **Dockerized execution** (no local `torch` install required), you can use `ddtx`.

1. Install `dtx` (for the `ddtx` wrapper CLI):

```bash
pip install dtx
```

2. Use `ddtx` to run inside Docker:

```bash
ddtx redteam scope "Describe your agent" output.yml
```

Features:
- No need to install `torch` locally
- Fully containerized execution
- Automatically mounts `.env` and working directories
- Use Docker-managed templates and tools

---

## Summary of Options

| Method | Use case | Install command |
|--------|----------|----------------|
| Local, full dependencies | Full feature set, local models | `pip install dtx[torch]` |
| Local, existing torch | You already have `torch` installed | `pip install dtx` |
| New env, fast install | Clean, fast setup | `uv pip install dtx[torch]` |
| Docker (ddtx) | No local Python dependencies, isolated | `pip install dtx` + use `ddtx` CLI |

