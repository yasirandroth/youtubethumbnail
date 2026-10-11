import os
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter

# --- CONFIGURATION ---
CANVAS_SIZE = (1080, 1920)

def create_viral_football_short(
    subject_path, 
    headline_text, 
    bottom_text, 
    logo_path="input_assets/logo.png", 
    output_path="output_shorts/viral_short.png"
):
    # 1. Load and process base image for 9:16 vertical canvas using high-quality Lanczos resampling
    print(f"Processing: {subject_path}")
    canvas = Image.open(subject_path).convert("RGBA")
    canvas = resize_and_crop(canvas, CANVAS_SIZE)
    
    # --- VISUAL & CLARITY ENHANCEMENTS ---
    canvas = canvas.filter(ImageFilter.SHARPEN)
    
    enhancer_sharpness = ImageEnhance.Sharpness(canvas)
    canvas = enhancer_sharpness.enhance(1.5)  # Increase edge sharpness by 50%
    
    enhancer_contrast = ImageEnhance.Contrast(canvas)
    canvas = enhancer_contrast.enhance(1.15)  # Boost contrast by 15%
    
    enhancer_color = ImageEnhance.Color(canvas)
    canvas = enhancer_color.enhance(1.10)     # Boost color saturation by 10%
    
    # --- Smooth Ambient Vignette Gradient ---
    vignette = Image.new("RGBA", CANVAS_SIZE, (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    for i in range(450):
        alpha = int(210 * (1 - i / 450))
        v_draw.line([(0, i), (CANVAS_SIZE[0], i)], fill=(0, 0, 0, alpha))
        v_draw.line([(0, CANVAS_SIZE[1] - i), (CANVAS_SIZE[0], CANVAS_SIZE[1] - i)], fill=(0, 0, 0, alpha))
    
    canvas = Image.alpha_composite(canvas, vignette)

    # Font Setup
    font_paths = [
        "C:\\Windows\\Fonts\\arialbd.ttf",
        "C:\\Windows\\Fonts\\segoeui.ttf",
        "arial.ttf"
    ]
    
    font_headline = None
    font_ticker = None
    font_tag = None
    
    for path in font_paths:
        try:
            font_headline = ImageFont.truetype(path, 75)
            font_ticker = ImageFont.truetype(path, 42)
            font_tag = ImageFont.truetype(path, 32)
            break
        except IOError:
            continue
            
    if not font_headline:
        font_headline = ImageFont.load_default()
        font_ticker = ImageFont.load_default()
        font_tag = ImageFont.load_default()

    draw = ImageDraw.Draw(canvas)

    # --- "BREAKING NEWS" Header Tag ---
    top_y = 150
    banner_height = 140
    
    tag_text = "🚨 BREAKING NEWS"
    bbox_tag = font_tag.getbbox(tag_text)
    tag_w = bbox_tag[2] - bbox_tag[0]
    tag_box = [(60, top_y - 45), (60 + tag_w + 40, top_y + 5)]
    draw.rounded_rectangle(tag_box, radius=10, fill=(230, 30, 30))
    draw.text((80, top_y - 38), tag_text, fill=(255, 255, 255), font=font_tag)

    # Main Headline Banner
    banner_box = [(60, top_y), (CANVAS_SIZE[0] - 60, top_y + banner_height)]
    draw.rounded_rectangle(banner_box, radius=20, fill=(10, 10, 15, 225), outline=(255, 215, 0), width=4)
    
    # Headline Text
    bbox_top = font_headline.getbbox(headline_text)
    text_w = bbox_top[2] - bbox_top[0]
    text_h = bbox_top[3] - bbox_top[0] if len(bbox_top) > 3 else (bbox_top[3] - bbox_top[1])
    # Safe text centering calculation
    text_h = bbox_top[3] - bbox_top[1]
    text_x = (CANVAS_SIZE[0] - text_w) // 2
    text_y = top_y + (banner_height - text_h) // 2 - 8
    
    draw.text((text_x + 4, text_y + 4), headline_text, fill=(0, 0, 0), font=font_headline)
    draw.text((text_x, text_y), headline_text, fill=(255, 215, 0), font=font_headline)

    # --- Broadcast Lower Third + Glowing "LIVE" Indicator ---
    bottom_y = CANVAS_SIZE[1] - 250
    ticker_height = 110
    
    draw.rectangle([(60, bottom_y), (CANVAS_SIZE[0] - 60, bottom_y + ticker_height)], fill=(12, 12, 18, 235))
    draw.rectangle([(60, bottom_y), (85, bottom_y + ticker_height)], fill=(255, 40, 40))
    
    # Glowing "LIVE" red dot
    dot_center_x, dot_center_y = 120, bottom_y + (ticker_height // 2)
    draw.ellipse([(dot_center_x - 14, dot_center_y - 14), (dot_center_x + 14, dot_center_y + 14)], fill=(255, 0, 0, 80))
    draw.ellipse([(dot_center_x - 8, dot_center_y - 8), (dot_center_x + 8, dot_center_y + 8)], fill=(255, 30, 30))

    # Ticker Text
    bbox_bot = font_ticker.getbbox(bottom_text)
    bot_h = bbox_bot[3] - bbox_bot[1]
    text_x_bot = 150
    text_y_bot = bottom_y + (ticker_height - bot_h) // 2 - 5
    draw.text((text_x_bot, text_y_bot), bottom_text, fill=(255, 255, 255), font=font_ticker)

    # --- Optional Channel Logo Overlay ---
    if os.path.exists(logo_path):
        logo = Image.open(logo_path).convert("RGBA")
        logo_size = (80, 80)
        logo = logo.resize(logo_size, Image.Resampling.LANCZOS)
        
        logo_x = CANVAS_SIZE[0] - 60 - logo_size[0] - 15
        logo_y = bottom_y + (ticker_height - logo_size[1]) // 2
        canvas.paste(logo, (logo_x, logo_y), logo)

    # Save final asset
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    final_img = canvas.convert("RGB")
    final_img.save(output_path, "PNG", quality=100)
    print(f"-> Saved: {output_path}")

def resize_and_crop(img, target_size):
    target_width, target_height = target_size
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        new_height = target_height
        new_width = int(target_height * img_ratio)
    else:
        new_width = target_width
        new_height = int(target_width / img_ratio)

    img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - target_width) / 2
    top = (new_height - target_height) / 2
    return img.crop((left, top, left + target_width, top + target_height))

if __name__ == "__main__":
    # --- BATCH FOLDER PROCESSING CONFIGURATION ---
    input_folder = "input_assets"      # Put all your raw football images here
    output_folder = "output_shorts"    # Finished graphics will save here automatically
    logo_file = "input_assets/logo.png" # Optional channel logo
    
    headline = "THE GOAT IS BACK!"     # Headline applied to all in batch (or you can customize per file)
    ticker = "FALSE 9 FOOTBALL TALKS"
    
    # Supported image extensions
    valid_extensions = (".png", ".jpg", ".jpeg", ".webp")
    
    if not os.path.exists(input_folder):
        print(f"Error: Directory '{input_folder}' does not exist. Please create it and add your images.")
    else:
        images = [f for f in os.listdir(input_folder) if f.lower().endswith(valid_extensions)]
        
        if not images:
            print(f"No images found in '{input_folder}'.")
        else:
            print(f"Found {len(images)} images to process. Starting batch generation...")
            for filename in images:
                src_path = os.path.join(input_folder, filename)
                # Keep original filename name with a clean output format
                base_name, _ = os.path.splitext(filename)
                out_path = os.path.join(output_folder, f"{base_name}_short.png")
                
                try:
                    create_viral_football_short(
                        subject_path=src_path,
                        headline_text=headline,
                        bottom_text=ticker,
                        logo_path=logo_file,
                        output_path=out_path
                    )
                except Exception as e:
                    print(f"Failed to process {filename}: {e}")
                    
            print("Batch processing complete! All graphics ready in folder:", output_folder)