from ..common.matcher_base import MatcherBase
from ..common.viz2d import plot_images, plot_matches, plot_keypoints
from .matching import Matching
from .utils import read_image

import matplotlib.pyplot as plt
import torch

class SuperGlueMatcher(MatcherBase):
    def load_image(self, img_path, resize, device):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        _, img, _ = read_image(img_path, device, resize, rotation=0, resize_float=False)
        return img.squeeze()

    def execute(self, img0, img1, max_num_keypoints, device=None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"

        config = {
            "superpoint": {
                "nms_radius": 4,
                "keypoint_threshold": 0.005,
                "max_keypoints": max_num_keypoints 
            },
            "superglue": {
                "weights": "indoor",
                "sinkhorn_iterations": 20,
                "match_threshold": 0.2,
            }
        }
        matching = Matching(config).eval().to(device)

        # Perform the matching
        img0 = img0.unsqueeze(0).unsqueeze(0)
        img1 = img1.unsqueeze(0).unsqueeze(0)
        pred = matching({"image0": img0, "image1": img1})
        pred = {k: v[0].cpu().numpy() for k, v in pred.items()}
        kpts0, kpts1 = pred["keypoints0"], pred["keypoints1"]
        matches, _ = pred["matches0"], pred["matching_scores0"]

        # Keep the matching keypoints
        valid = matches > -1
        m_kpts0 = kpts0[valid]
        m_kpts1 = kpts1[matches[valid]]

        return kpts0, kpts1, m_kpts0, m_kpts1

    def plot(self, img0, img1, m_kpts0, m_kpts1, kpts0, kpts1):
        plot_images([img0, img1])
        plot_matches(m_kpts0, m_kpts1, color="lime", lw=0.2)
        plot_keypoints([kpts0, kpts1], colors=["blue", "blue"], ps=10)
        plt.show()

