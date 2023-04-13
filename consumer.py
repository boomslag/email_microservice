import json, os, django
from confluent_kafka import Consumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from django.apps import apps

Contact = apps.get_model('automation', 'Contact')
EmailList = apps.get_model('automation', 'EmailList')
ContactEmailList = apps.get_model('automation', 'ContactEmailList')
EmailTemplate = apps.get_model('automation', 'EmailTemplate')
EmailCampaign = apps.get_model('automation', 'EmailCampaign')

consumer1 = Consumer({
    'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVER'),
    'security.protocol': os.environ.get('KAFKA_SECURITY_PROTOCOL'),
    'sasl.username': os.environ.get('KAFKA_USERNAME'), 
    'sasl.password': os.environ.get('KAFKA_PASSWORD'),
    'sasl.mechanism': 'PLAIN',
    'group.id': os.environ.get('KAFKA_GROUP'),
    'auto.offset.reset': 'earliest'
})
consumer1.subscribe([os.environ.get('KAFKA_TOPIC')])

while True:
    msg1 = consumer1.poll(1.0)

    if msg1 is not None and not msg1.error():
        topic1 = msg1.topic()
        value1 = msg1.value()

        if topic1 == os.environ.get('KAFKA_TOPIC'):
            if msg1.key() == b'user_agreed':
                user_data = json.loads(value1)

                # Create a new Contact entry
                contact, created = Contact.objects.get_or_create(
                    email=user_data['email'],
                    defaults={
                        'first_name': user_data.get('first_name', ''),
                        'last_name': user_data.get('last_name', '')
                    }
                )

                if created:
                    # Add the new contact to the specified EmailList
                    email_list = EmailList.objects.get(pk=1)  # Replace 1 with the desired EmailList ID
                    contact_email_list = ContactEmailList(contact=contact, email_list=email_list)
                    contact_email_list.save()

consumer1.close()