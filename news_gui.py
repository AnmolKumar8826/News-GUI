import io
import webbrowser
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image

class NewsApp:

    def __init__(self):
        # Fetch data from the News API
        self.data = requests.get('https://newsapi.org/v2/top-headlines?country=in&apiKey=07ce6431517e45c5b04b589c36e5bed6').json()
        # Initialize GUI
        self.load_gui()
        # Load the first news item
        self.load_news_item(0)

    def load_gui(self):
        # Initialize the Tkinter window
        self.root = Tk()
        
        self.root.state('zoomed')
        # self.root.geometry('1450x850')
        self.root.resizable(0, 0)
        self.root.title('Mera News App')
        self.root.config(background='black')

    def clear(self):
        # Clear all widgets on the screen for the next news item
        for i in self.root.pack_slaves():
            i.destroy()

    def load_news_item(self, index):
        # Clear the screen
        self.clear()

        # Display image for the news item, handle cases where no image is fetched
        try:
            img_url = self.data['articles'][index]['urlToImage']
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((1200,550))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((1200, 550))
            photo = ImageTk.PhotoImage(im)

        # Display the image
        label = Label(self.root, image=photo)
        label.pack(pady=(15,20))

        # Display the news heading
        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='black', fg='white', wraplength=800, justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        # Display news details/description
        details = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', wraplength=650, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        # Create a frame to hold button functionalities
        frame = Frame(self.root, bg='black')
        frame.pack(expand=True, side=BOTTOM, fill=BOTH)

        # Display 'Prev' button if not on the first news item
        if index != 0:
            prev = Button(frame, text='Prev', bg="red", width=16, height=3, command=lambda: self.load_news_item(index-1))
            prev.grid(row=0,column=0)

        # Display 'Read More' button to open the news link in a browser
        read = Button(frame, text='Read More', bg="light green", width=16, height=3, command=lambda: self.open_link(self.data['articles'][index]['url']))
        read.grid(row=0,column=2)

        # Display 'Next' button if not on the last news item
        if index != len(self.data['articles']) - 1:
            next = Button(frame, text='Next', bg="light green", width=16, height=3, command=lambda: self.load_news_item(index+1))
            next.grid(row=0,column=4)

        # Run the Tkinter main loop
        self.root.mainloop()

    def open_link(self, url):
        # Open the news link in a web browser
        webbrowser.open(url)


# Create an instance of the NewsApp class
obj = NewsApp()
