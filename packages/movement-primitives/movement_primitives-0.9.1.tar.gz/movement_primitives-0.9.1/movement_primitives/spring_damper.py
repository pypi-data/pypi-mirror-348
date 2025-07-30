"""Spring-Damper Based Attractors
==============================

Spring-damper based attractors are the basis of a DMP's transformation system.
"""
import numpy as np
import pytransform3d.rotations as pr
from .base import PointToPointMovement


class SpringDamper(PointToPointMovement):
    """Spring-damper system.

    This is similar to a DMP without the forcing term.

    Parameters
    ----------
    n_dims : int
        State space dimensions.

    dt : float, optional (default: 0.01)
        Time difference between DMP steps.

    k : float, optional (default: 1)
        Spring constant.

    c : float, optional (default: 2 * sqrt(k) (critical damping))
        Damping coefficient.

    int_dt : float, optional (default: 0.001)
        Time difference for Euler integration.
    """
    def __init__(self, n_dims, dt=0.01, k=1.0, c=None, int_dt=0.001):
        super(SpringDamper, self).__init__(n_dims, n_dims)
        self.n_dims = n_dims
        self.dt = dt
        self.k = k
        self.c = c
        self.int_dt = int_dt

        self.initialized = False
        self.configure()

    def reset(self):
        """Reset time."""
        self.t = 0.0
        self.last_t = None

    def step(self, last_y, last_yd, coupling_term=None):
        """Perform step.

        Parameters
        ----------
        last_y : array, shape (n_dims,)
            Last state.

        last_yd : array, shape (n_dims,)
            Last time derivative of state (e.g., velocity).

        coupling_term : object, optional (default: None)
            Coupling term that will be added to velocity.

        Returns
        -------
        y : array, shape (n_dims,)
            Next state.

        yd : array, shape (n_dims,)
            Next time derivative of state (e.g., velocity).
        """
        self.last_t = self.t
        self.t += self.dt

        if not self.initialized:
            self.current_y = np.copy(self.start_y)
            self.current_yd = np.copy(self.start_yd)
            self.initialized = True

        self.current_y[:], self.current_yd[:] = last_y, last_yd
        spring_damper_step(
            self.last_t, self.t,
            self.current_y, self.current_yd,
            self.goal_y,
            self.k, self.c,
            coupling_term=coupling_term,
            int_dt=self.int_dt)
        return np.copy(self.current_y), np.copy(self.current_yd)

    def open_loop(self, run_t=1.0, coupling_term=None):
        """Run open loop.

        Parameters
        ----------
        run_t : float, optional (default: execution_time)
            Run time. Can be shorter or longer than execution_time.

        coupling_term : object, optional (default: None)
            Coupling term that will be added to velocity.

        Returns
        -------
        T : array, shape (n_steps,)
            Time for each step.

        Y : array, shape (n_steps, n_dims)
            State at each step.
        """
        return spring_damper_open_loop(
            self.dt,
            self.start_y, self.goal_y,
            self.k, self.c,
            coupling_term,
            run_t, self.int_dt)


class SpringDamperOrientation(PointToPointMovement):
    """Spring-damper system for quaternions.

    This is similar to a Quaternion DMP without the forcing term.

    Parameters
    ----------
    dt : float, optional (default: 0.01)
        Time difference between DMP steps.

    k : float, optional (default: 1)
        Spring constant.

    c : float, optional (default: 2 * sqrt(k) (critical damping))
        Damping coefficient.

    int_dt : float, optional (default: 0.001)
        Time difference for Euler integration.
    """
    def __init__(self, dt=0.01, k=1.0, c=None, int_dt=0.001):
        super(SpringDamperOrientation, self).__init__(4, 3)

        self.dt = dt
        self.k = k
        self.c = c
        self.int_dt = int_dt

        self.initialized = False
        self.configure()

    def reset(self):
        """Reset time."""
        self.t = 0.0
        self.last_t = None

    def step(self, last_y, last_yd, coupling_term=None):
        """Perform step.

        Parameters
        ----------
        last_y : array, shape (n_dims,)
            Last state.

        last_yd : array, shape (n_dims,)
            Last time derivative of state (e.g., velocity).

        coupling_term : object, optional (default: None)
            Coupling term that will be added to velocity.

        Returns
        -------
        y : array, shape (n_dims,)
            Next state.

        yd : array, shape (n_dims,)
            Next time derivative of state (e.g., velocity).
        """
        self.last_t = self.t
        self.t += self.dt

        if not self.initialized:
            self.current_y = np.copy(self.start_y)
            self.current_yd = np.copy(self.start_yd)
            self.initialized = True

        self.current_y[:], self.current_yd[:] = last_y, last_yd
        spring_damper_step_quaternion(
            self.last_t, self.t,
            self.current_y, self.current_yd,
            self.goal_y,
            self.k, self.c,
            coupling_term=coupling_term,
            int_dt=self.int_dt)
        return np.copy(self.current_y), np.copy(self.current_yd)

    def open_loop(self, run_t=1.0, coupling_term=None):
        """Run open loop.

        Parameters
        ----------
        run_t : float, optional (default: execution_time)
            Run time. Can be shorter or longer than execution_time.

        coupling_term : object, optional (default: None)
            Coupling term that will be added to velocity.

        Returns
        -------
        T : array, shape (n_steps,)
            Time for each step.

        Y : array, shape (n_steps, n_dims)
            State at each step.
        """
        return spring_damper_open_loop_quaternion(
            self.dt,
            self.start_y, self.goal_y,
            self.k, self.c,
            coupling_term,
            run_t, self.int_dt)


