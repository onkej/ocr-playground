from paddleocr import PaddleOCR
import streamlit as st
import zipfile
import tempfile
import io

# Dict path for PaddleOCR (simplified Chinese characters)
dict_path = "./dict/ppocr_keys_v1.txt"

# create an ocr object
ocr = PaddleOCR(
    lang="ch",  # model used for Chinese text detection
    page_num=0, # number of PDF pages to process, 0 => all pages
    det_model_dir='models/ch_PP-OCRv4_det_infer',
    rec_model_dir='models/ch_PP-OCRv4_rec_infer',
    det_db_unclip_ratio=2.0, # ratio used for detecting text boxes
    rec_char_dict_path=dict_path, # character/label mappping dictionary
    # help=False, 
    use_space_char=False, # whether to use space character
    use_angle_cls=False, # disable angle classifier cuz official texts are well-aligned 
    use_gpu=True, # use GPU? 
)

def ocr_from_pdf(pdf):
    """Perform OCR on a pdf"""
    # Save the uploaded PDF to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf.write(pdf.read())  # Write the uploaded file's content to temp file
        temp_pdf_path = temp_pdf.name  # Get the file path

        # do OCR for current PDF
        result = ocr.ocr(temp_pdf_path, cls=True)

        # Extract text
        ocr_text = ""
        for page_res in result:
            for line in page_res:
                ocr_text += line[1][0] + "\n"

    return ocr_text


# streamlit UI
# title & description
st.title("📄 OCR Tool for Chinese PDFs")
st.write(
    "Designed for the purpose of supporting sociological research \
    on contemporary China, this tool aims to help you extract texts from \
    governmental PDF files. \
    \n\n**Note**: currently, it only supports files with simple layout, namely \
    ✨**mono-column texts**✨ **without charts or tables**. \
    More complex PDFs may not work well. `XD`"
)

# file uploader: ask user to upload their PDF files
uploaded_pdfs = st.file_uploader(
    "Upload your PDF files here", 
    type="pdf", 
    accept_multiple_files=True # allow selecting multiple files
)


if uploaded_pdfs:
    # Run OCR to extract text from images
    if st.button("Start OCR"):
        st.write("Be patient, this may take a while... `:)`")
        # Progress bar for all files
        overall_progress = st.progress(0)
        
        # Create an in-memory byte stream for the zip file
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for idx, pdf in enumerate(uploaded_pdfs):
                # Process current PDF
                with st.status(
                    f"🔄 Processing `{pdf.name}` ...", 
                    expanded=True
                ) as status:
                    ocr_text = ocr_from_pdf(pdf)
                # Update status
                status.update(
                    label=f"✅ `{pdf.name}` processed successfully!", 
                    state="complete"
                )
                # Update overall progress
                overall_progress.progress((idx+1) / len(uploaded_pdfs))

                 # Add this OCR text as a file inside the zip
                zip_file.writestr(f"{pdf.name.split('.')[0]}_ocr.txt", ocr_text)
        
        # Seek to the beginning of the byte stream before sending it for download
        zip_buffer.seek(0)

        st.success(f"✅ OCR completed for {len(uploaded_pdfs)} files!")
        # Provide a downloadable zip file containing all OCR results
        st.download_button(
            label="Download OCR Texts `(.zip)`",
            data=zip_buffer,
            file_name="ocr_output.zip",
            mime="application/zip"
        )
