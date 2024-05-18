from typing import Any
from transformers import pipeline
from dataclasses import dataclass

@dataclass
class Sentimets:
    def __init__(self, task: str = "text-classification") -> None:
        """
        Args:
            task (str) - task of models
        """

        self.MODEL_TEXT_TYPE = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.MODEL_TEXT_SENTIMENT = "bhadresh-savani/roberta-base-emotion"

        self.model_sentence_type = pipeline(task, self.MODEL_TEXT_TYPE)
        self.model_semtence_sentiment = pipeline(task, self.MODEL_TEXT_SENTIMENT)


    def predict(self, comments: list[str]) -> tuple[list[Any], list[Any]]:
        """Function makes predictions on data using selected models

        Args:
            comments (list[str]): list of comments

        Returns:
            tuple[list[Any], list[Any]]: labels from predictions of two models
        """
       
        result_type = self.model_sentence_type(comments)
        result_sentiment = self.model_semtence_sentiment(comments)

        list_type = []
        list_sentiments = []
        for (comm_type, comm_sentiment) in zip(result_type, result_sentiment): # type: ignore
            if round(comm_type["score"], 1) >= 0.5:
                list_type.append(comm_type["label"])
            else:
                list_type.append("type_undefined")

            if round(comm_sentiment["score"], 1) >= 0.5:
                list_sentiments.append(comm_sentiment["label"])
            else:
                list_sentiments.append("sentiment_undefined")

        return list_type, list_sentiments