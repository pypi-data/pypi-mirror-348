from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def evaluate_agent(y_true, y_pred, average='binary'):
    """
    Evaluate an agent's predictions using common classification metrics.

    Parameters:
    - y_true: list or array of ground truth labels
    - y_pred: list or array of predicted labels by the agent
    - average: averaging method for multi-class tasks ('binary', 'macro', 'micro', 'weighted')

    Returns:
    dict with accuracy, precision, recall, and F1 score
    """
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average=average, zero_division=0),
        'recall': recall_score(y_true, y_pred, average=average, zero_division=0),
        'f1': f1_score(y_true, y_pred, average=average, zero_division=0),
    }
