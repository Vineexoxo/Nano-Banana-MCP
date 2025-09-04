import asyncio
from io import BytesIO
from PIL import Image
from nano_banana_server import NanoBananaMCPServer

async def main():
    server = NanoBananaMCPServer()
    result = await server.generate_image_from_raw_bytes(
        prompt="A nano banana dish in a fancy restaurant with a Gemini theme"
    )
    if result["success"]:
        img_bytes = result["generated_image_bytes"]
        Image.open(BytesIO(img_bytes)).save("generated_image.png")
        print("Saved generated_image.png")
    else:
        print("Error:", result["error"])

if __name__ == "__main__":
    asyncio.run(main())