import cloudinary
import cloudinary.uploader

# Configuration
cloudinary.config(
    cloud_name="dm1obzrw0",
    api_key="315366156521239",
    api_secret="d_y6FkyMcPLf_WL_NSZlF6WKtpM",  # Click 'View Credentials' below to copy your API secret
    secure=True
)


def create_image(image):
    upload_result = cloudinary.uploader.upload(image)
    print("upload result image : ",upload_result["secure_url"])
    return upload_result["secure_url"]


#
#
# # Upload an image
# upload_result = cloudinary.uploader.upload("images/Screenshot 2024-05-08 at 15.24.45.png",
#                                            )
# print(upload_result["secure_url"])
#
# # Optimize delivery by resizing and applying auto-format and auto-quality
# optimize_url, _ = cloudinary_url("blue", fetch_format="auto", quality="auto")
# print(optimize_url)
#
# # Transform the image: auto-crop to square aspect_ratio
# auto_crop_url, _ = cloudinary_url('', width=500, height=500, crop="auto", gravity="auto")
# print(auto_crop_url)
