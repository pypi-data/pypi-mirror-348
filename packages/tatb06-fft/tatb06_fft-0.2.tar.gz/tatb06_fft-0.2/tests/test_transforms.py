import numpy as np
from numpy.typing import ArrayLike
from tatb06_fft import dft, fft

N = 2**7


#####
# DFT
#####


def test_dft():
    # Random uniform complex array between -1 and 1
    a = np.random.uniform(-1, 1, N) + 1j * np.random.uniform(-1, 1, N)

    np_ft = np.fft.fft(a, norm="ortho")

    assert is_almost_equal(np_ft, dft.dft(a, "explicit"))
    assert is_almost_equal(np_ft, dft.dft(a, "implicit"))


def test_idft():
    # Random uniform complex array between -1 and 1
    a = np.random.uniform(-1, 1, N) + 1j * np.random.uniform(-1, 1, N)

    np_ift = np.fft.ifft(a, norm="ortho")

    assert is_almost_equal(np_ift, dft.idft(a, "explicit"))
    assert is_almost_equal(np_ift, dft.idft(a, "implicit"))


def test_dft_forward_backward():
    # Random uniform complex array between -1 and 1
    a = np.random.uniform(-1, 1, N) + 1j * np.random.uniform(-1, 1, N)

    assert is_almost_equal(a, dft.idft(dft.dft(a, "explicit"), "explicit"))
    assert is_almost_equal(a, dft.idft(dft.dft(a, "implicit"), "implicit"))


#####
# FFT
#####


def test_pad_at_tail():
    a, p = fft._pad_at_tail(np.zeros(N - 2, dtype=np.complex128))
    assert (a == np.zeros(N, dtype=np.complex128)).all()
    assert p == 2

    a, p = fft._pad_at_tail(np.zeros(N, dtype=np.complex128))
    assert (a == np.zeros(N, dtype=np.complex128)).all()
    assert p == 0

    a, p = fft._pad_at_tail(np.zeros(0, dtype=np.complex128))
    assert (a == np.zeros(1, dtype=np.complex128)).all()
    assert p == 1


def test_pad_at_center():
    a, p = fft._pad_at_center(np.ones(6, dtype=np.complex128))
    assert (a == np.array([1, 1, 1, 0, 0, 1, 1, 1])).all()
    assert p == 2

    a, p = fft._pad_at_center(np.ones(7, dtype=np.complex128))
    assert (a == np.array([1, 1, 1, 0, 1, 1, 1, 1])).all()
    assert p == 1

    a, p = fft._pad_at_center(np.ones(8, dtype=np.complex128))
    assert (a == np.array([1, 1, 1, 1, 1, 1, 1, 1])).all()
    assert p == 0


def test_fft():
    # Random uniform complex array between -1 and 1
    a = np.random.uniform(-1, 1, N) + 1j * np.random.uniform(-1, 1, N)

    np_ft = np.fft.fft(a, norm="ortho")

    assert is_almost_equal(np_ft, fft.fft(a, "python_iter")[0])
    assert is_almost_equal(np_ft, fft.fft(a, "python_recur")[0])
    assert is_almost_equal(np_ft, fft.fft(a, "rust_iter")[0])
    assert is_almost_equal(np_ft, fft.fft(a, "rust_recur")[0])
    assert is_almost_equal(np_ft, fft.fft(a, "rust_parallell")[0])


def test_ifft():
    # Random uniform complex array between -1 and 1
    a = np.random.uniform(-1, 1, N) + 1j * np.random.uniform(-1, 1, N)

    np_ift = np.fft.ifft(a, norm="ortho")

    assert is_almost_equal(np_ift, fft.ifft(a, "python_iter")[0])
    assert is_almost_equal(np_ift, fft.ifft(a, "python_recur")[0])
    assert is_almost_equal(np_ift, fft.ifft(a, "rust_iter")[0])
    assert is_almost_equal(np_ift, fft.ifft(a, "rust_recur")[0])
    assert is_almost_equal(np_ift, fft.ifft(a, "rust_parallell")[0])


def test_fft_forward_backward():
    # Random uniform complex array between -1 and 1
    a = np.random.uniform(-1, 1, N) + 1j * np.random.uniform(-1, 1, N)

    assert is_almost_equal(a, fft.ifft(fft.fft(a, "python_iter")[0], "python_iter")[0])
    assert is_almost_equal(
        a, fft.ifft(fft.fft(a, "python_recur")[0], "python_recur")[0]
    )
    assert is_almost_equal(a, fft.ifft(fft.fft(a, "rust_iter")[0], "rust_iter")[0])
    assert is_almost_equal(a, fft.ifft(fft.fft(a, "rust_recur")[0], "rust_recur")[0])
    assert is_almost_equal(
        a, fft.ifft(fft.fft(a, "rust_parallell")[0], "rust_parallell")[0]
    )


#########
# Helpers
#########


def is_almost_equal(a: ArrayLike, b: ArrayLike, threshold=0.0000001) -> bool:
    a = np.asarray(a)
    b = np.asarray(b)

    assert a.shape == b.shape

    delta = np.abs(a - b)
    for val in delta:
        if val > threshold:
            return False

    return True
