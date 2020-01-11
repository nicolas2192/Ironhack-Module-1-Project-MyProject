import smtplib
from email.message import EmailMessage


def send_mail(recipient):
    sender = ""
    password = ""

    msg = EmailMessage()
    msg["Subject"] = "Analysis by Sector and Gender"
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content("""
                    Hello,
                    Find attached to this email 4 graphs and the database used to generate them.
                    
                    Regards,
                    Nicolas Cortinas.
                    """)

    files = ["data/results/Gender_PieChart.png", "data/results/Sector_BarChart.png", "data/results/data_table.csv",
             "data/results/SectorGenderAmount_BarChart.png", "data/results/SectorGenderMoney_BarChart.png"]
    for file in files:
        with open(file, mode="rb") as f:  # Reading the file in binary mode
            file_data = f.read()
            file_type = f.name[-3:]  # imghdr.what(f.name) only work on images
            file_name = f.name

        msg.add_attachment(file_data, maintype="application", subtype="octer-stream", filename=file_name)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)  # setting server and port
    server.login(sender, password)  # login to the account
    server.send_message(msg)  # sending email
    server.quit()  # ends up the connexion

    print(f"email sent to {recipient}")
