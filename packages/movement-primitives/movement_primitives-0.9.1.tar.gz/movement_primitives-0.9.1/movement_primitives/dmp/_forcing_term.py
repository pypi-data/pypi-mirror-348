import math
import numpy as np
try:
    from ..dmp_fast import phase
except ImportError:
    from ._canonical_system import phase


class ForcingTerm:
    """Defines the shape of a DMP.

    Parameters
    ----------
    n_dims : int
        State space dimensions.

    n_weights_per_dim : int, optional (default: 10)
        Number of weights of the function approximator per dimension.

    goal_t : float
        Time at the end.

    start_t : float
        Time at the start.

    overlap : float
        Value at which radial basis functions overlap.

    alpha_z : float
        Value of the alpha parameter of the canonical system.

    Attributes
    ----------
    weights_ : array, shape (n_dims, n_weights_per_dim)
        Weights of the forcing term.
    """
    def __init__(self, n_dims, n_weights_per_dim, goal_t, start_t, overlap,
                 alpha_z):
        if n_weights_per_dim <= 1:
            raise ValueError("The number of weights per dimension must be > 1!")
        self.n_weights_per_dim = n_weights_per_dim
        if start_t >= goal_t:
            raise ValueError("Goal must be chronologically after start!")
        self.goal_t = goal_t
        self.start_t = start_t
        self.overlap = overlap
        self.alpha_z = alpha_z

        self._init_rbfs(n_dims, n_weights_per_dim, start_t)

    def _init_rbfs(self, n_dims, n_weights_per_dim, start_t):
        self.log_overlap = float(-math.log(self.overlap))
        self.execution_time = self.goal_t - self.start_t
        self.weights_ = np.zeros((n_dims, n_weights_per_dim))
        self.centers = np.empty(n_weights_per_dim)
        self.widths = np.empty(n_weights_per_dim)
        # -1 because we want the last entry to be execution_time
        step = self.execution_time / (self.n_weights_per_dim - 1)
        # do first iteration outside loop because we need access to i and i - 1 in loop
        t = start_t
        self.centers[0] = phase(t, self.alpha_z, self.goal_t, self.start_t)
        for i in range(1, self.n_weights_per_dim):
            # normally lower_border + i * step but lower_border is 0
            t = i * step
            self.centers[i] = phase(t, self.alpha_z, self.goal_t, self.start_t)
            # Choose width of RBF basis functions automatically so that the
            # RBF centered at one center has value overlap at the next center
            diff = self.centers[i] - self.centers[i - 1]
            self.widths[i - 1] = self.log_overlap / diff ** 2
        # Width of last Gaussian cannot be calculated, just use the same width
        # as the one before
        self.widths[self.n_weights_per_dim - 1] = self.widths[
            self.n_weights_per_dim - 2]

    def _activations(self, z):
        z = np.atleast_2d(z)  # 1 x n_steps
        squared_dist = (z - self.centers[:, np.newaxis]) ** 2
        activations = np.exp(-self.widths[:, np.newaxis] * squared_dist)
        activations /= activations.sum(axis=0)  # normalize
        return activations

    def design_matrix(self, T):  # returns: n_weights_per_dim x n_steps
        Z = phase(T, alpha=self.alpha_z, goal_t=T[-1], start_t=T[0])
        return Z[np.newaxis, :] * self._activations(Z)

    def phase(self, t):
        return phase(t, alpha=self.alpha_z, goal_t=self.goal_t,
                     start_t=self.start_t)

    def forcing_term(self, z):
        z = np.atleast_1d(z)
        activations = self._activations(z)
        return z[np.newaxis, :] * self.weights_.dot(activations)

    def __call__(self, t):
        return self.forcing_term(self.phase(t))

    @property
    def shape(self):
        """Shape (n_dims, n_weights_per_dim) of weights configuring the forcing term."""
        return self.weights_.shape
