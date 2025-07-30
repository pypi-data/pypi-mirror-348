# mecha-ja-scorer.py
from .scorer import Scorer, AggregateOutput
import re
from collections import defaultdict

ANSWER_TYPE_MAP = {
    "Factoid": 0,
    "Non-Factoid": 1,
}


class MECHAJaScorer(Scorer):
    @staticmethod
    def _parse_rotation_id(qid: str) -> str:
        """
        question_id に '_rot{i}' が含まれているかを正規表現で調べる。
        含まれていれば i (数字) を文字列として返し、無ければ "no_rot" を返す。
        """
        pattern = r"(.*)_rot(\d+)$"
        match = re.match(pattern, qid)
        if match:
            return match.group(2)  # 例えば "2"
        else:
            return "no_rot"

    @staticmethod
    def score(refs: list[str], preds: list[str]) -> list[int]:
        """
        Checks whether each reference string is contained in the corresponding
        prediction string and returns a list of integer scores (1 for True, 0 for False).
        """
        scores = []
        for ref, pred in zip(refs, preds):
            score = 1 if ref in pred else 0
            scores.append(score)
        return scores

    def aggregate(self, scores: list[int]) -> AggregateOutput:
        """
        回転IDごとにスコアを集計して、以下のような構造を返す:
        {
          "rot_{rot_id}": {
            "overall": float,
            "Factoid": float,
            "Non-Factoid": float,
            "with_background": float,
            "without_background": float
          },
          "no_rot": { ... },
          ...
        }
        """
        data_all = defaultdict(list)
        data_by_rot: defaultdict[str, dict[str, list[int]]] = defaultdict(
            lambda: {
                "overall": [],
                "factoid": [],
                "non_factoid": [],
                "with_bg": [],
                "without_bg": [],
            }
        )
        docs = self.config.docs
        assert docs is not None
        for doc, score in zip(docs, scores):
            rot_id = MECHAJaScorer._parse_rotation_id(doc["question_id"])
            is_factoid = doc["answer_type"] == ANSWER_TYPE_MAP["Factoid"]
            has_bg = bool(doc["background_text"])

            # Overall
            data_all["overall"].append(score)
            data_by_rot[rot_id]["overall"].append(score)

            # Factoid / Non-Factoid
            if is_factoid:
                data_all["factoid"].append(score)
                data_by_rot[rot_id]["factoid"].append(score)
            else:
                data_all["non_factoid"].append(score)
                data_by_rot[rot_id]["non_factoid"].append(score)

            # With / Without Background
            if has_bg:
                data_all["with_bg"].append(score)
                data_by_rot[rot_id]["with_bg"].append(score)
            else:
                data_all["without_bg"].append(score)
                data_by_rot[rot_id]["without_bg"].append(score)

        def avg(lst):
            return sum(lst) / len(lst) if lst else 0.0

        result = {
            "overall": avg(data_all["overall"]),
            "Factoid": avg(data_all["factoid"]),
            "Non-Factoid": avg(data_all["non_factoid"]),
            "with_background": avg(data_all["with_bg"]),
            "without_background": avg(data_all["without_bg"]),
        }

        for rot_id, cat_scores in data_by_rot.items():
            result[f"rot_{rot_id}"] = {
                "overall": avg(cat_scores["overall"]),
                "Factoid": avg(cat_scores["factoid"]),
                "Non-Factoid": avg(cat_scores["non_factoid"]),
                "with_background": avg(cat_scores["with_bg"]),
                "without_background": avg(cat_scores["without_bg"]),
            }
        output = AggregateOutput(result["overall"], result)

        return output


def test_mechaja_scorer():
    refs = ["私は猫です。"]
    preds = ["私は猫です。"]
    from .scorer import ScorerConfig

    scorer = MECHAJaScorer(
        ScorerConfig(
            docs=[{"question_id": "q1", "answer_type": 0, "background_text": ""}]
        )
    )
    scores = MECHAJaScorer.score(refs, preds)

    assert scores == [1]
    output = scorer.aggregate(scores)
    assert output.overall_score == 1.0
    assert output.details == {
        "overall": 1.0,
        "Factoid": 1.0,
        "Non-Factoid": 0.0,
        "with_background": 0.0,
        "without_background": 1.0,
        "rot_no_rot": {
            "overall": 1.0,
            "Factoid": 1.0,
            "Non-Factoid": 0.0,
            "with_background": 0.0,
            "without_background": 1.0,
        },
    }
