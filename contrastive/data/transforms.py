#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  This software and supporting documentation are distributed by
#      Institut Federatif de Recherche 49
#      CEA/NeuroSpin, Batiment 145,
#      91191 Gif-sur-Yvette cedex
#      France
#
# This software is governed by the CeCILL license version 2 under
# French law and abiding by the rules of distribution of free software.
# You can  use, modify and/or redistribute the software under the
# terms of the CeCILL license version 2 as circulated by CEA, CNRS
# and INRIA at the following URL "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license version 2 and that you accept its terms.
"""
Transforms used in dataset
"""

import torchvision.transforms as transforms
import numpy as np

from contrastive.augmentations import *


def transform_nothing_done():
    return \
        transforms.Compose([
            SimplifyTensor(),
            EndTensor()
        ])


def transform_only_padding(input_size, config):
    if config.backbone_name != 'pointnet':
        return \
            transforms.Compose([
                SimplifyTensor(),
                PaddingTensor(shape=input_size,
                              fill_value=config.fill_value),
                BinarizeTensor(),
                EndTensor()
            ])
    else:
        return \
            transforms.Compose([
                SimplifyTensor(),
                PaddingTensor(shape=input_size,
                              fill_value=config.fill_value),
                BinarizeTensor(),
                EndTensor(),
                ToPointnetTensor(n_max=config.n_max)
            ])


def transform_foldlabel(sample_foldlabel, percentage, input_size, config):
    transforms_list = [SimplifyTensor(),
                       PaddingTensor(shape=input_size,
                                     fill_value=config.fill_value),
                       RemoveRandomBranchTensor(
                            sample_foldlabel=sample_foldlabel,
                            percentage=percentage,
                            variable_percentage=config.variable_percentage,
                            input_size=input_size,
                            keep_extremity=config.keep_extremity),
                       BinarizeTensor(),
                       TranslateTensor(config.max_translation)]
    
    if config.backbone_name == 'pointnet':
        transforms_list.append(ToPointnetTensor(n_max=config.n_max))
    if config.sigma_noise > 0:
        transforms_list.append(GaussianNoiseTensor(sigma=config.sigma_noise))
    
    return transforms.Compose(transforms_list)


# OBSOLETE
def transform_no_foldlabel(from_skeleton, input_size, config):
    transforms_list = [SimplifyTensor(),
                       PaddingTensor(shape=input_size,
                                     fill_value=config.fill_value),
                       PartialCutOutTensor_Roll(from_skeleton=from_skeleton,
                                                input_size=input_size,
                                                keep_extremity=config.keep_extremity,
                                                patch_size=config.patch_size),
                       BinarizeTensor(),
                       TranslateTensor(config.max_translation)]
    if config.backbone_name == 'pointnet':
        transforms_list.append(ToPointnetTensor(n_max=config.n_max))
    if config.sigma_noise > 0:
        transforms_list.append(GaussianNoiseTensor(sigma=config.sigma_noise))
    
    return transforms.Compose(transforms_list)


def transform_cutout(input_size, config):
    transforms_list = [SimplifyTensor(),
                       PaddingTensor(shape=input_size,
                                     fill_value=config.fill_value),
                       PartialCutOutTensor_Roll(from_skeleton=True,
                                                input_size=input_size,
                                                keep_extremity=config.keep_extremity,
                                                patch_size=config.patch_size),
                       BinarizeTensor(),
                       TranslateTensor(config.max_translation)]
    if config.backbone_name == 'pointnet':
        transforms_list.append(ToPointnetTensor(n_max=config.n_max))
    if config.sigma_noise > 0:
        transforms_list.append(GaussianNoiseTensor(sigma=config.sigma_noise))
    
    return transforms.Compose(transforms_list)


def transform_cutin(input_size, config):
    transforms_list = [SimplifyTensor(),
                       PaddingTensor(shape=input_size,
                                     fill_value=config.fill_value),
                       PartialCutOutTensor_Roll(from_skeleton=False,
                                                input_size=input_size,
                                                keep_extremity=config.keep_extremity,
                                                patch_size=config.patch_size),
                       BinarizeTensor(),
                       TranslateTensor(config.max_translation)]
    if config.backbone_name == 'pointnet':
        transforms_list.append(ToPointnetTensor(n_max=config.n_max))
    if config.sigma_noise > 0:
        transforms_list.append(GaussianNoiseTensor(sigma=config.sigma_noise))
    
    return transforms.Compose(transforms_list)


def transform_trimdepth(sample_distbottom, sample_foldlabel,
                        input_size, config):
    transforms_list = [SimplifyTensor(),
                       PaddingTensor(shape=input_size,
                                     fill_value=config.fill_value),
                       TrimDepthTensor(sample_distbottom=sample_distbottom,
                                       sample_foldlabel=sample_foldlabel,
                                       max_distance=config.max_distance,
                                       input_size=input_size,
                                       keep_extremity=config.keep_extremity,
                                       uniform=config.uniform_trim,
                                       binary=config.binary_trim),
                       BinarizeTensor(),
                       TranslateTensor(config.max_translation)]
    if config.backbone_name == 'pointnet':
        transforms_list.append(ToPointnetTensor(n_max=config.n_max))
    if config.sigma_noise > 0:
        transforms_list.append(GaussianNoiseTensor(sigma=config.sigma_noise))
    
    return transforms.Compose(transforms_list)


