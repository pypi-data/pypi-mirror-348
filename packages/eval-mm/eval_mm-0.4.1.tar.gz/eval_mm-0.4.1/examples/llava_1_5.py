import torch
from PIL import Image
from transformers import AutoProcessor, LlavaForConditionalGeneration
from base_vlm import BaseVLM
from utils import GenerationConfig

DEFAULT_IMAGE_TOKEN = "<image>"


class VLM(BaseVLM):
    def __init__(self, model_id: str = "llava-hf/llava-1.5-7b-hf") -> None:
        self.model_id = model_id
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = LlavaForConditionalGeneration.from_pretrained(
            self.model_id,
            torch_dtype=torch.float16,
            low_cpu_mem_usage=True,
        )
        self.processor = AutoProcessor.from_pretrained(self.model_id)
        self.model.to(self.device)

    def generate(
        self,
        images: list[Image.Image] | None,
        text: str,
        gen_kwargs: GenerationConfig = GenerationConfig(),
    ) -> str:
        if images is None:
            images = []
        if DEFAULT_IMAGE_TOKEN in text:
            text = text.replace(DEFAULT_IMAGE_TOKEN, "")
        content = [{"type": "image"} for _ in range(len(images))]
        content.extend([{"type": "text", "text": text}])
        messages = [
            {
                "role": "user",
                "content": content,
            },
        ]

        prompt = self.processor.apply_chat_template(
            messages, add_generation_prompt=True
        )

        # processorがimages=Noneと[]を区別する可能性があるため、分岐で処理
        if len(images) == 0:
            inputs = self.processor(text=prompt, return_tensors="pt").to(self.device)
        else:
            inputs = self.processor(images=images, text=prompt, return_tensors="pt").to(
                self.device
            )

        output = self.model.generate(**inputs, **gen_kwargs.__dict__)[0]
        generated_text = self.processor.decode(output, skip_special_tokens=True)
        answer = generated_text.split("ASSISTANT:")[-1].strip()
        return answer


if __name__ == "__main__":
    vlm = VLM()
    vlm.test_vlm()
