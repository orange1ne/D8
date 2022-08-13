from celery import shared_task
from models import Category, User, Post
from django.core.mail import send_mail


@shared_task
def send_mail():
    for post_category in Category.objects.all():
        group = post_category.lower() + '_subs'
        receivers = []
        for post in Post.objects.filter(Category=post_category):
            for user in User.objects.filter(groups__name=group):
                receivers.append(user.email)
            send_mail(
                subject=Post.name,
                message=Post.text,
                from_email='',
                recipient_list=[receivers],
            )
