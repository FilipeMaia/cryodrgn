import os.path
import argparse
import numpy as np
import torch
import pytest
from cryodrgn.source import ImageSource
from cryodrgn.commands_utils import filter_mrcs
from cryodrgn.utils import save_pkl, load_pkl

DATA_FOLDER = os.path.join(os.path.dirname(__file__), "..", "testing", "data")


@pytest.fixture
def mrcs_data():
    return ImageSource.from_file(f"{DATA_FOLDER}/toy_projections.mrc").images()


def test_filter_mrcs(mrcs_data):

    # Generate 15 random indices into the input mrcs
    indices = np.random.randint(0, mrcs_data.shape[0], size=15)
    save_pkl(indices, "output/random_indices.pkl")

    args = filter_mrcs.add_args(argparse.ArgumentParser()).parse_args(
        [
            f"{DATA_FOLDER}/toy_projections.mrc",
            "--ind",
            "output/random_indices.pkl",
            "-o",
            "output/toy_projections_filtered.mrc",
        ]
    )
    filter_mrcs.main(args)

    new_data = ImageSource.from_mrcs("output/toy_projections_filtered.mrc").images()
    assert torch.allclose(new_data[:], mrcs_data[indices])