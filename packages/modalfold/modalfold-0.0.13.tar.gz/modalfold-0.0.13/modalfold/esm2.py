import modal
import numpy as np
from dataclasses import dataclass
from typing import List, Union, Optional, TYPE_CHECKING

import logging

from . import app
from .base import EmbeddingAlgorithm, EmbeddingPrediction, PredictionMetadata
from .images import esm_image
from .utils import MINUTES, MODEL_DIR
from .images.volumes import model_weights
from .utils import Timer

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from transformers.modeling_outputs import BaseModelOutputWithPoolingAndCrossAttentions


@dataclass
class ESM2Output(EmbeddingPrediction):
    """Output from ESM2 prediction including all model outputs."""

    embeddings: np.ndarray  # (batch_size, seq_len, embedding_dim)
    metadata: PredictionMetadata
    hidden_states: Optional[np.ndarray] = None  # (batch_size, hidden_state_iter, seq_len, embedding_dim)


with esm_image.imports():
    import torch
    from transformers import EsmModel, AutoTokenizer


@app.cls(
    image=esm_image,
    gpu="T4",
    timeout=20 * MINUTES,
    container_idle_timeout=10 * MINUTES,
    volumes={MODEL_DIR: model_weights},
)
class ESM2(EmbeddingAlgorithm):
    """ESM2 protein language model."""

    DEFAULT_CONFIG = {
        "model_name": "esm2_t33_650M_UR50D",
        "output_hidden_states": True,
    }

    def __init__(self, config: dict = {}) -> None:
        super().__init__(config)
        self.metadata = self._initialize_metadata(
            model_name="ESM2",
            model_version="v4.49.0",  # HuggingFace transformers version
        )
        self.model_dir: Optional[str] = None
        self.tokenizer: Optional[AutoTokenizer] = None
        self.model: Optional[EsmModel] = None
        self.assert_valid_model(config)

    @staticmethod
    def assert_valid_model(config: dict) -> None:
        """
        Validate that the model name is supported.

        Available ESM2 models:
        - esm2_t48_15B_UR50D: 48 layers, 5120 hidden size, 40 attention heads
        - esm2_t36_3B_UR50D: 36 layers, 2560 hidden size, 40 attention heads
        - esm2_t33_650M_UR50D: 33 layers, 1280 hidden size, 20 attention heads
        - esm2_t30_150M_UR50D: 30 layers, 640 hidden size, 12 attention heads
        - esm2_t12_35M_UR50D: 12 layers, 480 hidden size, 20 attention heads
        - esm2_t6_8M_UR50D: 6 layers, 320 hidden size, 20 attention heads
        """
        models_name = [
            "esm2_t48_15B_UR50D",
            "esm2_t36_3B_UR50D",
            "esm2_t33_650M_UR50D",
            "esm2_t30_150M_UR50D",
            "esm2_t12_35M_UR50D",
            "esm2_t6_8M_UR50D",
        ]
        assert config["model_name"] in models_name, f"Model {config['model_name']} not supported"

    @modal.enter()
    def _initialize(self) -> None:
        self.model_dir = MODEL_DIR
        self._load()

    def _load(self) -> None:
        if self.tokenizer is None:
            self.tokenizer = AutoTokenizer.from_pretrained(f"facebook/{self.config['model_name']}")
        if self.model is None:
            self.model = EsmModel.from_pretrained(f"facebook/{self.config['model_name']}")
        self.device = "cuda"
        self.model = self.model.cuda()
        self.model.eval()
        self.ready = True

    @modal.method()
    def embed(self, sequences: Union[str, List[str]]) -> ESM2Output:
        if self.tokenizer is None and self.model is None:
            logger.warning("Model not loaded. Forcing the model to load... Next time call _load() first.")
            self._load()
        assert self.tokenizer is not None and self.model is not None, "Model not loaded"

        logger.debug(f'Embedding {len(sequences)} sequences using {self.config["model_name"]}')

        # adds <cls> to the start, <eos> to the end
        inputs = self.tokenizer(
            sequences,
            return_tensors="pt",
            padding=True,
            truncation=True,
        )
        inputs = inputs.to(self.device)
        inputs["output_hidden_states"] = self.config["output_hidden_states"]
        inputs["use_cache"] = True

        # TODO: implement multimer?!
        if any(":" in seq for seq in sequences):
            raise ValueError("Multimer not supported")

        with Timer("Model Inference") as timer:
            with torch.inference_mode():
                outputs = self.model(**inputs)

        outputs = self._convert_outputs(outputs, timer.duration)

        # TODO: check whether we might not want to send anything else, as we should try to send in as
        # much raw information as possible
        return outputs

    def _convert_outputs(
        self, outputs: "BaseModelOutputWithPoolingAndCrossAttentions", prediction_time: float
    ) -> ESM2Output:
        """Convert model outputs to ESM2Output format."""

        embeddings = outputs.last_hidden_state.cpu().numpy()
        self.metadata.prediction_time = prediction_time

        if self.config["output_hidden_states"]:
            assert torch.all(
                outputs.hidden_states[-1] == outputs.last_hidden_state
            ), "Last hidden state should be the same as the output of the model"
            hidden_states = np.stack([h.cpu().numpy() for h in outputs.hidden_states], axis=1)
        else:
            hidden_states = None

        return ESM2Output(metadata=self.metadata, embeddings=embeddings, hidden_states=hidden_states)


def get_esm2(gpu_type="T4", config: dict = {}):
    """
    Note that the app will still show that's using T4, but the actual method / function call will use the correct GPU,
    and display accordingly in the Modal dashboard.
    """
    Model = ESM2.with_options(gpu=gpu_type)  # type: ignore
    return Model(config=config)
