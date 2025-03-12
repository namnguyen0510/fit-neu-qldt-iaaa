import numpy as np
import bisect

def compute_position(user_score, bench_score):
    """
    Computes the position of user_score in the sorted bench_score list.
    
    Parameters:
        user_score (float): The score of the user.
        bench_score (list or array): The list of benchmark scores.
    
    Returns:
        dict: A dictionary with 'rank' (1-based position in sorted order)
              and 'percentile' (percentage of scores below user_score).
    """
    bench_score_sorted = sorted(bench_score)  # Sort the benchmark scores
    rank = bisect.bisect_right(bench_score_sorted, user_score)  # Find position
    rank = len(bench_score) - rank
    percentile = (rank / len(bench_score_sorted)) * 100  # Compute percentile
    
    return [rank,percentile]


