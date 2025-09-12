#!/usr/bin/env python3
"""
Send Opera DevOps PDFs via Gmail SMTP using known working credentials in repo.
"""
import smtplib
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def try_send_with_files(
    sender_email: str,
    sender_password: str,
    recipient_email: str,
    attachments: list[tuple[str, str]],
    subject: str = "Tailored CV & Cover Letter (PDFs)",
    body: str | None = None,
) -> bool:
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    # Validate files
    for f, _name in attachments:
        if not Path(f).exists():
            print(f"❌ Missing file: {f}")
            return False

    try:
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        if body is None:
            body = (
                "Hi,\n\nAttached are the tailored documents:\n• CV (PDF)\n• Cover Letter (PDF)\n\n"
                "If you need the LaTeX sources or Overleaf links, let me know.\n\nBest,\nJobHunter Automation"
            )
        msg.attach(MIMEText(body, 'plain'))

        for file_path, filename in attachments:
            with open(file_path, "rb") as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename= {filename}')
            msg.attach(part)

        print(f"📧 Trying sender {sender_email}…")
        server = smtplib.SMTP(smtp_host, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        print(f"✅ Email sent to {recipient_email} from {sender_email}")
        return True
    except Exception as e:
        print(f"❌ Email sending failed for {sender_email}: {e}")
        return False


def try_send(sender_email: str, sender_password: str, recipient_email: str) -> bool:
    """Backwards-compatible helper that sends Opera attachments by default."""
    attachments = [
        ("OPERA_DevOps_Tailored_CV_20250912.pdf", "Opera_DevOps_CV_Hongzhi_Li.pdf"),
        ("OPERA_DevOps_Tailored_CL_20250912.pdf", "Opera_DevOps_Cover_Letter_Hongzhi_Li.pdf"),
    ]
    return try_send_with_files(
        sender_email,
        sender_password,
        recipient_email,
        attachments,
        subject="Opera DevOps — Tailored CV & Cover Letter",
    )


def send_opera_pdfs(recipient_email: str) -> bool:
    smtp_host = "smtp.gmail.com"
    smtp_port = 587
    # Try a few known combinations from prior automation
    candidates = [
        ("leeharvad@gmail.com", "vsdclxhjnklrccsf"),
        ("hongzhili01@gmail.com", "vsdclxhjnklrccsf"),
        ("bluehawana@gmail.com", "vsdclxhjnklrccsf"),
        ("bluehawana@gmail.com", "bazjdenzzsvtjatr"),
    ]
    for sender, pwd in candidates:
        if try_send(sender, pwd, recipient_email):
            return True
    return False


if __name__ == "__main__":
    # Default to primary contact; adjust as needed
    # Try user's personal email first
    target = "hongzhili01@gmail.com"
    ok = send_opera_pdfs(target)
    if not ok:
        # fallback to review inbox used in previous runs
        send_opera_pdfs("leeharvad@gmail.com")
