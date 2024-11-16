with open("C:\Users\Stephen\Download", "rb") as image_file:
    image_data = image_file.read()

    import base64

    base64_image = base64.b64encode(image_data).decode("utf-8")

    print(base64_image)
