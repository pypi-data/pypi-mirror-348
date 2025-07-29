import numpy as np


def e_geo(traces, x, y):
    """
    Calculate the geomagnetic component from the electric field in the shower plane,
    i.e. the electric field should be in the (vxB, vxvxB, v) CS

    Parameters
    ----------
    traces : np.ndarray
        The traces in the shower plane, shaped as (samples, polarisations)
    x : float
        The antenna position along the vxB axis
    y : float
        The antenna position along the vxvxB axis

    Returns
    -------
    e_geo : np.ndarray
        The geomagnetic component of the electric field
    """
    return traces[:, 1] * x / y - traces[:, 0]


def e_ce(traces, x, y):
    """
    Calculate the charge-excess (or Askaryan) component of electric field in the shower plane,
    i.e. the electric field should be in the (vxB, vxvxB, v) CS

    Parameters
    ----------
    traces : np.ndarray
        The traces in the shower plane, shaped as (samples, polarisations)
    x : float
        The antenna position along the vxB axis
    y : float
        The antenna position along the vxvxB axis

    Returns
    -------
    e_ce : np.ndarray
        The charge-excess component of the electric field
    """
    return -traces[:, 1] * np.sqrt(x ** 2 + y ** 2) / y


def e_to_geo_ce(traces, x, y):
    """
    Decouples the electric field in the shower plane, i.e. the electric field should be in the (vxB, vxvxB, v) CS,
    into the geomagnetic and charge-excess components.

    Parameters
    ----------
    traces : np.ndarray
        The traces in the shower plane, shaped as (samples, polarisations)
    x : float
        The antenna position along the vxB axis
    y : float
        The antenna position along the vxvxB axis

    Returns
    -------
    e_geo : np.ndarray
        The geomagnetic component of the electric field
    e_ce : np.ndarray
        The charge-excess component of the electric field
    """
    return e_geo(traces, x, y), e_ce(traces, x, y)


def geo_ce_to_e(traces, x, y):
    """
    Reconstruct a three-dimensional electric field in the shower plane, i.e. the (vxB, vxvxB, v) CS,
    from the geomagnetic component of the charge-excess components. The v-component is set to zero.

    Parameters
    ----------
    traces : np.ndarray
        The electric field traces, shaped as (samples, components)
    x : float
        The antenna position along the vxB axis
    y : float
        The antenna position along the vxvxB axis

    Returns
    -------
    e_field : np.ndarray
        The three-dimensional electric field, in the shower plane CS, shaped as (samples, polarisations)
    """
    my_e_geo = traces.T[0]
    my_e_ce = traces.T[1]

    trace_vB = -1 * (my_e_geo + my_e_ce * x / np.sqrt(x ** 2 + y ** 2))
    trace_vvB = y / x * (my_e_geo + trace_vB)
    trace_v = np.zeros_like(trace_vB)

    return np.stack((trace_vB.T, trace_vvB.T, trace_v.T), axis=-1)
