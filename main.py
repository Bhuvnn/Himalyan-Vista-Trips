import os
from pathlib import Path
from PIL import Image

# ===== CONFIG (DO NOT CHANGE) =====
MAX_WIDTH = 1800
JPEG_QUALITY = 90

def optimize_image(input_path: Path, output_path: Path):
    with Image.open(input_path) as img:
        img = img.convert("RGB")

        # Resize only if image is larger than MAX_WIDTH
        if img.width > MAX_WIDTH:
            ratio = MAX_WIDTH / img.width
            new_height = int(img.height * ratio)
            img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        img.save(
            output_path,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True,
            subsampling=0
        )

def optimize_folder(input_dir):
    input_dir = Path(input_dir).resolve()
    output_dir = input_dir.parent / f"{input_dir.name}_optimized"

    print(f"\nInput Folder : {input_dir}")
    print(f"Output Folder: {output_dir}\n")

    for file in input_dir.rglob("*"):
        if file.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            relative_path = file.relative_to(input_dir)
            output_file = output_dir / relative_path.with_suffix(".jpg")

            optimize_image(file, output_file)
            print(f"✔ Optimized: {relative_path}")

    print("\n✅ All images optimized successfully.")
    print("👉 Review the output folder before replacing originals.")

# ===== RUN =====
if __name__ == "__main__":
    folder_path = input("Enter the image folder path: ").strip()
    optimize_folder(folder_path)
