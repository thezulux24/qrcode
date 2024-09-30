import streamlit as st
import qrcode
from io import BytesIO
import base64

def generate_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # Highest error correction level
        box_size=20,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    image = qr.make_image(fill='black', back_color='white')
    return image

st.title("QR Generator")

data = st.text_input("Enter the link for the QR code:")

if st.button("Generate QR Code"):
    if data:
        img = generate_qr(data)
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