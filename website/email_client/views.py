from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Client_Registration, Email_log
import socket
from smtplib import SMTP, SMTPException, SMTPAuthenticationError, SMTP_SSL
from django.core.mail import EmailMessage, get_connection
from django.shortcuts import render

class SendEmailView(APIView):
    def test_smtp_connection(self, smtp_host, smtp_port, use_ssl, use_tls, email_host_user, email_host_password):
        """Test SMTP connection before attempting to send email"""
        try:
            # First, test if the port is even reachable
            sock = socket.create_connection((smtp_host, smtp_port), timeout=10)
            sock.close()

            # Now test SMTP connection
            if use_ssl and smtp_port == 465:
                server = SMTP_SSL(smtp_host, smtp_port, timeout=10)
            elif use_tls and smtp_port == 587:
                server = SMTP(smtp_host, smtp_port, timeout=10)
                server.starttls()
            else:
                return False, "Invalid SSL/TLS configuration. Use SSL with port 465 or TLS with port 587."

            server.login(email_host_user, email_host_password)
            server.quit()
            return True, "Connection successful"

        except socket.timeout:
            return False, "Connection timed out. Please check if the SMTP host is correct and accessible."
        except socket.gaierror:
            return False, "Could not resolve SMTP host. Please check the hostname."
        except ConnectionRefusedError:
            return False, "Connection refused. Please check if the SMTP port is correct and not blocked."
        except SMTPAuthenticationError:
            return False, "Invalid SMTP credentials."
        except SMTPException as e:
            return False, f"SMTP Error: {str(e)}"
        except Exception as e:
            return False, f"Error: {str(e)}"

    def post(self, request):
        try:
            data = request.data

            # Step 1: Check if client exists
            client_id = data.get('id')
            try:
                client = Client_Registration.objects.get(id=client_id)
            except Client_Registration.DoesNotExist:
                return Response({"message": "Client does not exist, id is invalid, contact getsetdeployed team to get one."}, status=status.HTTP_404_NOT_FOUND)

            # Extract and validate email details
            required_fields = {
                'subject': data.get('subject'),
                'body': data.get('body'),
                'recipient_list': data.get('recipient_list'),
                'smtp_host': data.get('smtp_host'),
                'smtp_port': data.get('smtp_port'),
                'email_host_user': data.get('email_host_user'),
                'email_host_password': data.get('email_host_password')
            }

            # Check for missing fields
            missing_fields = [k for k, v in required_fields.items() if not v]
            if missing_fields:
                return Response(
                    {"error": f"Missing required fields: {', '.join(missing_fields)}"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Validate recipient_list
            recipient_list = required_fields['recipient_list']
            if not isinstance(recipient_list, list) or not all(isinstance(email, str) for email in recipient_list):
                return Response(
                    {"error": "recipient_list must be an array of email addresses."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Test SMTP connection first
            use_tls = data.get('use_tls', True)
            use_ssl = data.get('use_ssl', False)

            connection_success, connection_message = self.test_smtp_connection(
                required_fields['smtp_host'],
                required_fields['smtp_port'],
                use_ssl,
                use_tls,
                required_fields['email_host_user'],
                required_fields['email_host_password']
            )

            if not connection_success:
                return Response({"error": connection_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Configure email backend
            connection = get_connection(
                host=required_fields['smtp_host'],
                port=required_fields['smtp_port'],
                username=required_fields['email_host_user'],
                password=required_fields['email_host_password'],
                use_tls=use_tls,
                use_ssl=use_ssl,
            )

            # Create and send email
            email = EmailMessage(
                subject=required_fields['subject'],
                body=required_fields['body'],
                from_email=required_fields['email_host_user'],
                to=recipient_list,
                connection=connection,
            )
            email.content_subtype = "html"
            email.send(fail_silently=False)

            # Log success
            Email_log.objects.create(client=client, status='SENT')
            return Response({"success": "Email sent successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            # Log failure
            Email_log.objects.create(client=client, status='FAILED')
            return Response(
                {"error": f"Failed to send email: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def options(self, request, *args, **kwargs):
        response = Response({}, status=status.HTTP_204_NO_CONTENT)
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response

def home(request):
    return render(request, 'index.html')
