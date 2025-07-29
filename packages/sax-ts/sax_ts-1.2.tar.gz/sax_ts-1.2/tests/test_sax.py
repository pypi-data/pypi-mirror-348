import numpy as np
import pytest
from reference import discretise
from sax_ts import sax

np.random.seed(123)
a = np.arange(20)
b = np.random.random(1000)

D = [a, b]
WIN = [8, 12, 16, 20]
S = [2, 3, 5, 8]
W = [3, 4, 5, 6, 7, 8]
A = range(4, 12)

window_params = [(data, window, 1, 4, 4) for data in D for window in WIN]
stride_params = [(data, 16, stride, 5, 4) for data in D for stride in S]
w_divides_window_params = [(data, 16, 1, w, 4) for data in D for w in W[1::2]]
w_no_divides_window_params = [(data, 16, 1, w, 4) for data in D for w in W[::2]]
alpha_params = [(data, 16, 1, 5, alpha) for data in D for alpha in A]


@pytest.mark.parametrize("test_input,window,stride,w,alpha", window_params)
def test_window(test_input, window, stride, w, alpha):
    expected = discretise(test_input, window, stride, w, alpha)
    assert sax(test_input, window, stride, w, alpha) == expected


@pytest.mark.parametrize("test_input,window,stride,w,alpha", stride_params)
def test_stride(test_input, window, stride, w, alpha):
    expected = discretise(test_input, window, stride, w, alpha)
    assert sax(test_input, window, stride, w, alpha) == expected


@pytest.mark.parametrize("test_input,window,stride,w,alpha", w_divides_window_params)
def test_w_divides_window(test_input, window, stride, w, alpha):
    expected = discretise(test_input, window, stride, w, alpha)
    assert sax(test_input, window, stride, w, alpha) == expected


@pytest.mark.parametrize("test_input,window,stride,w,alpha", w_no_divides_window_params)
def test_w_no_divides_window(test_input, window, stride, w, alpha):
    expected = discretise(test_input, window, stride, w, alpha)
    assert sax(test_input, window, stride, w, alpha) == expected


@pytest.mark.parametrize("test_input,window,stride,w,alpha", alpha_params)
def test_alpha(test_input, window, stride, w, alpha):
    expected = discretise(test_input, window, stride, w, alpha)
    assert sax(test_input, window, stride, w, alpha) == expected
