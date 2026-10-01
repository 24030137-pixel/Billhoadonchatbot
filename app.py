import streamlit as st
from datetime import datetime
from io import BytesIO
import os


# =========================================================
# CAU HINH TRANG
# =========================================================

st.set_page_config(
    page_title="Lucky Tea",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CSS
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
# MENU TRA SUA
# =========================================================

MENU = {
    "Tra sua truyen thong": 25000,
    "Tra sua tran chau": 30000,
    "Tra sua matcha": 30000,
    "Tra sua socola": 30000,
    "Tra sua khoai mon": 32000,
    "Tra sua dau": 30000,
    "Tra dao": 28000,
    "Tra vai": 28000,
    "Tra chanh": 20000,
    "Tra tac": 20000,
}


# =========================================================
# TOPPING
# =========================================================

TOPPINGS = {
    "Tran chau den": 5000,
    "Tran chau trang": 5000,
    "Thach dua": 5000,
    "Thach trai cay": 5000,
    "Pudding trung": 7000,
    "Kem cheese": 8000,
    "Tran chau hoang kim": 7000,
    "Hat thuy tinh": 6000,
}


# =========================================================
# MUC DUONG
# =========================================================

SUGAR_LEVELS = [
    "100%",
    "80%",
    "70%",
    "50%",
    "30%",
    "0%"
]


# =========================================================
# MUC DA
# =========================================================

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
# HAM DINH DANG TIEN
# =========================================================

def format_money(number):
    return f"{number:,.0f} VNĐ".replace(",", ".")


def format_money_pdf(number):
    """
    PDF dung chu khong dau.
    """
    return f"{number:,.0f} VND".replace(",", ".")


# =========================================================
# SO BILL
# =========================================================

def get_bill_number():
    return f"HD{st.session_state.bill_number:04d}"


# =========================================================
# TINH TIEN TOPPING CHO 1 LY
# =========================================================

def calculate_topping_total(item):

    return sum(
        TOPPINGS[topping]
        for topping in item["toppings"]
    )


# =========================================================
# TINH TIEN 1 LOAI TRA SUA
# =========================================================

def calculate_item_total(item):

    topping_price_one_cup = calculate_topping_total(item)

    price_one_cup = (
        item["price"] +
        topping_price_one_cup
    )

    return price_one_cup * item["quantity"]


# =========================================================
# TINH TONG HOA DON
# =========================================================

def calculate_total():

    return sum(
        calculate_item_total(item)
        for item in st.session_state.cart
    )


# =========================================================
# TAO ICON CHO / MEO
# =========================================================

def create_pet_icon(bill_number):

    from PIL import Image, ImageDraw

    image = Image.new(
        "RGBA",
        (300, 300),
        (255, 255, 255, 0)
    )

    draw = ImageDraw.Draw(image)

    # =====================================================
    # BILL LE = MEO
    # =====================================================

    if bill_number % 2 == 1:

        # Tai trai
        draw.polygon(
            [
                (65, 95),
                (50, 25),
                (120, 70)
            ],
            fill=(255, 190, 200),
            outline=(90, 70, 70)
        )

        # Tai phai
        draw.polygon(
            [
                (180, 70),
                (250, 25),
                (235, 95)
            ],
            fill=(255, 190, 200),
            outline=(90, 70, 70)
        )

        # Mat
        draw.ellipse(
            (55, 55, 245, 245),
            fill=(255, 220, 190),
            outline=(90, 70, 70),
            width=6
        )

        # Ma
        draw.ellipse(
            (70, 165, 115, 200),
            fill=(255, 160, 175)
        )

        draw.ellipse(
            (185, 165, 230, 200),
            fill=(255, 160, 175)
        )

        # Mat
        draw.ellipse(
            (90, 110, 120, 145),
            fill=(55, 45, 45)
        )

        draw.ellipse(
            (180, 110, 210, 145),
            fill=(55, 45, 45)
        )

        # Diem sang
        draw.ellipse(
            (98, 115, 106, 123),
            fill="white"
        )

        draw.ellipse(
            (188, 115, 196, 123),
            fill="white"
        )

        # Mui
        draw.polygon(
            [
                (140, 150),
                (160, 150),
                (150, 165)
            ],
            fill=(240, 120, 145)
        )

        # Mieng
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

        # Rau
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

    # =====================================================
    # BILL CHAN = CHO
    # =====================================================

    else:

        # Tai trai
        draw.ellipse(
            (30, 70, 105, 190),
            fill=(170, 125, 90),
            outline=(90, 70, 60),
            width=6
        )

        # Tai phai
        draw.ellipse(
            (195, 70, 270, 190),
            fill=(170, 125, 90),
            outline=(90, 70, 60),
            width=6
        )

        # Mat
        draw.ellipse(
            (55, 55, 245, 245),
            fill=(225, 185, 135),
            outline=(90, 70, 60),
            width=6
        )

        # Mom
        draw.ellipse(
            (105, 135, 195, 210),
            fill=(245, 220, 190)
        )

        # Mat
        draw.ellipse(
            (90, 110, 120, 145),
            fill=(50, 45, 40)
        )

        draw.ellipse(
            (180, 110, 210, 145),
            fill=(50, 45, 40)
        )

        # Diem sang
        draw.ellipse(
            (98, 115, 106, 123),
            fill="white"
        )

        draw.ellipse(
            (188, 115, 196, 123),
            fill="white"
        )

        # Mui
        draw.ellipse(
            (130, 145, 170, 175),
            fill=(50, 45, 45)
        )

        # Mieng
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

        # Ma
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
# TAO PDF HOA DON
# TOAN BO NOI DUNG PDF KHONG DAU
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

    # Font thuong
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

    # Font dam
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
    # KHO GIAY A5
    # =====================================================

    c = canvas.Canvas(
        buffer,
        pagesize=A5
    )

    width, height = A5

    y = height - 30

    # =====================================================
    # ICON
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
    # LUCKY TEA
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
    # THONG TIN BILL
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
    # DUONG KE
    # =====================================================

    c.line(
        30,
        y,
        width - 30,
        y
    )

    y -= 18

    # =====================================================
    # DANH SACH MON
    # =====================================================

    for index, item in enumerate(
        st.session_state.cart,
        start=1
    ):

        # Gia topping tren 1 ly
        topping_total_one_cup = calculate_topping_total(item)

        # Gia 1 ly
        price_one_cup = (
            item["price"] +
            topping_total_one_cup
        )

        # Tong mon
        item_total = calculate_item_total(item)

        # -------------------------------------------------
        # TEN MON
        # -------------------------------------------------

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

        # -------------------------------------------------
        # GIA TRA SUA
        # -------------------------------------------------

        c.setFont(
            regular_font,
            8
        )

        c.drawString(
            42,
            y,
            f"Tra sua: {format_money_pdf(item['price'])}/ly"
        )

        y -= 13

        # -------------------------------------------------
        # SO LUONG
        # -------------------------------------------------

        c.drawString(
            42,
            y,
            f"So luong: {item['quantity']} ly"
        )

        y -= 13

        # -------------------------------------------------
        # DUONG / DA
        # -------------------------------------------------

        c.drawString(
            42,
            y,
            f"Duong: {item['sugar']} | Da: {item['ice']}"
        )

        y -= 13

        # -------------------------------------------------
        # TOPPING
        # -------------------------------------------------

        if item["toppings"]:

            c.setFont(
                bold_font,
                8
            )

            c.drawString(
                42,
                y,
                "Topping:"
            )

            y -= 12

            c.setFont(
                regular_font,
                8
            )

            for topping in item["toppings"]:

                topping_price = TOPPINGS[topping]

                c.drawString(
                    50,
                    y,
                    f"- {topping}: "
                    f"{format_money_pdf(topping_price)}/ly"
                )

                y -= 12

        else:

            c.setFont(
                regular_font,
                8
            )

            c.drawString(
                42,
                y,
                "Topping: Khong"
            )

            y -= 13

        # -------------------------------------------------
        # GIA 1 LY SAU TOPPING
        # -------------------------------------------------

        c.setFont(
            bold_font,
            8
        )

        c.drawString(
            42,
            y,
            f"Gia 1 ly sau topping: "
            f"{format_money_pdf(price_one_cup)}"
        )

        y -= 13

        # -------------------------------------------------
        # THANH TIEN
        # -------------------------------------------------

        c.drawRightString(
            width - 30,
            y,
            f"Thanh tien: {format_money_pdf(item_total)}"
        )

        y -= 20

        # -------------------------------------------------
        # XU LY BILL DAI
        # -------------------------------------------------

        if y < 70:

            c.showPage()

            y = height - 35

            c.setFont(
                regular_font,
                9
            )

    # =====================================================
    # TONG HOA DON
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
        format_money_pdf(total)
    )

    y -= 30

    # =====================================================
    # LOI CAM ON
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
    # LUU PDF
    # =====================================================

    c.save()

    buffer.seek(0)

    return buffer


