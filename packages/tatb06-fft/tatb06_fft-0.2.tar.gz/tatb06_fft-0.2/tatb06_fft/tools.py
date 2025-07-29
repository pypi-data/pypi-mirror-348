"""Contains helper functions for generating signals, plotting, and measuring function execution time"""

import time
import numpy as np
from numpy import float64
from numpy.typing import ArrayLike, NDArray
import matplotlib.pyplot as plt


def generate_sine_signal(
    parameters: list[tuple[float, float]], resolution: int
) -> NDArray[float64]:
    """Generates a signal on [0,2*pi] using multiple sine waves with the given parameters.

    :param parameters: A list containing the amplitudes and frequencies for the different sine waves.
        The layout should be [(amp1, freq1), (amp2, freq2), ...].
    :type parameters: list[tuple[float, float]]
    :param resolution: How many samples of the signal to return
    :type resolution: int
    :rtype: NDArray[float64]
    """
    samples = 2 * np.pi * np.arange(0, 1, 1 / resolution)
    signal = np.zeros(resolution)
    for amp, freq in parameters:
        signal += amp * np.sin(freq * samples)
    return signal


def generate_cosine_signal(
    parameters: list[tuple[float, float]], resolution: int
) -> NDArray[float64]:
    """Generates a signal on [0,1] using multiple cosine waves with the given parameters.

    :param parameters: A list containing the amplitudes and frequencies for the different cosine waves.
        The layout should be [(amp1, freq1), (amp2, freq2), ...].
    :type parameters: list[tuple[float, float]]
    :param resolution: How many samples of the signal to return
    :type resolution: int
    :rtype: NDArray[float64]
    """
    samples = 2 * np.pi * np.arange(0, 1, 1 / resolution)
    signal = np.zeros(resolution)
    for amp, freq in parameters:
        signal += amp * np.cos(freq * samples)
    return signal


def plot_magnitude_stem(
    a: ArrayLike, title: str = "", reorder: bool = True, show: bool = True
) -> None:
    """Plots a magnitude stem of the input data in a new figure.

    :param a: Input array, can be real or complex
    :type a: ArrayLike
    :param title: Title of the figure
    :type title: str
    :reorder: If set to True, reorder the data using reorder_frequencies() before plotting.
    :type reorder: bool
    :param show: If set to True, run plt.show() after plotting the stem. Should be False if you want to plot multiple plots
    :type show: bool
    """
    a = np.asarray(a)
    N = a.shape[0]

    if reorder:
        a = reorder_frequencies(a)

    # Generate frequencies for the x-axis
    freqs = np.arange(-N // 2, N // 2, 1)
    fig, ax = plt.subplots()
    ax.stem(freqs, np.abs(a), markerfmt="", basefmt="b")
    fig.suptitle(title)

    if show:
        plt.show()


def reorder_frequencies(a: ArrayLike) -> ArrayLike:
    """Moves the second half of the frequency data to the front for correct visualization.

    In the output of the FFT algorithm, the first half of the data corresponds to the frequencies 0 to N/2,
    and the second half corresponds to -N/2 to just below 0, which is why the reordering is needed.

    :param a: Input array, can be real or complex
    :type a: ArrayLike
    """
    a = np.asarray(a)
    N = a.shape[0]
    return np.concatenate((a[N // 2 :], a[: N // 2]), axis=0)


def time_function(f, args, n_samples=5):
    """Runs the given function a number of times and returns the average execution time.

    :param f: The function to measure
    :param args: A list containing the positional arguments sent to the function
    :type args: list
    :param n_samples: The number of samples to take, i.e. how many times the function is run
    :return: The mean execution time of the function calls
    """
    time = 0
    for _ in range(n_samples):
        time += _time_function_once(f, *args)
    return time / n_samples


def _time_function_once(f, *args):
    start = time.time()
    f(*args)
    end = time.time()
    return end - start
