import numpy as np
import pytest

from isetcam import mk_inv_gamma_table


def test_mk_inv_gamma_table_monotonic():
    gamma = np.linspace(0, 1, 4)
    n_entries = 4 * len(gamma)
    inv = mk_inv_gamma_table(gamma)
    expected = np.interp(np.linspace(0, 1, n_entries), gamma, np.arange(gamma.size))
    assert inv.shape == (n_entries,)
    assert np.allclose(inv, expected)


def test_mk_inv_gamma_table_nonmonotonic():
    gamma = np.array([0.0, 0.2, 0.1, 1.0])
    n_entries = 8
    with pytest.warns(UserWarning):
        inv = mk_inv_gamma_table(gamma, n_entries)
    sorted_gamma = np.sort(gamma)
    pos = np.where(np.diff(sorted_gamma) > 0)[0] + 1
    pos = np.insert(pos, 0, 0)
    expected = np.interp(np.linspace(0, 1, n_entries), sorted_gamma[pos], pos)
    assert inv.shape == (n_entries,)
    assert np.allclose(inv, expected)
