from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
import json

@csrf_exempt
def contact_form(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name')
            email = data.get('email')
            message = data.get('message')
            
            # Send email
            subject = f'New Contact Form Submission from {name}'
            email_message = f'''
            Name: {name}
            Email: {email}
            Message: {message}
            '''
            
            send_mail(
                subject=subject,
                message=email_message,
                from_email=email,
                recipient_list=['dharshankumarlearn@gmail.com'],  # Your email
                fail_silently=False,
            )
            
            return JsonResponse({'status': 'success', 'message': 'Email sent successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)