use std::{f64::consts::PI, thread};

use ndarray::prelude::*;
use num_complex::Complex64;
use pyo3::prelude::*;
use thread_pool::ThreadPool;

mod thread_pool;

#[pyfunction]
pub fn _fft_iter(mut x: Vec<Complex64>) -> PyResult<Vec<Complex64>> {
    let n = x.len();
    bit_reversal_permutation(&mut x);
    let mut block_size = 2;
    while block_size <= n {
        let half_block_size = block_size / 2;

        // Precompute my values
        let mut my_values = vec![];
        let my_block = (-2.0f64 * PI * Complex64::i() / block_size as f64).exp();
        let mut my = Complex64::ONE;
        for _ in 0..half_block_size {
            my_values.push(my);
            my *= my_block;
        }

        for i in (0..n).step_by(block_size) {
            for j in 0..half_block_size {
                let u = x[i + j];
                let v = my_values[j] * x[i + j + half_block_size];

                x[i + j] = u + v;
                x[i + j + half_block_size] = u - v;
            }
        }
        // Increase block size to next power of two
        block_size *= 2;
    }

    // Normalize output by dividing by sqrt(n)
    let sqrt_n = (n as f64).sqrt();
    let x_normalized = x
        .iter_mut()
        .map(|v| Complex64::new(v.re / sqrt_n, v.im / sqrt_n))
        .collect();

    Ok(x_normalized)
}

#[pyfunction]
pub fn _ifft_iter(mut x: Vec<Complex64>) -> PyResult<Vec<Complex64>> {
    let n = x.len();
    bit_reversal_permutation(&mut x);
    let mut block_size = 2;
    while block_size <= n {
        let half_block_size = block_size / 2;

        // Precompute my values
        let mut my_values = vec![];
        let my_block = (2.0f64 * PI * Complex64::i() / block_size as f64).exp();
        let mut my = Complex64::ONE;
        for _ in 0..half_block_size {
            my_values.push(my);
            my *= my_block;
        }

        for i in (0..n).step_by(block_size) {
            for j in 0..half_block_size {
                let u = x[i + j];
                let v = my_values[j] * x[i + j + half_block_size];

                x[i + j] = u + v;
                x[i + j + half_block_size] = u - v;
            }
        }
        // Increase block size to next power of two
        block_size *= 2;
    }

    // Normalize output by dividing by sqrt(n)
    let sqrt_n = (n as f64).sqrt();
    let x_normalized = x
        .iter_mut()
        .map(|v| Complex64::new(v.re / sqrt_n, v.im / sqrt_n))
        .collect();

    Ok(x_normalized)
}

#[pyfunction]
fn _fft_recur(x: Vec<Complex64>) -> PyResult<Vec<Complex64>> {
    // Convert input to an ndarray Array and send a mutable view of it to the implementation function
    let mut x_arr = Array1::<Complex64>::from_vec(x);
    Ok(_fft_recur_impl(x_arr.view_mut()).to_vec())
}

// Uses ndarray ArrayViews to avoid borrow checker
// Could be done with unsafe rust but this is easier
fn _fft_recur_impl(mut x: ArrayViewMut1<Complex64>) -> ArrayViewMut1<Complex64> {
    let n = x.len();
    let n_half = n / 2;
    if n == 1 {
        return x;
    } else {
        let mut y_t = _fft_recur_impl(x.slice_mut(s![0..n;2])).to_vec();
        let mut y_b = _fft_recur_impl(x.slice_mut(s![1..n;2])).to_vec();

        // Normalize by dividing by sqrt(2) at each recursion level
        // This is equivalent to dividing the final output by sqrt(n)
        let sqrt_2 = Complex64::from(2.0f64.sqrt());
        for (t, b) in y_t.iter_mut().zip(y_b.iter_mut()) {
            *t /= sqrt_2;
            *b /= sqrt_2;
        }

        let my = (-2.0f64 * PI * Complex64::i() / n as f64).exp();

        for i in 0..(n_half) {
            let z = my.powu(i as u32) * y_b[i];
            x[i] = y_t[i] + z;
            x[i + n_half] = y_t[i] - z;
        }

        return x;
    }
}

#[pyfunction]
fn _ifft_recur(x: Vec<Complex64>) -> PyResult<Vec<Complex64>> {
    // Convert input to an ndarray Array and send a mutable view of it to the implementation function
    let mut x_arr = Array1::<Complex64>::from_vec(x);
    Ok(_ifft_recur_impl(x_arr.view_mut()).to_vec())
}

