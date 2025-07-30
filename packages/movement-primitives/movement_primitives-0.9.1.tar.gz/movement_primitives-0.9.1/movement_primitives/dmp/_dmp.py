import numpy as np
from ._base import DMPBase, WeightParametersMixin
from ._forcing_term import ForcingTerm
from ._canonical_system import canonical_system_alpha
from ._forcing_term import phase
from ..utils import ensure_1d_array


def dmp_step_rk4(
        last_t, t, current_y, current_yd, goal_y, goal_yd, goal_ydd, start_y,
        start_yd, start_ydd, goal_t, start_t, alpha_y, beta_y, forcing_term,
        coupling_term=None, coupling_term_precomputed=None, int_dt=0.001,
        p_gain=0.0, tracking_error=0.0, smooth_scaling=False):
    """Integrate regular DMP for one step with RK4 integration.

    Parameters
    ----------
    last_t : float
        Time at last step.

    t : float
        Time at current step.

    current_y : array, shape (n_dims,)
        Current position. Will be modified.

    current_yd : array, shape (n_dims,)
        Current velocity. Will be modified.

    goal_y : array, shape (n_dims,)
        Goal position.

    goal_yd : array, shape (n_dims,)
        Goal velocity.

    goal_ydd : array, shape (n_dims,)
        Goal acceleration.

    start_y : array, shape (n_dims,)
        Start position.

    start_yd : array, shape (n_dims,)
        Start velocity.

    start_ydd : array, shape (n_dims,)
        Start acceleration.

    goal_t : float
        Time at the end.

    start_t : float
        Time at the start.

    alpha_y : array, shape (n_dims,)
        Constant in transformation system.

    beta_y : array, shape (n_dims,)
        Constant in transformation system.

    forcing_term : ForcingTerm
        Forcing term.

    coupling_term : CouplingTerm, optional (default: None)
        Coupling term. Must have a function coupling(y, yd) that returns
        additional velocity and acceleration.

    coupling_term_precomputed : tuple
        A precomputed coupling term, i.e., additional velocity and
        acceleration.

    int_dt : float, optional (default: 0.001)
        Time delta used internally for integration.

    p_gain : float, optional (default: 0)
        Proportional gain for tracking error.

    tracking_error : float, optional (default: 0)
        Tracking error from last step.

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.
    """
    if coupling_term is None:
        cd, cdd = np.zeros_like(current_y), np.zeros_like(current_y)
        if coupling_term_precomputed is not None:
            cd += coupling_term_precomputed[0]
            cdd += coupling_term_precomputed[1]
    else:
        cd, cdd = None, None  # will be computed in _dmp_acc()

    # RK4 (Runge-Kutta) for 2nd order differential integration
    # (faster and more accurate than Euler integration),
    # implemented following https://math.stackexchange.com/a/2023862/64116

    # precompute constants for following queries
    execution_time = goal_t - start_t
    dt = t - last_t
    dt_2 = 0.5 * dt
    T = np.array([t, t + dt_2, t + dt])
    Z = forcing_term.phase(T)
    F = forcing_term.forcing_term(Z)
    tdd = p_gain * tracking_error / dt

    C0 = current_yd
    K0 = _dmp_acc(
        current_y, C0, cdd, alpha_y, beta_y, goal_y, goal_yd, goal_ydd,
        start_y, Z[0], execution_time, F[:, 0], coupling_term, tdd,
        smooth_scaling)
    C1 = current_yd + dt_2 * K0
    K1 = _dmp_acc(
        current_y + dt_2 * C0, C1, cdd, alpha_y, beta_y, goal_y, goal_yd,
        goal_ydd, start_y, Z[1], execution_time, F[:, 1], coupling_term, tdd,
        smooth_scaling)
    C2 = current_yd + dt_2 * K1
    K2 = _dmp_acc(
        current_y + dt_2 * C1, C2, cdd, alpha_y, beta_y, goal_y, goal_yd,
        goal_ydd, start_y, Z[1], execution_time, F[:, 1], coupling_term, tdd,
        smooth_scaling)
    C3 = current_yd + dt * K2
    K3 = _dmp_acc(
        current_y + dt * C2, C3, cdd, alpha_y, beta_y, goal_y, goal_yd,
        goal_ydd, start_y, Z[2], execution_time, F[:, 2], coupling_term, tdd,
        smooth_scaling)

    current_y += dt * (current_yd + dt / 6.0 * (K0 + K1 + K2))
    current_yd += dt / 6.0 * (K0 + 2 * K1 + 2 * K2 + K3)

    if coupling_term is not None:
        cd, _ = coupling_term.coupling(current_y, current_yd)
        current_yd += cd / execution_time


