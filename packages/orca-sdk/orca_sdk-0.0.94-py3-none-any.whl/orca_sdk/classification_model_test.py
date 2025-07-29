import logging
import os
from uuid import uuid4

import numpy as np
import pytest
from datasets.arrow_dataset import Dataset

from .classification_model import ClassificationModel
from .datasource import Datasource
from .embedding_model import PretrainedEmbeddingModel
from .memoryset import LabeledMemoryset

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


SKIP_IN_GITHUB_ACTIONS = os.getenv("GITHUB_ACTIONS") == "true"


def test_create_model(model: ClassificationModel, readonly_memoryset: LabeledMemoryset):
    assert model is not None
    assert model.name == "test_model"
    assert model.memoryset == readonly_memoryset
    assert model.num_classes == 2
    assert model.memory_lookup_count == 3


def test_create_model_already_exists_error(readonly_memoryset, model: ClassificationModel):
    with pytest.raises(ValueError):
        ClassificationModel.create("test_model", readonly_memoryset)
    with pytest.raises(ValueError):
        ClassificationModel.create("test_model", readonly_memoryset, if_exists="error")


def test_create_model_already_exists_return(readonly_memoryset, model: ClassificationModel):
    with pytest.raises(ValueError):
        ClassificationModel.create("test_model", readonly_memoryset, if_exists="open", head_type="MMOE")

    with pytest.raises(ValueError):
        ClassificationModel.create("test_model", readonly_memoryset, if_exists="open", memory_lookup_count=37)

    with pytest.raises(ValueError):
        ClassificationModel.create("test_model", readonly_memoryset, if_exists="open", num_classes=19)

    with pytest.raises(ValueError):
        ClassificationModel.create("test_model", readonly_memoryset, if_exists="open", min_memory_weight=0.77)

    new_model = ClassificationModel.create("test_model", readonly_memoryset, if_exists="open")
    assert new_model is not None
    assert new_model.name == "test_model"
    assert new_model.memoryset == readonly_memoryset
    assert new_model.num_classes == 2
    assert new_model.memory_lookup_count == 3


def test_create_model_unauthenticated(unauthenticated, readonly_memoryset: LabeledMemoryset):
    with pytest.raises(ValueError, match="Invalid API key"):
        ClassificationModel.create("test_model", readonly_memoryset)


def test_get_model(model: ClassificationModel):
    fetched_model = ClassificationModel.open(model.name)
    assert fetched_model is not None
    assert fetched_model.id == model.id
    assert fetched_model.name == model.name
    assert fetched_model.num_classes == 2
    assert fetched_model.memory_lookup_count == 3
    assert fetched_model == model


def test_get_model_unauthenticated(unauthenticated):
    with pytest.raises(ValueError, match="Invalid API key"):
        ClassificationModel.open("test_model")


def test_get_model_invalid_input():
    with pytest.raises(ValueError, match="Invalid input"):
        ClassificationModel.open("not valid id")


def test_get_model_not_found():
    with pytest.raises(LookupError):
        ClassificationModel.open(str(uuid4()))


def test_get_model_unauthorized(unauthorized, model: ClassificationModel):
    with pytest.raises(LookupError):
        ClassificationModel.open(model.name)


def test_list_models(model: ClassificationModel):
    models = ClassificationModel.all()
    assert len(models) > 0
    assert any(model.name == model.name for model in models)


def test_list_models_unauthenticated(unauthenticated):
    with pytest.raises(ValueError, match="Invalid API key"):
        ClassificationModel.all()


def test_list_models_unauthorized(unauthorized, model: ClassificationModel):
    assert ClassificationModel.all() == []


def test_update_model(model: ClassificationModel):
    model.update_metadata(description="New description")
    assert model.description == "New description"


def test_update_model_no_description(model: ClassificationModel):
    assert model.description is not None
    model.update_metadata(description=None)
    assert model.description is None


def test_delete_model(readonly_memoryset: LabeledMemoryset):
    ClassificationModel.create("model_to_delete", LabeledMemoryset.open(readonly_memoryset.name))
    assert ClassificationModel.open("model_to_delete")
    ClassificationModel.drop("model_to_delete")
    with pytest.raises(LookupError):
        ClassificationModel.open("model_to_delete")


def test_delete_model_unauthenticated(unauthenticated, model: ClassificationModel):
    with pytest.raises(ValueError, match="Invalid API key"):
        ClassificationModel.drop(model.name)


def test_delete_model_not_found():
    with pytest.raises(LookupError):
        ClassificationModel.drop(str(uuid4()))
    # ignores error if specified
    ClassificationModel.drop(str(uuid4()), if_not_exists="ignore")


def test_delete_model_unauthorized(unauthorized, model: ClassificationModel):
    with pytest.raises(LookupError):
        ClassificationModel.drop(model.name)


def test_delete_memoryset_before_model_constraint_violation(hf_dataset):
    memoryset = LabeledMemoryset.from_hf_dataset("test_memoryset_delete_before_model", hf_dataset)
    ClassificationModel.create("test_model_delete_before_memoryset", memoryset)
    with pytest.raises(RuntimeError):
        LabeledMemoryset.drop(memoryset.id)


