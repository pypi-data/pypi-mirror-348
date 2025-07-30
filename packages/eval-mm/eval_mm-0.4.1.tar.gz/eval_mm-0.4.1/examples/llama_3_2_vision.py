import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor
from base_vlm import BaseVLM
from utils import GenerationConfig


class VLM(BaseVLM):
    def __init__(
        self, model_id: str = "meta-llama/Llama-3.2-11B-Vision-Instruct"
    ) -> None:
        self.model_id = model_id
        self.model = MllamaForConditionalGeneration.from_pretrained(
            self.model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.processor = AutoProcessor.from_pretrained(self.model_id)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def generate(
        self,
        images: list[Image.Image] | None,
        text: str,
        gen_kwargs: GenerationConfig = GenerationConfig(),
    ) -> str:
        if images is None:
            images = []
        num_images = len(images)
        content = [{"type": "image"} for _ in range(num_images)]
        content.extend([{"type": "text", "text": text}])
        messages = [
            {
                "role": "user",
                "content": content,
            }
        ]
        input_text = self.processor.apply_chat_template(
            messages, add_generation_prompt=True
        )

        inputs = self.processor(
            text=input_text,
            images=images,
            add_special_tokens=False,
            return_tensors="pt",
        ).to(self.device)

        output_ids = self.model.generate(**inputs, **gen_kwargs.__dict__)
        generated_ids = [
            output_ids[len(input_ids) :]
            for input_ids, output_ids in zip(inputs.input_ids, output_ids)
        ]
        return self.processor.decode(
            generated_ids[0],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=True,
        )


if __name__ == "__main__":
    vlm = VLM()
    vlm.test_vlm()