def _dmp_acc(Y, V, cdd, alpha_y, beta_y, goal_y, goal_yd, goal_ydd,
             start_y, z, execution_time, f, coupling_term, tdd,
             smooth_scaling):
    """DMP acceleration.

    Parameters
    ----------
    Y : array, shape (n_dims,)
        Current state (position).

    V : array, shape (n_dims,)
        Current state derivative (velocity).

    cdd : array, shape (n_dims,)
        Coupling term acceleration.

    alpha_y : array, shape (n_dims,)
        Constant of transformation system.

    beta_y : array, shape (n_dims,)
        Constant of transformation system.

    goal_y : shape (n_dims,)
        Goal state (position).

    goal_yd : shape (n_dims,)
        Goal state derivative (velocity).

    goal_ydd : shape (n_dims,)
        Second goal state derivative (acceleration).

    start_y : array, shape (n_dims,)
        Start position.

    z : float
        Current phase.

    execution_time : float
        Time to execute the DMP.

    f : array, shape (n_dims,)
        Forcing term acceleration.

    coupling_term : object
        Coupling term object. Must have a function 'coupling' that takes as
        arguments the current position and velocity and returns a velocity and
        acceleration. (Velocity will be ignored.)

    tdd : array, shape (n_dims,)
        Acceleration correction from tracking error controller.

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.

    Returns
    -------
    ydd : array, shape (n_dims,)
        Resulting acceleration.
    """
    if coupling_term is not None:
        _, cdd = coupling_term.coupling(Y, V)
    if smooth_scaling:
        smoothing = beta_y * (goal_y - start_y) * z
    else:
        smoothing = 0.0
    return (
        alpha_y * (
            beta_y * (goal_y - Y)
            - execution_time * V
            - smoothing
        )
        + f
        + cdd
        + tdd
    ) / execution_time ** 2


