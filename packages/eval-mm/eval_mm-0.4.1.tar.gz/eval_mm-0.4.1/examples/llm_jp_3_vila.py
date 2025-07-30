import torch
from llava.constants import IMAGE_TOKEN_INDEX
from llava.conversation import conv_templates
from llava.mm_utils import (
    get_model_name_from_path,
    process_images,
    tokenizer_image_token,
)
from llava.model.builder import load_pretrained_model
from base_vlm import BaseVLM
from utils import GenerationConfig
from PIL import Image


class VLM(BaseVLM):
    def __init__(self, model_id: str = "llm-jp/llm-jp-3-vila-14b") -> None:
        self.model_id = model_id
        model_name = get_model_name_from_path(self.model_id)
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tokenizer, self.model, self.image_processor, _ = load_pretrained_model(
            self.model_id, model_name, device=device
        )

    def generate(
        self,
        images: list[Image.Image] | None,
        text: str,
        gen_kwargs: GenerationConfig = GenerationConfig(),
    ) -> str:
        if images is None:
            images = []
        qs = text
        if "<image>" not in text:
            qs = "<image>\n" * len(images) + text
        conv_mode = "llmjp_v3"
        conv = conv_templates[conv_mode].copy()
        conv.append_message(conv.roles[0], qs)
        conv.append_message(conv.roles[1], None)
        prompt = conv.get_prompt()

        images_tensor = [
            process_images(images, self.image_processor, self.model.config).to(
                self.model.device, dtype=torch.float16
            )
        ]
        input_ids = (
            tokenizer_image_token(
                prompt, self.tokenizer, IMAGE_TOKEN_INDEX, return_tensors="pt"
            )
            .unsqueeze(0)
            .to(self.model.device)
        )

        with torch.inference_mode():
            output_ids = self.model.generate(
                input_ids,
                images=images_tensor,
                **gen_kwargs.__dict__,
            )

        outputs = self.tokenizer.batch_decode(output_ids, skip_special_tokens=True)[0]
        return outputs


if __name__ == "__main__":
    vlm = VLM()
    vlm.test_vlm()
