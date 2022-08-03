# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.core.mail import send_mail
#
# from .models import Post
#
#
# @receiver(post_save, sender=Post)
# def notify_subscribers(sender, instance, created, **kwargs):
#
#     if created:
#         subject = f'{instance.name} {instance.time.strftime("%d %m %Y")}'
#     else:
#         subject = f'Post changed for {instance.name} {instance.time.strftime("%d %m %Y")}'
#
#     send_mail(
#         subject=subject,
#         message=instance.text,
#         from_email='',
#         recipient_list=[''],
#     )