def dmp_step_euler(
        last_t, t, current_y, current_yd, goal_y, goal_yd, goal_ydd, start_y,
        start_yd, start_ydd, goal_t, start_t, alpha_y, beta_y, forcing_term,
        coupling_term=None, coupling_term_precomputed=None, int_dt=0.001,
        p_gain=0.0, tracking_error=0.0, smooth_scaling=False):
    """Integrate regular DMP for one step with Euler integration.

    Parameters
    ----------
    last_t : float
        Time at last step.

    t : float
        Time at current step.

    current_y : array, shape (n_dims,)
        Current position. Will be modified.

    current_yd : array, shape (n_dims,)
        Current velocity. Will be modified.

    goal_y : array, shape (n_dims,)
        Goal position.

    goal_yd : array, shape (n_dims,)
        Goal velocity.

    goal_ydd : array, shape (n_dims,)
        Goal acceleration.

    start_y : array, shape (n_dims,)
        Start position.

    start_yd : array, shape (n_dims,)
        Start velocity.

    start_ydd : array, shape (n_dims,)
        Start acceleration.

    goal_t : float
        Time at the end.

    start_t : float
        Time at the start.

    alpha_y : array, shape (n_dims,)
        Constant in transformation system.

    beta_y : array, shape (n_dims,)
        Constant in transformation system.

    forcing_term : ForcingTerm
        Forcing term.

    coupling_term : CouplingTerm, optional (default: None)
        Coupling term. Must have a function coupling(y, yd) that returns
        additional velocity and acceleration.

    coupling_term_precomputed : tuple
        A precomputed coupling term, i.e., additional velocity and
        acceleration.

    int_dt : float, optional (default: 0.001)
        Time delta used internally for integration.

    p_gain : float, optional (default: 0)
        Proportional gain for tracking error.

    tracking_error : float, optional (default: 0)
        Tracking error from last step.

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.
    """
    if start_t >= goal_t:
        raise ValueError("Goal must be chronologically after start!")

    if t <= start_t:
        return np.copy(start_y), np.copy(start_yd), np.copy(start_ydd)

    execution_time = goal_t - start_t

    current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is None:
            cd, cdd = np.zeros_like(current_y), np.zeros_like(current_y)
            if coupling_term_precomputed is not None:
                cd += coupling_term_precomputed[0]
                cdd += coupling_term_precomputed[1]
        else:
            cd, cdd = None, None
        z = forcing_term.phase(current_t)
        f = forcing_term.forcing_term(z).squeeze()
        tdd = p_gain * tracking_error / dt

        ydd = _dmp_acc(
            current_y, current_yd, cdd, alpha_y, beta_y, goal_y, goal_yd,
            goal_ydd, start_y, z, execution_time, f, coupling_term, tdd,
            smooth_scaling)
        current_yd += dt * ydd
        current_y += dt * current_yd

        if coupling_term is not None:
            cd, _ = coupling_term.coupling(current_y, current_yd)
            current_yd += cd / execution_time


DMP_STEP_FUNCTIONS = {
    "rk4": dmp_step_rk4,
    "euler": dmp_step_euler
}
DEFAULT_DMP_STEP_FUNCTION = "rk4"

try:
    from ..dmp_fast import dmp_step as dmp_step_euler_cython, dmp_step_rk4 as dmp_step_rk4_cython
    DMP_STEP_FUNCTIONS["euler-cython"] = dmp_step_euler_cython
    DMP_STEP_FUNCTIONS["rk4-cython"] = dmp_step_rk4_cython
    DEFAULT_DMP_STEP_FUNCTION = "rk4-cython"
except ImportError:
    pass


