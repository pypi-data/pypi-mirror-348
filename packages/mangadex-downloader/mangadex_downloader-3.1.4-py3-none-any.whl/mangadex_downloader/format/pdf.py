# MIT License

# Copyright (c) 2022-present Rahman Yusuf

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging
import io
import os
import time
import math

from .base import ConvertedChaptersFormat, ConvertedVolumesFormat, ConvertedSingleFormat
from .utils import get_chapter_info, get_volume_cover
from ..utils import create_directory
from ..progress_bar import progress_bar_manager as pbm

log = logging.getLogger(__name__)

try:
    from PIL import Image, ImageFile, ImageSequence, PdfParser, __version__, features
except ImportError:
    pillow_ready = False
else:
    pillow_ready = True


class PillowNotInstalled(Exception):
    """Raised when trying to download in PDF format but Pillow is not installed"""

    pass


class _PageRef:
    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs

    def __call__(self):
        return self._func(*self._args, **self._kwargs)


# Utility function for Pillow library
def _write_image(im, filename, existing_pdf, image_refs):
    # FIXME: Should replace ASCIIHexDecode with RunLengthDecode
    # (packbits) or LZWDecode (tiff/lzw compression).  Note that
    # PDF 1.2 also supports Flatedecode (zip compression).

    params = None
    decode = None

    #
    # Get image characteristics

    width, height = im.size

    dict_obj = {"BitsPerComponent": 8}
    if im.mode == "1":
        if features.check("libtiff"):
            filter = "CCITTFaxDecode"
            dict_obj["BitsPerComponent"] = 1
            params = PdfParser.PdfArray(
                [
                    PdfParser.PdfDict(
                        {
                            "K": -1,
                            "BlackIs1": True,
                            "Columns": width,
                            "Rows": height,
                        }
                    )
                ]
            )
        else:
            filter = "DCTDecode"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceGray")
        procset = "ImageB"  # grayscale
    elif im.mode == "L":
        filter = "DCTDecode"
        # params = f"<< /Predictor 15 /Columns {width-2} >>"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceGray")
        procset = "ImageB"  # grayscale
    elif im.mode == "LA":
        filter = "JPXDecode"
        # params = f"<< /Predictor 15 /Columns {width-2} >>"
        procset = "ImageB"  # grayscale
        dict_obj["SMaskInData"] = 1
    elif im.mode == "P":
        filter = "ASCIIHexDecode"
        palette = im.getpalette()
        dict_obj["ColorSpace"] = [
            PdfParser.PdfName("Indexed"),
            PdfParser.PdfName("DeviceRGB"),
            len(palette) // 3 - 1,
            PdfParser.PdfBinary(palette),
        ]
        procset = "ImageI"  # indexed color

        if "transparency" in im.info:
            smask = im.convert("LA").getchannel("A")
            smask.encoderinfo = {}

            image_ref = _write_image(smask, filename, existing_pdf, image_refs)[0]
            dict_obj["SMask"] = image_ref
    elif im.mode == "RGB":
        filter = "DCTDecode"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceRGB")
        procset = "ImageC"  # color images
    elif im.mode == "RGBA":
        filter = "JPXDecode"
        procset = "ImageC"  # color images
        dict_obj["SMaskInData"] = 1
    elif im.mode == "CMYK":
        filter = "DCTDecode"
        dict_obj["ColorSpace"] = PdfParser.PdfName("DeviceCMYK")
        procset = "ImageC"  # color images
        decode = [1, 0, 1, 0, 1, 0, 1, 0]
    else:
        msg = f"cannot save mode {im.mode}"
        raise ValueError(msg)

    #
    # image

    op = io.BytesIO()

    if filter == "ASCIIHexDecode":
        ImageFile._save(im, op, [("hex", (0, 0) + im.size, 0, im.mode)])
    elif filter == "CCITTFaxDecode":
        im.save(
            op,
            "TIFF",
            compression="group4",
            # use a single strip
            strip_size=math.ceil(width / 8) * height,
        )
    elif filter == "DCTDecode":
        Image.SAVE["JPEG"](im, op, filename)
    elif filter == "JPXDecode":
        del dict_obj["BitsPerComponent"]
        Image.SAVE["JPEG2000"](im, op, filename)
    else:
        msg = f"unsupported PDF filter ({filter})"
        raise ValueError(msg)

    stream = op.getvalue()
    if filter == "CCITTFaxDecode":
        stream = stream[8:]
        filter = PdfParser.PdfArray([PdfParser.PdfName(filter)])
    else:
        filter = PdfParser.PdfName(filter)

    image_ref = image_refs.pop(0)
    existing_pdf.write_obj(
        image_ref,
        stream=stream,
        Type=PdfParser.PdfName("XObject"),
        Subtype=PdfParser.PdfName("Image"),
        Width=width,  # * 72.0 / x_resolution,
        Height=height,  # * 72.0 / y_resolution,
        Filter=filter,
        Decode=decode,
        DecodeParms=params,
        **dict_obj,
    )

    return image_ref, procset


