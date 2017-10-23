import imaplib, time, spotipy, sys, time, smtplib
import spotipy.util as util
import email as eemail
#import urllib.request as request



#Datastruktur för spellista x

#Klass för låtar x

#Kolla mailen vartannan minut x

#Första låten hittas i mailen

#Lägg till nya låtar i spellista

    #Ta tiden på första låten

    #Skapa nytt uppdateringsintervall (t.ex. låtlängd/3)

    #Kolla mailen 3 gånger

    #Repetera


# Kolla igenom mailen: 
    #Leta efter avsändare philipjclaesson@gmail.com
        #Om ett specialkommando hittas: utför (PAUSE, PLAY, SKIP)

    #Leta efter https://spotify...

    #Plocka ut vad som står därefter

    #Lägg till i spellist-objekt




# Tidtagning: 

# Om spellistan är tom 
    # Lägg till nuvarande tid + låttid som changetime

# I playnext: 
    # Sätt changetime till 


class Playlist(): 
    def __init__(self,sp, mail): 
        self.queue = []
        self.history = []
        self.sp = sp
        self.change_time = 0
        self.mail = mail

    def enqueue(self, track): 
        if len(self.queue) == 0: #If first song in playlist
            self.change_time = (time.time()) + (track.time) #+ 60 #60 seconds is added to give admin time to start the queue
            # Send email to pc
            self.notify_pc()


        self.queue.append(track)
        #Lägg till i spotifyspellistan mha spotipy
        self.sp.user_playlist_add_tracks("clarreman", "3SNSkgrZZrLsdLXP5PpexC", tracks = {track.id:track.id})

    def notify_pc(self):


        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login("klequeue@gmail.com","password_here")
        server.sendmail(to_addrs = "philipjclaesson@gmail.com", from_addr="klequeue@gmail.com", msg="Subject: New!\n New songs are queued.")
        server.quit()

    

    def play_next(self): 
        old = self.queue.pop(0)
        self.history.append(old)
        # time = skaffa med hjälp av spotipy

        # Ange vilken tid musiken ska bytas. 
        if len(self.queue) > 0: 
            self.change_time += ((self.queue[0].time) - 10) # 10 är medelvärdet för delay vid 20s avscanningsintervaller
            print("Changed song! ")
        else: #Queue is empty
            self.change_time = 0

        try: 
            self.sp.user_playlist_remove_specific_occurrences_of_tracks("clarreman", "3SNSkgrZZrLsdLXP5PpexC", [{ "uri":old.id, "positions":[0]}]) #[ { “uri”:”4iV5W9uYEdYUVa79Axb7Rh”, “positions”:[2] },
        except:
            try: 
                self.sp.user_playlist_remove_specific_occurrences_of_tracks("clarreman", "3SNSkgrZZrLsdLXP5PpexC", [{ "uri":old.id, "positions":[1]}]) #[ { “uri”:”4iV5W9uYEdYUVa79Axb7Rh”, “positions”:[2] },
            except:
                pass


        """
        if self.queue[0]: 
            return self.queue[0].get_time()
        else: #Om kön är tom
            return 180 #Intervallet sätts till 180/3s 
        """

    def __str__(self):
        out = ""
        for track in self.queue:
            out += (str(track)+" \n")
        if self.is_empty(): 
            out = "Playlist is empty."
        
        return (out)

    def write(self):

        with open ("/Users/philipclaesson/Google Drive/appengine-guestbook-python/index.html", 'r') as readfile: 
            lines = readfile.readlines()
            new = lines[0:65]


        with open ("/Users/philipclaesson/Google Drive/appengine-guestbook-python/index.html", 'w+') as writefile: 

            #print(new)
            newplay = str(self).split("\n")
            for i in range(len(newplay)): 
                newplay[i] = "    "+newplay[i]+"<br>"+"\n"

            new = new + newplay
            new = new + ["  <br>","  <br>","  <br>","  <br>","  <br>","   <br>","   <br>","    </div>\n","  </body>\n","</html>\n"]
            for line in new: 
                writefile.write(line)

    def is_empty(self): 
        if len(self.queue) > 0: 
            return False
        else: 
            return True
    def sp_update(self, newsp):
        self.sp = newsp

