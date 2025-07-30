"""A list of transforms."""

from .transform import Transform
from .transform_velocity import velocity_transform

TRANSFORMS = {
    str(Transform.NONE): lambda x: x,
    str(Transform.VELOCITY): velocity_transform,
}
