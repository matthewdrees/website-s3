"""Code that helps generate postings. Broken out from SConstruct to be testable."""

from pathlib import Path


def getPostImageDimensions(
    source_image_dimensions,
    post_dimensions_portrait_height,
    post_dimensions_landscape_height,
):
    """Get 'WxH' dimesions for post image based on source_image_dimensions.

    If source_image_dimension width >= height, photo is landscape, otherwise portrait. Cap image
    height appropriately while keeping aspect ratio. Most images are 4x3 aspect ratio but some
    panoramics work their way in there.

    :param image_dimensions: source 'WxH' image dimensions as a string
    :param post_dimension_portrait_height: If portrait, cap height to this dimension.
    :param post_dimension_landscape_height: If landscape, cap height to this dimension.
    :return: 'WxH' dimensions for post image (e.g. "1024x768")
    :rtype: str

    Doctests:
    >>> getPostImageDimensions('120x90', 240, 180)
    '120x90'
    >>> getPostImageDimensions('90x120', 240, 180)
    '90x120'
    >>> getPostImageDimensions('240x180', 240, 180)
    '240x180'
    >>> getPostImageDimensions('180x240', 240, 180)
    '180x240'
    >>> getPostImageDimensions('4032x3024', 240, 180)
    '240x180'
    >>> getPostImageDimensions('3024x4032', 240, 180)
    '180x240'
    >>> getPostImageDimensions('4032x3024', 1024, 768)
    '1024x768'
    >>> getPostImageDimensions('3024x4032', 1024, 768)
    '768x1024'
    >>> getPostImageDimensions('4032x3024', 1600, 1200)
    '1600x1200'
    >>> getPostImageDimensions('3024x4032', 1600, 1200)
    '1200x1600'
    >>> getPostImageDimensions('13336x3868', 240, 180)
    '620x180'
    >>> getPostImageDimensions('13336x3868', 1024, 768)
    '2647x768'
    >>> getPostImageDimensions('13336x3868', 1600, 1200)
    '4137x1200'
    """
    dimensions = [int(s) for s in source_image_dimensions.split("x")]
    assert len(dimensions) == 2
    width, height = dimensions

    def cap_dimensions_by_height(width, height, y_cap):
        if height <= y_cap:
            return str(width) + "x" + str(height)
        return str(width * y_cap // height) + "x" + str(y_cap)

    if width >= height:
        return cap_dimensions_by_height(width, height, post_dimensions_landscape_height)
    return cap_dimensions_by_height(width, height, post_dimensions_portrait_height)


def getImageCaptionFromFilename(source_filename):
    """Get image caption string from filename.

    :param filename: filename of source image, with or without path
    :return: caption string

    >>> getImageCaptionFromFilename('01 i am a filename.jpg')
    'i am a filename'
    >>> getImageCaptionFromFilename('path/to/01 i am a filename.jpg')
    'i am a filename'
    >>> getImageCaptionFromFilename('99.jpg')
    ''
    >>> getImageCaptionFromFilename('02-not-really-valid-but-deal-with-it.jpg')
    'not-really-valid-but-deal-with-it'
    """
    p = Path(source_filename)
    caption = p.stem
    for i in range(len(caption)):
        if caption[i].isalpha():
            return caption[i:]
    return ""


if __name__ == "__main__":
    import doctest

    doctest.testmod()
