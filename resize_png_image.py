from PIL import Image

# Open the image file
with Image.open("ex.png") as im:
    # Resize the image
    im_resized = im.resize((50, 50))

    # Save the resized image
    im_resized.save("exit.png")
