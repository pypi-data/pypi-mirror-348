"""Cython implementations of basic DMP functions."""
import numpy as np
cimport numpy as np
cimport cython
from libcpp cimport bool
from libc.math cimport sqrt, cos, sin, acos, pi, exp


np.import_array()


cdef double M_2PI = 2.0 * pi
cdef double M_PI_HALF = 0.5 * pi
cdef double EPSILON = 1e-10


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef phase(t, double alpha, double goal_t, double start_t):
    """Map time to phase.

    Parameters
    ----------
    t : float
        Current time.

    alpha : float
        Value of the alpha parameter of the canonical system.

    goal_t : float
        Time at which the execution should be done.

    start_t : float
        Time at which the execution should start.

    Returns
    -------
    z : float
        Value of phase variable.
    """
    cdef double execution_time = goal_t - start_t
    return np.exp(-alpha * (t - start_t) / execution_time)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef dmp_step(
        double last_t, double t, np.ndarray[double, ndim=1] current_y, np.ndarray[double, ndim=1] current_yd,
        np.ndarray[double, ndim=1] goal_y, np.ndarray[double, ndim=1] goal_yd,
        np.ndarray[double, ndim=1] goal_ydd, np.ndarray[double, ndim=1] start_y,
        np.ndarray[double, ndim=1] start_yd, np.ndarray[double, ndim=1] start_ydd,
        double goal_t, double start_t, np.ndarray[double, ndim=1] alpha_y, np.ndarray[double, ndim=1] beta_y,
        object forcing_term, object coupling_term=None,
        tuple coupling_term_precomputed=None,
        double int_dt=0.001, double p_gain=0.0,
        np.ndarray tracking_error=None,
        bint smooth_scaling=False):
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
        current_y[:] = start_y
        current_yd[:] = start_yd

    cdef double execution_time = goal_t - start_t

    cdef int n_dims = current_y.shape[0]

    cdef np.ndarray[double, ndim=1] current_ydd = np.empty(n_dims, dtype=np.float64)

    cdef np.ndarray[double, ndim=1] cd = np.empty(n_dims, dtype=np.float64)
    cdef np.ndarray[double, ndim=1] cdd = np.empty(n_dims, dtype=np.float64)

    cdef np.ndarray[double, ndim=1] f = np.empty(n_dims, dtype=np.float64)

    cdef int d
    cdef double current_t
    cdef double dt
    cdef double z
    cdef double smoothing

    current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is not None:
            cd[:], cdd[:] = coupling_term.coupling(current_y, current_yd)
        elif coupling_term_precomputed is not None:
            cd[:] = coupling_term_precomputed[0]
            cdd[:] = coupling_term_precomputed[1]
        else:
            cd[:] = 0.0
            cdd[:] = 0.0
        if tracking_error is not None:
            cdd += p_gain * tracking_error / dt

        z = forcing_term.phase(current_t)
        f[:] = forcing_term.forcing_term(z).squeeze()

        for d in range(n_dims):
            if smooth_scaling:
                smoothing = beta_y[d] * (goal_y[d] - start_y[d]) * z
            else:
                smoothing = 0.0

            current_ydd[d] = (
                alpha_y[d] * (
                    beta_y[d] * (goal_y[d] - current_y[d])
                    - execution_time * current_yd[d]
                    - smoothing
                )
                + f[d]
                + cdd[d]
            ) / execution_time ** 2
            current_yd[d] += dt * current_ydd[d] + cd[d] / execution_time
            current_y[d] += dt * current_yd[d]


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef dmp_step_rk4(
        double last_t, double t, np.ndarray[double, ndim=1] current_y, np.ndarray[double, ndim=1] current_yd,
        np.ndarray[double, ndim=1] goal_y, np.ndarray[double, ndim=1] goal_yd,
        np.ndarray[double, ndim=1] goal_ydd, np.ndarray[double, ndim=1] start_y,
        np.ndarray[double, ndim=1] start_yd, np.ndarray[double, ndim=1] start_ydd,
        double goal_t, double start_t, np.ndarray[double, ndim=1] alpha_y, np.ndarray[double, ndim=1] beta_y,
        object forcing_term, object coupling_term=None,
        tuple coupling_term_precomputed=None,
        double int_dt=0.001, double p_gain=0.0,
        np.ndarray tracking_error=None,
        bint smooth_scaling=False):
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
    cdef int n_dims = current_y.shape[0]

    cdef np.ndarray[double, ndim=1] cd = np.zeros(n_dims, dtype=np.float64)
    cdef np.ndarray[double, ndim=1] cdd = np.zeros(n_dims, dtype=np.float64)
    if coupling_term_precomputed is not None:
        cd += coupling_term_precomputed[0]
        cdd += coupling_term_precomputed[1]

    # precompute constants for following queries
    cdef double execution_time = goal_t - start_t
    cdef double dt = t - last_t
    cdef double dt_2 = 0.5 * dt
    cdef np.ndarray[double, ndim=1] T = np.array([t, t + dt_2, t + dt])
    cdef np.ndarray[double, ndim=1] Z = forcing_term.phase(T)
    cdef np.ndarray[double, ndim=2] F = forcing_term.forcing_term(Z)
    cdef np.ndarray[double, ndim=1] tdd
    if tracking_error is not None:
        tdd = p_gain / dt * tracking_error
    else:
        tdd = np.zeros(n_dims, dtype=np.float64)

    cdef np.ndarray[double, ndim=1] K0 = _dmp_acc(
        current_y, current_yd, cdd, dt, alpha_y, beta_y, goal_y, goal_yd,
        goal_ydd, start_y, Z[0], execution_time, F[:, 0], coupling_term,
        p_gain, tdd, smooth_scaling)
    cdef np.ndarray[double, ndim=1] C1 = current_yd + dt_2 * K0
    cdef np.ndarray[double, ndim=1] K1 = _dmp_acc(
        current_y + dt_2 * current_yd, C1, cdd, dt, alpha_y, beta_y, goal_y, goal_yd,
        goal_ydd, start_y, Z[1], execution_time, F[:, 1], coupling_term,
        p_gain, tdd, smooth_scaling)
    cdef np.ndarray[double, ndim=1] C2 = current_yd + dt_2 * K1
    cdef np.ndarray[double, ndim=1] K2 = _dmp_acc(
        current_y + dt_2 * C1, C2, cdd, dt, alpha_y, beta_y, goal_y, goal_yd,
        goal_ydd, start_y, Z[1], execution_time, F[:, 1], coupling_term,
        p_gain, tdd, smooth_scaling)
    cdef np.ndarray[double, ndim=1] C3 = current_yd + dt * K2
    cdef np.ndarray[double, ndim=1] K3 = _dmp_acc(
        current_y + dt * C2, C3, cdd, dt, alpha_y, beta_y, goal_y, goal_yd,
        goal_ydd, start_y, Z[2], execution_time, F[:, 2], coupling_term,
        p_gain, tdd, smooth_scaling)

    cdef int i
    for i in range(n_dims):
        current_y[i] += dt * (current_yd[i] + 2 * C1[i] + 2 * C2[i] + C3[i]) / 6.0
        current_yd[i] += dt * (K0[i] + 2 * K1[i] + 2 * K2[i] + K3[i]) / 6.0

    if coupling_term is not None:
        cd[:], _ = coupling_term.coupling(current_y, current_yd)
        current_yd += cd / execution_time


