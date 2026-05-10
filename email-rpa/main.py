import os
from imap_tools import MailBox
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = os.getenv("IMAP_SERVER")

DOWNLOAD_FOLDER = "downloads"

# Create downloads folder if not exists
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

print("Starting RPA Bot...")
print("Connecting to mailbox...")

with MailBox(IMAP_SERVER).login(EMAIL, PASSWORD) as mailbox:

    print("Connected successfully")
    print("Fetching and processing emails...")

    email_count = 0

    # Fetch emails newest first
    # Change limit as needed
    for msg in mailbox.fetch(reverse=True, limit=2000):

        email_count += 1

        print("\n--------------------------------")
        print(f"Email #{email_count}")
        print("Subject:", msg.subject)

        # Skip emails without attachments
        if not msg.attachments:
            print("No attachments found")
            continue

        print(f"Found {len(msg.attachments)} attachment(s)")

        # Process attachments
        for attachment in msg.attachments:

            filename = attachment.filename

            print("Attachment:", filename)

            # Skip invalid filenames
            if not filename or filename.strip() == "":
                print("Skipped invalid filename")
                continue

            # Remove invalid Windows filename characters
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

            # Avoid duplicate downloads
            if os.path.exists(file_path):
                print("File already exists, skipping")
                continue

            # Save attachment
            with open(file_path, 'wb') as f:
                f.write(attachment.payload)

            print(f"Downloaded: {filename}")

print("\nRPA Job Completed")