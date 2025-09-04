import os
import asyncio
from typing import Optional

from nano_banana_server import generate_image_with_nano_banana


async def main() -> None:
    here = os.path.dirname(__file__)
    image_path = os.path.join(here, "test_image.png")
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Input image not found: {image_path}")

    with open(image_path, "rb") as f:
        input_bytes = f.read()

    prompt = (
        "Top-down (flat lay) view of this scene with a warm, festive look, "
        "a small lit diya placed to the side casting soft glow and shadows."
    )

    result = await generate_image_with_nano_banana(
        prompt=prompt,
        input_image_bytes=input_bytes,
        input_image_mime_type="image/png",
    )

    if not result.get("success"):
        raise RuntimeError(f"Generation failed: {result.get('error')}")

    output_path = os.path.join(here, "generated_top_view_diya.png")
    with open(output_path, "wb") as f:
        f.write(result["generated_image_bytes"])  # raw bytes path

    print(f"✅ Saved: {output_path} ({result.get('generated_image_size')} bytes)")


if __name__ == "__main__":
    asyncio.run(main())


