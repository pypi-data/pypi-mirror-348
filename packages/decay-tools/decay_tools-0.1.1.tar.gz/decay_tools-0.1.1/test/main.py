import sys

sys.path.append("src/")

import numpy as np
from decay_tools import (
    DecayParameters,
    DoubleDecayParameters,
    fit_single_schmidt,
    fit_double_schmidt,
    get_hist_and_bins,
    estimate_n_bins,
    visualize_double_fit,
    visualize_single_fit
)

# from visualize import visualize_single_fit, visualize_double_fit

if __name__ == "__main__":
    times_mks = np.array([2, 2, 2.1, 2.1, 2.7, 2.8, 2.8, 2.8, 2.8, 3, 3.4, 3.5, 3.6, 3.6, 4, 4, 4, 4.1, 4.3, 4.4, 4.6, 4.7, 5, 5.3, 5.3, 5.5, 5.7, 5.9, 6.3, 6.5, 6.7, 6.7, 7, 7.3, 7.4, 7.8, 7.9, 8.2, 8.3, 8.3, 8.5, 9, 10.2, 10.3, 10.4, 10.7, 11.2, 11.2, 11.6, 11.6, 11.7, 12.1, 12.5, 13.1, 13.2, 13.3, 13.6, 13.7, 13.8, 13.8, 16, 16.8, 19.7, 20.3, 21.5, 21.5, 21.6, 22.2, 23.2, 25.5, 26.7, 27.6, 30.6, 31.8, 31.8, 32.1, 34.6, 44.9, 44.9, 47.6, 59, 76.3, 80.8, 95.2, 1323.4, 11220.7, 55098.1, 113904.2])
    true_half_life = 8
    true_n0 = 5_000
    times_mks = np.random.exponential(scale=true_half_life / np.log(2), size=true_n0)
    print(f"True T1/2={true_half_life:.2f}; Sampled T1/2={np.mean(times_mks)*np.log(2):.2f}")
    log_times = np.log(times_mks)
    guess = DecayParameters(true_half_life * 1.2, true_n0*0.7, 0)
    print(estimate_n_bins(log_times, method="std"))
    data, bins = get_hist_and_bins(logt=log_times, n_bins_method="iqr")
    
    res = fit_single_schmidt(data, bins, initial_guess=guess)
    print(res)
    visualize_single_fit(data, bins, res)
    
    true_half_life_2 = 80
    true_n0_2 = 1_000
    times_mks_2 = np.random.exponential(scale=true_half_life_2 / np.log(2), size=true_n0_2)
    print(f"Second activity: True T1/2={true_half_life:.2f}; Sampled T1/2={np.mean(times_mks_2)*np.log(2):.2f}")
    comb_times_mks = np.append(times_mks, times_mks_2)
    comb_log_times = np.log(comb_times_mks)
    print(comb_times_mks)
    print("\n")
    data, bins = get_hist_and_bins(logt=comb_log_times, n_bins_method="iqr")
    g = DoubleDecayParameters(
        hl_short_us=0.7 * true_half_life,
        hl_long_us=1.3 * true_half_life_2,
        n0_short=true_n0 * 0.9,
        n0_long=true_n0_2*1.2,
        c=0
    )
    comb_res = fit_double_schmidt(data, bins, g)
    print(comb_res)
    visualize_double_fit(data, bins, comb_res)
