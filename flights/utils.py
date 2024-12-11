from django.core.mail import send_mail


def send_test_email(message="This is a test email sent from Django."):
    subject = "Test Email"
    from_email = ""
    recipient_list = [""]

    try:
        send_mail(subject, message, from_email, recipient_list)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")
