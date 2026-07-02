#!/usr/bin/env bash
# Runs the complex seed with 4 agents for 5 epochs using local LLaMA 3
python -m cli.run_experiment --seed examples/seed_complex.json --epochs 5 --pop 4 --provider ollama --model llama3