class DMP(WeightParametersMixin, DMPBase):
    r"""Dynamical movement primitive (DMP).

    Equation of transformation system (according to [1]_, Eq. 2.1):

    .. math::

        \ddot{y} = (\alpha_y (\beta_y (g - y) - \tau \dot{y}) + f(z) + C_t) / \tau^2

    and if smooth scaling is activated (according to [2]_):

    .. math::

        \ddot{y} = (\alpha_y (\beta_y (g - y) - \tau \dot{y} - \underline{\beta_y (g - y_0) z}) + f(z) + C_t) / \tau^2

    Parameters
    ----------
    n_dims : int
        State space dimensions.

    execution_time : float, optional (default: 1)
        Execution time of the DMP: :math:`\tau`.

    dt : float, optional (default: 0.01)
        Time difference between DMP steps: :math:`\Delta t`.

    n_weights_per_dim : int, optional (default: 10)
        Number of weights of the function approximator per dimension.

    int_dt : float, optional (default: 0.001)
        Time difference for Euler integration of transformation system.

    p_gain : float, optional (default: 0)
        Gain for proportional controller of DMP tracking error.
        The domain is [0, execution_time**2/dt].

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.

    alpha_y : float or array-like, shape (n_dims,), optional (default: 25.0)
        Parameter of the transformation system.

    beta_y : float, list with length n_dims, or array with shape (n_dims,), optional (default: 6.25)
        Parameter of the transformation system.

    Attributes
    ----------
    execution_time_ : float
        Execution time of the DMP.

    dt_ : float
        Time difference between DMP steps. This value can be changed to adapt
        the frequency.

    References
    ----------
    .. [1] Ijspeert, A. J., Nakanishi, J., Hoffmann, H., Pastor, P., Schaal, S.
       (2013). Dynamical Movement Primitives: Learning Attractor Models for
       Motor Behaviors. Neural Computation 25 (2), 328-373. DOI:
       10.1162/NECO_a_00393,
       https://homes.cs.washington.edu/~todorov/courses/amath579/reading/DynamicPrimitives.pdf

    .. [2] Pastor, P., Hoffmann, H., Asfour, T., Schaal, S. (2009). Learning
       and Generalization of Motor Skills by Learning from Demonstration.
       In 2009 IEEE International Conference on Robotics and Automation,
       (pp. 763-768). DOI: 10.1109/ROBOT.2009.5152385,
       https://h2t.iar.kit.edu/pdf/Pastor2009.pdf
    """
    def __init__(self, n_dims, execution_time=1.0, dt=0.01,
                 n_weights_per_dim=10, int_dt=0.001, p_gain=0.0,
                 smooth_scaling=False, alpha_y=25.0, beta_y=6.25):
        super(DMP, self).__init__(n_dims, n_dims)
        self._execution_time = execution_time
        self.dt_ = dt
        self.n_weights_per_dim = n_weights_per_dim
        self.int_dt = int_dt
        self.p_gain = p_gain
        self.smooth_scaling = smooth_scaling

        self._init_forcing_term()

        self.alpha_y = ensure_1d_array(alpha_y, n_dims, "alpha_y")
        self.beta_y = ensure_1d_array(beta_y, n_dims, "beta_y")

    def _init_forcing_term(self):
        alpha_z = canonical_system_alpha(0.01, self.execution_time_, 0.0)
        self.forcing_term = ForcingTerm(
            self.n_dims, self.n_weights_per_dim, self.execution_time_,
            0.0, 0.8, alpha_z)

    def get_execution_time_(self):
        return self._execution_time

    def set_execution_time_(self, execution_time):
        self._execution_time = execution_time
        weights = self.forcing_term.weights_
        self._init_forcing_term()
        self.forcing_term.weights_ = weights

    execution_time_ = property(get_execution_time_, set_execution_time_)

    def step(self, last_y, last_yd, coupling_term=None,
             step_function=DEFAULT_DMP_STEP_FUNCTION):
        """DMP step.

        Parameters
        ----------
        last_y : array, shape (n_dims,)
            Last state.

        last_yd : array, shape (n_dims,)
            Last time derivative of state (e.g., velocity).

        coupling_term : object, optional (default: None)
            Coupling term that will be added to velocity.

        step_function : str, optional (default: 'rk4-cython')
            DMP integration function. Possible options: 'rk4', 'euler',
            'euler-cython', 'rk4-cython'.

        Returns
        -------
        y : array, shape (n_dims,)
            Next state.

        yd : array, shape (n_dims,)
            Next time derivative of state (e.g., velocity).
        """
        try:
            step_function = DMP_STEP_FUNCTIONS[step_function]
        except KeyError:
            raise ValueError(
                f"Step function must be in {DMP_STEP_FUNCTIONS.keys()}.")

        assert len(last_y) == self.n_dims
        assert len(last_yd) == self.n_dims
        self.last_t = self.t
        self.t += self.dt_

        if not self.initialized:
            self.current_y = np.copy(self.start_y)
            self.current_yd = np.copy(self.start_yd)
            self.initialized = True

        # https://github.com/studywolf/pydmps/blob/master/pydmps/cs.py
        tracking_error = self.current_y - last_y

        step_function(
            self.last_t, self.t,
            self.current_y, self.current_yd,
            self.goal_y, self.goal_yd, self.goal_ydd,
            self.start_y, self.start_yd, self.start_ydd,
            self.execution_time_, 0.0,
            self.alpha_y, self.beta_y,
            self.forcing_term,
            coupling_term=coupling_term,
            int_dt=self.int_dt,
            p_gain=self.p_gain,
            tracking_error=tracking_error,
            smooth_scaling=self.smooth_scaling)
        return np.copy(self.current_y), np.copy(self.current_yd)

    def open_loop(self, run_t=None, coupling_term=None,
                  step_function=DEFAULT_DMP_STEP_FUNCTION):
        """Run DMP open loop.

        Parameters
        ----------
        run_t : float, optional (default: execution_time)
            Run time of DMP. Can be shorter or longer than execution_time.

        coupling_term : object, optional (default: None)
            Coupling term that will be added to velocity.

        step_function : str, optional (default: 'rk4-cython')
            DMP integration function. Possible options: 'rk4', 'euler',
            'euler-cython', 'rk4-cython'.

        Returns
        -------
        T : array, shape (n_steps,)
            Time for each step.

        Y : array, shape (n_steps, n_dims)
            State at each step.

        Raises
        ------
        ValueError
            If step function is unknown.
        """
        try:
            step_function = DMP_STEP_FUNCTIONS[step_function]
        except KeyError:
            raise ValueError(
                f"Step function must be in {DMP_STEP_FUNCTIONS.keys()}.")

        return dmp_open_loop(
            self.execution_time_, 0.0, self.dt_,
            self.start_y, self.goal_y,
            self.alpha_y, self.beta_y,
            self.forcing_term,
            coupling_term,
            run_t, self.int_dt,
            step_function,
            smooth_scaling=self.smooth_scaling)

    def imitate(self, T, Y, regularization_coefficient=0.0,
                allow_final_velocity=False):
        r"""Imitate demonstration.

        Target forces of the forcing term are computed according to

        .. math::

            f_{target} =
            \tau^2 \ddot{y}_{demo}
            - \alpha_y(
                \beta_y (g-y_{demo})
                - \tau \dot{y}_{demo}
                - \underline{\beta_y (g-y_0) z}
            ),

        where the underlined part is only used when smooth scaling is used.

        Parameters
        ----------
        T : array, shape (n_steps,)
            Time for each step.

        Y : array, shape (n_steps, n_dims)
            State at each step.

        regularization_coefficient : float, optional (default: 0)
            Regularization coefficient for regression.

        allow_final_velocity : bool, optional (default: False)
            Allow a final velocity.
        """
        self.forcing_term.weights_[:, :], start_y, _, _, goal_y, _, _ = \
            dmp_imitate(
            T, Y,
            n_weights_per_dim=self.n_weights_per_dim,
            regularization_coefficient=regularization_coefficient,
            alpha_y=self.alpha_y, beta_y=self.beta_y,
            overlap=self.forcing_term.overlap,
            alpha_z=self.forcing_term.alpha_z,
            allow_final_velocity=allow_final_velocity,
            smooth_scaling=self.smooth_scaling)
        self.configure(start_y=start_y, goal_y=goal_y)


