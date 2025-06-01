import numpy as np
import pytest
from isetcam import ie_poisson, ie_prctile, ie_mvnrnd, ie_normpdf


def test_ie_poisson_scalar_frozen():
    val1, seed1 = ie_poisson(5, n_samp=4, noise_flag="frozen", seed=42)
    val2, seed2 = ie_poisson(5, n_samp=4, noise_flag="frozen", seed=42)
    assert seed1 == 42
    assert seed2 == 42
    assert np.array_equal(val1, val2)


def test_ie_poisson_random():
    val1, seed1 = ie_poisson(2, n_samp=2, noise_flag="random")
    val2, seed2 = ie_poisson(2, n_samp=2, noise_flag="random")
    assert not np.array_equal(val1, val2) or seed1 != seed2


def test_ie_prctile_basic():
    data = np.arange(10)
    p50 = ie_prctile(data, 50)
    assert np.allclose(p50, np.percentile(data, 50))


def test_ie_prctile_error():
    with pytest.raises(ValueError):
        ie_prctile([1, 2, 3], 150)


def test_ie_mvnrnd_shape():
    mu = [0, 0]
    sigma = [[1, 0], [0, 1]]
    out = ie_mvnrnd(mu, sigma, k=5)
    assert out.shape == (5, 2)


def test_ie_normpdf_values():
    val = ie_normpdf(0)
    assert np.isclose(val, 1 / np.sqrt(2 * np.pi))
