import numpy as np
from scipy.ndimage import affine_transform


def random_flip_rotation_translation(shape, max_translation=10, max_rotation=10):
    """Create random affine transform matrix for 3D volume."""
    # Random flips (diagonal -1s)
    flip = np.diag([np.random.choice([-1, 1]) for _ in range(3)])

    # Random small rotations (in degrees → radians)
    angles = np.deg2rad(np.random.uniform(-max_rotation, max_rotation, size=3))
    cx, cy, cz = np.cos(angles)
    sx, sy, sz = np.sin(angles)

    # Rotation matrices
    Rx = np.array([[1, 0, 0],
                   [0, cx, -sx],
                   [0, sx, cx]])
    Ry = np.array([[cy, 0, sy],
                   [0, 1, 0],
                   [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0],
                   [sz, cz, 0],
                   [0, 0, 1]])
    rotation = Rz @ Ry @ Rx

    # Combine flip and rotation
    transform_matrix = flip @ rotation

    # Center of the volume
    center = np.array(shape) / 2

    # Random translation
    translation = np.random.uniform(-max_translation, max_translation, size=3)

    # Offset to apply rotation around center
    offset = center - transform_matrix @ center + translation

    return transform_matrix, offset


def augment_sample(ct, masks, dose, beamlet_dose=None):
    """Apply the same 3D affine augmentation to all spatial arrays."""
    assert ct.shape == masks.shape == dose.shape, "All inputs must have the same shape"

    transform_matrix, offset = random_flip_rotation_translation(ct.shape)

    # Augment CT (interpolation order 1 for smooth intensity)
    ct_aug = affine_transform(ct, transform_matrix, offset=offset, order=1, mode='nearest')

    # Augment masks (order 0 to preserve binary)
    masks_aug = affine_transform(masks, transform_matrix, offset=offset, order=0, mode='nearest')

    # Augment dose (continuous value)
    dose_aug = affine_transform(dose, transform_matrix, offset=offset, order=1, mode='nearest')

    # Augment beamlet dose if provided
    beamlet_aug = None
    if beamlet_dose is not None:
        beamlet_aug = affine_transform(beamlet_dose, transform_matrix, offset=offset, order=1, mode='nearest')

    return ct_aug, masks_aug, dose_aug, beamlet_aug