import streamlit as st
import qrcode
from io import BytesIO
import base64
from PIL import Image

def generate_qr(data, logo=None):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Highest error correction level
        box_size=20,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill='black', back_color='white').convert('RGB')

    if logo:
        logo = Image.open(logo)
        logo = logo.convert("RGBA")  # Ensure the logo is in RGBA format
        logo = logo.resize((image.size[0] // 3, image.size[1] // 3))
        pos = ((image.size[0] - logo.size[0]) // 2, (image.size[1] - logo.size[1]) // 2)
        image.paste(logo, pos, mask=logo)

    return image

st.title("QR Generator")
st.write("Simple and Secure")

data = st.text_input("Enter the link for the QR code:")
logo = st.file_uploader("Upload a logo (optional)", type=["png", "jpg", "jpeg"])

if st.button("Generate QR Code"):
    if data:
        img = generate_qr(data, logo)
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        img_html = f'<img src="data:image/png;base64,{img_base64}" width="300" style="display: block; margin-left: auto; margin-right: auto;" />'
        st.markdown(img_html, unsafe_allow_html=True)
        st.download_button(
            label="Download QR Code as PNG",
            data=buffer,
            file_name="qrcode.png",
            mime="image/png"
        )
    else:
        st.error("Please enter a link to generate the QR code.")