from typing import Any

import cv2
import numpy as np


def find_image(base_image: Any, reference_image_path: str, tolerance: float) -> list[tuple[int, int]]:
    """
    Find all instances of a reference image within a base screenshot.

    Args:
        base_image: PIL Image or numpy array of the screenshot
        reference_image_path: Path to the reference image file
        tolerance: Matching threshold (0.0 to 1.0, higher is stricter)

    Returns:
        List of (x, y) coordinates where matches are found
    """
    base_array = np.array(base_image)
    base_bgr = cv2.cvtColor(base_array, cv2.COLOR_RGB2BGR)

    reference = cv2.imread(reference_image_path)
    if reference is None:
        return []

    result = cv2.matchTemplate(base_bgr, reference, cv2.TM_CCOEFF_NORMED)

    locations = np.where(result >= tolerance)

    matches = []
    ref_h, ref_w = reference.shape[:2]

    for pt in zip(*locations[::-1]):
        center_x = pt[0] + ref_w // 2
        center_y = pt[1] + ref_h // 2
        matches.append((center_x, center_y))

    if not matches:
        return []

    filtered_matches = []
    matches.sort()

    for match in matches:
        if not filtered_matches:
            filtered_matches.append(match)
        else:
            is_duplicate = False
            for existing in filtered_matches:
                distance = ((match[0] - existing[0])**2 + (match[1] - existing[1])**2)**0.5
                if distance < min(ref_w, ref_h) * 0.5:
                    is_duplicate = True
                    break
            if not is_duplicate:
                filtered_matches.append(match)

    return filtered_matches