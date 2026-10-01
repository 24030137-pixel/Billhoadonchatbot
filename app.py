import streamlit as st
from datetime import datetime
from io import BytesIO
import os

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="Lucky Tea",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS GIAO DIỆN
# =========================================================

st.markdown(
    """
    <style>

    .main {
        padding-top: 1rem;
    }

    .lucky-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 0px;
    }

    .lucky-subtitle {
        text-align: center;
        font-size: 17px;
        margin-bottom: 20px;
    }

    .total-box {
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid rgba(128,128,128,0.35);
        margin-top: 15px;
        margin-bottom: 15px;
    }

    .total-title {
        font-size: 18px;
        font-weight: 600;
    }

    .total-money {
        font-size: 32px;
        font-weight: 800;
    }

    .bill-number {
        text-align: center;
        font-size: 23px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    div.stButton > button {
        border-radius: 10px;
        font-weight: 600;
        min-height: 45px;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# MENU
# =========================================================

MENU = {
    "Trà sữa truyền thống": 25000,
    "Trà sữa trân châu": 30000,
    "Trà sữa matcha": 30000,
    "Trà sữa socola": 30000,
    "Trà sữa khoai môn": 32000,
    "Trà sữa dâu": 30000,
    "Trà đào": 28000,
    "Trà vải": 28000,
    "Trà chanh": 20000,
    "Trà tắc": 20000,
}

# =========================================================
# TOPPING
# =========================================================

TOPPINGS = {
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch dừa": 5000,
    "Thạch trái cây": 5000,
    "Pudding trứng": 7000,
    "Kem cheese": 8000,
    "Trân châu hoàng kim": 7000,
    "Hạt thủy tinh": 6000,
}

# =========================================================
# MỨC ĐƯỜNG / ĐÁ
# =========================================================

SUGAR_LEVELS = [
    "100%",
    "80%",
    "70%",
    "50%",
    "30%",
    "0%"
]

ICE_LEVELS = [
    "100%",
    "90%",
    "80%",
    "70%"
]

# =========================================================
# SESSION STATE
# =========================================================

if "cart" not in st.session_state:
    st.session_state.cart = []

if "bill_number" not in st.session_state:
    st.session_state.bill_number = 1


# =========================================================
# HÀM ĐỊNH DẠNG TIỀN
# =========================================================

def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


# =========================================================
# HÀM LẤY SỐ BILL
# =========================================================

def get_bill_number():
    return f"HD{st.session_state.bill_number:04d}"


# =========================================================
# TÍNH TIỀN MỘT MÓN
# =========================================================

def calculate_item_total(item):

    topping_total = sum(
        TOPPINGS[topping]
        for topping in item["toppings"]
    )

    price_per_cup = (
        item["price"] + topping_total
    )

    return price_per_cup * item["quantity"]


# =========================================================
# TÍNH TỔNG HÓA ĐƠN
# =========================================================

def calculate_total():

    return sum(
        calculate_item_total(item)
        for item in st.session_state.cart
    )


# =========================================================
# TẠO ICON MÈO / CHÓ
# =========================================================

def create_pet_icon(bill_number):

    from PIL import Image, ImageDraw

    # Tạo ảnh nền trong suốt
    image = Image.new(
        "RGBA",
        (300, 300),
        (255, 255, 255, 0)
    )

    draw = ImageDraw.Draw(image)

    # -----------------------------------------------------
    # BILL LẺ = MÈO
    # BILL CHẴN = CHÓ
    # -----------------------------------------------------

    if bill_number % 2 == 1:

        # ==============================
        # MÈO
        # ==============================

        # Tai trái
        draw.polygon(
            [
                (65, 95),
                (50, 25),
                (120, 70)
            ],
            fill=(255, 190, 200),
            outline=(90, 70, 70)
        )

        # Tai phải
        draw.polygon(
            [
                (180, 70),
                (250, 25),
                (235, 95)
            ],
            fill=(255, 190, 200),
            outline=(90, 70, 70)
        )

        # Mặt
        draw.ellipse(
            (55, 55, 245, 245),
            fill=(255, 220, 190),
            outline=(90, 70, 70),
            width=6
        )

        # Má trái
        draw.ellipse(
            (70, 165, 115, 200),
            fill=(255, 160, 175)
        )

        # Má phải
        draw.ellipse(
            (185, 165, 230, 200),
            fill=(255, 160, 175)
        )

        # Mắt trái
        draw.ellipse(
            (90, 110, 120, 145),
            fill=(55, 45, 45)
        )

        # Mắt phải
        draw.ellipse(
            (180, 110, 210, 145),
            fill=(55, 45, 45)
        )

        # Chấm sáng mắt
        draw.ellipse(
            (98, 115, 106, 123),
            fill="white"
        )

        draw.ellipse(
            (188, 115, 196, 123),
            fill="white"
        )

        # Mũi
        draw.polygon(
            [
                (140, 150),
                (160, 150),
                (150, 165)
            ],
            fill=(240, 120, 145)
        )

        # Miệng
        draw.arc(
            (130, 155, 150, 180),
            0,
            180,
            fill=(80, 60, 60),
            width=4
        )

        draw.arc(
            (150, 155, 170, 180),
            0,
            180,
            fill=(80, 60, 60),
            width=4
        )

        # Râu trái
        draw.line(
            (100, 155, 35, 145),
            fill=(90, 70, 70),
            width=4
        )

        draw.line(
            (100, 170, 30, 175),
            fill=(90, 70, 70),
            width=4
        )

        # Râu phải
        draw.line(
            (200, 155, 265, 145),
            fill=(90, 70, 70),
            width=4
        )

        draw.line(
            (200, 170, 270, 175),
            fill=(90, 70, 70),
            width=4
        )

    else:

        # ==============================
        # CHÓ
        # ==============================

        # Tai trái
        draw.ellipse(
            (30, 70, 105, 190),
            fill=(170, 125, 90),
            outline=(90, 70, 60),
            width=6
        )

        # Tai phải
        draw.ellipse(
            (195, 70, 270, 190),
            fill=(170, 125, 90),
            outline=(90, 70, 60),
            width=6
        )

        # Mặt
        draw.ellipse(
            (55, 55, 245, 245),
            fill=(225, 185, 135),
            outline=(90, 70, 60),
            width=6
        )

        # Mõm
        draw.ellipse(
            (105, 135, 195, 210),
            fill=(245, 220, 190)
        )

        # Mắt trái
        draw.ellipse(
            (90, 110, 120, 145),
            fill=(50, 45, 40)
        )

        # Mắt phải
        draw.ellipse(
            (180, 110, 210, 145),
            fill=(50, 45, 40)
        )

        # Chấm sáng
        draw.ellipse(
            (98, 115, 106, 123),
            fill="white"
        )

        draw.ellipse(
            (188, 115, 196, 123),
            fill="white"
        )

        # Mũi
        draw.ellipse(
            (130, 145, 170, 175),
            fill=(50, 45, 45)
        )

        # Miệng
        draw.arc(
            (130, 160, 150, 190),
            0,
            180,
            fill=(70, 55, 50),
            width=4
        )

        draw.arc(
            (150, 160, 170, 190),
            0,
            180,
            fill=(70, 55, 50),
            width=4
        )

        # Má
        draw.ellipse(
            (70, 170, 110, 200),
            fill=(255, 170, 170)
        )

        draw.ellipse(
            (190, 170, 230, 200),
            fill=(255, 170, 170)
        )

    return image


# =========================================================
# TẠO PDF HÓA ĐƠN
# =========================================================

def create_pdf():

    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A5
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from reportlab.lib.utils import ImageReader

    buffer = BytesIO()

    # =====================================================
    # FONT
    # =====================================================

    regular_font = "Helvetica"
    bold_font = "Helvetica-Bold"

    regular_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
        "C:/Windows/Fonts/arial.ttf"
    ]

    bold_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf"
    ]

    # Font thường
    for path in regular_paths:

        if os.path.exists(path):

            try:

                pdfmetrics.registerFont(
                    TTFont(
                        "LuckyTeaRegular",
                        path
                    )
                )

                regular_font = "LuckyTeaRegular"

                break

            except Exception:
                pass

    # Font đậm
    for path in bold_paths:

        if os.path.exists(path):

            try:

                pdfmetrics.registerFont(
                    TTFont(
                        "LuckyTeaBold",
                        path
                    )
                )

                bold_font = "LuckyTeaBold"

                break

            except Exception:
                pass

    # =====================================================
    # TẠO CANVAS
    # =====================================================

    c = canvas.Canvas(
        buffer,
        pagesize=A5
    )

    width, height = A5

    y = height - 30

    # =====================================================
    # ICON CHÓ / MÈO
    # =====================================================

    pet_icon = create_pet_icon(
        st.session_state.bill_number
    )

    pet_buffer = BytesIO()

    pet_icon.save(
        pet_buffer,
        format="PNG"
    )

    pet_buffer.seek(0)

    c.drawImage(
        ImageReader(pet_buffer),
        width / 2 - 30,
        y - 5,
        width=60,
        height=60,
        mask="auto"
    )

    y -= 72

    # =====================================================
    # TÊN LUCKY TEA
    # =====================================================

    c.setFont(
        bold_font,
        19
    )

    c.drawCentredString(
        width / 2,
        y,
        "LUCKY TEA"
    )

    y -= 20

    c.setFont(
        regular_font,
        10
    )

    c.drawCentredString(
        width / 2,
        y,
        "HOA DON BAN HANG"
    )

    y -= 22

    # =====================================================
    # THÔNG TIN BILL
    # =====================================================

    bill_number = get_bill_number()

    current_time = datetime.now().strftime(
        "%d/%m/%Y %H:%M"
    )

    c.setFont(
        regular_font,
        9
    )

    c.drawString(
        30,
        y,
        f"So bill: {bill_number}"
    )

    y -= 14

    c.drawString(
        30,
        y,
        f"Thoi gian: {current_time}"
    )

    y -= 18

    # =====================================================
    # ĐƯỜNG KẺ
    # =====================================================

    c.line(
        30,
        y,
        width - 30,
        y
    )

    y -= 18

    # =====================================================
    # DANH SÁCH MÓN
    # =====================================================

    for index, item in enumerate(
        st.session_state.cart,
        start=1
    ):

        item_total = calculate_item_total(item)

        # -----------------------------------------------
        # TÊN MÓN
        # -----------------------------------------------

        c.setFont(
            bold_font,
            9
        )

        c.drawString(
            30,
            y,
            f"{index}. {item['name']}"
        )

        y -= 14

        # -----------------------------------------------
        # SỐ LƯỢNG
        # -----------------------------------------------

        c.setFont(
            regular_font,
            8
        )

        c.drawString(
            42,
            y,
            f"SL: {item['quantity']} x "
            f"{format_money(item['price'])}"
        )

        y -= 13

        # -----------------------------------------------
        # ĐƯỜNG / ĐÁ
        # -----------------------------------------------

        c.drawString(
            42,
            y,
            f"Duong: {item['sugar']} | "
            f"Da: {item['ice']}"
        )

        y -= 13

        # -----------------------------------------------
        # TOPPING
        # -----------------------------------------------

        if item["toppings"]:

            topping_text = ", ".join(
                item["toppings"]
            )

            c.drawString(
                42,
                y,
                f"Topping: {topping_text}"
            )

            y -= 13

        # -----------------------------------------------
        # THÀNH TIỀN
        # -----------------------------------------------

        c.setFont(
            bold_font,
            8
        )

        c.drawRightString(
            width - 30,
            y,
            format_money(item_total)
        )

        y -= 18

        # Nếu hóa đơn dài
        if y < 70:

            c.showPage()

            c.setFont(
                regular_font,
                9
            )

            y = height - 35

    # =====================================================
    # TỔNG TIỀN
    # =====================================================

    c.line(
        30,
        y,
        width - 30,
        y
    )

    y -= 22

    total = calculate_total()

    c.setFont(
        bold_font,
        12
    )

    c.drawString(
        30,
        y,
        "TONG THANH TOAN"
    )

    c.drawRightString(
        width - 30,
        y,
        format_money(total)
    )

    y -= 30

    # =====================================================
    # LỜI CẢM ƠN
    # =====================================================

    c.setFont(
        regular_font,
        9
    )

    c.drawCentredString(
        width / 2,
        y,
        "Cam on quy khach!"
    )

    y -= 14

    c.drawCentredString(
        width / 2,
        y,
        "Hen gap lai tai Lucky Tea"
    )

    # =====================================================
    # LƯU PDF
    # =====================================================

    c.save()

    buffer.seek(0)

    return buffer


# =========================================================
# ẢNH CHÍNH PHOTO1.JPG
# =========================================================

image_path = "photo1.jpg"

if os.path.exists(image_path):

    st.image(
        image_path,
        use_container_width=True
    )

else:

    st.warning(
        "Không tìm thấy ảnh photo1.jpg"
    )


# =========================================================
# HEADER LUCKY TEA
# =========================================================

st.markdown(
    """
    <div class="lucky-title">
        🧋 LUCKY TEA
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="lucky-subtitle">
        Đặt món • Tùy chỉnh • Tính tiền • Xuất hóa đơn
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# KHU VỰC CHỌN MÓN
# =========================================================

left_col, right_col = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# CHỌN TRÀ SỮA
# =========================================================

with left_col:

    st.subheader("🧋 Chọn thức uống")

    drink = st.selectbox(
        "Loại trà sữa",
        list(MENU.keys())
    )

    price = MENU[drink]

    st.info(
        f"Giá một ly: **{format_money(price)}**"
    )

    quantity = st.number_input(
        "Số lượng",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )


# =========================================================
# ĐƯỜNG / ĐÁ
# =========================================================

with right_col:

    st.subheader("⚙️ Tùy chỉnh")

    sugar = st.select_slider(
        "🍬 Mức độ đường",
        options=SUGAR_LEVELS,
        value="70%"
    )

    ice = st.select_slider(
        "🧊 Mức độ đá",
        options=ICE_LEVELS,
        value="100%"
    )


# =========================================================
# TOPPING
# =========================================================

st.subheader("🍡 Thêm topping")

toppings = st.multiselect(
    "Chọn topping",
    list(TOPPINGS.keys())
)

if toppings:

    topping_total = sum(
        TOPPINGS[topping]
        for topping in toppings
    )

    st.info(
        "Topping: "
        + ", ".join(toppings)
        + f" | Phụ thu: **{format_money(topping_total)}**"
    )


# =========================================================
# TÍNH TIỀN MÓN ĐANG CHỌN
# =========================================================

current_topping_total = sum(
    TOPPINGS[topping]
    for topping in toppings
)

current_item_total = (
    price + current_topping_total
) * quantity

st.markdown(
    f"""
    <div class="total-box">
        <div class="total-title">
            Thành tiền món đang chọn
        </div>
        <div class="total-money">
            {format_money(current_item_total)}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# THÊM MÓN
# =========================================================

if st.button(
    "➕ THÊM MÓN VÀO HÓA ĐƠN",
    use_container_width=True
):

    new_item = {
        "name": drink,
        "price": price,
        "quantity": quantity,
        "toppings": toppings.copy(),
        "sugar": sugar,
        "ice": ice
    }

    st.session_state.cart.append(
        new_item
    )

    st.success(
        f"Đã thêm {quantity} ly {drink} vào hóa đơn!"
    )

    st.rerun()


# =========================================================
# HÓA ĐƠN HIỆN TẠI
# =========================================================

st.divider()

st.markdown(
    f"""
    <div class="bill-number">
        🧾 HÓA ĐƠN {get_bill_number()}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHƯA CÓ MÓN
# =========================================================

if len(st.session_state.cart) == 0:

    st.info(
        "🧾 Chưa có món nào trong hóa đơn."
    )


# =========================================================
# HIỂN THỊ HÓA ĐƠN
# =========================================================

else:

    for index, item in enumerate(
        st.session_state.cart
    ):

        item_total = calculate_item_total(item)

        with st.container(
            border=True
        ):

            col1, col2, col3 = st.columns(
                [4, 2, 1]
            )

            # -------------------------------------------
            # THÔNG TIN MÓN
            # -------------------------------------------

            with col1:

                st.markdown(
                    f"### {index + 1}. {item['name']}"
                )

                st.write(
                    f"🍬 Đường: **{item['sugar']}**"
                )

                st.write(
                    f"🧊 Đá: **{item['ice']}**"
                )

                if item["toppings"]:

                    st.write(
                        "🍡 Topping: "
                        + ", ".join(
                            item["toppings"]
                        )
                    )

                else:

                    st.write(
                        "🍡 Topping: Không"
                    )

            # -------------------------------------------
            # SỐ LƯỢNG
            # -------------------------------------------

            with col2:

                st.write("Số lượng")

                st.markdown(
                    f"### {item['quantity']}"
                )

                st.write(
                    "Đơn giá: "
                    + format_money(
                        item["price"]
                    )
                )

            # -------------------------------------------
            # THÀNH TIỀN
            # -------------------------------------------

            with col3:

                st.write("Thành tiền")

                st.markdown(
                    f"### {format_money(item_total)}"
                )

            # -------------------------------------------
            # XÓA MÓN
            # -------------------------------------------

            if st.button(
                "🗑️ Xóa món này",
                key=f"delete_{index}",
                use_container_width=True
            ):

                st.session_state.cart.pop(
                    index
                )

                st.rerun()


    # =====================================================
    # TỔNG TIỀN
    # =====================================================

    total = calculate_total()

    st.markdown(
        f"""
        <div class="total-box">
            <div class="total-title">
                💰 TỔNG THANH TOÁN
            </div>
            <div class="total-money">
                {format_money(total)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # XUẤT HÓA ĐƠN
    # =====================================================

    st.subheader("🧾 Xuất hóa đơn")

    try:

        pdf_file = create_pdf()

        st.download_button(
            label="📄 XUẤT HÓA ĐƠN PDF",
            data=pdf_file,
            file_name=f"{get_bill_number()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as error:

        st.error(
            "Không thể tạo hóa đơn PDF."
        )

        st.code(
            str(error)
        )


    # =====================================================
    # THANH TOÁN
    # =====================================================

    st.divider()

    if st.button(
        "💰 THANH TOÁN & TẠO BILL MỚI",
        use_container_width=True
    ):

        st.session_state.cart = []

        st.session_state.bill_number += 1

        st.success(
            "✅ Thanh toán thành công! "
            f"Bill {get_bill_number()} đã được tạo."
        )

        st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;">
        🧋 <b>Lucky Tea</b><br>
        Cảm ơn quý khách đã ủng hộ 💕
    </div>
    """,
    unsafe_allow_html=True
)
