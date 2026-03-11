#!/usr/bin/env python3

import logging
import sys
import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)


def parse_args():
    """
    Parse command line arguments.
    """
    try:
        num_points = int(sys.argv[1])
        output_file = sys.argv[2]
    except ValueError:
        logging.error("Error: Number of points must be an integer")
        sys.exit(1)
    except IndexError:
        logging.error("Error: Number of points and output file must be provided")
        sys.exit(1)

    return num_points, output_file


def calculate_pi(num_points):
    """
    Calculate pi using the Monte Carlo method with NumPy (vectorized).
    """
    master = np.random.default_rng()
    seed = int(master.integers(0, 2**32))
    rng = np.random.default_rng(seed)
    logging.info("Calculating pi using %d points (NumPy)", num_points)
    x = rng.random(num_points)
    y = rng.random(num_points)
    num_inside = np.sum(x**2 + y**2 <= 1)
    return 4.0 * num_inside / num_points


def save_result(pi, num_points, output_file):
    """
    Save the result to a CSV file.
    """
    df = pd.DataFrame({"pi": [pi], "num_points": [num_points]})
    df.to_csv(output_file, index=False)


def main():
    """
    Main function.
    """
    num_points, output_file = parse_args()
    pi = calculate_pi(num_points)
    save_result(pi, num_points, output_file)
    logging.info("Pi: %s", pi)
    logging.info("Saved result to %s", output_file)


if __name__ == "__main__":
    main()
