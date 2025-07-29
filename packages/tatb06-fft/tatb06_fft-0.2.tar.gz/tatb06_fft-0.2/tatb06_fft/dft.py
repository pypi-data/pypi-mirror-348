"""Contains DFT and inverse DFT algorithms"""

import numpy as np
from numpy import complex128
from numpy.typing import ArrayLike, NDArray


def dft(a: ArrayLike, variant: str = "explicit") -> NDArray[complex128]:
    """Computes the Fourier transform of the input data using the DFT-matrix

    :param a: Input array, can be real or complex
    :type a: ArrayLike
    :param variant: The implementation used, can be 'explicit' or 'implicit'. (Default 'explicit')
    :type variant: str
    :return: The transformed array
    :rtype: NDArray[complex128]
    """
    a = np.asarray(a)
    match variant:
        case "explicit":
            return _dft_explicit(a)
        case "implicit":
            return _dft_implicit(a)
        case _:
            raise ValueError(f"Invalid variant '{variant}'")


def _dft_explicit(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the Fourier transform of the input data using the DFT-matrix.

    Explicitly creates and stores the whole DFT-matrix in memory, and then transforms the input by multiplication.
    """
    N = a.shape[0]
    F = np.zeros((N, N), dtype=complex128)
    b = -2j * np.pi / N  # Precompute this
    for l in range(N):
        for k in range(N):
            F[l, k] = np.exp(l * k * b)

    return F @ a / np.sqrt(N)


def _dft_implicit(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the Fourier transform of the input data using the DFT-matrix.

    Does not compute the whole DFT-matrix, instead does the multiplication implicitly
    """
    N = a.shape[0]
    freq = np.zeros(N, dtype=complex128)
    for l in range(N):
        omega = np.exp(-2j * l * np.pi / N)
        for k in range(N):
            freq[l] += (omega**k) * a[k]

    return freq / np.sqrt(N)


def idft(a: ArrayLike, variant: str = "explicit") -> NDArray[complex128]:
    """Computes the inverse Fourier transform of the input data using the DFT-matrix

    :param a: Input array, can be real or complex
    :type a: ArrayLike
    :param variant: The implementation used, can be 'explicit' or 'implicit'. (Default 'explicit')
    :type variant: str
    :return: The transformed array
    :rtype: NDArray[complex128]
    """
    a = np.asarray(a)
    match variant:
        case "explicit":
            return _idft_explicit(a)
        case "implicit":
            return _idft_implicit(a)
        case _:
            raise ValueError(f"Invalid variant '{variant}'")


def _idft_explicit(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the inverse Fourier transform of the input data using the DFT-matrix.

    Explicitly creates and stores the whole DFT-matrix in memory, and then transforms the input by multiplication.
    """
    N = a.shape[0]
    F = np.zeros((N, N), dtype=complex128)
    b = 2j * np.pi / N  # Precompute this
    for l in range(N):
        for k in range(N):
            F[l, k] = np.exp(l * k * b)

    return F @ a / np.sqrt(N)


def _idft_implicit(a: NDArray[complex128]) -> NDArray[complex128]:
    """Computes the inverse Fourier transform of the input data using the DFT-matrix.

    Does not compute the whole DFT-matrix, instead does the multiplication implicitly
    """
    N = a.shape[0]
    freq = np.zeros(N, dtype=complex128)
    for l in range(N):
        omega = np.exp(2j * l * np.pi / N)
        for k in range(N):
            freq[l] += (omega**k) * a[k]

    return freq / np.sqrt(N)
