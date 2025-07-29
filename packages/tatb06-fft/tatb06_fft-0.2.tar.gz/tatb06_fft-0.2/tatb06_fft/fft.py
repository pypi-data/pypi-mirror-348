"""Contains algorithms for the FFT"""

import numpy as np
from numpy import complex128
from numpy.typing import ArrayLike, NDArray

from ._tatb06_fft import _fft_iter as _rust_fft_iter
from ._tatb06_fft import _fft_recur as _rust_fft_recur
from ._tatb06_fft import _fft_parallell as _rust_fft_parallell

from ._tatb06_fft import _ifft_iter as _rust_ifft_iter
from ._tatb06_fft import _ifft_recur as _rust_ifft_recur
from ._tatb06_fft import _ifft_parallell as _rust_ifft_parallell


def fft(a: ArrayLike, variant: str = "python_iter") -> tuple[NDArray[complex128], int]:
    """Computes the Fourier transform of the input data using the Cooley–Tukey FFT algorithm.

    Pads the input array with zeros at the tail if its length is not a power of two.

    :param a: Input array, can be real or complex
    :type a: ArrayLike
    :param variant: The implementation used, can be 'python_iter', 'python_recur', 'rust_iter', 'rust_recur', 'rust_parallell'. (Default 'python_iter').
    :type variant: str
    :return: A tuple containing the transformed array and with how many zeros the array was padded.
    :rtype: tuple[NDArray[complex128], int]
    """
    a = np.asarray(a)
    # Pad the array to the neares power of two
    a, pad_size = _pad_at_tail(a)

    match variant:
        case "python_iter":
            return _fft_iter(a), pad_size
        case "python_recur":
            return _fft_recur(a), pad_size
        case "rust_iter":
            return np.array(_rust_fft_iter(a)), pad_size
        case "rust_recur":
            return np.array(_rust_fft_recur(a)), pad_size
        case "rust_parallell":
            return np.array(_rust_fft_parallell(a)), pad_size
        case _:
            raise ValueError(f"Invalid variant '{variant}'")


def _fft_iter(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the Fourier transform of the input data using the iterative variant of the Cooley–Tukey FFT algorithm"""
    N = a.shape[0]
    a = _bit_reversal_permutation(a)

    block_size = 2
    while block_size <= N:
        half_block_size = block_size // 2
        my_block = np.exp(-2j * np.pi / block_size)

        for i in range(0, N, block_size):
            my = complex(1)
            for j in range(0, half_block_size):
                u = a[i + j]
                v = my * a[i + j + half_block_size]
                a[i + j] = u + v
                a[i + j + half_block_size] = u - v
                my *= my_block

        block_size *= 2

    return a / np.sqrt(N)


def _fft_recur(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the Fourier transform of the input data using the recursive variant of the Cooley–Tukey FFT algorithm"""
    N = a.shape[0]
    if N == 1:
        return a
    else:
        yT = _fft_recur(a[0:N:2]) / np.sqrt(2)
        yB = _fft_recur(a[1:N:2]) / np.sqrt(2)
        my = np.exp(-2j * np.pi / N)
        d = my ** np.arange(N // 2)
        z = d * yB
        return np.concatenate((yT + z, yT - z), axis=0)


def ifft(a: ArrayLike, variant: str = "python_iter") -> tuple[NDArray[complex128], int]:
    """Computes the inverse Fourier transform of the input data using the Cooley–Tukey FFT algorithm

    Pads the input array with zeros at the center (i.e. at the high frequencies) if its length is not a power of two.

    :param a: Input array, can be real or complex
    :type a: ArrayLike
    :param variant: The implementation used, can be 'python_iter', 'python_recur', 'rust_iter', 'rust_recur', 'rust_parallell'. (Default 'python_iter').
    :type variant: str
    :return: A tuple containing the transformed array and with how many zeros the array was padded.
    :rtype: tuple[NDArray[complex128], int]
    """
    a = np.asarray(a)
    # Pad the array to the neares power of two
    a, pad_size = _pad_at_center(a)

    match variant:
        case "python_iter":
            return _ifft_iter(a), pad_size
        case "python_recur":
            return _ifft_recur(a), pad_size
        case "rust_iter":
            return np.array(_rust_ifft_iter(a)), pad_size
        case "rust_recur":
            return np.array(_rust_ifft_recur(a)), pad_size
        case "rust_parallell":
            return np.array(_rust_ifft_parallell(a)), pad_size
        case _:
            raise ValueError(f"Invalid variant '{variant}'")


def _ifft_iter(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the inverse Fourier transform of the input data using iterative variant of the Cooley–Tukey FFT algorithm"""
    N = a.shape[0]
    a = _bit_reversal_permutation(a)

    block_size = 2
    while block_size <= N:
        half_block_size = block_size // 2
        my_block = np.exp(2j * np.pi / block_size)

        for i in range(0, N, block_size):
            my = complex(1)
            for j in range(0, half_block_size):
                u = a[i + j]
                v = my * a[i + j + half_block_size]
                a[i + j] = u + v
                a[i + j + half_block_size] = u - v
                my *= my_block

        block_size *= 2

    return a / np.sqrt(N)


def _ifft_recur(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the inverse Fourier transform of the input data using recursive variant of the Cooley–Tukey FFT algorithm"""
    N = a.shape[0]
    if N == 1:
        return a
    else:
        yT = _ifft_recur(a[0:N:2]) / np.sqrt(2)
        yB = _ifft_recur(a[1:N:2]) / np.sqrt(2)
        my = np.exp(2j * np.pi / N)
        d = my ** np.arange(N // 2)
        z = d * yB
        return np.concatenate((yT + z, yT - z), axis=0)


def _reverse_bits(n, bit_width):
    # Bit representation as string
    b = f"{n:0{bit_width}b}"
    # Return reversed bit string converted to int
    return int(b[::-1], 2)


def _bit_reversal_permutation(x):
    n = x.shape[0]
    x_out = np.zeros(n, dtype=complex)
    log2n = int(np.log2(n))
    for i in range(n):
        x_out[_reverse_bits(i, log2n)] = x[i]
    return x_out


def _pad_at_tail(a: NDArray[complex128]) -> tuple[NDArray[complex128], int]:
    """Pad with zeros to the nearest power of two. The zeros are added to the end of the array."""
    N = a.shape[0]
    pad_to = 1
    while pad_to < N:
        pad_to *= 2
    pad_size = pad_to - N

    a_padded = np.concatenate((a, np.zeros(pad_size, dtype=complex128)))
    return (a_padded, pad_size)


def _pad_at_center(a: NDArray[complex128]) -> tuple[NDArray[complex128], int]:
    """Pad with zeros to the nearest power of two. The zeros are added at the center of the array since that corresponds to adding more high frequencies."""
    N = a.shape[0]
    assert N >= 2

    pad_to = 1
    while pad_to < N:
        pad_to *= 2
    pad_size = pad_to - N

    a_padded = np.concatenate(
        (a[: N // 2], np.zeros(pad_size, dtype=complex128), a[N // 2 :])
    )
    return (a_padded, pad_size)
