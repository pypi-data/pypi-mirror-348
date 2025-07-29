"""""" # start delvewheel patch
def _delvewheel_patch_1_10_1():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pantab.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

__version__ = "5.2.2"


from pantab._reader import frame_from_hyper, frame_from_hyper_query, frames_from_hyper
from pantab._writer import frame_to_hyper, frames_to_hyper

__all__ = [
    "__version__",
    "frame_from_hyper",
    "frame_from_hyper_query",
    "frames_from_hyper",
    "frame_to_hyper",
    "frames_to_hyper",
]
