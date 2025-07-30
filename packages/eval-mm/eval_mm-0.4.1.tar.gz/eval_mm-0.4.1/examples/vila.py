# This file is modified from https://github.com/haotian-liu/LLaVA/

# rye add protobuf
# uv pip install flash-attn --no-build-isolation --python .venv

from base_vlm import BaseVLM
from utils import GenerationConfig

import torch

from llava_vila.conversation import SeparatorStyle, conv_templates
from llava_vila.mm_utils import (
    get_model_name_from_path,
    process_images,
    tokenizer_image_token,
)
from llava_vila.model.builder import load_pretrained_model
from PIL import Image


class VLM(BaseVLM):
    def __init__(self, model_id: str = "Efficient-Large-Model/VILA1.5-13b"):
        self.model_id = model_id
        model_name = get_model_name_from_path(self.model_id)
        self.model_name = model_name
        self.tokenizer, self.model, self.image_processor, _ = load_pretrained_model(
            self.model_id, model_name
        )
        # from transformers import AutoModelForCausalLM, AutoTokenizer, AutoProcessor
        # self.model = AutoModelForCausalLM.from_pretrained("Efficient-Large-Model/VILA-13b")
        # self.tokenizer = self.model.config.tokenizer
        # self.image_processor = AutoProcessor.from_pretrained("Efficient-Large-Model/VILA-13b")

    def generate(
        self,
        images: list[Image.Image] | None,
        text: str,
        gen_kwargs: GenerationConfig = GenerationConfig(),
    ) -> str:
        qs = text
        if images is None:
            images = []
        if "<image>" not in text:
            qs = "<image>\n" * len(images) + text

        if "llama-2" in self.model_name.lower():
            conv_mode = "llava_llama_2"
        elif "v1" in self.model_name.lower():
            conv_mode = "llava_v1"
        elif "mpt" in self.model_name.lower():
            conv_mode = "mpt"
        else:
            conv_mode = "llava_v0"

        conv = conv_templates[conv_mode].copy()
        conv.append_message(conv.roles[0], qs)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()
        if images is None:
            images_tensor = None
        else:
            images_tensor = [
                process_images(images, self.image_processor, self.model.config).to(
                    self.model.device, dtype=torch.float16
                )
            ]
        input_ids = (
            tokenizer_image_token(prompt, self.tokenizer, -200, return_tensors="pt")
            .unsqueeze(0)
            .cuda()
        )

        stop_str = conv.sep if conv.sep_style != SeparatorStyle.TWO else conv.sep2
        # keywords = [stop_str] # if needed, add keywords

        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids,
                images=images_tensor,
                **gen_kwargs.__dict__,
            )
        outputs = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
        outputs = outputs.strip()
        if outputs.endswith(stop_str):
            outputs = outputs[: -len(stop_str)]
        outputs = outputs.strip()
        return outputs


if __name__ == "__main__":
    vlm = VLM("Efficient-Large-Model/VILA1.5-13b")
    vlm.test_vlm()
