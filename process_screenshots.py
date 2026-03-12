import cv2
import os
import argparse
import glob
import urllib.request

def download_model(model_path="FSRCNN_x2.pb"):
    # Download the pre-trained FSRCNN model if it does not exist locally
    if not os.path.exists(model_path):
        print(f"Downloading AI model {model_path}...")
        url = "https://github.com/Saafke/FSRCNN_Tensorflow/raw/master/models/FSRCNN_x2.pb"
        urllib.request.urlretrieve(url, model_path)
        print("Download complete.")

def crop_image(image, min_x=600, max_x=1318, min_y=102, max_y=1120):
    h, w = image.shape[:2]
    return image[max(0, min_y):min(h, max_y), max(0, min_x):min(w, max_x)]

def denoise_document(image):
    return cv2.fastNlMeansDenoisingColored(image, None, h=10, hColor=10, templateWindowSize=7, searchWindowSize=21)

def upscale_document_ai(image, model_path="FSRCNN_x2.pb"):
    # Initialize the AI Super Resolution module
    sr = cv2.dnn_superres.DnnSuperResImpl_create()
    
    # Read the model and set the algorithm and scale factor (2x)
    sr.readModel(model_path)
    sr.setModel("fsrcnn", 2)
    
    # Upsample the image using the AI model
    return sr.upsample(image)

def main():
    parser = argparse.ArgumentParser(description="Process document screenshots.")
    parser.add_argument('--crop', action='store_true', help="Enable image cropping")
    parser.add_argument('--denoise', action='store_true', help="Enable noise removal")
    parser.add_argument('--upscale', action='store_true', help="Enable AI-based 2x upscaling")
    
    args = parser.parse_args()
    
    # Apply all functions by default if no arguments are provided
    if not (args.crop or args.denoise or args.upscale):
        args.crop = True
        args.denoise = True
        args.upscale = True

    input_dir = "screenshots"
    output_dir = "processed_screenshots"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Ensure AI model is present if upscaling is requested
    if args.upscale:
        download_model()

    image_paths = glob.glob(os.path.join(input_dir, "*.png"))
    
    if not image_paths:
        print(f"No PNG images found in '{input_dir}' folder.")
        return

    for path in image_paths:
        filename = os.path.basename(path)
        img = cv2.imread(path)
        
        if img is None:
            print(f"Failed to load {filename}")
            continue
        
        # Order of operations: Crop -> Denoise -> AI Upscale
        if args.crop:
            img = crop_image(img)
            
        if args.denoise:
            img = denoise_document(img)
            
        if args.upscale:
            img = upscale_document_ai(img)
            
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, img)
        print(f"Processed: {filename}")

    print("All processing complete.")

if __name__ == "__main__":
    main()