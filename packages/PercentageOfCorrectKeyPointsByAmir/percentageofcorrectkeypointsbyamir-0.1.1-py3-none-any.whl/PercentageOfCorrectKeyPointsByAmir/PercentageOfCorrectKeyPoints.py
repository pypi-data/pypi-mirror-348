import numpy as np

class PercentageOfCorrectKeyPoints:
  """  PercentageOfCorrectKeyPoints class""" 

  def __init__(self, relative_distance_threshold):
    """ Initializes the BERT model.

        Args:
            relative_distance_threshold: the threshold for the percentage of correct keypoints.
    """
    self.relative_distance_threshold = relative_distance_threshold

  def apply(self, y_true, y_pred):
    """ Calculate the percentage of correct keypoints.
        
        Args: 
             y_true (np.ndarray): Input tensor of shape (B, H, W, num_kp)
             y_pred (np.ndarray): Input tensor of shape (B, H, W, num_kp)
             
        Returns:
             float: the percentage of correct keypoints.

    """

    assert y_true.shape == y_pred.shape,   " The shapes are different"
    assert isinstance(y_true, np.ndarray), " The label array is not an np array"
    assert isinstance(y_pred, np.ndarray), " The prediction array is not an np array"

    
    h = y_true.shape[1]  # get the H

    # compute euclidian distance (default of the np.linalg.norm is L2)
    dist = np.linalg.norm(y_true - y_pred, axis=-1) # shape : (B, H, W)
    
    # calculate the threshold
    threshold = self.relative_distance_threshold * h

    # calculate the number of correct predictions
    correct = np.sum(dist < threshold)  

    return correct/dist.size