def test_evaluate(model, eval_datasource: Datasource):
    result = model.evaluate(eval_datasource)
    assert result is not None
    assert isinstance(result, dict)
    # And anomaly score statistics are present and valid
    assert isinstance(result["anomaly_score_mean"], float)
    assert isinstance(result["anomaly_score_median"], float)
    assert isinstance(result["anomaly_score_variance"], float)
    assert -1.0 <= result["anomaly_score_mean"] <= 1.0
    assert -1.0 <= result["anomaly_score_median"] <= 1.0
    assert -1.0 <= result["anomaly_score_variance"] <= 1.0
    assert isinstance(result["accuracy"], float)
    assert isinstance(result["f1_score"], float)
    assert isinstance(result["loss"], float)
    assert len(result["precision_recall_curve"]["thresholds"]) == 4
    assert len(result["precision_recall_curve"]["precisions"]) == 4
    assert len(result["precision_recall_curve"]["recalls"]) == 4
    assert len(result["roc_curve"]["thresholds"]) == 4
    assert len(result["roc_curve"]["false_positive_rates"]) == 4
    assert len(result["roc_curve"]["true_positive_rates"]) == 4


def test_evaluate_combined(model, eval_datasource: Datasource, eval_dataset: Dataset):
    result_datasource = model.evaluate(eval_datasource)

    result_dataset = model.evaluate(eval_dataset)

    for result in [result_datasource, result_dataset]:
        assert result is not None
        assert isinstance(result, dict)
        assert isinstance(result["accuracy"], float)
        assert isinstance(result["f1_score"], float)
        assert isinstance(result["loss"], float)
        assert np.allclose(result["accuracy"], 0.5)
        assert np.allclose(result["f1_score"], 0.5)

        assert isinstance(result["precision_recall_curve"]["thresholds"], list)
        assert isinstance(result["precision_recall_curve"]["precisions"], list)
        assert isinstance(result["precision_recall_curve"]["recalls"], list)
        assert isinstance(result["roc_curve"]["thresholds"], list)
        assert isinstance(result["roc_curve"]["false_positive_rates"], list)
        assert isinstance(result["roc_curve"]["true_positive_rates"], list)

        assert np.allclose(result["roc_curve"]["thresholds"], [0.0, 0.8155114054679871, 0.834095299243927, 1.0])
        assert np.allclose(result["roc_curve"]["false_positive_rates"], [1.0, 0.5, 0.0, 0.0])
        assert np.allclose(result["roc_curve"]["true_positive_rates"], [1.0, 0.5, 0.5, 0.0])
        assert np.allclose(result["roc_curve"]["auc"], 0.625)

        assert np.allclose(
            result["precision_recall_curve"]["thresholds"], [0.0, 0.0, 0.8155114054679871, 0.834095299243927]
        )
        assert np.allclose(result["precision_recall_curve"]["precisions"], [0.5, 0.5, 1.0, 1.0])
        assert np.allclose(result["precision_recall_curve"]["recalls"], [1.0, 0.5, 0.5, 0.0])
        assert np.allclose(result["precision_recall_curve"]["auc"], 0.75)


def test_evaluate_with_telemetry(model):
    samples = [
        {"text": "chicken noodle soup is the best", "label": 1},
        {"text": "cats are cute", "label": 0},
    ]
    eval_datasource = Datasource.from_list("eval_datasource_2", samples)
    result = model.evaluate(eval_datasource, value_column="text", record_predictions=True, tags={"test"})
    assert result is not None
    predictions = model.predictions(tag="test")
    assert len(predictions) == 2
    assert all(p.tags == {"test"} for p in predictions)
    assert all(p.expected_label == s["label"] for p, s in zip(predictions, samples))


def test_predict(model: ClassificationModel, label_names: list[str]):
    predictions = model.predict(["Do you love soup?", "Are cats cute?"])
    assert len(predictions) == 2
    assert predictions[0].prediction_id is not None
    assert predictions[1].prediction_id is not None
    assert predictions[0].label == 0
    assert predictions[0].label_name == label_names[0]
    assert 0 <= predictions[0].confidence <= 1
    assert predictions[1].label == 1
    assert predictions[1].label_name == label_names[1]
    assert 0 <= predictions[1].confidence <= 1

    assert predictions[0].logits is not None
    assert predictions[1].logits is not None
    assert len(predictions[0].logits) == 2
    assert len(predictions[1].logits) == 2
    assert predictions[0].logits[0] > predictions[0].logits[1]
    assert predictions[1].logits[0] < predictions[1].logits[1]


def test_predict_disable_telemetry(model: ClassificationModel, label_names: list[str]):
    predictions = model.predict(["Do you love soup?", "Are cats cute?"], save_telemetry=False)
    assert len(predictions) == 2
    assert predictions[0].prediction_id is None
    assert predictions[1].prediction_id is None
    assert predictions[0].label == 0
    assert predictions[0].label_name == label_names[0]
    assert 0 <= predictions[0].confidence <= 1
    assert predictions[1].label == 1
    assert predictions[1].label_name == label_names[1]
    assert 0 <= predictions[1].confidence <= 1


