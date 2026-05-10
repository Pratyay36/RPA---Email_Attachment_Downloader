import os
from imap_tools import MailBox
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")

DOWNLOAD_FOLDER = "downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

print("Starting RPA Bot...")
print("Connecting to mailbox...")

with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD) as mailbox:

    print("Connected successfully")
    print("Fetching and processing emails...")

    email_count = 0

    for msg in mailbox.fetch(reverse=True, limit=2000):

        email_count += 1

        print("\n--------------------------------")
        print(f"Email #{email_count}")
        print("Subject:", msg.subject)

        if not msg.attachments:
            print("No attachments found")
            continue

        print(f"Found {len(msg.attachments)} attachment(s)")

        for attachment in msg.attachments:

            filename = attachment.filename

            print("Attachment:", filename)

            if not filename or filename.strip() == "":
                print("Skipped invalid filename")
                continue

            filename = (
                filename
                .replace("/", "_")
                .replace("\\", "_")
                .replace(":", "_")
                .replace("*", "_")
                .replace("?", "_")
                .replace("\"", "_")
                .replace("<", "_")
                .replace(">", "_")
                .replace("|", "_")
            )

            file_path = os.path.join(
                DOWNLOAD_FOLDER,
                filename
            )

            if os.path.exists(file_path):
                print("File already exists, skipping")
                continue

            with open(file_path, 'wb') as f:
                f.write(attachment.payload)

            print(f"Downloaded: {filename}")

print("\nRPA Job Completed")
