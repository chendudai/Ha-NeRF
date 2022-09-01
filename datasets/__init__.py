
from .blender_mask_grid_sample import BlenderDataset
from .phototourism_mask_grid_sample import PhototourismDataset
from .phototourism_mask_grid_sample import WikiScenesDataset

dataset_dict = {'blender': BlenderDataset,
                'phototourism': PhototourismDataset,
                'wikiscenes': WikiScenesDataset}