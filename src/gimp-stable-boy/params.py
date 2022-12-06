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

import gimpfu


IMAGE_TARGETS = ['Layers', 'Images']

SAMPLERS = [
    'Euler a', 'Euler', 'LMS', 'Heun', 'DPM2', 'DPM2 a', 'DPM++ 2S a', 'DPM++ 2M', 'DPM fast', 'DPM adaptive',
    'LMS Karras', 'DPM2 Karras', 'DPM2 a Karras', 'DPM++ 2S a Karras', 'DPM++ 2M Karras', 'DDIM', 'PLMS'
]

INPAINTING_FILL = ['Fill', 'Original', 'Latent noise', 'Latent nothing']

UPSCALERS = ['None', 'Lanczos', 'Nearest', 'LDSR', 'ESRGAN_4x', 'SwinIR_4x', 'ScuNET', 'ScuNET PSNR']

GIMP_PARAMS = {
    'TXT2IMG': [
        (gimpfu.PF_STRING, "prompt", "Prompt", ""),
        (gimpfu.PF_STRING, "negative_prompt", "Negative prompt", ""),
        (gimpfu.PF_STRING, "seed", "Seed", "-1"),
        (gimpfu.PF_SLIDER, "steps", "Steps", 25, (10, 150, 25)),
        (gimpfu.PF_OPTION, "sampler_index", "Sampler", 0, SAMPLERS),
        (gimpfu.PF_BOOL, "restore_faces", "Restore faces", False),
        (gimpfu.PF_SLIDER, "cfg_scale", "CFG", 7.5, (0, 20, 0.5)),
        (gimpfu.PF_SLIDER, "num_images", "Number of images", 1, (1, 4, 1)),
        (gimpfu.PF_OPTION, "img_target", "Results as", 0, IMAGE_TARGETS),
        (gimpfu.PF_STRING, "api_base_url", "API URL", "http://localhost:7860"),
    ],
    'IMG2IMG': [
        (gimpfu.PF_STRING, "prompt", "Prompt", ""),
        (gimpfu.PF_STRING, "negative_prompt", "Negative prompt", ""),
        (gimpfu.PF_STRING, "seed", "Seed", "-1"),
        (gimpfu.PF_SLIDER, "steps", "Steps", 25, (10, 150, 25)),
        (gimpfu.PF_OPTION, "sampler_index", "Sampler", 0, SAMPLERS),
        (gimpfu.PF_BOOL, "restore_faces", "Restore faces", False),
        (gimpfu.PF_SLIDER, "cfg_scale", "CFG", 7.5, (0, 20, 0.5)),
        (gimpfu.PF_SLIDER, "denoising_strength", "Denoising strength %", 50.0, (0, 100, 1)),
        (gimpfu.PF_SLIDER, "num_images", "Number of images", 1, (1, 4, 1)),
        (gimpfu.PF_OPTION, "img_target", "Results as", 0, IMAGE_TARGETS),
        (gimpfu.PF_STRING, "api_base_url", "API URL", "http://localhost:7860"),
    ],
    'INPAINTING': [
        (gimpfu.PF_STRING, "prompt", "Prompt", ""),
        (gimpfu.PF_STRING, "negative_prompt", "Negative prompt", ""),
        (gimpfu.PF_STRING, "seed", "Seed", "-1"),
        (gimpfu.PF_SLIDER, "steps", "Steps", 25, (10, 150, 25)),
        (gimpfu.PF_OPTION, "sampler_index", "Sampler", 0, SAMPLERS),
        (gimpfu.PF_BOOL, "restore_faces", "Restore faces", False),
        (gimpfu.PF_SLIDER, "cfg_scale", "CFG", 7.5, (0, 20, 0.5)),
        (gimpfu.PF_SLIDER, "denoising_strength", "Denoising strength %", 50.0, (0, 100, 1)),
        (gimpfu.PF_SLIDER, "mask_blur", "Mask blur", 4, (0, 32, 1)),
        (gimpfu.PF_OPTION, "inpainting_fill", "Inpainting fill", 1, INPAINTING_FILL),
        (gimpfu.PF_BOOL, "inpaint_full_res", "Inpaint at full resolution", True),
        (gimpfu.PF_INT, "inpaint_full_res_padding", "Full res. inpainting padding", 0),
        (gimpfu.PF_SLIDER, "num_images", "Number of images", 1, (1, 4, 1)),
        (gimpfu.PF_OPTION, "img_target", "Results as", 0, IMAGE_TARGETS),
        (gimpfu.PF_STRING, "api_base_url", "API URL", "http://localhost:7860"),
    ],
    'EXTRAS': [
        # (gimpfu.PF_OPTION, "resize_mode", "Resize mode", 0, RESIZE_MODES),
        (gimpfu.PF_SLIDER, "upscaling_resize", "Upscaling factor", 2, (1, 4, 1)),
        (gimpfu.PF_OPTION, "upscaler_1", "Upscaler 1", 0, UPSCALERS),
        (gimpfu.PF_OPTION, "upscaler_2", "Upscaler 2", 0, UPSCALERS),
        (gimpfu.PF_SLIDER, "extras_upscaler_2_visibility", "Upscaler 2 visibility", 0, (0, 1, 0.1)),
        (gimpfu.PF_STRING, "api_base_url", "API URL", "http://localhost:7860"),
    ]
}
