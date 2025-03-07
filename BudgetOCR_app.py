from pathlib import Path
from pdf2image import convert_from_path
from paddleocr import PaddleOCR

import streamlit as st
# import shutil


# global poppler_dir

# Paths
# poppler_dir = "/opt/homebrew/opt/poppler/bin"
pdf_dir = Path("pdfs")
img_dir = Path("images")
txt_dir = Path("output")

img_dir.mkdir(parents=True, exist_ok=True)
txt_dir.mkdir(parents=True, exist_ok=True)


# Streamlit UI
st.title("📄 OCR Tool for Chinese PDFs")
# st.write("Welcome to the Budget OCR Tool! 🎉")
st.write("This tool will help you extract texts from **mono-column** Chinese PDFs. Before starting, make sure to visit [here](https://poppler.freedesktop.org) to **install `poppler`** on your system. Then, install the required packages by running the following command in your Terminal.")
st.write("**`pip install -r requirements.txt`**")

poppler_dir = st.text_input("Enter the path to poppler:", "/opt/homebrew/opt/poppler/bin") # Ask user to input the path to Poppler


def pdf_to_img(pdf_dir, img_dir, poppler_dir):
    """Convert PDFs to images with a progress bar in Streamlit."""
    pdfs = list(pdf_dir.glob("*.pdf"))
    
    for pdf in pdfs:
        province_dir = img_dir / pdf.stem
        province_dir.mkdir(parents=True, exist_ok=True)
        imgs = convert_from_path(
            pdf, 
            dpi=300, 
            poppler_path=poppler_dir
        )

        n_digits = 2 if len(imgs) < 100 else 3 
        progress_bar = st.progress(0)  # Streamlit progress bar

        for i, img in enumerate(imgs, 1):
            page_num = str(i).zfill(n_digits)
            img_path = province_dir / f"{pdf.stem}_{page_num}.png"
            img.save(img_path, "PNG")
            progress_bar.progress(i / len(imgs))  # Update progress bar

        st.success(f"✅ Conversion completed for `{pdf}`. Images saved to `{province_dir}`.")

def ocr_from_img(img_dir, txt_dir):
    """Perform OCR on images with a progress bar in Streamlit."""
    ocr = PaddleOCR(lang="ch", use_angle_cls=True)
    provinces = [p for p in img_dir.glob("*") if p.is_dir()]

    for p in provinces:
        p_txt = txt_dir / f"{p.stem}_ocr.txt"
        p_imgs = sorted(p.glob("*.png"))
        
        progress_bar = st.progress(0)

        with open(p_txt, "w") as f:
            for i, img in enumerate(p_imgs):
                st.write(f"==> Extracting from: `{img}` ...")
                result = ocr.ocr(str(img), cls=True)
                for line in result:
                    for word in line:
                        f.write(word[1][0] + "\n")
                
                progress_bar.progress((i + 1) / len(p_imgs))  # Update progress

        st.success(f"✅ OCR completed. Budget of {p.stem} province saved to `{p_txt}`.")



# Convert PDFs to images
if st.button("Start converting PDFs to images") and pdf_dir.exists():
    st.write("Starting converting PDFs to images...")
    pdf_to_img(pdf_dir, img_dir, poppler_dir)

# Run OCR to extract text from images
if st.button("Start OCR"):
    st.write("Starting OCR...")
    ocr_from_img(img_dir, txt_dir)
    st.success("🥳 All done! You may check your `output` folder now.")