// Uses ndarray ArrayViews to avoid borrow checker
// Could be done with unsafe rust but this is easier
fn _ifft_recur_impl(mut x: ArrayViewMut1<Complex64>) -> ArrayViewMut1<Complex64> {
    let n = x.len();
    let n_half = n / 2;
    if n == 1 {
        return x;
    } else {
        let mut y_t = _ifft_recur_impl(x.slice_mut(s![0..n;2])).to_vec();
        let mut y_b = _ifft_recur_impl(x.slice_mut(s![1..n;2])).to_vec();

        // Normalize by dividing by sqrt(2) at each recursion level
        // This is equivalent to dividing the final output by sqrt(n)
        let sqrt_2 = Complex64::from(2.0f64.sqrt());
        for (t, b) in y_t.iter_mut().zip(y_b.iter_mut()) {
            *t /= sqrt_2;
            *b /= sqrt_2;
        }

        let my = (2.0f64 * PI * Complex64::i() / n as f64).exp();

        for i in 0..(n_half) {
            let z = my.powu(i as u32) * y_b[i];
            x[i] = y_t[i] + z;
            x[i + n_half] = y_t[i] - z;
        }

        return x;
    }
}

#[pyfunction]
pub fn _fft_parallell(mut x: Vec<Complex64>) -> PyResult<Vec<Complex64>> {
    // Create a thread pool with a thread count equal to the number of available cores
    let thread_pool = ThreadPool::new(thread::available_parallelism().unwrap().get());

    let n = x.len();
    bit_reversal_permutation(&mut x);
    // Create a raw pointer to the data
    // Store it as usize to get around the borrow checker when sending between threads
    let x_addr = x.as_mut_ptr() as usize;

    let mut block_size = 2;
    while block_size <= n {
        let half_block_size = block_size / 2;

        // Precompute my values
        let mut my_values = vec![];
        let my_block = (-2.0f64 * PI * Complex64::i() / block_size as f64).exp();
        let mut my = Complex64::ONE;
        for _ in 0..half_block_size {
            my_values.push(my);
            my *= my_block;
        }

        if block_size >= 512 {
            // Create a raw pointer to the my vector
            // Store it as usize to get around the borrow checker when sending between threads
            let my_values_addr = my_values.as_mut_ptr() as usize;

            for i in (0..n).step_by(block_size) {
                thread_pool.run(move || {
                    for j in 0..half_block_size {
                        unsafe {
                            let u = *(x_addr as *mut Complex64).add(i + j);
                            let my = *(my_values_addr as *mut Complex64).add(j);
                            let v = my * *(x_addr as *mut Complex64).add(i + j + half_block_size);

                            *(x_addr as *mut Complex64).add(i + j) = u + v;
                            *(x_addr as *mut Complex64).add(i + j + half_block_size) = u - v;
                        }
                    }
                });
            }
        } else {
            for i in (0..n).step_by(block_size) {
                for j in 0..half_block_size {
                    let u = x[i + j];
                    let v = my_values[j] * x[i + j + half_block_size];

                    x[i + j] = u + v;
                    x[i + j + half_block_size] = u - v;
                }
            }
        }

        block_size *= 2;

        // Wait for worker tasks to finish
        thread_pool.sync();
    }

    // Normalize output by dividing by sqrt(n)
    let sqrt_n = (n as f64).sqrt();
    let x_normalized = x
        .iter_mut()
        .map(|v| Complex64::new(v.re / sqrt_n, v.im / sqrt_n))
        .collect();

    Ok(x_normalized)
}

#[pyfunction]
pub fn _ifft_parallell(mut x: Vec<Complex64>) -> PyResult<Vec<Complex64>> {
    // Create a thread pool with a thread count equal to the number of available cores
    let thread_pool = ThreadPool::new(thread::available_parallelism().unwrap().get());

    let n = x.len();
    bit_reversal_permutation(&mut x);
    // Create a raw pointer to the data
    // Store it as usize to get around the borrow checker when sending between threads
    let x_addr = x.as_mut_ptr() as usize;

    let mut block_size = 2;
    while block_size <= n {
        let half_block_size = block_size / 2;

        // Precompute my values
        let mut my_values = vec![];
        let my_block = (2.0f64 * PI * Complex64::i() / block_size as f64).exp();
        let mut my = Complex64::ONE;
        for _ in 0..half_block_size {
            my_values.push(my);
            my *= my_block;
        }

        if block_size >= 512 {
            // Create a raw pointer to the my vector
            // Store it as usize to get around the borrow checker when sending between threads
            let my_values_addr = my_values.as_mut_ptr() as usize;

            for i in (0..n).step_by(block_size) {
                thread_pool.run(move || {
                    for j in 0..half_block_size {
                        unsafe {
                            let u = *(x_addr as *mut Complex64).add(i + j);
                            let my = *(my_values_addr as *mut Complex64).add(j);
                            let v = my * *(x_addr as *mut Complex64).add(i + j + half_block_size);

                            *(x_addr as *mut Complex64).add(i + j) = u + v;
                            *(x_addr as *mut Complex64).add(i + j + half_block_size) = u - v;
                        }
                    }
                });
            }
        } else {
            for i in (0..n).step_by(block_size) {
                for j in 0..half_block_size {
                    let u = x[i + j];
                    let v = my_values[j] * x[i + j + half_block_size];

                    x[i + j] = u + v;
                    x[i + j + half_block_size] = u - v;
                }
            }
        }

        block_size *= 2;

        // Wait for worker tasks to finish
        thread_pool.sync();
    }

    // Normalize output by dividing by sqrt(n)
    let sqrt_n = (n as f64).sqrt();
    let x_normalized = x
        .iter_mut()
        .map(|v| Complex64::new(v.re / sqrt_n, v.im / sqrt_n))
        .collect();

    Ok(x_normalized)
}

