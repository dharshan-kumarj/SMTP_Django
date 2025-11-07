import threading
import queue
import logging
from django.core.mail import send_mail
from django.conf import settings

logger = logging.getLogger(__name__)

# Create a global queue for email tasks
email_queue = queue.Queue()

class EmailWorker(threading.Thread):
    """Background worker thread to process email queue"""
    
    def __init__(self):
        super().__init__(daemon=True)
        self._stop_event = threading.Event()
    
    def run(self):
        """Process emails from the queue"""
        while not self._stop_event.is_set():
            try:
                # Wait for an email task (timeout after 1 second to check stop event)
                email_data = email_queue.get(timeout=1)
                
                try:
                    # Send the email
                    send_mail(
                        subject=email_data['subject'],
                        message=email_data['message'],
                        from_email=email_data['from_email'],
                        recipient_list=email_data['recipient_list'],
                        fail_silently=False,
                    )
                    logger.info(f"Email sent successfully to {email_data['recipient_list']}")
                except Exception as e:
                    logger.error(f"Failed to send email: {str(e)}")
                finally:
                    email_queue.task_done()
                    
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Email worker error: {str(e)}")
    
    def stop(self):
        """Stop the worker thread"""
        self._stop_event.set()

# Start the email worker thread
email_worker = EmailWorker()
email_worker.start()

def queue_email(subject, message, from_email, recipient_list):
    """
    Add an email to the queue for async processing
    
    Args:
        subject: Email subject
        message: Email body
        from_email: Sender email
        recipient_list: List of recipient emails
    """
    email_data = {
        'subject': subject,
        'message': message,
        'from_email': from_email,
        'recipient_list': recipient_list,
    }
    email_queue.put(email_data)
    logger.info(f"Email queued for {recipient_list}")