def dmp_transformation_system(
        Y, V, alpha_y, beta_y, goal_y, goal_yd, goal_ydd, start_y, z,
        execution_time):
    """Compute acceleration generated by transformation system of DMP."""
    return (
        alpha_y * (
            beta_y * (goal_y - Y)
            + execution_time * (goal_yd - V)
            - beta_y * (goal_y - start_y) * z
        )
    ) / execution_time ** 2 + goal_ydd


def determine_forces(T, Y, alpha_y, beta_y, alpha_z, allow_final_velocity,
                     smooth_scaling=False):
    """Determine forces that the forcing term should generate.

    Parameters
    ----------
    T : array, shape (n_steps,)
        Time of each step.

    Y : array, shape (n_steps, n_dims)
        Position at each step.

    alpha_y : array, shape (n_dims,)
        Parameter of the transformation system.

    beta_y : array, shape (n_dims,)
        Parameter of the transformation system.

    alpha_z : float
        Parameter of the canonical system.

    allow_final_velocity : bool
        Whether a final velocity is allowed. Will be set to 0 otherwise.

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.

    Returns
    -------
    F : array, shape (n_steps, n_dims)
        Forces.

    start_y : array, shape (n_dims,)
        Start position.

    start_yd : array, shape (n_dims,)
        Start velocity.

    start_ydd : array, shape (n_dims,)
        Start acceleration.

    goal_y : array, shape (n_dims,)
        Final position.

    goal_yd : array, shape (n_dims,)
        Final velocity.

    goal_ydd : array, shape (n_dims,)
        Final acceleration.
    """
    n_dims = Y.shape[1]
    DT = np.gradient(T)
    Yd = np.empty_like(Y)
    for d in range(n_dims):
        Yd[:, d] = np.gradient(Y[:, d]) / DT
    if not allow_final_velocity:
        Yd[-1, :] = 0.0
    Ydd = np.empty_like(Y)
    for d in range(n_dims):
        Ydd[:, d] = np.gradient(Yd[:, d]) / DT
    Ydd[-1, :] = 0.0

    execution_time = T[-1] - T[0]
    goal_y = Y[-1]
    start_y = Y[0]
    Z = phase(T, alpha_z, T[-1], T[0])
    F = np.empty((len(T), n_dims))
    for t in range(len(T)):
        if smooth_scaling:
            smoothing = beta_y * (goal_y - start_y) * Z[t]
        else:
            smoothing = 0.0
        F[t, :] = execution_time ** 2 * Ydd[t] - alpha_y * (
            beta_y * (goal_y - Y[t])
            - Yd[t] * execution_time
            - smoothing
        )
    return F, Y[0], Yd[0], Ydd[0], Y[-1], Yd[-1], Ydd[-1]


