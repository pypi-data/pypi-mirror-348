import tensorflow as tf
import math

def pbs(y, q):
    """
    Computes Penalized Brier Score.
    
    Args:
        y_true: Ground truth (one-hot encoded), shape [batch_size, num_classes]
        y_pred: Predicted probabilities, shape [batch_size, num_classes]
        
    Returns:
        Mean PBS across batch
    """
    y = tf.cast(y, tf.float32)
    c = y.get_shape()[1]

    # Calculate payoff term
    ST = tf.math.subtract(q, tf.reduce_sum(tf.where(y == 1, q, y), axis=1)[:, None])
    ST = tf.where(ST < 0, tf.constant(0, dtype=tf.float32), ST)
    payoff = tf.reduce_sum(tf.math.ceil(ST), axis=1)
    M = (c - 1) / (c)
    payoff = tf.where(payoff > 0, tf.constant(M, dtype=tf.float32), payoff)
    
    # Brier score + penalty
    brier = tf.math.reduce_mean(tf.math.square(tf.math.subtract(y, q)), axis=1)
    return tf.math.reduce_mean(brier + payoff)


def pll(y, q):
    """
    Computes Penalized Logarithmic Loss.
    
    Args:
        y_true: Ground truth (one-hot encoded)
        y_pred: Predicted probabilities
        
    Returns:
        Mean PLL across batch
    """
    y = tf.cast(y, tf.float32)
    c = y.get_shape()[1]

    # Calculate payoff term
    ST = tf.math.subtract(q, tf.reduce_sum(tf.where(y == 1, q, y), axis=1)[:, None])
    ST = tf.where(ST < 0, tf.constant(0, dtype=tf.float32), ST)
    payoff = tf.reduce_sum(tf.math.ceil(ST), axis=1)
    M = math.log(1 / c)
    payoff = tf.where(payoff > 0, tf.constant(M, dtype=tf.float32), payoff)
    log_loss = tf.keras.losses.categorical_crossentropy(y, q)

    # Cross-entropy - penalty
    ce_loss = tf.cast(log_loss, tf.float32)
    return tf.math.reduce_mean(ce_loss - payoff)
