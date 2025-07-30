import sys
import time
from multiprocessing import Pool
from eqc_direct.client import EqcClient
from eqc_direct.utils import convert_hamiltonian_to_poly_format
import numpy as np


def run_single():
    np.random.seed(13)

    ham_mat = np.loadtxt("QPLIB_0018_OBJ.csv", delimiter=",", dtype=float)
    poly_idx, poly_coef = convert_hamiltonian_to_poly_format(
        linear_terms=ham_mat[:, 0], quadratic_terms=ham_mat[:, 1:]
    )
    start = time.time()
    eqc_client = EqcClient()
    lock_id, start_ts, end_ts = eqc_client.wait_for_lock()
    print("Lock:", lock_id)
    resp = eqc_client.process_job(
        poly_indices=poly_idx,
        poly_coefficients=poly_coef,
        relaxation_schedule=1,
        sum_constraint=1,
        solution_precision=0.1,
        lock_id=lock_id,
    )
    eqc_client.release_lock(lock_id=lock_id)
    print(resp)


if __name__ == "__main__":
    run_single()