# =========================================================
# ANH CHINH
# =========================================================

image_path = "photo1.jpg"

if os.path.exists(image_path):

    st.image(
        image_path,
        use_container_width=True
    )

else:

    st.warning(
        "Khong tim thay anh photo1.jpg"
    )


# =========================================================
# HEADER
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
        Dat mon • Tuy chinh • Tinh tien • Xuat hoa don
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# KHU VUC CHON MON
# =========================================================

left_col, right_col = st.columns(
    [1, 1],
    gap="large"
)


# =========================================================
# CHON TRA SUA
# =========================================================

with left_col:

    st.subheader("🧋 Chon thuc uong")

    drink = st.selectbox(
        "Loai tra sua",
        list(MENU.keys())
    )

    price = MENU[drink]

    st.info(
        f"Gia mot ly: **{format_money(price)}**"
    )

    quantity = st.number_input(
        "So luong",
        min_value=1,
        max_value=50,
        value=1,
        step=1
    )


# =========================================================
# DUONG / DA
# =========================================================

with right_col:

    st.subheader("⚙️ Tuy chinh")

    sugar = st.select_slider(
        "🍬 Muc do duong",
        options=SUGAR_LEVELS,
        value="70%"
    )

    ice = st.select_slider(
        "🧊 Muc do da",
        options=ICE_LEVELS,
        value="100%"
    )