cdef _dmp_acc(
        np.ndarray[double, ndim=1] Y, np.ndarray[double, ndim=1] V,
        np.ndarray[double, ndim=1] cdd, double dt, np.ndarray[double, ndim=1] alpha_y, np.ndarray[double, ndim=1] beta_y,
        np.ndarray[double, ndim=1] goal_y, np.ndarray[double, ndim=1] goal_yd,
        np.ndarray[double, ndim=1] goal_ydd, np.ndarray[double, ndim=1] start_y,
        double z, double execution_time, np.ndarray[double, ndim=1] f,
        object coupling_term, double p_gain, np.ndarray[double, ndim=1] tdd,
        bint smooth_scaling):
    if coupling_term is not None:
        _, cdd[:] = coupling_term.coupling(Y, V)

    cdef int n_dims = Y.shape[0]
    cdef np.ndarray[double, ndim=1] Ydd = np.empty(n_dims, dtype=np.float64)
    cdef int d
    cdef double smoothing
    for d in range(n_dims):
        if smooth_scaling:
            smoothing = beta_y[d] * (goal_y[d] - start_y[d]) * z
        else:
            smoothing = 0.0
        Ydd[d] = (
            alpha_y[d] * (
                beta_y[d] * (goal_y[d] - Y[d])
                - execution_time * V[d]
                - smoothing
            )
            + f[d]
            + cdd[d]
            + tdd[d]
        ) / execution_time ** 2
    return Ydd


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef dmp_step_quaternion(
        double last_t, double t,
        np.ndarray[double, ndim=1] current_y,
        np.ndarray[double, ndim=1] current_yd,
        np.ndarray[double, ndim=1] goal_y,
        np.ndarray[double, ndim=1] goal_yd,
        np.ndarray[double, ndim=1] goal_ydd,
        np.ndarray[double, ndim=1] start_y,
        np.ndarray[double, ndim=1] start_yd,
        np.ndarray[double, ndim=1] start_ydd,
        double goal_t, double start_t, np.ndarray[double, ndim=1] alpha_y, np.ndarray[double, ndim=1] beta_y,
        forcing_term, coupling_term=None, coupling_term_precomputed=None,
        double int_dt=0.001, bint smooth_scaling=False):
    """Integrate quaternion DMP for one step with Euler integration.

    Parameters
    ----------
    last_t : float
        Time at last step.

    t : float
        Time at current step.

    current_y : array, shape (7,)
        Current position. Will be modified.

    current_yd : array, shape (6,)
        Current velocity. Will be modified.

    goal_y : array, shape (7,)
        Goal position.

    goal_yd : array, shape (6,)
        Goal velocity.

    goal_ydd : array, shape (6,)
        Goal acceleration.

    start_y : array, shape (7,)
        Start position.

    start_yd : array, shape (6,)
        Start velocity.

    start_ydd : array, shape (6,)
        Start acceleration.

    goal_t : float
        Time at the end.

    start_t : float
        Time at the start.

    alpha_y : array, shape (6,)
        Constant in transformation system.

    beta_y : array, shape (6,)
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

    smooth_scaling : bool, optional (default: False)
        Avoids jumps during the beginning of DMP execution when the goal
        is changed and the trajectory is scaled by interpolating between
        the old and new scaling of the trajectory.
    """
    if t <= start_t:
        current_y[:] = start_y
        current_yd[:] = start_yd

    cdef double execution_time = goal_t - start_t

    cdef np.ndarray[double, ndim=1] current_ydd = np.empty(3, dtype=np.float64)

    cdef np.ndarray[double, ndim=1] cd = np.zeros(3, dtype=np.float64)
    cdef np.ndarray[double, ndim=1] cdd = np.zeros(3, dtype=np.float64)

    cdef np.ndarray[double, ndim=1] f = np.empty(3, dtype=np.float64)

    cdef np.ndarray[double, ndim=1] goal_y_minus_start_y

    cdef int d
    cdef double current_t
    cdef double dt
    cdef double z
    cdef np.ndarray[double, ndim=1] smoothing = np.empty(3, dtype=np.float64)
    if not smooth_scaling:
        smoothing[:] = 0

    current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is not None:
            cd[:], cdd[:] = coupling_term.coupling(current_y, current_yd)
        elif coupling_term_precomputed is not None:
            cd[:] = coupling_term_precomputed[0]
            cdd[:] = coupling_term_precomputed[1]

        z = forcing_term.phase(current_t)
        f[:] = forcing_term.forcing_term(z).squeeze()

        if smooth_scaling:
            goal_y_minus_start_y = compact_axis_angle_from_quaternion(
                concatenate_quaternions(goal_y, q_conj(start_y)))
            smoothing[:] = beta_y * z * goal_y_minus_start_y

        current_ydd[:] = (
            alpha_y * (
                beta_y * compact_axis_angle_from_quaternion(
                    concatenate_quaternions(goal_y, q_conj(current_y)))
                - execution_time * current_yd
                - smoothing
            )
            + f
            + cdd
        ) / execution_time ** 2
        current_yd += dt * current_ydd + cd / execution_time
        current_y[:] = concatenate_quaternions(
            quaternion_from_compact_axis_angle(dt * current_yd), current_y)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef dmp_step_dual_cartesian(
        double last_t, double t,
        np.ndarray[double, ndim=1] current_y, np.ndarray[double, ndim=1] current_yd,
        np.ndarray[double, ndim=1] goal_y, np.ndarray[double, ndim=1] goal_yd, np.ndarray[double, ndim=1] goal_ydd,
        np.ndarray[double, ndim=1] start_y, np.ndarray[double, ndim=1] start_yd, np.ndarray[double, ndim=1] start_ydd,
        double goal_t, double start_t, np.ndarray[double, ndim=1] alpha_y, np.ndarray[double, ndim=1] beta_y,
        forcing_term, coupling_term=None,
        double int_dt=0.001,
        double p_gain=0.0, np.ndarray tracking_error=None,
        bint smooth_scaling=False):
    """Integrate bimanual Cartesian DMP for one step with Euler integration.

    Parameters
    ----------
    last_t : float
        Time at last step.

    t : float
        Time at current step.

    current_y : array, shape (14,)
        Current position. Will be modified.

    current_yd : array, shape (12,)
        Current velocity. Will be modified.

    goal_y : array, shape (14,)
        Goal position.

    goal_yd : array, shape (12,)
        Goal velocity.

    goal_ydd : array, shape (12,)
        Goal acceleration.

    start_y : array, shape (14,)
        Start position.

    start_yd : array, shape (12,)
        Start velocity.

    start_ydd : array, shape (12,)
        Start acceleration.

    goal_t : float
        Time at the end.

    start_t : float
        Time at the start.

    alpha_y : array, shape (12,)
        Constant in transformation system.

    beta_y : array, shape (12,)
        Constant in transformation system.

    forcing_term : ForcingTerm
        Forcing term.

    coupling_term : CouplingTerm, optional (default: None)
        Coupling term. Must have a function coupling(y, yd) that returns
        additional velocity and acceleration.

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
    if t <= start_t:
        current_y[:] = start_y
        current_yd[:] = start_yd

    cdef double execution_time = goal_t - start_t

    cdef np.ndarray[double, ndim=1] current_ydd = np.empty_like(current_yd)

    cdef int n_vel_dims = current_yd.shape[0]

    cdef np.ndarray[double, ndim=1] cd = np.empty(n_vel_dims, dtype=float)
    cdef np.ndarray[double, ndim=1] cdd = np.empty(n_vel_dims, dtype=float)

    cdef np.ndarray[double, ndim=1] f = np.empty(n_vel_dims, dtype=float)
    cdef np.ndarray[double, ndim=1] goal_y_minus_start_y
    cdef double smoothing_pos
    cdef np.ndarray[double, ndim=1] smoothing_orn = np.empty(3, dtype=float)
    if not smooth_scaling:
        smoothing_orn[:] = 0.0

    cdef double z

    cdef int pps
    cdef int pvs
    cdef np.ndarray[long, ndim=2] POS_INDICES = np.array(
        [[0, 0], [1, 1], [2, 2], [7, 6], [8, 7], [9, 8]], dtype=int)

    cdef double dt
    cdef double current_t = last_t
    while current_t < t:
        dt = int_dt
        if t - current_t < int_dt:
            dt = t - current_t
        current_t += dt

        if coupling_term is None:
            cd[:] = 0.0
            cdd[:] = 0.0
        else:
            cd[:], cdd[:] = coupling_term.coupling(current_y, current_yd)

        z = forcing_term.phase(current_t)
        f[:] = forcing_term.forcing_term(z).squeeze()
        if tracking_error is not None:
            for pps, pvs in POS_INDICES:
                cdd[pvs] += p_gain * tracking_error[pps] / dt
            for ops, ovs in ((slice(3, 7), slice(3, 6)), (slice(10, 14), slice(9, 12))):
                cdd[ovs] += p_gain * compact_axis_angle_from_quaternion(tracking_error[ops]) / dt

        # position components
        for pps, pvs in POS_INDICES:
            if smooth_scaling:
                smoothing_pos = beta_y[pps] * (goal_y[pps] - start_y[pps]) * z
            else:
                smoothing_pos = 0.0
            current_ydd[pvs] = (
                alpha_y[pvs] * (
                    beta_y[pvs] * (goal_y[pps] - current_y[pps])
                    - execution_time * current_yd[pvs]
                    - smoothing_pos
                )
                + f[pvs]
                + cdd[pvs]
            ) / execution_time ** 2
            current_yd[pvs] += dt * current_ydd[pvs] + cd[pvs] / execution_time
            current_y[pps] += dt * current_yd[pvs]

        # orientation components
        for ops, ovs in ((slice(3, 7), slice(3, 6)), (slice(10, 14), slice(9, 12))):
            if smooth_scaling:
                goal_y_minus_start_y = compact_axis_angle_from_quaternion(
                    concatenate_quaternions(goal_y[ops], q_conj(start_y[ops])))
                smoothing_orn[:] = beta_y[ovs] * z * goal_y_minus_start_y
            current_ydd[ovs] = (
                alpha_y[ovs] * (
                    beta_y[ovs] * compact_axis_angle_from_quaternion(
                        concatenate_quaternions(goal_y[ops], q_conj(current_y[ops])))
                    - execution_time * current_yd[ovs]
                    - smoothing_orn
                )
                + f[ovs]
                + cdd[ovs]
            ) / execution_time ** 2
            current_yd[ovs] += dt * current_ydd[ovs] + cd[ovs] / execution_time
            current_y[ops] = concatenate_quaternions(
                quaternion_from_compact_axis_angle(dt * current_yd[ovs]),
                current_y[ops])


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef concatenate_quaternions(
        np.ndarray[double, ndim=1] q1, np.ndarray[double, ndim=1] q2):
    """Concatenate two quaternions.

    We use Hamilton's quaternion multiplication.

    Parameters
    ----------
    q1 : array-like, shape (4,)
        First quaternion

    q2 : array-like, shape (4,)
        Second quaternion

    Returns
    -------
    q12 : array-like, shape (4,)
        Quaternion that represents the concatenated rotation q1 * q2
    """
    cdef np.ndarray[double, ndim=1] q12 = np.empty(4)
    q12[0] = q1[0] * q2[0]
    # cross product q1[1:] x q2[1:]
    q12[1] = q1[2] * q2[3] - q1[3] * q2[2]
    q12[2] = q1[3] * q2[1] - q1[1] * q2[3]
    q12[3] = q1[1] * q2[2] - q1[2] * q2[1]
    cdef int i
    for i in range(1, 4):
        q12[0] -= q1[i] * q2[i]
        q12[i] += q1[0] * q2[i] + q2[0] * q1[i]

    cdef double norm = sqrt(q12[0] * q12[0] + q12[1] * q12[1] + q12[2] * q12[2] + q12[3] * q12[3])
    for i in range(4):
        q12[i] /= norm
    return q12


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef quaternion_from_compact_axis_angle(np.ndarray[double, ndim=1] a):
    """Compute quaternion from compact axis-angle (exponential map).

    We usually assume active rotations.

    Parameters
    ----------
    a : array-like, shape (4,)
        Axis of rotation and rotation angle: angle * (x, y, z)

    Returns
    -------
    q : array-like, shape (4,)
        Unit quaternion to represent rotation: (w, x, y, z)
    """
    cdef double angle = sqrt(a[0] * a[0] + a[1] * a[1] + a[2] * a[2])
    if angle == 0.0:
        return np.array([1.0, 0.0, 0.0, 0.0])

    cdef np.ndarray[double, ndim=1] axis
    axis = a / angle

    cdef np.ndarray[double, ndim=1] q = np.empty(4)
    cdef double half_angle = angle / 2.0
    q[0] = cos(half_angle)
    cdef double s = sin(half_angle)
    q[1] = s * axis[0]
    q[2] = s * axis[1]
    q[3] = s * axis[2]
    return q


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cdef q_conj(np.ndarray[double, ndim=1] q):
    """Conjugate of quaternion.

    The conjugate of a unit quaternion inverts the rotation represented by
    this unit quaternion. The conjugate of a quaternion q is often denoted
    as q*.

    Parameters
    ----------
    q : array-like, shape (4,)
        Unit quaternion to represent rotation: (w, x, y, z)

    Returns
    -------
    q_c : array-like, shape (4,)
        Conjugate (w, -x, -y, -z)
    """
    return np.array([q[0], -q[1], -q[2], -q[3]])


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef compact_axis_angle_from_quaternion(np.ndarray[double, ndim=1] q):
    """Compute compact axis-angle from quaternion (logarithmic map).

    We usually assume active rotations.

    Parameters
    ----------
    q : array-like, shape (4,)
        Unit quaternion to represent rotation: (w, x, y, z)

    Returns
    -------
    a : array-like, shape (3,)
        Axis of rotation and rotation angle: angle * (x, y, z). The angle is
        constrained to [0, pi).
    """
    cdef double p_norm_sqr = q[1] * q[1] + q[2] * q[2] + q[3] * q[3]
    if p_norm_sqr < 1e-32:
        return np.zeros(3)
    cdef double q_norm = sqrt(q[0] * q[0] + p_norm_sqr)
    cdef np.ndarray[double, ndim=1] q_n = q / q_norm
    cdef double p_norm = sqrt(p_norm_sqr) / q_norm
    # Source of the solution: http://stackoverflow.com/a/32266181
    cdef double angle = ((2 * acos(q_n[0]) + pi) % M_2PI - pi)
    return q_n[1:] / (p_norm / angle)


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef matrix_from_compact_axis_angle(np.ndarray[double, ndim=1] r):
    cdef double theta = np.linalg.norm(r)
    if theta == 0.0:
        return np.eye(3)
    cdef double ux = r[0] / theta
    cdef double uy = r[1] / theta
    cdef double uz = r[2] / theta
    cdef double c = cos(theta)
    cdef double s = sin(theta)
    cdef double ci = 1.0 - c
    cdef np.ndarray[double, ndim=2] R = np.empty((3, 3), dtype=float)
    R[0, 0] = ci * ux * ux + c
    R[0, 1] = ci * ux * uy - uz * s
    R[0, 2] = ci * ux * uz + uy * s
    R[1, 0] = ci * uy * ux + uz * s
    R[1, 1] = ci * uy * uy + c
    R[1, 2] = ci * uy * uz - ux * s
    R[2, 0] = ci * uz * ux - uy * s
    R[2, 1] = ci * uz * uy + ux * s
    R[2, 2] = ci * uz * uz + c
    return R


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
cpdef obstacle_avoidance_acceleration_2d(
        np.ndarray[double, ndim=1] y, np.ndarray[double, ndim=1] yd,
        np.ndarray[double, ndim=1] obstacle_position, double gamma, double beta):
    """Compute acceleration for obstacle avoidance in 2D.

    Parameters
    ----------
    y : array, shape (2,)
        Current position.

    yd : array, shape (2,)
        Current velocity.

    obstacle_position : array, shape (2,)
        Position of the point obstacle.

    gamma : float
        Obstacle avoidance parameter.

    beta : float
        Obstacle avoidance parameter.

    Returns
    -------
    cdd : array, shape (2,)
        Acceleration.
    """
    cdef np.ndarray[double, ndim=1] obstacle_diff = obstacle_position - y
    cdef double r = obstacle_diff[0] * yd[1] - obstacle_diff[1] * yd[0]
    if r != 0.0:
        r *= M_PI_HALF / abs(r)
    cdef np.ndarray[double, ndim=1] r_vec = np.array([0.0, 0.0, r])
    cdef np.ndarray[double, ndim=2] R = matrix_from_compact_axis_angle(r_vec)[:2, :2]
    cdef double theta_nom = obstacle_diff[0] * yd[0] + obstacle_diff[1] * yd[1]
    cdef double obstacle_diff_norm = sqrt(obstacle_diff[0] * obstacle_diff[0] + obstacle_diff[1] * obstacle_diff[1])
    cdef double yd_norm = sqrt(yd[0] * yd[0] + yd[1] * yd[1])
    cdef double theta_denom = obstacle_diff_norm * yd_norm + EPSILON
    cdef double theta = acos(theta_nom / theta_denom)
    cdef np.ndarray[double, ndim=1] rotated_velocity = np.dot(R, yd)
    cdef np.ndarray[double, ndim=1] cdd = gamma * rotated_velocity * (theta * exp(-beta * theta))
    return cdd
