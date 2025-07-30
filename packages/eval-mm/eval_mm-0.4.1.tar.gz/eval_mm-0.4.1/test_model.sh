#!/bin/bash
set -eux  # エラーが発生したらスクリプトを停止する

# Set CUDA devices
export CUDA_VISIBLE_DEVICES=0

# Model name to group name mapping
declare -A MODEL_GROUP_MAP=(
    ["stabilityai/japanese-instructblip-alpha"]="normal"
    ["stabilityai/japanese-stable-vlm"]="calm"
    ["cyberagent/llava-calm2-siglip"]="calm"
    ["llava-hf/llava-1.5-7b-hf"]="normal"
    ["llava-hf/llava-v1.6-mistral-7b-hf"]="normal"
    ["neulab/Pangea-7B-hf"]="sarashina"
    ["meta-llama/Llama-3.2-11B-Vision-Instruct"]="normal"
    ["OpenGVLab/InternVL2-8B"]="normal"
    ["Qwen/Qwen2-VL-7B-Instruct"]="normal"
    ["Qwen/Qwen2.5-VL-7B-Instruct"]="normal"
    ["gpt-4o-2024-05-13"]="normal"
    ["mistralai/Pixtral-12B-2409"]="pixtral"
    ["llm-jp/llm-jp-3-vila-14b"]="vilaja"
    ["Efficient-Large-Model/VILA1.5-13b"]="vilaja"
    ["SakanaAI/Llama-3-EvoVLM-JP-v2"]="evovlm"
    ["google/gemma-3-4b-it"]="normal"
    ["sbintuitions/sarashina2-vision-8b"]="sarashina"
    ["microsoft/Phi-4-multimodal-instruct"]="phi"
    ["MIL-UT/Asagi-14B"]="normal"
)

for model_name in "${!MODEL_GROUP_MAP[@]}"; do
    model_group=${MODEL_GROUP_MAP[$model_name]}
    uv sync --group $model_group
    uv run --group $model_group  python examples/test_model.py \
        --model_id "$model_name"
done