class Track(): 
    def __init__(self, sp, track_id, user = "Unknown", name = None, artist = None, time = None): 
        self.id = track_id
        if user: self.user = user
        else: self.user = "Unknown"
        print("ID")
        print(self.id)
        self.info = sp.track(self.id)
        #Hamta namn och artist och time fran spotipy. Tid i sekunder!
        track = (sp.track(track_id))
        self.name = track['name']
        self.time = track['duration_ms']/1000
        self.artist = ""
        for artist in track['artists']: 
            self.artist += (artist['name']+", ")




    def get_time(self):
        return self.time 

    def __str__(self):
        string = ("<p>" + self.name + "</p><p> by " + self.artist + "queued by <i>" + self.user+ "</i></p><hr>")
        return string




class Mail():
    def __init__(self):
        pass
        """
        self.user= 'klequeue@gmail.com'
        self.password= 'password_here'
        self.M = imaplib.IMAP4_SSL('imap.gmail.com', '993')
        self.M.login(self.user, self.password)
        """
        
    def check_mail(self):
        "Kollar inboxen. Itererar över mail. Returnerar en tupel med 1. lista med tuplar med kommandon och avsändare, 2.lista med tuplar med låtar och avsändare om ny mail har kommit"
        self.user= 'klequeue@gmail.com'
        self.password= 'password_here' #Add password here
        self.M = imaplib.IMAP4_SSL('imap.gmail.com', '993')
        self.M.login(self.user, self.password)
        self.M.select()

        commandos = []
        tracks = []
        typ, data = self.M.search(None, 'ALL')
        for mail in data[0].split(): #Itererar över mail. 
            try: 
                command, track_id, user = self.search_mail(mail)
                if track_id: #Om man har fått ett eller flera track-id
                    tracks.append((track_id, user))
                if command: #Om man har fått ett kommando
                    commandos.append((command, user))
            except:
                print("Caught exception in check_mail")
            self.M.store(mail, '+FLAGS', '\\Deleted') #Tar bort
        self.M.expunge() #Tar bort epost

        if len(commandos) > 0 or len (tracks) > 0: 
            result = (commandos, tracks)
        else: 
            result = False

        self.M.close()

        return result #Returnerar en tupel om något har hänt, annars False
    

    def search_mail(self, mail):
        "Söker igenom ett mail"
        typ, data = self.M.fetch(mail, "(RFC822)") #"(UID BODY[TEXT])")
        user = self.get_user(data)
        track_id = False
        command = False
        for d in data[0]:
            d = str(d)
            #print(d)
            song, start_index = self.song_check(d) #Kollar om det är ett spotifymail
            if song:
                track_id = (self.get_song_id(d, start_index)) #Get song id and append to track_ids
            else: 
                command = self.command_check(d)
                #Gör något för kommandon
        return command, track_id, user


    def get_user(self, data): 
        "Takes email data. Returns the sender of the email. Fungerar inte!"
        user = None
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = eemail.message_from_string(str(response_part[1]))
                #print(msg)
                user = msg['From']
                start_index = 6 + int(str(response_part[1]).find("From: ")) #6 is the length 
                rest = str(response_part[1])[start_index:]
                end_index = int(rest.find(">"))+1
                name = rest[:end_index]
        return name

    def song_check(self, d): 
        "Kollar om det är ett spotifymail"
        song = False
        start_index = int(d.find("https://open.spotify.com/track/")) #String length is 31
        print(start_index)
        if start_index > 0: 
            song = True

        return song, start_index

    def command_check(self, d):
        "Kollar om mailet innehåller ett kommando. Commands: QUEUE" #Next + Back, Pause + Run? 
        command = False
        if d.find("queue") > 0 or d.find("QUEUE") > 0 or d.find("Queue") > 0:
            command = "QUEUE"
        return command
            

    def get_song_id(self, data, start_index):
            "Takes data (string) and start_index. Returns spotify-id."
            id_index = start_index + 31 
            song_id = str(data[id_index:id_index+22])#id length is 22
            print("Found song id: "+song_id)
            return(song_id)

    def send_email(self, message, reciever): 
        self.M.select()
        self.M.sendmail('klequeue@gmail.com', reciever, 'Subject: Klequeue\n'+message)