def dmp_imitate(
        T, Y, n_weights_per_dim, regularization_coefficient, alpha_y, beta_y,
        overlap, alpha_z, allow_final_velocity,
        determine_forces=determine_forces, smooth_scaling=False):
    """Compute weights and metaparameters of DMP.

    Parameters
    ----------
    T : array, shape (n_steps,)
        Time of each step.

    Y : array, shape (n_steps, n_dims)
        Position at each step.

    n_weights_per_dim : int
        Number of weights per dimension.

    regularization_coefficient : float, optional (default: 0)
        Regularization coefficient for regression.

    alpha_y : array, shape (n_dims,)
        Parameter of the transformation system.

    beta_y : array, shape (n_dims,)
        Parameter of the transformation system.

    overlap : float
        At which value should radial basis functions of the forcing term
        overlap?

    alpha_z : float
        Parameter of the canonical system.

    allow_final_velocity : bool
        Whether a final velocity is allowed. Will be set to 0 otherwise.

    determine_forces : callable
        Function to compute forces of the forcing term and metaparameters given
        the demonstration.

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.

    Returns
    -------
    weights : array, shape (n_dims, n_weights_per_dim)
        Weights of the forcing term.

    start_y : array, shape (n_dims,)
        Start position.

    start_yd : array, shape (n_dims,)
        Start velocity.

    start_ydd : array, shape (n_dims,)
        Start acceleration.

    goal_y : array, shape (n_dims,)
        Final position.

    goal_yd : array, shape (n_dims,)
        Final velocity.

    goal_ydd : array, shape (n_dims,)
        Final acceleration.
    """
    if regularization_coefficient < 0.0:
        raise ValueError("Regularization coefficient must be >= 0!")

    forcing_term = ForcingTerm(
        Y.shape[1], n_weights_per_dim, T[-1], T[0], overlap, alpha_z)
    F, start_y, start_yd, start_ydd, goal_y, goal_yd, goal_ydd = \
        determine_forces(
            T, Y, alpha_y, beta_y,
            alpha_z, allow_final_velocity,
            smooth_scaling
        )
    # F shape (n_steps, n_dims)

    X = forcing_term.design_matrix(T)  # shape (n_weights_per_dim, n_steps)

    return (ridge_regression(X, F, regularization_coefficient),
            start_y, start_yd, start_ydd, goal_y, goal_yd, goal_ydd)


