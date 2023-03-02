"""LLM Chain specifically for evaluating question answering."""
from __future__ import annotations

from typing import Any, List

from langchain.chains.llm import ChatModelChain
from langchain.chat_models.base import BaseChatModel
from langchain.evaluation.qa.eval_prompt import CHAT_COMP_PROMPT
from langchain.prompts.base import BasePromptTemplate


class QACompChatChain(ChatModelChain):
    """LLM Chain specifically for evaluating question answering."""

    @classmethod
    def from_llm(
        cls,
        llm: BaseChatModel,
        prompt: BasePromptTemplate = CHAT_COMP_PROMPT,
        **kwargs: Any,
    ) -> QACompChatChain:
        expected_input_vars = {"query", "answer", "result"}
        if expected_input_vars != set(prompt.input_variables):
            raise ValueError(
                f"Input variables should be {expected_input_vars}, "
                f"but got {prompt.input_variables}"
            )
        return cls(llm=llm, prompt=prompt, **kwargs)

    def evaluate(
        self,
        examples: List[dict],
        predictions_a: List[dict],
        predictions_b: List[dict],
        question_key: str = "query",
        answer_key: str = "answer",
        prediction_key: str = "result",
    ) -> List[dict]:
        """Evaluate question answering examples and predictions."""
        inputs = [
            {
                "query": example[question_key],
                "answer": example[answer_key],
                "student_a": predictions_a[i][prediction_key],
                "student_b": predictions_b[i][prediction_key],
            }
            for i, example in enumerate(examples)
        ]
        results = [self(inp) for inp in inputs]
        return results