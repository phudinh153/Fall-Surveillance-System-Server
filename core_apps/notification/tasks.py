import celery


@celery.shared_task()
def send_notification():
    from time import sleep

    sleep(2)
    print("Sending notification", flush=True)

    return "Notification sent"
