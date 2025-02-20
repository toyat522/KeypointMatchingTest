from abc import ABC, abstractmethod

class MatcherBase(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        pass

    @abstractmethod
    def load_image(self, img_path, resize):
        pass

    @abstractmethod
    def execute(self, img0, img1):
        pass

    @abstractmethod
    def plot(self, img0, img1, m_kpts0, m_kpts1, kpts0, kpts1):
        pass

    @abstractmethod
    def get_matcher_model(self):
        pass

    @abstractmethod
    def get_descriptor_model(self):
        pass

    @abstractmethod
    def get_extraction_time(self):
        pass

    @abstractmethod
    def get_matching_time(self):
        pass