def transform_translation(input_size, config):
    transforms_list = [SimplifyTensor(),
                       PaddingTensor(shape=input_size,
                                     fill_value=config.fill_value),
                       BinarizeTensor(),
                       TranslateTensor(config.max_translation)]
    if config.backbone_name == 'pointnet':
        transforms_list.append(ToPointnetTensor(n_max=config.n_max))
    if config.sigma_noise > 0:
        transforms_list.append(GaussianNoiseTensor(sigma=config.sigma_noise))
    
    return transforms.Compose(transforms_list)


def transform_random(sample_foldlabel, percentage,
                     sample_distbottom, input_size, config):
    np.random.seed()
    alpha = np.random.uniform()
    if alpha < config.distribution[0]:
        return transform_foldlabel(sample_foldlabel, percentage,
                                   input_size, config)
    elif alpha < config.distribution[1]:
        return transform_trimdepth(sample_distbottom,
                                   sample_foldlabel,
                                   input_size, config)
    elif alpha < config.distribution[2]:
        return transform_cutout(input_size, config)
    elif alpha < config.distribution[3]:
        return transform_cutin(input_size, config)
    else:
        return transform_translation(input_size, config)
    

def transform_mixed(sample_foldlabel, percentage,
                    sample_distbottom, input_size, config):
    transforms_list = [SimplifyTensor(),
                       PaddingTensor(shape=input_size,
                                     fill_value=config.fill_value)]
    if 'foldlabel' in config.mixed_list:
        transforms_list.append(RemoveRandomBranchTensor(
                            sample_foldlabel=sample_foldlabel,
                            percentage=percentage,
                            variable_percentage=config.variable_percentage,
                            input_size=input_size,
                            keep_extremity=config.keep_extremity))
    if 'cutout' in config.mixed_list:
        transforms_list.append(PartialCutOutTensor_Roll(
                                from_skeleton=True,
                                input_size=input_size,
                                keep_extremity=config.keep_extremity,
                                patch_size=config.patch_size))
    # BEWARE: the bottom kept using foldlabel and cutout are not protected
    # by trimdepth. Add keep_extremity to trimdepth config to preserve.
    # Likewise, keep top is the same argument for each augmentation.
    # for now, stick to foldlabel + cutout.
    if 'trimdepth' in config.mixed_list:
        transforms_list.append(TrimDepthTensor(
                                sample_distbottom=sample_distbottom,
                                sample_foldlabel=sample_foldlabel,
                                max_distance=config.max_distance,
                                input_size=input_size,
                                keep_extremity=config.keep_extremity,
                                uniform=config.uniform_trim,
                                binary=config.binary_trim))
    transforms_list.append(BinarizeTensor())
    transforms_list.append(TranslateTensor(config.max_translation))
    if config.backbone_name == 'pointnet':
        transforms_list.append(ToPointnetTensor(n_max=config.n_max))
    if config.sigma_noise > 0:
        transforms_list.append(GaussianNoiseTensor(sigma=config.sigma_noise))
    
    return transforms.Compose(transforms_list)


# DEPRECATED
def transform_both(sample_foldlabel, percentage, from_skeleton,
                   input_size, config):
    if config.backbone_name != 'pointnet':
        return \
            transforms.Compose([
                SimplifyTensor(),
                PaddingTensor(shape=input_size,
                              fill_value=config.fill_value),
                RemoveRandomBranchTensor(
                    sample_foldlabel=sample_foldlabel,
                    percentage=percentage,
                    variable_percentage=config.variable_percentage,
                    input_size=input_size,
                    keep_bottom=config.keep_bottom),
                PartialCutOutTensor_Roll(from_skeleton=from_skeleton,
                                         input_size=input_size,
                                         keep_bottom=config.keep_bottom,
                                         patch_size=config.patch_size),
                BinarizeTensor(),
                RotateTensor(max_angle=config.max_angle)
            ])
    else:
        return \
            transforms.Compose([
                SimplifyTensor(),
                PaddingTensor(shape=input_size,
                              fill_value=config.fill_value),
                RemoveRandomBranchTensor(
                    sample_foldlabel=sample_foldlabel,
                    percentage=percentage,
                    variable_percentage=config.variable_percentage,
                    input_size=input_size,
                    keep_bottom=config.keep_bottom),
                PartialCutOutTensor_Roll(from_skeleton=from_skeleton,
                                         input_size=input_size,
                                         keep_bottom=config.keep_bottom,
                                         patch_size=config.patch_size),
                RotateTensor(max_angle=config.max_angle),
                BinarizeTensor(),
                ToPointnetTensor(n_max=config.n_max)
            ])


def transform_foldlabel_resize(sample_foldlabel, percentage,
                               resize_ratio, input_size, config):
    if config.backbone_name != 'pointnet':
        return \
            transforms.Compose([
                SimplifyTensor(),
                RemoveRandomBranchTensor(
                    sample_foldlabel=sample_foldlabel,
                    percentage=percentage,
                    variable_percentage=config.variable_percentage,
                    input_size=input_size,
                    keep_bottom=config.keep_bottom),
                BinarizeTensor(),
                ResizeTensor(resize_ratio),
                RotateTensor(max_angle=config.max_angle)
            ])
    else:
        return \
            transforms.Compose([
                SimplifyTensor(),
                RemoveRandomBranchTensor(
                    sample_foldlabel=sample_foldlabel,
                    percentage=percentage,
                    variable_percentage=config.variable_percentage,
                    input_size=input_size,
                    keep_bottom=config.keep_bottom),
                RotateTensor(max_angle=config.max_angle),
                BinarizeTensor(),
                ResizeTensor(resize_ratio),
                ToPointnetTensor(n_max=config.n_max)
            ])
