import numpy as np
import pytest
from numpy.testing import assert_allclose
from reference import paa_window
from sax_ts import paa

np.random.seed(123)
a = np.arange(20)
b = np.random.random(1000)

D = [a]
WIN = [8, 12, 16, 20]
S = [2, 3, 5, 8]
W = [3, 4, 5, 6, 7, 8]
A = range(4, 12)

window_params = [(data, window, 1, 4) for data in D for window in WIN]
stride_params = [(data, 16, stride, 5) for data in D for stride in S]
w_divides_window_params = [(data, 16, 1, w) for data in D for w in W[1::2]]
w_no_divides_window_params = [(data, 16, 1, w) for data in D for w in W[::2]]


@pytest.mark.parametrize("test_input,window,stride,w", window_params)
def test_window(test_input, window, stride, w):
    expected = paa_window(test_input, window, stride, w)
    assert_allclose(paa(test_input, window, stride, w), expected, atol=1e-6)


@pytest.mark.parametrize("test_input,window,stride,w", stride_params)
def test_stride(test_input, window, stride, w):
    expected = paa_window(test_input, window, stride, w)
    assert_allclose(paa(test_input, window, stride, w), expected, atol=1e-6)


@pytest.mark.parametrize("test_input,window,stride,w", w_divides_window_params)
def test_w_divides_window(test_input, window, stride, w):
    expected = paa_window(test_input, window, stride, w)
    assert_allclose(paa(test_input, window, stride, w), expected, atol=1e-6)


@pytest.mark.parametrize("test_input,window,stride,w", w_no_divides_window_params)
def test_w_no_divides_window(test_input, window, stride, w):
    expected = paa_window(test_input, window, stride, w)
    assert_allclose(paa(test_input, window, stride, w), expected, atol=1e-6)
