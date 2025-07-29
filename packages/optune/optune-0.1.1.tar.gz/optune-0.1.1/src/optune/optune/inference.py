from typing import Tuple, List
from optune.optune.lm_response_types import ClassificationResponse
import requests
import json


class Inference:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url


    def shutdown(self):
        pass

    def _model_inference(self, model_name: str, input_text: str) -> Tuple[List[float], List[str]]:
        url = f"{self.base_url}/public/triton/v2/models/{model_name}/infer"

        payload = json.dumps({
            "inputs": [{
                "name": "input_text",
                "shape": [1, 1],
                "datatype": "BYTES",
                "data": [input_text]
            }],
            "outputs": [{
                "name": "labels",
                "parameters" : { "classification": 1 }
            }, 
            {
                "name": "raw_logits",
                "parameters" : { "binary_data": False }
            }]
        })
        response = requests.request("POST", url, headers={'Content-Type': 'application/json'}, data=payload)
        response.raise_for_status()
        inference_output = response.json()["outputs"]
        raw_logits = next((output["data"] for output in inference_output if output["name"] == "raw_logits"), None)
        response_labels = next((output["data"] for output in inference_output if output["name"] == "labels"), None)
        return raw_logits, response_labels
    
    def _parse_response(self, response: list[str]) -> list[ClassificationResponse]:
        labels = [label.split(":")[2] for label in response]
        return [ClassificationResponse(labels=labels)]
    
    def infer(self, prompt: str, usecase_name: str, group_name: str) -> Tuple[List[ClassificationResponse], List[float]]:
        model_name = f"model_{group_name}_{usecase_name}"
        raw_logits, response_labels = self._model_inference(model_name, prompt)
        return self._parse_response(response_labels), raw_logits
