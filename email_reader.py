#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Importing libraries
import imaplib, email
from email.header import decode_header
import webbrowser
import os


# In[13]:


class EmailReader:
    def __init__(self, user = 'kurtji9803@gmail.com', password = 'dhjhyyfpsbptpbwd', imap_url = 'imap.gmail.com'):
        self.user = user
        self.password = password
        self.imap_url = imap_url
        
    def clean(self, text):
        # clean text for creating a folder
        return "".join(c if c.isalnum() else "_" for c in text)
    
    def connect(self, mailbox = 'INBOX'):
        # this is done to make SSL connection with GMAIL
        self.con = imaplib.IMAP4_SSL(self.imap_url)

        # logging the user in
        self.con.login(self.user, self.password)

        # Select the mailbox you want to read emails from
        # mailbox = 'INBOX'
        return self.con.select(mailbox)
    
    # Function to search for a key value pair
    def search(self, mailbox = 'INBOX', n = 250):
        # Get emails from the connection
        status, total_messages = self.connect(mailbox)

        # Get the total number of messages in the mailbox
        total_messages = int(total_messages[0])
    
        # Calculate the range of messages to fetch
        n = n - 1
        start_index = max(1, total_messages - n)
        end_index = total_messages

        # Search for the messages within the range
        # result, data = con.search(None, key, '"{}"'.format(value))
        status, messages = self.con.search(None, f'{start_index}:{end_index}')
        
        # store the emails
        self.messages = messages
    
    def writetotxt(self, file = 'emails.txt'):
        # Open the output file for writing
        with open(file, 'w', encoding="utf-8") as f:
            
            # Iterate over the messages and fetch their content
            for message_id in self.messages[0].split()[::-1]:
                status, msg = self.con.fetch(message_id, '(RFC822)')

                # Extract the email content using the email module
                for response in msg:
                    if type(response) is tuple:

                        my_msg=email.message_from_bytes((response[1]))

                        # extract subject
                        subject, encoding = decode_header(my_msg["Subject"])[0]

                        # in case of no encoding
                        encoding = 'unicode_escape' if not encoding else encoding

                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            subject = subject.decode(encoding)
                        # extract from
                        From, encoding = decode_header(my_msg.get("From"))[0]

                        # in case of no encoding
                        encoding = 'unicode_escape' if not encoding else encoding

                        if isinstance(From, bytes):
                            From = From.decode(encoding)

                        f.write('\n')
                        f.write(f"Subject: {my_msg['subject']}\n")
                        f.write(f"From: {my_msg['from']}\n")
                        f.write(f"To: {my_msg['to']}\n")
                        f.write(f"Date: {my_msg['date']}\n")
                        f.write("Body: ")


            # Method 3
                        # if the email message is multipart
                        if my_msg.is_multipart():
                            # iterate over email parts
                            for part in my_msg.walk():
                                # extract content type of email
                                content_type = part.get_content_type()
                                content_disposition = str(part.get("Content-Disposition"))
                                try:
                                    # get the email body
                                    body = part.get_payload(decode=True).decode()
                                except:
                                    pass
                                if content_type == "text/plain" and "attachment" not in content_disposition:
                                    # write plain text to file
                                    f.write(body.replace('\n', ' '))
                                    f.write(' ')
                                # elif "attachment" in content_disposition:
                                #     # download attachment
                                #     filename = part.get_filename()
                                #     if filename:
                                #         folder_name = self.clean(subject)
                                #         if not os.path.isdir(folder_name):
                                #             # make a folder for this email (named after the subject)
                                #             os.mkdir(folder_name)
                                #         filepath = os.path.join(folder_name, filename)
                                #         # download attachment and save it
                                #         open(filepath, "wb").write(part.get_payload(decode=True))

                                elif "attachment" in content_disposition:
                                    # make an "attachment" folder if it doesn't exist
                                    if not os.path.isdir("attachments"):
                                        os.mkdir("attachments")

                                    # download attachment
                                    filename = part.get_filename()
                                    if filename:
                                        folder_name = "attachments\\" + self.clean(subject)
                                        if not os.path.isdir(folder_name):
                                            # make an "attachment" folder if it doesn't exist
                                            os.mkdir(folder_name)
                                        filepath = os.path.join(folder_name, self.clean(filename))
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))

                        else:
                            # extract content type of email
                            content_type = my_msg.get_content_type()
                            # get the email body
                            body = my_msg.get_payload(decode=True).decode(encoding)
                            if content_type == "text/plain":
                                # write text parts
                                f.write(body.replace('\n', ' '))
                                f.write(' ')

                        # HTML files
                        if content_type == "text/html":
                            f.write('html\n')
                        f.write('\n' + '='*200 + '\n')

# read and write gmails
# emailreader = EmailReader()
# emailreader.search()
# emailreader.writetotxt()

# # read only outlook and 126 emails
# import win32com.client
# #other libraries to be used in this script
# import os
# from datetime import datetime, timedelta

# outlook = win32com.client.Dispatch('outlook.application')
# mapi = outlook.GetNamespace("MAPI")

# for account in mapi.Accounts:
# 	print(account.DeliveryStore.DisplayName)

# inbox = mapi.GetDefaultFolder(6)

# # inbox = mapi.GetDefaultFolder(6).Folders["Inbox"]
# # Retrieve the messages
# messages = inbox.Items
# # Sort the messages by date received (oldest to newest)
# messages.Sort("[ReceivedTime]", False)
# # Get last n emails
# n = 500
# # Retrieve the 10 most recent messages in the folder
# recent_messages = []
# for i in range(n):
#     if i >= len(messages):
#         break
#     message = messages[i+1] # messages are 1-indexed
#     recent_messages.append(message)

# # Loop through the messages and print the body content
# for message in recent_messages:
#     body_content = message.body
#     # print(body_content)