# =========================================================
# TOPPING CHO RIENG MON DANG CHON
# =========================================================

st.subheader("🍡 Topping cho mon nay")

toppings = st.multiselect(
    "Chon topping",
    list(TOPPINGS.keys()),
    key="current_toppings"
)


# =========================================================
# HIEN THI TOPPING VA GIA
# =========================================================

current_topping_total = sum(
    TOPPINGS[topping]
    for topping in toppings
)

if toppings:

    st.info(
        "Topping da chon: "
        + ", ".join(toppings)
        + f" | Them {format_money(current_topping_total)}/ly"
    )

else:

    st.caption(
        "Mon nay khong co topping."
    )


# =========================================================
# TINH GIA MON DANG CHON
# =========================================================

current_price_one_cup = (
    price +
    current_topping_total
)

current_item_total = (
    current_price_one_cup *
    quantity
)


st.markdown(
    f"""
    <div class="total-box">
        <div class="total-title">
            Thanh tien mon dang chon
        </div>

        <div class="total-money">
            {format_money(current_item_total)}
        </div>

        <div>
            {format_money(current_price_one_cup)} / ly
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# THEM MON VAO BILL
# =========================================================

if st.button(
    "➕ THEM MON VAO HOA DON",
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
        f"Da them {quantity} ly {drink} vao hoa don!"
    )

    # Reset topping sau khi them
    st.session_state.current_toppings = []

    st.rerun()


# =========================================================
# HOA DON HIEN TAI
# =========================================================

st.divider()

st.markdown(
    f"""
    <div class="bill-number">
        🧾 HOA DON {get_bill_number()}
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# CHUA CO MON
# =========================================================

if len(st.session_state.cart) == 0:

    st.info(
        "🧾 Chua co mon nao trong hoa don."
    )


# =========================================================
# CO MON
# =========================================================

else:

    # =====================================================
    # HIEN THI TUNG MON
    # =====================================================

    for index, item in enumerate(
        st.session_state.cart
    ):

        item_total = calculate_item_total(item)

        topping_total_one_cup = calculate_topping_total(
            item
        )

        with st.container(
            border=True
        ):

            col1, col2, col3 = st.columns(
                [4, 2, 1]
            )

            # ------------------------------------------------
            # THONG TIN MON
            # ------------------------------------------------

            with col1:

                st.markdown(
                    f"### {index + 1}. {item['name']}"
                )

                st.write(
                    f"🍬 Duong: **{item['sugar']}**"
                )

                st.write(
                    f"🧊 Da: **{item['ice']}**"
                )

                if item["toppings"]:

                    st.write(
                        "🍡 Topping: "
                        + ", ".join(
                            item["toppings"]
                        )
                    )

                    st.caption(
                        "Tien topping moi ly: "
                        + format_money(
                            topping_total_one_cup
                        )
                    )

                else:

                    st.write(
                        "🍡 Topping: Khong"
                    )

            # ------------------------------------------------
            # SO LUONG
            # ------------------------------------------------

            with col2:

                st.write(
                    "So luong"
                )

                st.markdown(
                    f"### {item['quantity']} ly"
                )

                st.write(
                    "Gia tra sua: "
                    + format_money(
                        item["price"]
                    )
                )

            # ------------------------------------------------
            # THANH TIEN
            # ------------------------------------------------

            with col3:

                st.write(
                    "Thanh tien"
                )

                st.markdown(
                    f"### {format_money(item_total)}"
                )

            # ------------------------------------------------
            # XOA MON
            # ------------------------------------------------

            if st.button(
                "🗑️ Xoa mon nay",
                key=f"delete_{index}",
                use_container_width=True
            ):

                st.session_state.cart.pop(
                    index
                )

                st.rerun()


    # =====================================================
    # TONG TIEN
    # =====================================================

    total = calculate_total()

    st.markdown(
        f"""
        <div class="total-box">
            <div class="total-title">
                💰 TONG THANH TOAN
            </div>

            <div class="total-money">
                {format_money(total)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


    # =====================================================
    # XUAT HOA DON
    # =====================================================

    st.subheader("🧾 Xuat hoa don")

    try:

        pdf_file = create_pdf()

        st.download_button(
            label="📄 XUAT HOA DON PDF",
            data=pdf_file,
            file_name=f"{get_bill_number()}.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as error:

        st.error(
            "Khong the tao hoa don PDF."
        )

        st.code(
            str(error)
        )


    # =====================================================
    # THANH TOAN
    # =====================================================

    st.divider()

    if st.button(
        "💰 THANH TOAN & TAO BILL MOI",
        use_container_width=True
    ):

        st.session_state.cart = []

        st.session_state.bill_number += 1

        st.success(
            "Thanh toan thanh cong!"
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
        Cam on quy khach da ung ho 💕
    </div>
    """,
    unsafe_allow_html=True
)
