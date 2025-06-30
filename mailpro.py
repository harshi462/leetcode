from collections import deque
import time
import uuid

class Email:
    def __init__(self, to, subject, timestamp):
        self.id = str(uuid.uuid4())[:8]  # Unique ID
        self.to = to
        self.subject = subject
        self.timestamp = timestamp  # UNIX timestamp
        self.created_at = int(time.time())

    def __str__(self):
        return f"[{self.id}] To: {self.to}, Subject: '{self.subject}', Scheduled: {time.ctime(self.timestamp)}"

class EmailScheduler:
    def __init__(self):
        self.queue = deque()

    def schedule_email(self, to, subject, delay_sec):
        send_time = int(time.time()) + delay_sec
        email = Email(to, subject, send_time)
        self.queue.append(email)
        print(f"✅ Email Scheduled:\n{email}\n")

    def cancel_email(self, search_term):
    # Find all emails that match the search term (either by recipient or subject)
        matched_emails = [email for email in self.queue if search_term in email.to or search_term in email.subject]

        if not matched_emails:
              print("⚠️ No emails found with that recipient or subject.")
              return

    # If multiple emails are found, let the user choose
        if len(matched_emails) > 1:
            print("Multiple emails found. Please select the email to cancel:")
            for i, email in enumerate(matched_emails, start=1):
                 print(f"{i}. {email}")
                 
            choice = int(input("Enter the number of the email to cancel: "))
            email_to_cancel = matched_emails[choice - 1]
        else:
           email_to_cancel = matched_emails[0]

    # Cancel the email by removing it from the queue
        self.queue = deque([email for email in self.queue if email != email_to_cancel])
        print(f"❌ Email Cancelled:\n{email_to_cancel}\n")



    def reschedule_email(self, email_id, new_delay_sec):
        for email in self.queue:
            if email.id == email_id:
                email.timestamp = int(time.time()) + new_delay_sec
                print(f"🔁 Email Rescheduled:\n{email}\n")
                return
        print("⚠️ Email ID not found.")

    def process_emails(self):
        current_time = int(time.time())
        while self.queue and self.queue[0].timestamp <= current_time:
            email = self.queue.popleft()
            print(f"📤 Email Sent:\n{email}\n")

    def view_queue(self):
        if not self.queue:
            print("📭 No scheduled emails.\n")
            return
        print("📅 Scheduled Emails:")
        for email in self.queue:
            print(email)
        print()



def run_scheduler():
    scheduler = EmailScheduler()

    while True:
        print("Options: [1] Schedule  [2] Cancel  [3] Reschedule  [4] View Queue  [5] Process Emails  [6] Exit")
        choice = input("Enter choice: ")
    
        if choice == '1':
            to = input("Enter recipient email: ")
            subject = input("Enter subject: ")
            delay = int(input("Send after how many seconds? "))
            scheduler.schedule_email(to, subject, delay)

        elif choice == '2':
            email_id = input("Enter Email ID to cancel: ")
            scheduler.cancel_email(email_id)

        elif choice == '3':
            email_id = input("Enter Email ID to reschedule: ")
            delay = int(input("New delay (in seconds): "))
            scheduler.reschedule_email(email_id, delay)

        elif choice == '4':
            scheduler.view_queue()

        elif choice == '5':
            print("⏳ Processing emails...")
            scheduler.process_emails()

        elif choice == '6':
            print("Exiting Email Scheduler.")
            break

        else:
            print("Invalid choice.")


run_scheduler()