pub fn bit_reversal_permutation(x: &mut Vec<Complex64>) {
    let n = x.len();

    let log2n = n.ilog2();
    for i in 0..n {
        let new_i = reverse_bits(i as u64, log2n) as usize;
        if new_i > i {
            x.swap(i, new_i);
        }
    }
}

// https://github.com/EugeneGonzalez/bit_reverse/blob/master/src/lookup.rs
#[cfg_attr(rustfmt, rustfmt_skip)]
const REVERSE_LOOKUP: [u8; 256] = [
    0,  128, 64, 192, 32, 160,  96, 224, 16, 144, 80, 208, 48, 176, 112, 240,
    8,  136, 72, 200, 40, 168, 104, 232, 24, 152, 88, 216, 56, 184, 120, 248,
    4,  132, 68, 196, 36, 164, 100, 228, 20, 148, 84, 212, 52, 180, 116, 244,
    12, 140, 76, 204, 44, 172, 108, 236, 28, 156, 92, 220, 60, 188, 124, 252,
    2,  130, 66, 194, 34, 162,  98, 226, 18, 146, 82, 210, 50, 178, 114, 242,
    10, 138, 74, 202, 42, 170, 106, 234, 26, 154, 90, 218, 58, 186, 122, 250,
    6,  134, 70, 198, 38, 166, 102, 230, 22, 150, 86, 214, 54, 182, 118, 246,
    14, 142, 78, 206, 46, 174, 110, 238, 30, 158, 94, 222, 62, 190, 126, 254,
    1,  129, 65, 193, 33, 161,  97, 225, 17, 145, 81, 209, 49, 177, 113, 241,
    9,  137, 73, 201, 41, 169, 105, 233, 25, 153, 89, 217, 57, 185, 121, 249,
    5,  133, 69, 197, 37, 165, 101, 229, 21, 149, 85, 213, 53, 181, 117, 245,
    13, 141, 77, 205, 45, 173, 109, 237, 29, 157, 93, 221, 61, 189, 125, 253,
    3,  131, 67, 195, 35, 163,  99, 227, 19, 147, 83, 211, 51, 179, 115, 243,
    11, 139, 75, 203, 43, 171, 107, 235, 27, 155, 91, 219, 59, 187, 123, 251,
    7,  135, 71, 199, 39, 167, 103, 231, 23, 151, 87, 215, 55, 183, 119, 247,
    15, 143, 79, 207, 47, 175, 111, 239, 31, 159, 95, 223, 63, 191, 127, 255
];

pub fn reverse_bits(n: u64, bit_width: u32) -> u64 {
    let blocks = bit_width / 8;
    let rest = bit_width - blocks * 8;
    let mut n_rev = 0u64;
    for block in 0..blocks {
        n_rev |= (REVERSE_LOOKUP[(n >> (block * 8)) as u8 as usize] as u64)
            << (bit_width - (block + 1) * 8);
    }
    n_rev |= (REVERSE_LOOKUP[(n >> (bit_width - rest)) as u8 as usize] as u64) >> (8 - rest);
    return n_rev;
}

pub fn reverse_bits_slow(mut n: u64, bit_width: u32) -> u64 {
    let mut result = 0;
    for _ in 0..bit_width {
        result <<= 1;
        result |= n & 1;
        n >>= 1;
    }
    result
}

#[pymodule]
fn _tatb06_fft(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(_fft_iter, m)?)?;
    m.add_function(wrap_pyfunction!(_ifft_iter, m)?)?;
    m.add_function(wrap_pyfunction!(_fft_recur, m)?)?;
    m.add_function(wrap_pyfunction!(_ifft_recur, m)?)?;
    m.add_function(wrap_pyfunction!(_fft_parallell, m)?)?;
    m.add_function(wrap_pyfunction!(_ifft_parallell, m)?)?;
    Ok(())
}
