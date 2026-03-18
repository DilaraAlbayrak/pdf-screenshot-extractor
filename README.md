# PDF Screenshot Extractor and AI Enhancer
This repository provides a two-stage Python pipeline to extract pages from locked PDFs and enhance their visual quality. It bypasses standard PDF restrictions by automating screen captures and subsequently applies image processing and AI upscaling to optimise the output.

## Workflow Overview
The process is divided into two discrete scripts:
- ```capture_pdf.py```: Automates the screen capturing of an active PDF viewer.
- ```process_screenshots.py```: Crops, denoises, and enhances the captured screenshots using OpenCV and a Fast Super-Resolution Convolutional Neural Network (FSRCNN).

Requirements:
```pyautogui```
```mss```
```opencv-contrib-python```

## Step 1: Capture the PDF pages
Open your PDF document in a reader, set it to "Single-page view" and "Fit height".
Execute the capture script: ```python capture_pdf.py```

- You will have a 5-second window to bring the PDF viewer to the foreground and ensure it is in focus.
- The script mimics pressing the right arrow key to turn the pages.
- Screenshots are saved sequentially as PNG files in an automatically generated screenshots/ directory.
- Customisation: Modify total_pages and render_delay within the script to match your specific document length and your machine's rendering speed.

## Step 2: Process and enhance images
After the screen captures are complete, run the processing script to crop unwanted interface elements (such as taskbars or reader menus), remove visual noise, and upscale the resolution.
To run all enhancements (the default behaviour):

```python process_screenshots.py```

To run specific processes, use the command-line flags:

```python process_screenshots.py --crop``` or ```
python process_screenshots.py --denoise --upscale```

<img width="1536" height="912" alt="image" src="https://github.com/user-attachments/assets/bb1bd7cf-b79e-4c27-92ed-2d4f3fce402c" />


- Crop: Trims the image to specified bounding box coordinates. You must adjust the ```min_x```, ```max_x```, ```min_y```, and ```max_y``` variables within the script to align with your monitor's resolution and the exact position of the PDF page _(Above image is just an illustration, I recommend to use "rotate" feature of your PDF Viewer, and capture screenshots horizontally to approximate original document dimensions)_. 
- Denoise: Applies Non-Local Means Denoising to filter out background artefacts whilst preserving sharp text and table edges.
- Upscale: Automatically downloads the pre-trained ```FSRCNN_x2.pb``` AI model upon first run and applies a 2x resolution enhancement tailored for clear edges.
- The final outputs are saved to the ```processed_screenshots``` directory.
