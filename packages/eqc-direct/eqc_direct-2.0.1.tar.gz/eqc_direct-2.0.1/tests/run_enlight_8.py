import sys
import time
from multiprocessing import Pool
from eqc_direct.eqc_client import EqcClient
import numpy as np


def run_single():
    np.random.seed(13)
    ham_mat = np.load("enlight8_alpha1.0.npy")
    print(ham_mat)
    print(ham_mat.shape)
    start = time.time()
    eqc_client = EqcClient()
    lock_id, start_ts, end_ts = eqc_client.wait_for_lock()
    print("Lock:", lock_id)
    resp = eqc_client.process_job(
        hamiltonian=ham_mat,
        relaxation_schedule=2,
        sum_constraint=30,
        continuous_soln=False,
        lock_id=lock_id,
    )
    eqc_client.release_lock(lock_id=lock_id)
    print(resp)


if __name__ == "__main__":
    run_single()
