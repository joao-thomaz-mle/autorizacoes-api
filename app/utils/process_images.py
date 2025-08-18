import io
from collections import defaultdict
from typing import Dict, List

import cv2
import fitz
import numpy as np
from PIL import Image  # noqa: F401

from app.utils.logger import get_logger

logger = get_logger(name=__name__)


def convert_blob_to_images(
    blob: bytes, extensao: str, MAX_IMAGES_PER_BLOB: int
) -> List[Image.Image]:
    imagens = []
    ext = extensao.lower().strip(".") if extensao else ""
    try:
        if ext == "pdf":
            with fitz.open(stream=blob, filetype="pdf") as pdf_doc:
                logger.info(f"Processando PDF com {len(pdf_doc)} página(s)...")
                for pagina in pdf_doc:
                    if len(imagens) >= MAX_IMAGES_PER_BLOB:
                        logger.warning(
                            f"⚠️ BLOB has reached the maximum limit of {MAX_IMAGES_PER_BLOB} images."
                        )
                        break
                    pix = pagina.get_pixmap(matrix=fitz.Matrix(3.0, 3.0), alpha=False)
                    imagens.append(Image.open(io.BytesIO(pix.tobytes("png"))))
        elif ext in ["jpg", "jpeg", "png", "bmp"]:
            imagens.append(Image.open(io.BytesIO(blob)))
        else:
            logger.warning(f"Formato de arquivo não suportado: '{ext}'.")
    except Exception as e:
        logger.error(f"Erro ao converter BLOB para imagem (ext: .{ext}): {e}")
    return imagens


def apply_clahe(imagem: Image.Image) -> Image.Image:
    try:
        imagem_cv = cv2.cvtColor(np.array(imagem), cv2.COLOR_RGB2BGR)
        imagem_cinza = cv2.cvtColor(imagem_cv, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        return Image.fromarray(clahe.apply(imagem_cinza))
    except Exception:
        return imagem


def imagens_para_bytes(images: Image.Image, formato: str = "PNG") -> List[bytes]:
    buffer = io.BytesIO()
    images.save(buffer, format=formato)
    return [buffer.getvalue()]


def process_blobs(
    blobs_and_id: Dict[str, bytes],
    img_enhancement: bool = True,
    MAX_IMAGES_PER_BLOB: int = 20,
) -> Dict[str, list[bytes]]:
    """get the pdf blob, in bytes, convert to png images, apply enchacement if wanted, and get the png bytes.
    args: blobs_and_id : Dict[str, list[bytes]]: Dictionary mapping IDs to their corresponding byte content.
          img_enhancement (bool): Flag indicating whether to apply image enhancement.
    output: defaultdict(str, list): A dictionary mapping IDs - str to their corresponding PNG image bytes.
    """
    byte_png_images_and_id = defaultdict(list)
    if blobs_and_id:
        for blob_id, blob in blobs_and_id.items():
            logger.info(f"Converting BLOB {blob_id} to images...")
            imagens = convert_blob_to_images(
                blob=blob, extensao="pdf", MAX_IMAGES_PER_BLOB=MAX_IMAGES_PER_BLOB
            )

            for img in imagens:
                if img_enhancement:
                    img = apply_clahe(imagem=img)
                img_bytes = imagens_para_bytes(images=img, formato="PNG")
                byte_png_images_and_id[blob_id].append(img_bytes[0])
            logger.info(f"✅ Converted image from BLOB {blob_id} to png bytes.")
    return byte_png_images_and_id
