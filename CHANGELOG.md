# Changelog

## 0.4

### New and improved

- **Support for scripts** is here, starting with **X/Y plot**. Note that this is disabled by default (see readme).
- Inpainting mask is now applied to new layers.
- **Shared settings** between different commands via a preferences dialog. Currently only used for the API URL.
- Major refactoring (moved to a command pattern), which makes it easier to add functionality in future. Commands (== GIMP plugins) are dynamically located in the source tree and registered.

### Bugs fixed

- Autofitting the inpainting mask region didn't work properly if the mask layer wasn't active.

## v0.3.3

### New and improved

- Improved timeout handling

## v0.3.2

### New and improved

- Updated available samplers
- Progress bar updates while request is running and timeouts are handled
- Renamed "Extras" to "Upscale"

## v0.3.1

### New and improved

- Internal refactoring

## v0.3 (2022-12-06)

### New and improved

- Inpainting automatically determines area to process based on mask position
- Ability to choose upscaler settings

## v0.2 (2022-12-04)

### New and improved

- Support for rectangular selections, allowing you to partially process images

### Bugs fixed

- Windows startup issue ([#3](https://github.com/tgiesselmann/gimp-stable-boy/pull/3))

## v0.1 (2022-12-02)

### New and improved

- Text to image
- Image to image
- Inpainting
- Simple upscaling
- All operations work on full images only
