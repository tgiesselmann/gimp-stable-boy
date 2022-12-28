#!/usr/bin/env python
#
# Stable Boy
# Copyright (C) 2022 Torben Giesselmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
import gimpfu
from urlparse import urljoin
import gimp_stable_boy as sb
from gimp_stable_boy.config import PREFERENCES_SHELF_GROUP as PREFS
from .._command import PluginCommand, StableDiffusionCommand
from ..text_to_image import Txt2ImgCommand
from ..image_to_image import Img2ImgCommand
from ..inpainting import InpaintingCommand


class XyPlotCommand(StableDiffusionCommand):
    uri = ''
    metadata = StableDiffusionCommand.CommandMetadata(
        sb.__prefix__ + "-xyplot",
        sb.__name__ + " " + sb.__version__ + " - X/Y plot",
        sb.__description__,
        sb.__author__,
        sb.__author__ + " (c) " + sb.__year__,
        sb.__year__,
        sb.__menu__ + "/XY plot",
        "*",
        [
            (gimpfu.PF_OPTION, 'mode', 'Mode', 0, sb.config.MODES),
            (gimpfu.PF_OPTION, 'x_type', 'X', 0, sb.config.SCRIPT_XY_PLOT_AXIS_OPTIONS),
            (gimpfu.PF_STRING, 'x_values', 'X values', ''),
            (gimpfu.PF_OPTION, 'y_type', 'Y', 0, sb.config.SCRIPT_XY_PLOT_AXIS_OPTIONS),
            (gimpfu.PF_STRING, 'y_values', 'Y values', ''),
            (gimpfu.PF_BOOL, 'draw_legend', 'Draw legend', True),
            (gimpfu.PF_BOOL, 'no_fixed_seeds', 'No fixed seeds', False),
            (gimpfu.PF_BOOL, 'grid_only', 'Grid only', True),
        ],
        [],)
    mode_cmds = {'Text to Image': Txt2ImgCommand,
                 'Image to Image': Img2ImgCommand,
                 'Inpainting': InpaintingCommand,}

    def __init__(self, **kwargs):
        self.mode = sb.config.MODES[kwargs['mode']]
        # Update kwargs with values from mode's previously saved prefs
        _mode_meta = self.mode_cmds[self.mode].metadata
        prefs_keys = [param[1] for param in _mode_meta.params if param[1] not in ['image', 'drawable']]
        for prefs_key in prefs_keys:
            kwargs[prefs_key] = sb.gimp.pref_value(_mode_meta.proc_name, prefs_key)

        self.autofit_inpainting = kwargs.get('autofit_inpainting', False)
        self.apply_inpainting_mask = kwargs.get('apply_inpainting_mask', False)
        StableDiffusionCommand.__init__(self, **kwargs)
        self.uri = 'sdapi/v1/txt2img/script' if self.mode == 'Text to Image' else 'sdapi/v1/img2img/script'
        self.url = urljoin(sb.gimp.pref_value(PREFS, 'api_base_url', sb.config.DEFAULT_API_URL), self.uri)

    def _determine_active_area(self):
        if self.autofit_inpainting:
            return sb.gimp.autofit_inpainting_area(self.img)
        else:
            return StableDiffusionCommand._determine_active_area(self)

    def _make_request_data(self, **kwargs):
        req_data = StableDiffusionCommand._make_request_data(self, **kwargs)
        req_data['script_name'] = 'X/Y plot'
        req_data['script_args'] = [
            kwargs['x_type'], kwargs['x_values'],
            kwargs['y_type'], kwargs['y_values'],
            kwargs['draw_legend'],
            not kwargs['grid_only'], kwargs['no_fixed_seeds']
        ]
        if self.mode in ['Image to Image', 'Inpainting']:
            req_data['denoising_strength'] = float(kwargs['denoising_strength']) / 100
            req_data['init_images'] = [sb.gimp.encode_img(self.img, self.x, self.y, self.width, self.height)]
            if self.mode == 'Inpainting':
                req_data['inpainting_mask_invert'] = 1
                req_data['inpainting_fill'] = kwargs['inpainting_fill']
                req_data['mask_blur'] = kwargs['mask_blur']
                req_data['inpaint_full_res'] = kwargs['inpaint_full_res']
                req_data['inpaint_full_res_padding'] = kwargs['inpaint_full_res_padding']
                req_data['mask'] = sb.gimp.encode_mask(self.img, self.x, self.y, self.width, self.height)
        return req_data

    def _process_response(self, resp):
        all_imgs = resp['images']
        self.images = [all_imgs.pop(0)]  # grid is always a separate image
        if self.req_data['script_args'][5] is False:  # grid only?
            return
        # Create layer structure with layer names based on X/Y values
        x_label = sb.config.SCRIPT_XY_PLOT_AXIS_OPTIONS[self.req_data['script_args'][0]]
        y_label = sb.config.SCRIPT_XY_PLOT_AXIS_OPTIONS[self.req_data['script_args'][2]]
        LayerResult = PluginCommand.LayerResult
        parent_layer_group = LayerResult("X/Y plot: " + x_label + " / " + y_label, None, [])
        for x in re.split(r'\s*,\s*', self.req_data['script_args'][1]):
            x_layer_group = LayerResult(x_label + ': ' + str(x), None, [])
            parent_layer_group.children.append(x_layer_group)
            for y in re.split(r'\s*,\s*', self.req_data['script_args'][3]):
                x_layer_group.children.append(
                    LayerResult(
                        x_label
                        + ': ' + str(x) + ' / ' + y_label + ': '
                        + str(y), all_imgs.pop(0), None))
        self.layers = [parent_layer_group]

    def _estimate_timeout(self, req_data):
        return 300
