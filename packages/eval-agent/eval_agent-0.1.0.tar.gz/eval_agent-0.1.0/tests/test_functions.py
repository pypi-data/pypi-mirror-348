from eval_agent import functions

def test_perfect_predictions():
    y_true = [0, 1, 1, 0, 1]
    y_pred = [0, 1, 1, 0, 1]
    result = functions.evaluate_agent(y_true, y_pred)
    assert result["accuracy"] == 1.0
    assert result["precision"] == 1.0
    assert result["recall"] == 1.0
    assert result["f1"] == 1.0

def test_partial_predictions():
    y_true = [1, 0, 1, 0]
    y_pred = [1, 0, 0, 0]
    result = functions.evaluate_agent(y_true, y_pred)
    assert result["accuracy"] == 0.75
    assert round(result["precision"], 2) == 1.0
    assert round(result["recall"], 2) == 0.5
    assert round(result["f1"], 2) == 0.67

def test_all_wrong_predictions():
    y_true = [1, 1, 0, 0]
    y_pred = [0, 0, 1, 1]
    result = functions.evaluate_agent(y_true, y_pred)
    assert result["accuracy"] == 0.0
    assert result["precision"] == 0.0
    assert result["recall"] == 0.0
    assert result["f1"] == 0.0
