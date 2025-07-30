"""Base Classes
============

Base classes of movement primitives."""
import abc
import numpy as np
from .utils import check_1d_array_length


class PointToPointMovement(abc.ABC):
    """Base class for point to point movements (discrete motions).

    Parameters
    ----------
    n_pos_dims : int
        Number of dimensions of the position that will be controlled.

    n_vel_dims : int
        Number of dimensions of the velocity that will be controlled.

    Attributes
    ----------
    n_dims : int
        Number of state space dimensions.

    n_vel_dims : int
        Number of velocity dimensions.

    t : float
        Current time.

    last_t : float
        Time during last step.

    start_y : array, shape (n_dims,)
        Initial state.

    start_yd : array, shape (n_vel_dims,)
        Initial velocity.

    start_ydd : array, shape (n_vel_dims,)
        Initial acceleration.

    goal_y : array, shape (n_dims,)
        Goal state.

    goal_yd : array, shape (n_vel_dims,)
        Goal velocity.

    goal_ydd : array, shape (n_vel_dims,)
        Goal acceleration.

    current_y : array, shape (n_dims,)
        Current state.

    current_yd : array, shape (n_vel_dims,)
        Current velocity.
    """
    def __init__(self, n_pos_dims, n_vel_dims):
        self.n_dims = n_pos_dims
        self.n_vel_dims = n_vel_dims

        self.t = 0.0
        self.last_t = None

        self.start_y = np.zeros(n_pos_dims)
        self.start_yd = np.zeros(n_vel_dims)
        self.start_ydd = np.zeros(n_vel_dims)

        self.goal_y = np.zeros(n_pos_dims)
        self.goal_yd = np.zeros(n_vel_dims)
        self.goal_ydd = np.zeros(n_vel_dims)

        self.current_y = np.zeros(n_pos_dims)
        self.current_yd = np.zeros(n_vel_dims)

    def configure(
            self, t=None, start_y=None, start_yd=None, start_ydd=None,
            goal_y=None, goal_yd=None, goal_ydd=None):
        """Set meta parameters.

        Parameters
        ----------
        t : float, optional
            Time at current step.

        start_y : array, shape (n_dims,)
            Initial state.

        start_yd : array, shape (n_vel_dims,)
            Initial velocity.

        start_ydd : array, shape (n_vel_dims,)
            Initial acceleration.

        goal_y : array, shape (n_dims,)
            Goal state.

        goal_yd : array, shape (n_vel_dims,)
            Goal velocity.

        goal_ydd : array, shape (n_vel_dims,)
            Goal acceleration.

        Raises
        ------
        ValueError
            If the length of the configured meta parameter is not correct.
        """
        if t is not None:
            self.t = t

        if start_y is not None:
            check_1d_array_length(start_y, "start_y", self.n_dims)
            self.start_y = start_y
        if start_yd is not None:
            check_1d_array_length(start_yd, "start_yd", self.n_vel_dims)
            self.start_yd = start_yd
        if start_ydd is not None:
            check_1d_array_length(start_ydd, "start_ydd", self.n_vel_dims)
            self.start_ydd = start_ydd
        if goal_y is not None:
            check_1d_array_length(goal_y, "goal_y", self.n_dims)
            self.goal_y = goal_y
        if goal_yd is not None:
            check_1d_array_length(goal_yd, "goal_yd", self.n_vel_dims)
            self.goal_yd = goal_yd
        if goal_ydd is not None:
            check_1d_array_length(goal_ydd, "goal_ydd", self.n_vel_dims)
            self.goal_ydd = goal_ydd

    @abc.abstractmethod
    def step(self, last_y, last_yd):
        """Perform step.

        Parameters
        ----------
        last_y : array, shape (n_dims,)
            Last state.

        last_yd : array, shape (n_dims,)
            Last time derivative of state (e.g., velocity).

        Returns
        -------
        y : array, shape (n_dims,)
            Next state.

        yd : array, shape (n_dims,)
            Next time derivative of state (e.g., velocity).
        """

    def n_steps_open_loop(self, last_y, last_yd, n_steps):
        """Perform 'n_steps' steps.

        Parameters
        ----------
        last_y : array, shape (n_dims,)
            Last state.

        last_yd : array, shape (n_dims,)
            Last time derivative of state (e.g., velocity).

        n_steps : int
            Number of steps.

        Returns
        -------
        y : array, shape (n_dims,)
            Next state.

        yd : array, shape (n_dims,)
            Next time derivative of state (e.g., velocity).
        """
        for _ in range(n_steps):
            last_y, last_yd = self.step(last_y, last_yd)
        return last_y, last_yd
