import numpy as np

class PercentageOfCorrectKeyPoints:
  """  PercentageOfCorrectKeyPoints class"""

  def __init__(self, relative_distance_threshold):
    """ Initialization.

        Args:
            relative_distance_threshold: the threshold for the percentage of correct keypoints.
    """
    self.relative_distance_threshold = relative_distance_threshold

  def get_max_coords(self, heatmaps):
    """ Calculate the the coordinates the maximizes the heatmapt.

        Args:
             heatmaps (np.ndarray): Input np array of shape (B, H, W, num_kp)

        Returns:
             coords (np.ndarray): Output np array of shape (B, num_kp, 2) includinf the x and y coordinates.

    """

    batch_size, h, w, num_kps = heatmaps.shape
    coords = np.zeros((batch_size, num_kps, 2), dtype=np.float32)
    for b in range(batch_size):     # for all batcehs
        for k in range(num_kps):    # for all key points
            idx = np.argmax(heatmaps[b, :, :, k])  
            y, x = np.unravel_index(idx, (h, w))   # find the maximum location
            coords[b, k] = [x, y]  

    return coords # shape : (B, num_kp, 2)

  def apply(self, y_true, y_pred):
    """ Calculate the percentage of correct keypoints.

        Args:
             y_true (np.ndarray): Input np array of shape (B, H, W, num_kp)
             y_pred (np.ndarray): Input np array of shape (B, H, W, num_kp)

        Returns:
             float: the percentage of correct keypoints.

    """

    assert y_true.shape == y_pred.shape,   " The shapes are different"
    assert isinstance(y_true, np.ndarray), " The label array is not an np array"
    assert isinstance(y_pred, np.ndarray), " The prediction array is not an np array"
    assert len(y_true.shape) == 4, " the number of dimensions is not 4"
 
    h = y_true.shape[1]  # get the H
    
    true_coords = self.get_max_coords(y_true)  # shape : (B, num_kp, 2)
    pred_coords = self.get_max_coords(y_pred)  # shape : (B, num_kp, 2)

    # compute euclidian distance (default of the np.linalg.norm is L2)
    dist = np.linalg.norm(pred_coords - true_coords, axis=-1) # shape : (B, num_kp)

    # calculate the threshold
    threshold = self.relative_distance_threshold * h

    # calculate the number of correct predictions
    correct = np.sum(dist < threshold)

    return correct/dist.size