def ridge_regression(X, Y, regularization_coefficient):
    r"""Ridge regression: linear regression with Tikhonov regularization.

    A linear model :math:`Y = X W^T` or :math:`y = W x` that minimizes
    :math:`||Y - X W^T||_2^2 + \lambda ||W||_2^2`, where :math:`\lambda`
    is the regularization coefficient.

    Parameters
    ----------
    X : array, shape (n_samples, n_features)
        Input features of linear model.

    Y : array, shape (n_samples, n_outputs)
        Target values.

    regularization_coefficient : float
        Regularization coefficient.

    Returns
    -------
    weights : array, shape (n_outputs, n_features)
        Weights of linear model.
    """
    return np.linalg.pinv(
        X.dot(X.T) + regularization_coefficient * np.eye(X.shape[0])
    ).dot(X).dot(Y).T


def dmp_open_loop(
        goal_t, start_t, dt, start_y, goal_y, alpha_y, beta_y, forcing_term,
        coupling_term=None, run_t=None, int_dt=0.001,
        step_function=dmp_step_rk4, smooth_scaling=False,
        start_yd=None, start_ydd=None, goal_yd=None, goal_ydd=None):
    """Run DMP without external feedback.

    Parameters
    ----------
    goal_t : float
        Time at the end.

    start_t : float
        Time at the start.

    dt : float, optional (default: 0.01)
        Time difference between DMP steps.

    start_y : array, shape (n_dims,)
        Start position.

    goal_y : array, shape (n_dims,)
        Goal position.

    alpha_y : array, shape (n_dims,)
        Constant in transformation system.

    beta_y : array, shape (n_dims,)
        Constant in transformation system.

    forcing_term : ForcingTerm
        Forcing term.

    coupling_term : CouplingTerm, optional (default: None)
        Coupling term. Must have a function coupling(y, yd) that returns
        additional velocity and acceleration.

    run_t : float, optional (default: goal_t)
        Time at which the DMP will be stopped.

    int_dt : float, optional (default: 0.001)
        Time delta used internally for integration.

    step_function : callable, optional (default: dmp_step_rk4)
        DMP integration function.

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.

    start_yd : shape (n_dims,)
        Start state derivative (velocity).

    start_ydd : shape (n_dims,)
        Second start state derivative (acceleration).

    goal_yd : shape (n_dims,)
        Goal state derivative (velocity).

    goal_ydd : shape (n_dims,)
        Second goal state derivative (acceleration).

    Returns
    -------
    T : array, shape (n_steps,)
        Times.

    Y : array, shape (n_steps, n_dims)
        Positions.
    """
    if goal_yd is None:
        goal_yd = np.zeros_like(goal_y)
    if goal_ydd is None:
        goal_ydd = np.zeros_like(goal_y)
    if start_yd is None:
        start_yd = np.zeros_like(start_y)
    if start_ydd is None:
        start_ydd = np.zeros_like(start_y)

    if run_t is None:
        run_t = goal_t

    current_y = np.copy(start_y)
    current_yd = np.copy(start_yd)

    T = np.arange(start_t, run_t + dt, dt)
    Y = np.empty((len(T), len(current_y)))
    Y[0] = current_y

    for i in range(1, len(T)):
        step_function(
            T[i - 1], T[i], current_y, current_yd,
            goal_y=goal_y, goal_yd=goal_yd, goal_ydd=goal_ydd,
            start_y=start_y, start_yd=start_yd, start_ydd=start_ydd,
            goal_t=goal_t, start_t=start_t,
            alpha_y=alpha_y, beta_y=beta_y,
            forcing_term=forcing_term, coupling_term=coupling_term,
            int_dt=int_dt, smooth_scaling=smooth_scaling)
        Y[i] = current_y

    return T, Y