class PDFPlugin:
    def __init__(self, ims):
        # "Circular Imports" problem

        pbm.set_convert_total(len(ims))
        self.tqdm = pbm.get_convert_pb(recreate=not pbm.stacked)

        self.register_pdf_handler()

    def check_truncated(self, img):
        # Pillow won't load truncated images
        # See https://github.com/python-pillow/Pillow/issues/1510
        # Image reference: https://mangadex.org/chapter/1615adcb-5167-4459-8b12-ee7cfbdb10d9/16
        err = None
        try:
            img.load()
        except OSError as e:
            err = e
        else:
            return False

        if err:
            ImageFile.LOAD_TRUNCATED_IMAGES = True

        # Load it again
        img.load()

        return True

    def _save_all(self, im, fp, filename):
        self._save(im, fp, filename, save_all=True)

    # This was modified version of Pillow/PdfImagePlugin.py version 9.5.0
    # The images will be automatically converted to RGB and closed when done converting to PDF  # noqa: E501
    def _save(self, im, fp, filename, save_all=False):
        is_appending = im.encoderinfo.get("append", False)
        if is_appending:
            existing_pdf = PdfParser.PdfParser(f=fp, filename=filename, mode="r+b")
        else:
            existing_pdf = PdfParser.PdfParser(f=fp, filename=filename, mode="w+b")

        dpi = im.encoderinfo.get("dpi")
        if dpi:
            x_resolution = dpi[0]
            y_resolution = dpi[1]
        else:
            x_resolution = y_resolution = im.encoderinfo.get("resolution", 72.0)

        info = {
            "title": (
                None
                if is_appending
                else os.path.splitext(os.path.basename(filename))[0]
            ),
            "author": None,
            "subject": None,
            "keywords": None,
            "creator": None,
            "producer": None,
            "creationDate": None if is_appending else time.gmtime(),
            "modDate": None if is_appending else time.gmtime(),
        }
        for k, default in info.items():
            v = im.encoderinfo.get(k) if k in im.encoderinfo else default
            if v:
                existing_pdf.info[k[0].upper() + k[1:]] = v

        #
        # make sure image data is available
        im.load()

        existing_pdf.start_writing()
        existing_pdf.write_header()
        existing_pdf.write_comment(f"created by Pillow {__version__} PDF driver")

        #
        # pages
        encoderinfo = im.encoderinfo.copy()
        ims = [im]
        if save_all:
            append_images = im.encoderinfo.get("append_images", [])
            ims.extend(append_images)

        number_of_pages = 0
        image_refs = []
        page_refs = []
        contents_refs = []
        for im_ref in ims:
            img = im_ref() if isinstance(im_ref, _PageRef) else im_ref
            im_number_of_pages = 1
            if save_all:
                try:
                    im_number_of_pages = img.n_frames
                except AttributeError:
                    # Image format does not have n_frames.
                    # It is a single frame image
                    pass
            number_of_pages += im_number_of_pages
            for i in range(im_number_of_pages):
                image_refs.append(existing_pdf.next_object_id(0))
                if im.mode == "P" and "transparency" in im.info:
                    image_refs.append(existing_pdf.next_object_id(0))

                page_refs.append(existing_pdf.next_object_id(0))
                contents_refs.append(existing_pdf.next_object_id(0))
                existing_pdf.pages.append(page_refs[-1])

            # Reduce Opened files
            if isinstance(im_ref, _PageRef):
                img.close()

        #
        # catalog and list of pages
        existing_pdf.write_catalog()

        if ImageFile.LOAD_TRUNCATED_IMAGES:
            ImageFile.LOAD_TRUNCATED_IMAGES = False

        page_number = 0
        for im_ref in ims:
            # The reason i did this is to prevent error in Unix-based OS
            # If the application is opening too much files,
            # the OS will throw an error "OSError: Too many open files"
            im = im_ref() if isinstance(im_ref, _PageRef) else im_ref

            truncated = self.check_truncated(im)

            if im.mode != "RGB":
                # Convert to RGB mode
                im_sequence = im.convert("RGB")

                # Close image to save memory
                im.close()
            else:
                # Already in RGB mode
                im_sequence = im

            # Copy necessary encoderinfo to new image
            im_sequence.encoderinfo = encoderinfo.copy()

            im_pages = (
                ImageSequence.Iterator(im_sequence) if save_all else [im_sequence]
            )
            for im in im_pages:
                image_ref, procset = _write_image(
                    im, filename, existing_pdf, image_refs
                )

                #
                # page

                existing_pdf.write_page(
                    page_refs[page_number],
                    Resources=PdfParser.PdfDict(
                        ProcSet=[PdfParser.PdfName("PDF"), PdfParser.PdfName(procset)],
                        XObject=PdfParser.PdfDict(image=image_ref),
                    ),
                    MediaBox=[
                        0,
                        0,
                        im.width * 72.0 / x_resolution,
                        im.height * 72.0 / y_resolution,
                    ],
                    Contents=contents_refs[page_number],
                )

                #
                # page contents

                page_contents = b"q %f 0 0 %f 0 0 cm /image Do Q\n" % (
                    im.width * 72.0 / x_resolution,
                    im.height * 72.0 / y_resolution,
                )

                existing_pdf.write_obj(contents_refs[page_number], stream=page_contents)

                self.tqdm.update(1)
                page_number += 1

            # Close image to save memory
            im_sequence.close()

            # For security sake
            if truncated:
                ImageFile.LOAD_TRUNCATED_IMAGES = False

        #
        # trailer
        existing_pdf.write_xref_and_trailer()
        if hasattr(fp, "flush"):
            fp.flush()
        existing_pdf.close()

    def register_pdf_handler(self):
        Image.init()

        Image.register_save("PDF", self._save)
        Image.register_save_all("PDF", self._save_all)
        Image.register_extension("PDF", ".pdf")

        Image.register_mime("PDF", "application/pdf")


