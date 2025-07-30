from datasets import Dataset, load_dataset
from .task import Task
from PIL import Image

MULTI_CHOICE_PROMPT = (
    "与えられた選択肢の中から最も適切な回答のアルファベットを直接記入してください。"
)

OPTIONS_MAP = {
    0: "A",
    1: "B",
    2: "C",
    3: "D",
}


def parse_options(options):
    option_letters = [chr(ord("A") + i) for i in range(len(options))]
    choices_str = "\n".join(
        [
            f"{option_letter}. {option}"
            for option_letter, option in zip(option_letters, options)
        ]
    )
    return choices_str


def construct_prompt(question, options):
    parsed_options = parse_options(options)
    return f"{question}\n{parsed_options}\n\n{MULTI_CHOICE_PROMPT}"


def rotate_single_example(doc):
    """
    1つの doc に対して4パターン (options を左回転0,1,2,3) を作り、
    その際に answer も回転にあわせて更新し、各パターンの辞書をリストで返す。
    """
    base_opts = doc["options"]
    n = len(base_opts)  # 4想定
    orig_answer_idx = doc["answer"]  # 0~3
    results = []
    for i in range(n):
        rotated_options = base_opts[i:] + base_opts[:i]
        new_answer_idx = (orig_answer_idx - i) % n
        new_doc = dict(doc)
        new_doc["options"] = rotated_options
        new_doc["answer"] = new_answer_idx
        new_doc["answer_text"] = OPTIONS_MAP[new_answer_idx]
        new_doc["question_id"] = f"{doc['question_id']}_rot{i}"
        new_doc["input_text"] = construct_prompt(
            new_doc["question"], new_doc["options"]
        )
        results.append(new_doc)
    return results


def rotate_options_fn(batch):
    """
    batched=True 用の関数。
    batch: dict of lists
    これを1つずつ取り出して rotate_single_example で4つに拡張し、
    最終的に「列ごとのリスト」を返す。
    """
    # 出力用の空リストを用意
    new_batch = {
        "question": [],
        "options": [],
        "answer": [],
        "answer_text": [],
        "image": [],
        "question_id": [],
        "answer_type": [],
        "background_text": [],
        "input_text": [],
    }

    num_examples = len(batch["question_id"])
    for i in range(num_examples):
        # i番目のサンプル doc をまとめる
        doc = {
            "question": batch["question"][i],
            "options": batch["options"][i],
            "answer": batch["answer"][i],
            "answer_type": batch["answer_type"][i],
            "image": batch["image"][i],
            "background_text": batch["background_text"][i],
            "question_id": batch["question_id"][i],
        }
        # rotateして複数サンプルに展開
        rotated_docs = rotate_single_example(doc)
        # new_batch にappend
        for rd in rotated_docs:
            new_batch["question"].append(rd["question"])
            new_batch["options"].append(rd["options"])
            new_batch["answer"].append(rd["answer"])
            new_batch["answer_text"].append(rd["answer_text"])
            new_batch["image"].append(rd["image"])
            new_batch["question_id"].append(rd["question_id"])
            new_batch["answer_type"].append(rd["answer_type"])
            new_batch["background_text"].append(rd["background_text"])
            new_batch["input_text"].append(rd["input_text"])

    return new_batch


class MECHAJa(Task):
    default_metric = "mecha-ja"

    def _prepare_dataset(self) -> Dataset:
        ds = load_dataset("llm-jp/MECHA-ja", split="test")

        ds = ds.map(
            lambda x, idx: {
                "question": x["question"],
                "options": x["options"],
                "answer": x["answer"],  # 0~3
                "answer_type": x["answer_type"],
                "image": x["image"],
                "background_text": x["background_text"],
                "question_id": str(idx),
                "answer_text": OPTIONS_MAP[x["answer"]],
                "input_text": construct_prompt(x["question"], x["options"]),
            },
            with_indices=True,
        )
        # rotate_choices が有効なら4パターン展開
        if self.config.rotate_choices:
            ds = ds.map(
                rotate_options_fn,
                num_proc=8,
                batched=True,
                remove_columns=ds.column_names,
            )

        return ds

    @staticmethod
    def doc_to_text(doc) -> str:
        return doc["input_text"]

    @staticmethod
    def doc_to_visual(doc) -> list[Image.Image]:
        return [doc["image"]]

    @staticmethod
    def doc_to_id(doc) -> str:
        return str(doc["question_id"])

    @staticmethod
    def doc_to_answer(doc) -> str:
        return doc["answer_text"]


def test_task():
    from eval_mm.tasks.task import TaskConfig

    task = MECHAJa(TaskConfig())
    ds = task.dataset
    print(ds[0])
    assert isinstance(task.doc_to_text(ds[0]), str)
    assert isinstance(task.doc_to_visual(ds[0]), list)
    assert isinstance(task.doc_to_visual(ds[0])[0], Image.Image)
    assert isinstance(task.doc_to_id(ds[0]), str)
    assert isinstance(task.doc_to_answer(ds[0]), str)

    task = MECHAJa(TaskConfig(rotate_choices=True))
    ds = task.dataset
    print(ds[0])
    assert isinstance(task.doc_to_text(ds[0]), str)
    assert isinstance(task.doc_to_visual(ds[0]), list)
    assert isinstance(task.doc_to_visual(ds[0])[0], Image.Image)
    assert isinstance(task.doc_to_id(ds[0]), str)
    assert isinstance(task.doc_to_answer(ds[0]), str)
    assert ds[0]["question_id"] == "0_rot0"