def spring_damper_step(
        last_t, t, current_y, current_yd, goal_y, k=1.0, c=None,
        coupling_term=None, coupling_term_precomputed=None, int_dt=0.001):
    c = _default_critically_damped_c(c, k)

    current_ydd = np.empty_like(current_yd)

    current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is not None:
            cd, cdd = coupling_term.coupling(current_y, current_yd)
        else:
            cd, cdd = np.zeros_like(current_y), np.zeros_like(current_y)
        if coupling_term_precomputed is not None:
            cd += coupling_term_precomputed[0]
            cdd += coupling_term_precomputed[1]

        current_ydd[:] = k * (goal_y - current_y) - c * current_yd + cdd
        current_yd += dt * current_ydd + cd
        current_y += dt * current_yd


def _default_critically_damped_c(c, k):
    if c is None:
        c = 2.0 * np.sqrt(k)
    return c


def spring_damper_step_quaternion(
        last_t, t, current_y, current_yd, goal_y, k=1.0, c=None,
        coupling_term=None, coupling_term_precomputed=None, int_dt=0.001):
    c = _default_critically_damped_c(c, k)

    current_ydd = np.empty_like(current_yd)

    current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is not None:
            cd, cdd = coupling_term.coupling(current_y, current_yd)
        else:
            cd, cdd = np.zeros(3), np.zeros(3)
        if coupling_term_precomputed is not None:
            cd += coupling_term_precomputed[0]
            cdd += coupling_term_precomputed[1]

        current_ydd[:] = (
            k * pr.compact_axis_angle_from_quaternion(
                pr.concatenate_quaternions(goal_y, pr.q_conj(current_y)))
            - c * current_yd
            + cdd)
        current_yd += dt * current_ydd + cd
        current_y[:] = pr.concatenate_quaternions(
            pr.quaternion_from_compact_axis_angle(dt * current_yd), current_y)


def spring_damper_open_loop(
        dt, start_y, goal_y, k=1.0, c=None, coupling_term=None, run_t=1.0,
        int_dt=0.001):
    y = np.copy(start_y)
    yd = np.zeros_like(start_y)

    T = np.arange(0.0, run_t + dt, dt)
    Y = np.empty((len(T), len(y)))
    Y[0] = y
    for i in range(1, len(T)):
        spring_damper_step(
            T[i - 1], T[i], y, yd, goal_y=goal_y, k=k, c=c,
            coupling_term=coupling_term, int_dt=int_dt)
        Y[i] = y
    return T, Y


def spring_damper_open_loop_quaternion(
        dt, start_y, goal_y, k=1.0, c=None, coupling_term=None, run_t=1.0,
        int_dt=0.001):
    y = np.copy(start_y)
    yd = np.zeros(3)

    T = np.arange(0.0, run_t + dt, dt)
    Y = np.empty((len(T), len(y)))
    Y[0] = y
    for i in range(1, len(T)):
        spring_damper_step_quaternion(
            T[i - 1], T[i], y, yd, goal_y=goal_y, k=k, c=c,
            coupling_term=coupling_term, int_dt=int_dt)
        Y[i] = y
    return T, Y
