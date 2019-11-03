import numpy as np
from io import BytesIO
from django import forms
from django.core.exceptions import ValidationError
from fastai.vision import pil2tensor


class CustomImageField(forms.ImageField):
    def to_python(self, data):
        """
        Check that the file-upload field data contains a valid image (GIF, JPG,
        PNG, etc. -- whatever Pillow supports).
        """
        f = super().to_python(data)
        if f is None:
            return None

        from PIL import Image
        from fastai.vision import Image as fImage
        # We need to get a file object for Pillow. We might have a path or we might
        # have to read the data into memory.
        if hasattr(data, 'temporary_file_path'):
            file = data.temporary_file_path()
        else:
            if hasattr(data, 'read'):
                file = BytesIO(data.read())
            else:
                file = BytesIO(data['content'])

        try:
            # load() could spot a truncated JPEG, but it loads the entire
            # image in memory, which is a DoS vector. See #3848 and #18520.
            image = Image.open(file).convert('RGB')
            # verify() must be called immediately after the constructor.
            image.verify()

            # Annotating so subclasses can reuse it for their own validation
            f.image = fImage(pil2tensor(image, dtype=np.float32).div_(255))
            # Pillow doesn't detect the MIME type of all formats. In those
            # cases, content_type will be None.
            f.content_type = Image.MIME.get(image.format)
        except Exception as exc:
            # Pillow doesn't recognize it as an image.
            raise ValidationError(
                self.error_messages['invalid_image'],
                code='invalid_image',
            ) from exc
        if hasattr(f, 'seek') and callable(f.seek):
            f.seek(0)
        return f


class ImageUploadForm(forms.Form):
    image = CustomImageField(
        label="What are you currently upto!!", required=True
    )

