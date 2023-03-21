class EmailProcessor:
    
    def __init__(self):
        self.emails = []
        self.email = ''
        self.msgs = []
        # define delimiter
        self.delimiter = '=' * 200 + '\n'
    
    def fill_list(self, file = 'emails.txt'):
        with open(file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.encode('unicode_escape', 'ignore').decode('unicode_escape', 'ignore')

                if line != '\n':
                    if line == self.delimiter:
                        self.emails.append(self.email)
                        self.email = ''
                    else:
                        line = line.split()
#                         print(line)
                        if line:
                            s = ''
                            # Join the remaining words back into a string
                            for word in line[:-1]:
                                if 'http' in word or 'blockblock' in word or word == '[]' or word.startswith('&'):
                                    pass
                                else:
                                    s += (word + ' ')
                            word = line[-1]
                            if not('http' in word or 'blockblock' in word or word == '[]' or word.startswith('&')):
                                s += word

                            line = s.replace('\u200c', '')
                            self.email += (line + '\n')
                            
    def fill_json(self, file = 'emails.txt'):
        # only fill emails list if it's empty
        if not self.emails:
            # create the email list
            self.fill_list(file)

        self.msgs = []
        count = 0
        for email in self.emails:
            email = email.split('\n')
            msg = {'Subject': '', 'From': '', 'To':'', 'Date': '', 'Body': ''}
            temp = ''
            for line in email:
#                 print(line)

                new_key = line.split(':', maxsplit=1)[0]
#                 print('split: ', line.split(':', maxsplit=1))
                if new_key not in msg.keys():
                    msg[key] += line
                else:
                    key = new_key
                    msg[key] = "".join(line.split(':', maxsplit=1)[1:]).lstrip() if len(line.split(':', maxsplit=1)) > 1 else ""
        #             msg[key] = line.split(': ')[1:]
            self.msgs.append(msg)
            count += 1
#             print('msg: ', msg)
        print('APPENDED ', count, 'EMAILS')
    
    def write_json(self, inputfile='emails.txt', outputfile='emails_cleaned.txt'):
        import json
        # writes the json-formatted data into a txt file
        self.fill_json(inputfile)
        with open(outputfile, "w") as f:
            for msg in self.msgs:
        #         f.write(msg + '\n')
                json.dump(msg, f, indent=4)
                f.write('\n')
        print('emails in json format written to', outputfile)
    
    def write_csv(self, inputfile='emails.txt',outputfile='emails_cleaned.csv'):
        import pandas as pd
        import csv
        # writes into a csv file
        self.fill_json(inputfile)
        final = pd.DataFrame(self.msgs)
        final.to_csv(outputfile, index=False, quoting=csv.QUOTE_ALL)
        print('emails in csv format written to', outputfile)


emailprocessor = EmailProcessor()
emailprocessor.write_json()
emailprocessor.write_csv()