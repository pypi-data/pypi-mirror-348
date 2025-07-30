import sys
import time
import numpy as np
from eqc_direct.client import EqcClient
from eqc_direct.utils import convert_hamiltonian_to_poly_format


def run_single():
    ham_mat = np.round(
        np.loadtxt("tam_200_example_2.csv", delimiter=",", dtype=np.float32)
    )
    poly_idx, poly_coef = convert_hamiltonian_to_poly_format(
        linear_terms=ham_mat[:, 0], quadratic_terms=ham_mat[:, 1:]
    )
    print(ham_mat.shape)
    start = time.time()
    eqc_client = EqcClient()
    lock_id, start_ts, end_ts = eqc_client.wait_for_lock()
    print("Lock:", lock_id)
    resp = eqc_client.process_job(
        poly_coefficients=poly_coefs,
        poly_indices=poly_idx,
        sum_constraint=100,
        relaxation_schedule=2,
        solution_precision=1,
    )

    eqc_client.release_lock(lock_id=lock_id)
    print(resp)
    print("Execution time:", time.time() - start)


if __name__ == "__main__":
    run_single()
