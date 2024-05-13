from time import sleep
from backend.workers import celery
from celery.schedules import crontab # type: ignore
from backend.data_access import (get_all_users, get_creator_songs, get_email_and_name_of_inactive_users, get_recently_played_songs, get_all_songs)
from backend.utils import send_email, send_activity_summary_email, send_export_complete_email
import datetime as dt
import csv



@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Schedule for daily reminders to inactive users
    sender.add_periodic_task(crontab(hour=17, minute=0), reminder_email.s(), name='daily_inactive_user_reminder')
    # Monthly activity summary for all users
    sender.add_periodic_task(crontab(day_of_month=1, hour=8), monthly_activity_summary.s(), name='monthly_activity_summary')




@celery.task
def reminder_email():
    """
    Send a reminder email to users who haven't been active.
    """
    inactive_users = get_email_and_name_of_inactive_users()
    for email, name in inactive_users:
        send_email(email, "We Miss You!", "It looks like you haven't played any songs recently. Come back for more music!", name)

@celery.task
def test_task():
    """
    Send a reminder email to users who haven't been active.
    """
    email = 'surajnish02@gmail.com'
    name = "hello  !!!#F "
    print(email)
    send_email(email, "We Miss You!", "It looks like you haven't played any songs recently. Come back for more music!", name)

@celery.task
def monthly_activity_summary():
    """
    Send a monthly email summarizing user activity.
    """
    users = get_all_users()
    for user in users:
        user_id = user['id']
        recent_songs = get_recently_played_songs(user_id)
        # Assuming send_activity_summary_email() is a utility function you have for sending the email.
        send_activity_summary_email(user['email'], "Your Monthly Music Summary", recent_songs, user)

@celery.task
def export_songs_csv(email):
    """
    Export a CSV file containing all songs.
    """
    print(email, "email")
    songs = get_all_songs()
    csv_file_path = "exported_songs.csv"
    with open(csv_file_path, "w", newline="") as csvfile:
        fieldnames = ["Song Name", "Singer", "Genre"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({
                "Song Name": '',
                "Singer": '',
                "Genre": '',
            })
        for song in songs:
            writer.writerow({
                "Song Name": song['name'],
                "Singer": song['singer'],
                "Genre": song['genre'],
            })
    # Assuming send_export_complete_email() is a utility function you have for notifying the completion.
    send_export_complete_email("Export Complete", email, csv_file_path)
    return csv_file_path


@celery.task
def export_creators_csv(email, user_id):
    """
    Export a CSV file containing all songs.
    """
    print(email, "email", user_id, "user_id")
    songs = get_creator_songs(user_id)
    csv_file_path = "exported_songs.csv"
    with open(csv_file_path, "w", newline="") as csvfile:
        fieldnames = ["Song Name", "Singer", "Genre"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerow({
                "Song Name": '',
                "Singer": '',
                "Genre": '',
            })
        writer.writerow({
                "Song Name": '',
                "Singer": '',
                "Genre": '',
            })
        for song in songs:
            writer.writerow({
                "Song Name": song['name'],
                "Singer": song['singer'],
                "Genre": song['genre'],
            })
    send_export_complete_email("Export Complete", email, csv_file_path)
    return csv_file_path

