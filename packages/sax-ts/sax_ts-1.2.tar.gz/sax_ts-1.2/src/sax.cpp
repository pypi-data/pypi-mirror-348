#include "sax.h"
#include <algorithm>
#include <cmath>
#include <vector>

// --- Public functions ---
std::vector<std::vector<char>> sax(const std::vector<double> &ts,
                                  const int window, const int stride,
                                  const int w, const int alpha) {
  int num_windows = (ts.size() - window) / stride + 1;
  std::vector<std::vector<char>> windows(num_windows, std::vector<char>(w));
  std::vector<double> window_segment(window);

  for (int i = 0; i < num_windows; ++i) {
    std::vector<double> window_segment(ts.begin() + i * stride,
                                       ts.begin() + i * stride + window);
    znorm(window_segment, window);
    discretise(window_segment, windows[i], window, w, alpha);
  }

  return windows;
}

std::vector<std::vector<double>> paa(const std::vector<double> &ts,
                                     const int window, const int stride,
                                     const int w) {
  int num_windows = (ts.size() - window) / stride + 1;
  std::vector<std::vector<double>> windows(num_windows, std::vector<double>(w));
  std::vector<double> window_segment(window);

  for (int i = 0; i < num_windows; ++i) {
    std::vector<double> window_segment(ts.begin() + i * stride,
                                       ts.begin() + i * stride + window);
    znorm(window_segment, window);
    paa_window(window_segment, windows[i], window, w);
  }

  return windows;
}

// --- Helper functions ---
void znorm(std::vector<double> &window_segment, const int window) {
  double sum = 0;
  double sq_sum = 0;
  for (double val : window_segment) {
    sum += val;
  }
  double mean = sum / static_cast<double>(window);
  for (double val : window_segment) {
    sq_sum += (val - mean) * (val - mean);
  }
  double std_dev = std::sqrt(sq_sum / static_cast<double>(window));
  for (double &val : window_segment) {
    val = (val - mean) / std_dev;
  }
}

void discretise(std::vector<double> &window_segment, std::vector<char> &word,
                const int window, const int w, const int alpha) {
  process_window(window_segment, window, w,
    [&](double avg, int idx) {
      word[idx] = static_cast<char>(std::upper_bound(
                      breakpoints[alpha].begin(), breakpoints[alpha].end(), avg
                  ) - breakpoints[alpha].begin()) + 'a';
    }
  );
}

void paa_window(std::vector<double> &window_segment,
                std::vector<double> &result_window, const int window,
                const int w) {
  process_window(window_segment, window, w,
    [&](double avg, int idx) {
      result_window[idx] = avg;
    }
  );
}

void process_window(
    const std::vector<double> &window_segment,
    int window, int w,
    const std::function<void(double, int)> &on_symbol_complete) {

  double sum = 0.0;
  int a = 0, b = 0;
  int window_index = 0;
  int symbol_index = 0;

  for (int j = 0; j < window * w; ++j) {
    sum += window_segment[window_index];
  
    // Count each value in window_segment w times
    a = (a + 1) % w;
    if (a == 0) {
      window_index += 1;
    }
    
    // In total, there are window * w additions, which should result in w
    // symbols; each symbol consists of window values
    b = (b + 1) % window;
    if (b == 0) {
      double avg = sum / window;

      // Handle values close to zero
      if (std::abs(avg) < EPSILON) {
        avg = 0.0;
      }

      // Write to this symbol index location and increment
      on_symbol_complete(avg, symbol_index++);
      sum = 0;
    }
  }
}
