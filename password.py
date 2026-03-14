import customtkinter as ctk
from Password_checker.code.password_importer import score
from Password_checker.code.qr_generator.qr_code import generate_qr
from database.db_entry import log_event
from database.integrity import store_fingerprint


def open_password_window(parent):

    window = ctk.CTkToplevel(parent)
    window.geometry("700x400")
    window.title("Password Strength Checker")
    
    window.focus()
    window.grab_set()
    window.lift()

    left_frame = ctk.CTkFrame(window)
    right_frame = ctk.CTkFrame(window)

    left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)
    window.grid_rowconfigure(0, weight=1)

    def gen_qr(password):

        if password == "":
            print("No password entered")
            return

        img = generate_qr(password).get_image()

        ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=(200, 200))

        qr_label = ctk.CTkLabel(right_frame, image=ctk_img, text="")
        qr_label.image = ctk_img
        qr_label.pack(pady=20)

        gen_button.configure(state="disabled")

        window.after(
            5000,
            lambda: [qr_label.destroy(), gen_button.configure(state="normal")]
        )

        sco = score(password)[-1]
        log_event("QR Generation", int(sco))
        store_fingerprint()

    def checkpass(password):

        result = score(password)

        label1.configure(text="")
        label2.configure(text="")
        label3.configure(text="")
        label4.configure(text="")
        label5.configure(text="")

        if result[1]:
            label1.configure(text="⚠️ Too Common")
        else:
            label1.configure(text="✔️ Not Common")

        if not result[3]:
            label2.configure(text="⚠️ No upper case characters")
        else:
            label2.configure(text="✔️ Contains upper case characters")

        if not result[4]:
            label3.configure(text="⚠️ No lower case characters")
        else:
            label3.configure(text="✔️ Contains lower case characters")

        if not result[5]:
            label4.configure(text="⚠️ No digits")
        else:
            label4.configure(text="✔️ Contains digits")

        if not result[6]:
            label5.configure(text="⚠️ No special characters")
        else:
            label5.configure(text="✔️ Contains special characters")

        label6.configure(text=f"Entropy Score = {int(result[-1])}")

        sco = result[-1]
        log_event("Password Strength Check", int(sco))
        store_fingerprint()

    password_entry = ctk.CTkEntry(
        left_frame,
        placeholder_text="Enter your Password",
        show="*"
    )
    password_entry.pack(pady=20)

    show_var = ctk.BooleanVar()

    def toggle_password():
        if show_var.get():
            password_entry.configure(show="")
        else:
            password_entry.configure(show="*")

    show_checkbox = ctk.CTkCheckBox(
        left_frame,
        text="Show Password",
        variable=show_var,
        command=toggle_password
    )
    show_checkbox.pack(pady=5)

    check_button = ctk.CTkButton(
        left_frame,
        text="Submit",
        command=lambda: checkpass(password_entry.get())
    )
    check_button.pack(pady=10)

    window.bind("<Return>", lambda event: checkpass(password_entry.get()))

    gen_button = ctk.CTkButton(
        right_frame,
        text="Generate QR Code",
        command=lambda: gen_qr(password_entry.get())
    )
    gen_button.pack(pady=10)

    label1 = ctk.CTkLabel(left_frame, text="")
    label1.pack()

    label2 = ctk.CTkLabel(left_frame, text="")
    label2.pack()

    label3 = ctk.CTkLabel(left_frame, text="")
    label3.pack()

    label4 = ctk.CTkLabel(left_frame, text="")
    label4.pack()

    label5 = ctk.CTkLabel(left_frame, text="")
    label5.pack()

    label6 = ctk.CTkLabel(left_frame, text="")
    label6.pack()