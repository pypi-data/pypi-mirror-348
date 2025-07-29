import pytest
import json
from typing import Dict
from reward_kit.models import MetricResult, EvaluateResult


def test_metric_result_creation():
    """Test creating a MetricResult."""
    metric = MetricResult(score=0.5, reason="Test reason", success=False)
    assert metric.score == 0.5
    assert metric.reason == "Test reason"
    assert metric.success is False


def test_metric_result_serialization():
    """Test serializing MetricResult to JSON."""
    metric = MetricResult(score=0.75, reason="Test serialization", success=True)
    json_str = metric.model_dump_json()
    data = json.loads(json_str)
    assert data["score"] == 0.75
    assert data["reason"] == "Test serialization"
    assert data["success"] is True


def test_metric_result_deserialization():
    """Test deserializing MetricResult from JSON."""
    json_str = '{"score": 0.9, "reason": "Test deserialization", "success": null}'
    metric = MetricResult.model_validate_json(json_str)
    assert metric.score == 0.9
    assert metric.reason == "Test deserialization"
    assert metric.success is None


def test_evaluate_result_creation():
    """Test creating an EvaluateResult."""
    metrics: Dict[str, MetricResult] = {
        "metric1": MetricResult(score=0.5, reason="Reason 1", success=False),
        "metric2": MetricResult(score=0.7, reason="Reason 2", success=True),
    }
    result = EvaluateResult(score=0.6, reason="Overall assessment", metrics=metrics)
    assert result.score == 0.6
    assert result.reason == "Overall assessment"
    assert len(result.metrics) == 2
    assert result.metrics["metric1"].score == 0.5
    assert result.metrics["metric2"].reason == "Reason 2"
    assert result.metrics["metric2"].success is True


def test_evaluate_result_serialization():
    """Test serializing EvaluateResult to JSON."""
    metrics = {
        "metric1": MetricResult(score=0.5, reason="Reason 1", success=False),
        "metric2": MetricResult(score=0.7, reason="Reason 2", success=True),
    }
    result = EvaluateResult(score=0.6, reason="Overall assessment", metrics=metrics)
    json_str = result.model_dump_json()
    data = json.loads(json_str)
    assert data["score"] == 0.6
    assert data["reason"] == "Overall assessment"
    assert len(data["metrics"]) == 2
    assert data["metrics"]["metric1"]["score"] == 0.5
    assert data["metrics"]["metric1"]["success"] is False
    assert data["metrics"]["metric2"]["reason"] == "Reason 2"


def test_evaluate_result_deserialization():
    """Test deserializing EvaluateResult from JSON."""
    json_str = (
        '{"score": 0.8, "reason": "Overall", "metrics": {'
        '"metric1": {"score": 0.4, "reason": "Reason A", "success": false}, '
        '"metric2": {"score": 0.9, "reason": "Reason B", "success": true}'
        '}, "error": null}'
    )
    result = EvaluateResult.model_validate_json(json_str)
    assert result.score == 0.8
    assert result.reason == "Overall"
    assert len(result.metrics) == 2
    assert result.metrics["metric1"].score == 0.4
    assert result.metrics["metric1"].success is False
    assert result.metrics["metric2"].reason == "Reason B"
    assert result.error is None


def test_empty_metrics_evaluate_result():
    """Test EvaluateResult with empty metrics dictionary."""
    result = EvaluateResult(score=1.0, reason="Perfect score", metrics={})
    assert result.score == 1.0
    assert result.reason == "Perfect score"
    assert result.metrics == {}

    json_str = result.model_dump_json()
    data = json.loads(json_str)
    assert data["score"] == 1.0
    assert data["reason"] == "Perfect score"
    assert data["metrics"] == {}


def test_metric_result_dict_access():
    """Test dictionary-style access for MetricResult."""
    metric = MetricResult(score=0.7, reason="Dict access test", success=True)

    # __getitem__
    assert metric['score'] == 0.7
    assert metric['reason'] == "Dict access test"
    assert metric['success'] is True
    with pytest.raises(KeyError):
        _ = metric['invalid_key']

    # __contains__
    assert 'score' in metric
    assert 'reason' in metric
    assert 'success' in metric
    assert 'invalid_key' not in metric

    # get()
    assert metric.get('score') == 0.7
    assert metric.get('reason') == "Dict access test"
    assert metric.get('success') is True
    assert metric.get('invalid_key') is None
    assert metric.get('invalid_key', 'default_val') == 'default_val'

    # keys()
    assert set(metric.keys()) == {'score', 'reason', 'success'}

    # values() - order might not be guaranteed by model_fields, so check content
    # Pydantic model_fields preserves declaration order.
    expected_values = [True, 0.7, "Dict access test"] # Based on current field order in model
    actual_values = list(metric.values())
    # To make it order-independent for this test, let's check presence
    assert metric.score in actual_values
    assert metric.reason in actual_values
    assert metric.success in actual_values


    # items()
    expected_items = {('score', 0.7), ('reason', "Dict access test"), ('success', True)}
    assert set(metric.items()) == expected_items

    # __iter__
    assert set(list(metric)) == {'score', 'reason', 'success'}


def test_evaluate_result_dict_access():
    """Test dictionary-style access for EvaluateResult."""
    metric1_obj = MetricResult(score=0.5, reason="Reason 1", success=False)
    metrics_dict: Dict[str, MetricResult] = {
        "metric1": metric1_obj,
    }
    result = EvaluateResult(score=0.6, reason="Overall assessment", metrics=metrics_dict, error="Test Error")

    # __getitem__
    assert result['score'] == 0.6
    assert result['reason'] == "Overall assessment"
    assert result['error'] == "Test Error"
    assert result['metrics'] == metrics_dict # Returns the dict of MetricResult objects
    assert result['metrics']['metric1'] == metric1_obj
    assert result['metrics']['metric1']['score'] == 0.5 # Accessing MetricResult via __getitem__

    with pytest.raises(KeyError):
        _ = result['invalid_key']
    with pytest.raises(KeyError): # Accessing non-existent key in nested metric
        _ = result['metrics']['metric1']['invalid_sub_key']


    # __contains__
    assert 'score' in result
    assert 'reason' in result
    assert 'metrics' in result
    assert 'error' in result
    assert 'invalid_key' not in result

    # get()
    assert result.get('score') == 0.6
    assert result.get('invalid_key') is None
    assert result.get('invalid_key', 'default_val') == 'default_val'

    # keys()
    assert set(result.keys()) == {'score', 'reason', 'metrics', 'error'}

    # values() - check presence due to potential order variation of model_fields
    actual_values = list(result.values())
    assert result.score in actual_values
    assert result.reason in actual_values
    assert result.metrics in actual_values
    assert result.error in actual_values


    # items()
    # Note: result.metrics is a dict of MetricResult objects.
    # For exact item matching, we compare sorted lists of (key, value) tuples.
    expected_items_list = sorted([
        ('score', 0.6),
        ('reason', "Overall assessment"),
        ('metrics', metrics_dict),
        ('error', "Test Error")
    ])
    # result.items() returns a list of tuples, so convert to list then sort.
    actual_items_list = sorted(list(result.items()))
    assert actual_items_list == expected_items_list

    # __iter__
    assert set(list(result)) == {'score', 'reason', 'metrics', 'error'}
