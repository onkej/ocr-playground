📄 OCR Tool for Chinese PDFs
============================== 

Link to App: [PaddleOCR for Chinese PDFs](https://onkej-paddleocr-for-chinese-pdfs.hf.space)


Designed for the purpose of supporting sociological research on contemporary China, this tool aims to help researchers extract texts from PDF files written in simplified Chinese.


**Table of Contents**
- [📄 OCR Tool for Chinese PDFs](#-ocr-tool-for-chinese-pdfs)
- [Context](#context)
- [Installation](#installation)
- [Usage](#usage)
- [Parameters, Problems, Ideas](#parameters-problems-ideas)
- [References](#references)


# Context
I am working on an academic project called Chine CoREF at UAR2999 Études aréales, CNRS. This initiative aims to build a comprehensive digital platform dedicated to contemporary China, providing valuable resources and tools to support French and European scholars in their research on the country.

One of our key objectives is to collect and archive open resources from Chinese governmental websites. However, many of these resources, such as official reports and budget documents, are not in machine-readable or searchable formats, particularly PDFs. 

To address this challenge, we plan to systematically gather and process budget files from provincial and municipal finance department websites. In this context, I tried to develop a web application designed to assist scholars and research assistants in converting PDF files into plain text. This tool enables users to efficiently extract and process textual content, ensuring that researchers can efficiently analyze and utilize these critical data.

# Installation
To run the application, you need to install:
- Python 3.12
- Download this repository by running the following command in your terminal, or simply by clicking the green `Code` button and selecting `Download ZIP`):
```bash
git clone https://github.com/onkej/ocr-playground.git
```
- Open the terminal and navigate to the project directory:
```bash
cd ocr-playground
```
- Create a virtual environment for the project and activate it:
```bash
python -m venv ocr
source ocr/bin/activate
```
- Install the required packages:
```bash
pip install -r requirements.txt
```

# Usage
Wait for the installation to complete, then run the application:
```bash
streamlit run zhsOCR.py
```

The application will open in your default web browser, allowing you to upload PDF files and it will extract texts from them. For example, you can test the tool by uploading one or more PDF files provided in the `pdfs` folder. These files are samples of provincial budget documents that you can use to evaluate the tool's performance.

At the end of the process, you can click to download all extracted texts (in a `.zip` file) to your local for post-processing and further analysis. Hopefully, the quality of the extracted texts would be satisfying and doesn't need much manual correction.

> **Note**: by now the application only supports extracting files in simple layout structures (i.e. text content). It may not work perfectly with all PDF files, especially those with complex layouts (charts, tables, etc.)or low-quality scanned images. 


# Parameters, Problems, Ideas

1. **About model selection**: I planned to make it a sharable online tool. Initially I did the job locally on my computer for testing how it goes on some very clear provincial budget samples (`pdfs` folders). I learned that **PaddleOCR** is better for handling Chinese texts. Indeed, after testing on a sample, I found the results were much better than the tools I used last year such as `PyMuPDF`, though there are still some words that are not recognized correctly, for example, 纾 in 纾困 and 踔 in 踔厉奋发 were both missing, 市 in 市县 was recognized as 币, 斤 in 四两拨千斤 became 片, 着 in 着力 turned out to be 看. But it's still a good start and I can continue to improve it later.

2. **`pp-ocr` pipeline**: Basically, the pipeline is made up of a series of components, mainly a text detector and a text recognizor:
   1. **Text Detection** uses a DB model (`det_algorithm='DB'`), which is a deep learning algorithm for detecting text regions.  
   2. **Text recognition** uses the SVTR algorithm (`rec_algorithm='SVTR_LCNet'`) to predict text based on the output of detected text regions. 
   
3. **About the wrong characters**: Based on the above observations, I started to inspect the text boxes found by the model in their semi-automatic annotation tool called `PPOCRLabel`. I noticed that after detection, each line was cropped in a long rectanglar box, but at some lines the box height were narrower, where some strokes at the top edge could not be included. I suppose this is the reason why the above wrongly recognized chracters were produced, and fortunately this type of problem can be solved by slightly increasing the parameter `det_db_unclip_ratio` from 1.5 to 2.0 when initializing the OCR object. After this adjustment, the OCR model worked much better and wrong characters above were all corrected!

4. **About the missing characters**: for these missing characters, I think it's because the default dictionary of the model does not contain these words and/or the model is not trained on these words. So I downloaded the dictionary file from the PaddleOCR repository and checked that the word 纾 is actually included but 踔 is not. I added this word to the end of the dictionary, specified explicitly the path to this dictionary and relaunch the script -- this time 纾 came back, but the result got worse as the model became to predict 踔 in many other places that should not be. So I finally decided to remove this word as it's not worth the effort to fix.


5. **PDF? or image?** At first, I learned that in general, OCR tools require images as input, so I spent some time to explore common pdf-to-image conversion packages. I tried to use the `pdf2image` to do the job, but there's a shortcoming that this package requires installing `poppler`, which is a system dependency. I thought it might be complicated in terms of deployment on Streamlit. So, even though I successfully converted PDF files to images and extracted the texts perfectly, I preferred to switch to another approach. At this very time I learned PaddleOCR can accept PDF files as input so I decided to switch to this easier feature instead.

6. **About deployment**: it failed `XD`... maybe because of some dependencies that cannot be correctly installed on the server. I will try to deploy it later. So far, I have tested it on my local and it works well. Hopefully it will work on yours too. 🤪


# References
- [PaddleOCR Documentation](https://paddlepaddle.github.io/PaddleOCR/latest/ppocr/overview.html)
```bibtex
@misc{du2022svtrscenetextrecognition,
      title={SVTR: Scene Text Recognition with a Single Visual Model}, 
      author={Yongkun Du and Zhineng Chen and Caiyan Jia and Xiaoting Yin and Tianlun Zheng and Chenxia Li and Yuning Du and Yu-Gang Jiang},
      year={2022},
      eprint={2205.00159},
      archivePrefix={arXiv},
      primaryClass={cs.CV},
      url={https://arxiv.org/abs/2205.00159}, 
}
```
