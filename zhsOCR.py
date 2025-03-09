from pathlib import Path
from paddleocr import PaddleOCR
import streamlit as st


# Paths - Input & Output
pdf_dir = Path("pdfs")
txt_dir = Path("output")
txt_dir.mkdir(parents=True, exist_ok=True)

# Path - Dict (simplified Chinese characters)
dict_path = "./dict/ppocr_keys_v1.txt"

# Streamlit UI
st.title("📄 OCR Tool for Chinese PDFs")
st.write("This tool will help you extract texts from **mono-column** Chinese PDFs. \
    \n\nPlease upload your PDFs to the `pdfs` folder and click the button below to start the OCR process. \
    \n\nThe extracted texts will be saved to the `output` folder."
    )


def ocr_from_pdf(pdf_dir, txt_dir):
    """Perform OCR on pdfs with a progress bar in Streamlit."""
    ocr = PaddleOCR( # initialize ocr object, set parameters 
        lang="ch",  # model used for Chinese text detection
        page_num=0, # number of PDF pages to process, 0 => all pages
        use_angle_cls=False, # disable angle classifier cuz we're dealing with \ well-aligned official texts
        use_gpu=False, # use GPU? 
        rec_char_dict_path=dict_path, # character/label mappping dictionary
        det_db_unclip_ratio=2.0, # ratio used for detecting text boxes
        help=False
    )
    provinces = [p for p in pdf_dir.glob("*.pdf")]

    total_files = len(provinces)

    if total_files == 0:
        st.warning("⚠️ No PDF files found in the selected directory! 🈚️")
        return

    # Progress bar for all files
    overall_progress = st.progress(0)

    for idx, p in enumerate(provinces):
        p_txt = txt_dir / f"{p.stem}_ocr.txt"
        # p_imgs = sorted(p.glob("*.png"))
        
        # Display current file status
        with st.status(f"🔄 Processing `{p.name}` ...", expanded=True) as status:
            with open(p_txt, "w") as f:
                result = ocr.ocr(str(p), cls=True)

                for i in range(len(result)):
                    for line in result[i]:
                        f.write(line[1][0] + "\n")
            status.update(label=f"✅ `{p.name}` processed successfully!", state="complete")
        # Update overall progress
        overall_progress.progress((idx + 1) / total_files)

    

# Run OCR to extract text from images
if st.button("Start OCR"):
    st.write("Starting OCR... This may take a while...")
    ocr_from_pdf(pdf_dir, txt_dir)
    st.success("🥳 All done! You may check your `output` folder now ;)")
