from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import logging
from .tasks import queue_email

logger = logging.getLogger(__name__)

@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            email = data.get('email', '').strip()
            message = data.get('message', '').strip()
            
            # Validate input
            if not name or not email or not message:
                return JsonResponse({
                    'status': 'error', 
                    'message': 'All fields are required'
                }, status=400)
            
            # Queue email for async processing (returns immediately)
            subject = f'New Contact Form Submission from {name}'
            email_message = f'''
Name: {name}
Email: {email}
Message: {message}
            '''
            
            queue_email(
                subject=subject,
                message=email_message,
                from_email=email,
                recipient_list=['dharshankumarj.dev@gmail.com'],
            )
            
            logger.info(f"Contact form submitted by {name} ({email})")
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Your message has been queued and will be sent shortly'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'error', 
                'message': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            logger.error(f"Contact form error: {str(e)}")
            return JsonResponse({
                'status': 'error', 
                'message': 'An error occurred processing your request'
            }, status=500)
    
    return JsonResponse({
        'status': 'error', 
        'message': 'Method not allowed'
    }, status=405)