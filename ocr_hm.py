from pathlib import Path
from pdf2image import convert_from_path
from paddleocr import PaddleOCR
import argparse


"""
poppler_dir:    Path to poppler (pdf2image dependency!)
pdf_dir:        Path to Budget PDFs
img_dir:        Path to generated budget images
ocr_dir:        Path to generated OCR texts
"""

# global poppler_dir
poppler_dir = "/opt/homebrew/opt/poppler/bin"
pdf_dir = "pdfs"
img_dir = "images"
txt_dir = "output"


def pdf_to_img(pdf_dir, img_dir):
    """ convert PDFs to images"""
    pdf_dir, img_dir = Path(pdf_dir), Path(img_dir)
    img_dir.mkdir(parents=True, exist_ok=True)
    pdfs = list(pdf_dir.glob("*.pdf"))

    for pdf in pdfs:
        province_dir = img_dir / pdf.stem
        province_dir.mkdir(parents=True, exist_ok=True)
        imgs = convert_from_path(
            pdf, 
            dpi=300, 
            poppler_path=poppler_dir
        )
        n_digits = 3 if len(imgs) > 99 else 2

        for i, img in enumerate(imgs, 1):
            page_num = str(i).zfill(n_digits)  # Use zfill to pad with zeros
            img_path = province_dir / f"{pdf.stem}_{page_num}.jpg"
            img.save(img_path, "JPEG")     


def ocr_from_img(img_dir, txt_dir):
    """get ocr texts from images"""
    txt_dir = Path(txt_dir)
    txt_dir.mkdir(parents=True, exist_ok=True)
    ocr = PaddleOCR(lang="ch", use_angle_cls=True)
    provinces = [p for p in Path(img_dir).glob("*") if not p.name.startswith(".")]
    
    for p in provinces:
        print(f"==> Processing images of {p.stem} province ...")
        p_txt = txt_dir / f"{p.stem}_ocr.txt" # create empty txt for each province
        p_imgs = sorted(p.glob("*.jpg")) # group all images of the province
        
        with open(p_txt, "w") as f:
            for img in p_imgs:
                print(f"==> Extracting from: {img} ...")
                result = ocr.ocr(str(img), cls=True)
                for line in result:
                    for word in line:
                        f.write(word[1][0] + "\n")

        print(f"==> Finished. Budget of {p.stem} province saved to {p_txt}.")


if __name__ == "__main__":
    pdf_to_img(pdf_dir, img_dir)
    ocr_from_img(img_dir, txt_dir)

    # parser = argparse.ArgumentParser(
    #     description="Extract OCR texts from PDFs"
    # )
    # parser.add_argument('pdf_dir', help="Path to PDFs", type=str, required=False, default="pdfs")
    # parser.add_argument('img_dir', help="Path to images", type=str, required=False, default="images")
    # parser.add_argument('output', help="Path to output", type=str, required=False, default="output")

    # args = parser.parse_args()
    # pdf_dir = args.pdf_dir
    # img_dir = args.img_dir
    # txt_dir = args.txt_dir

