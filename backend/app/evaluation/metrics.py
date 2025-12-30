
def calculate_metrics(ground_truth, predictions, threshold=80):
    """
    Computes FP, FN, TP, TN and standard accuracy metrics.
    
    Args:
        ground_truth: List of booleans (True=Fake/Tampered, False=Authentic)
        predictions: List of final_scores (0-100). 
                     Score < Threshold => Classified as FAKE.
                     Score >= Threshold => Classified as AUTHENTIC.
                     
    Note: Usually Score < Threshold is "Positive" detection of Fake.
          So:
          Unique Positive (Prediction says Fake) => Score < Threshold
          Unique Negative (Prediction says Authentic) => Score >= Threshold
          True Positive (TP) => Is Fake AND Predicted Fake
          False Positive (FP) => Is Authentic AND Predicted Fake (Alarm!) 
          True Negative (TN) => Is Authentic AND Predicted Authentic
          False Negative (FN) => Is Fake AND Predicted Authentic (Miss!)
    """
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    
    for truth_is_fake, score in zip(ground_truth, predictions):
        pred_is_fake = score < threshold
        
        if truth_is_fake and pred_is_fake:
            tp += 1
        elif not truth_is_fake and not pred_is_fake:
            tn += 1
        elif not truth_is_fake and pred_is_fake:
            fp += 1
        elif truth_is_fake and not pred_is_fake:
            fn += 1
            
    total = len(ground_truth)
    accuracy = (tp + tn) / total if total > 0 else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    return {
        "TP": tp, "TN": tn, "FP": fp, "FN": fn,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1": f1
    }

def generate_distribution_plot(scores, buckets=10):
    """
    Generates a simple ASCII histogram of scores.
    """
    hist = [0] * buckets
    for s in scores:
        idx = int(s / (100/buckets))
        if idx >= buckets: idx = buckets - 1
        hist[idx] += 1
        
    max_val = max(hist) if hist else 1
    
    plot_str = "Score Distribution (0-100):\n"
    for i in range(buckets):
        range_start = i * (100//buckets)
        range_end = (i+1) * (100//buckets)
        bar_len = int((hist[i] / max_val) * 20)
        bar = "#" * bar_len
        plot_str += f"{range_start:3}-{range_end:3}: {bar} ({hist[i]})\n"
        
    return plot_str