def main(): 
    print("Running")
    "Deklarerar variabler"
    email = Mail()
    scope = 'playlist-modify-public'
    username = 'clarreman'
    token = util.prompt_for_user_token(username, scope, client_id = 'ba25294d15a84c68b55b570118c9f46b', client_secret = 'c6dffe0cfacf41a68cca4cef93f4e267', redirect_uri = 'http://yoursite.com/callback/')
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    interval = 20 # 20s
    playlist = Playlist(sp, email)
    """
    commandos, tracks = email.check_mail()
    for track in tracks:
        t = Track(sp, track_id = track[0], user = track[1])
        playlist.enqueue(t)

    print((playlist))

    """

    #Körning av programmet
    playlist.write()
    while 1: 
        #try: 
        time.sleep(interval)
        connection = False
        token = util.prompt_for_user_token(username, scope, client_id = 'ba25294d15a84c68b55b570118c9f46b', client_secret = 'c6dffe0cfacf41a68cca4cef93f4e267', redirect_uri = 'http://yoursite.com/callback/')
        sp = spotipy.Spotify(auth=token)
        playlist.sp_update(sp)
        while connection == False:
            try: 
                new_mail = email.check_mail()
                connection = True
            except: 
                print("Caught email exception")
                connection = False
                time.sleep(10)


        if new_mail: 
            #print("New Mail!")
        #gör saker beroende på innehåll
            commands = new_mail[0]
            tracks = new_mail[1]

            for command in commands: # commands är en lista med tuplar
                pass #do commands

            for track in tracks: #Tracks är en lista med tuplar
                try: 
                    t = Track(sp, track[0], track[1]) # Track_id and User
                    playlist.enqueue(t)
                except: 
                    pass

            #Write playlist to file
            playlist.write()
        #else: 
            #print("No mail")

        if playlist.change_time <= time.time() and playlist.is_empty() == False:
            playlist.play_next() #Byt låt! 
            playlist.write()
        #except: 
        #    pass


def return_playlist(email, playlist, user):
    "Skriv ut och maila spellistan till den som ber om den. "
    pass


def pause_playlist(playlist):
    "Osäkert om denna och nästa behövs?"
    pass

def play_playlist(playlist):
    pass




def spotify(username):
    track_id = "3xwtw4SUxNMdJj7cXzcRuZ"
    playlist_id = "3SNSkgrZZrLsdLXP5PpexC"

    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, client_id = 'client_id_here', client_secret = 'client_secret_here', redirect_uri = 'http://yoursite.com/callback/')
    if token:
        sp = spotipy.Spotify(auth=token)
        sp.trace = False
        results = sp.user_playlist_add_tracks(username, "3kQO92SDgW1RAYJDVteSu4", tracks = {"3xwtw4SUxNMdJj7cXzcRuZ":"3xwtw4SUxNMdJj7cXzcRuZ"})
        #request.Request("https://api.spotify.com/v1/users/clarreman/playlists/3SNSkgrZZrLsdLXP5PpexC/tracks", data= {'track':'3xwtw4SUxNMdJj7cXzcRuZ'})
        #HTTPHandler.http_open("https://api.spotify.com/v1/users/clarreman/playlists/3SNSkgrZZrLsdLXP5PpexC/tracks", data = 'spotify:track:4iV5W9uYEdYUVa79Axb7Rh,spotify:track:1301WleyT98MSxVHPZCA6M')

        #print(results)

    else:
        print ("Can't get token for", username)

main()        
#email = Mail()
#email.checkMail()
#spotify("clarreman")

# check for new mail every minute

#while 1:
#    print 'Sending'
#    email.sendData()
#    time.sleep(60)