class PDFFile:
    file_ext = ".pdf"

    def check_dependecies(self):
        if not pillow_ready:
            raise PillowNotInstalled("pillow is not installed")

    def convert(self, imgs, target):
        pdf_plugin = PDFPlugin(imgs)

        # Because images from BaseFormat.get_images() was just bunch of pathlib.Path
        # objects, we need convert it to _PageRef for be able Modified Pillow can convert it
        images = []
        for im in imgs:
            images.append(_PageRef(Image.open, im))

        im_ref = images.pop(0)
        im = im_ref()

        pdf_plugin.check_truncated(im)

        im.save(target, save_all=True, append_images=images)

    def insert_ch_info_img(self, images, chapter, path, count):
        """Insert chapter info (cover) image"""
        img_name = count.get() + ".png"
        img_path = path / img_name

        if self.config.use_chapter_cover:
            get_chapter_info(self.manga, chapter, img_path)
            images.append(img_path)
            count.increase()

    def insert_vol_cover_img(self, images, volume, path, count):
        """Insert volume cover"""
        img_name = count.get() + ".png"
        img_path = path / img_name

        if self.config.use_volume_cover:
            get_volume_cover(self.manga, volume, img_path, self.replace)
            images.append(img_path)
            count.increase()


class PDF(ConvertedChaptersFormat, PDFFile):
    def on_finish(self, file_path, chapter, images):
        self.worker.submit(lambda: self.convert(images, file_path))


class PDFVolume(ConvertedVolumesFormat, PDFFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # `images` variable are only filled download images from MangaDex server
        # (look at ConvertedVolumesFormat.download_volumes() at `for chap_class, chap_images in chapters`)  # noqa: E501
        # This is volume format, which mean user can add volume cover + chapter cover
        # But volume cover + chapter cover are separated images
        # and it does not get added to `images` variable
        # also PDF library (in this case Pillow) need a argument that iterating images
        # So we're gonna fill images to self.images and convert from that
        # rather than depending from `images` parameter from on_finish()
        self.images = []

    def on_prepare(self, file_path, volume, count):
        # We should clear self.images, to prevent older volumes to be re-converted
        self.images.clear()

        volume_name = self.get_volume_name(volume)
        self.volume_path = create_directory(volume_name, self.path)

        self.insert_vol_cover_img(self.images, volume, self.volume_path, count)

    def on_iter_chapter(self, file_path, chapter, count):
        self.insert_ch_info_img(self.images, chapter, self.volume_path, count)

    def on_convert(self, file_path, volume, images):
        self.worker.submit(lambda: self.convert(self.images, file_path))

    def on_received_images(self, file_path, chapter, images):
        self.images.extend(images)


class PDFSingle(ConvertedSingleFormat, PDFFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # See `PDFVolume.__init__()` for more info
        self.images = []

    def on_prepare(self, file_path, base_path):
        self.images_directory = base_path

    def on_iter_chapter(self, file_path, chapter, count):
        self.insert_ch_info_img(self.images, chapter, self.images_directory, count)

    def on_finish(self, file_path, images):
        self.worker.submit(lambda: self.convert(self.images, file_path))

    def on_received_images(self, file_path, chapter, images):
        self.images.extend(images)