def test_predict_unauthenticated(unauthenticated, model: ClassificationModel):
    with pytest.raises(ValueError, match="Invalid API key"):
        model.predict(["Do you love soup?", "Are cats cute?"])


def test_predict_unauthorized(unauthorized, model: ClassificationModel):
    with pytest.raises(LookupError):
        model.predict(["Do you love soup?", "Are cats cute?"])


def test_predict_constraint_violation(readonly_memoryset: LabeledMemoryset):
    model = ClassificationModel.create(
        "test_model_lookup_count_too_high",
        readonly_memoryset,
        num_classes=2,
        memory_lookup_count=readonly_memoryset.length + 2,
    )
    with pytest.raises(RuntimeError):
        model.predict("test")


def test_record_prediction_feedback(model: ClassificationModel):
    predictions = model.predict(["Do you love soup?", "Are cats cute?"])
    expected_labels = [0, 1]
    model.record_feedback(
        {
            "prediction_id": p.prediction_id,
            "category": "correct",
            "value": p.label == expected_label,
        }
        for expected_label, p in zip(expected_labels, predictions)
    )


def test_record_prediction_feedback_missing_category(model: ClassificationModel):
    prediction = model.predict("Do you love soup?")
    with pytest.raises(ValueError):
        model.record_feedback({"prediction_id": prediction.prediction_id, "value": True})


def test_record_prediction_feedback_invalid_value(model: ClassificationModel):
    prediction = model.predict("Do you love soup?")
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        model.record_feedback({"prediction_id": prediction.prediction_id, "category": "correct", "value": "invalid"})


def test_record_prediction_feedback_invalid_prediction_id(model: ClassificationModel):
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        model.record_feedback({"prediction_id": "invalid", "category": "correct", "value": True})


def test_predict_with_memoryset_override(model: ClassificationModel, hf_dataset: Dataset):
    inverted_labeled_memoryset = LabeledMemoryset.from_hf_dataset(
        "test_memoryset_inverted_labels",
        hf_dataset.map(lambda x: {"label": 1 if x["label"] == 0 else 0}),
        embedding_model=PretrainedEmbeddingModel.GTE_BASE,
    )
    with model.use_memoryset(inverted_labeled_memoryset):
        predictions = model.predict(["Do you love soup?", "Are cats cute?"])
        assert predictions[0].label == 1
        assert predictions[1].label == 0

    predictions = model.predict(["Do you love soup?", "Are cats cute?"])
    assert predictions[0].label == 0
    assert predictions[1].label == 1


def test_predict_with_expected_labels(model: ClassificationModel):
    prediction = model.predict("Do you love soup?", expected_labels=1)
    assert prediction.expected_label == 1


def test_predict_with_expected_labels_invalid_input(model: ClassificationModel):
    # invalid number of expected labels for batch prediction
    with pytest.raises(ValueError, match=r"Invalid input.*"):
        model.predict(["Do you love soup?", "Are cats cute?"], expected_labels=[0])
    # invalid label value
    with pytest.raises(ValueError):
        model.predict("Do you love soup?", expected_labels=5)


def test_last_prediction_with_batch(model: ClassificationModel):
    predictions = model.predict(["Do you love soup?", "Are cats cute?"])
    assert model.last_prediction is not None
    assert model.last_prediction.prediction_id == predictions[-1].prediction_id
    assert model.last_prediction.input_value == "Are cats cute?"
    assert model._last_prediction_was_batch is True


def test_last_prediction_with_single(model: ClassificationModel):
    # Test that last_prediction is updated correctly with single prediction
    prediction = model.predict("Do you love soup?")
    assert model.last_prediction is not None
    assert model.last_prediction.prediction_id == prediction.prediction_id
    assert model.last_prediction.input_value == "Do you love soup?"
    assert model._last_prediction_was_batch is False


@pytest.mark.skipif(
    SKIP_IN_GITHUB_ACTIONS, reason="Skipping explanation test because in CI we don't have Anthropic API key"
)
def test_explain(writable_memoryset: LabeledMemoryset):

    writable_memoryset.analyze(
        {"name": "neighbor", "neighbor_counts": [1, 3]},
        lookup_count=3,
    )

    model = ClassificationModel.create(
        "test_model_for_explain",
        writable_memoryset,
        num_classes=2,
        memory_lookup_count=3,
        description="This is a test model for explain",
    )

    predictions = model.predict(["Do you love soup?", "Are cats cute?"])
    assert len(predictions) == 2

    try:
        explanation = predictions[0].explanation
        print(explanation)
        assert explanation is not None
        assert len(explanation) > 10
        assert "soup" in explanation.lower()
    except Exception as e:
        if "ANTHROPIC_API_KEY" in str(e):
            logging.info("Skipping explanation test because ANTHROPIC_API_KEY is not set on server")
        else:
            raise e
    finally:
        try:
            ClassificationModel.drop("test_model_for_explain")
        except Exception as e:
            logging.info(f"Failed to drop test model for explain: {e}")
