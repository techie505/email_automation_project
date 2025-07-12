import csv
import time
import os
from email_sender import send_email
from spam_filter import is_spam

with open("templates/email_template.txt", "r") as f:
    template = f.read()

with open("emails.csv", "r") as f:
    recipients = list(csv.DictReader(f))

attachment_files = [os.path.join("attachments", "5th sem.pdf")]

batch_size = int(input("How many emails do you want to send in one batch? "))
delay_choice = input("Do you want to delay sending? (yes/no): ").strip().lower()

delay_seconds = 0
if delay_choice == "yes":
    delay_amount = float(input("Enter delay between batches: "))
    delay_unit = input("Is that in seconds, minutes, or hours? ").strip().lower()

    if delay_unit == "seconds":
        delay_seconds = delay_amount
    elif delay_unit == "minutes":
        delay_seconds = delay_amount * 60
    elif delay_unit == "hours":
        delay_seconds = delay_amount * 3600
    else:
        print("Invalid time unit. Using 0 delay.")

repeat_times = int(input("How many additional times do you want to resend this batch? "))
total_batches = repeat_times + 1

for cycle in range(total_batches):
    print(f"Sending batch {cycle + 1} of {total_batches}...")

    for i, row in enumerate(recipients[:batch_size]):
        name = row["name"]
        email = row["email"]
        body = template.format(name=name)

        if is_spam(body):
            print(f"Message to {name} not sent: Detected as SPAM.")
        else:
            send_email(email, name, body, attachment_files)

        time.sleep(8)

    if cycle < total_batches - 1:
        print(f"Waiting {delay_seconds} seconds before next batch...")
        time.sleep(delay_seconds)

print("All batches sent as per schedule.")
