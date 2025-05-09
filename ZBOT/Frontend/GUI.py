#IMPORT PACKAGES FOR FUNCTIONS 
from PyQt5.QtWidgets import QHBoxLayout,QApplication ,QMainWindow,QTextEdit,QStackedWidget,QWidget, QLineEdit,QGridLayout,QVBoxLayout,QPushButton,QFrame,QLabel,QSizePolicy
from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor,QTextCharFormat,QFont,QPixmap,QTextBlockFormat
from PyQt5.QtCore import Qt, QSize ,QTimer
from dotenv import dotenv_values 
import sys
import os 
#IMP VARIABLES 
env_vars = dotenv_values(".env")
Assistantname = env_vars.get("Assistantname")
current_dir = os.getcwd()
old_chat_message =""
TempDirPath = rf"{current_dir}\Frontend\Files"
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"

def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    modified_answer = '\n'.join(non_empty_lines)
    return modified_answer

def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how","why","what","who","where","when","which","whose","whom","can you","what's","where's","how's"]
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1]+ "?"
        else :
            new_query = new_query + "?"
    else:
        if query_words[-1][-1] in ['.','?','!']:
            new_query = new_query[:-1]+ "."
        else :
            new_query = new_query + "."
    return new_query.capitalize()

#MAIN WINDOW CLASS
def SetMicrophoneStatus(Command):
    with open(rf'{TempDirPath}\Mic.data',"w", encoding='utf-8') as file:
        file.write(Command)
        
        # RETURNS TRUE IF MIC ON 
def GetMicrophoneStatus():
    with open(rf'{TempDirPath}\Mic.data',"r", encoding='utf-8') as file:
        Status = file.read()
    return Status 

#CHANGE ASSISTANT STATUS
def SetAssistantStatus(Status):
    with open(rf'{TempDirPath}\Status.data',"w", encoding='utf-8') as file:
        file.write(Status)
        SetAssistantStatus("speaking......")
        
def GetAssistantStatus():
    with open(rf'{TempDirPath}\Status.data',"r", encoding='utf-8') as file:
        Status = file.read()
    return Status 

def MicButtonInitialed():
    SetMicrophoneStatus("False")
    
def MicButtonClosed():
    SetMicrophoneStatus("True")
    #returns path to graphics directory
def GraphicsDirectoryPath(Filename):
    Path = rf'{GraphicsDirPath}\{Filename}'
    return Path
# returns path to file directory 
def TempDirectoryPath(Filename):
    Path = rf'{TempDirPath}\{Filename}'
    return Path 

def ShowTextToScreen(Text):
    with open(rf'{TempDirPath}\Responses.data',"w",encoding='utf-8') as file:
        file.write(Text)
        
class ChatSection(QWidget):
        def __init__(self):
            super(ChatSection, self).__init__()
            layout = QVBoxLayout(self)
            layout.setContentsMargins(-10,40,40,100)
            layout.setSpacing(-100)
            self.chat_text_edit = QTextEdit()
            self.chat_text_edit.setReadOnly(True)
            self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
            self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
            layout.addWidget(self.chat_text_edit)
            self.setStyleSheet("background-color: black;")
            layout.setSizeConstraint(QVBoxLayout.SetDefaultConstraint)
            layout.setStretch(1,1)
            self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding))
            text_color = QColor(Qt.blue)
            text_color_text = QTextCharFormat()
            text_color_text.setForeground(text_color)
            self.chat_text_edit.setCurrentCharFormat(text_color_text)
            self.gif_label = QLabel()
            self.gif_label.setStyleSheet("border: none;")
            movie = QMovie(GraphicsDirectoryPath('final.gif')) #############################
            max_gif_size_W = 480 #480
            max_gif_size_H = 270 #270
            
            movie.setScaledSize(QSize(max_gif_size_W, max_gif_size_H))
            self.gif_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
            self.gif_label.setMovie(movie)
            movie.start()
            layout.addWidget(self.gif_label)
            self.label =QLabel("")
            self.label.setStyleSheet("color: white; font-size:16px; margin-right:195px; border:none;margin-top:-30px;")
            self.label.setAlignment(Qt.AlignRight)
            layout.addWidget(self.label)
            layout.setSpacing(-10)
            layout.addWidget(self.gif_label)
            font = QFont()
            font.setPointSize(13)
            self.chat_text_edit.setFont(font)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.loadMessages)
            self.timer.timeout.connect(self.SpeechRecogText)
            self.timer.start(5)
            self.chat_text_edit.viewport().installEventFilter(self)
            self.setStyleSheet("""
                QScrollBar:vertical{
                border: none;
                background: black;
                width: 10px;
                margin: 0px 0px 0px 0px;
                }
                QScrollBar::handle:vertical{
                               background:white;
                               min-height:20px;
                }
                QScrollBar:: add-line:vertical{
                               background: black;
                               subcontrol-position: bottom;
                               subcontrol-origin: margin;
                               height:10px;
                }
                QScrollBar:: sub-line:vertical{
                    background: black;
                    subontrol-position:top;
                    subcontrol-position: margin;
                    height:10px;
                }
                QScrollBar:: up-arrow:vertical, QSrollBar::down-arrow:vertical{
                               border:none;
                               background: none;
                               color:none;
                }
                QScrollBar:: add-page:vertical, QScrollBar::sub-page:vertical{
                               background: none;
                }
            """)
        def loadMessages(self):
                global old_chat_message
            
                with open (TempDirectoryPath('Responses.data'),"r", encoding='utf-8') as file :
                    messages = file.read()
                
                    if None == messages:
                        pass 
                    elif len(messages )<= 1:
                        pass 
                    elif str(old_chat_message)== str(messages):
                        pass 
                    else:
                        # self.addMessage(message=messages, color ='white')
                        # old_chat_message = messages
                        self.addMessage(message=str(messages), color='white')
                        old_chat_message = messages
                    
        def SpeechRecogText(self):
                        with open(TempDirectoryPath('Status.data'),"r", encoding =' utf-8') as file :
                            messages = file.read()
                            self.label.setText(messages)
        def load_icon(self,path,width=60,height=60):
            pixmap = QPixmap(path)
            new_pixmap =pixmap.scaled(width,height)
            self.icon_label.setPixmap(new_pixmap)
        def toggle_icon(self, event=None):
            if self.toggled:
                self.load_icon(GraphicsDirectoryPath('voice.png'),60,60)
                MicButtonInitialed()
            else:
                self.load_icon(GraphicsDirectoryPath('mic.png'),60,60)
                MicButtonClosed()
                
            self.toggled = not self.toggled 
            
        def addMessage(self,message,color):
            cursor = self.chat_text_edit.textCursor()
            format = QTextCharFormat()
            formatm = QTextBlockFormat()
            formatm.setTopMargin(10)
            formatm.setLeftMargin(10)
            format.setForeground(QColor(color))
            cursor.setCharFormat(format)
            cursor.setBlockFormat(formatm)
            cursor.insertText(message +"\n")
            self.chat_text_edit.setTextCursor(cursor)
class InitialScreen(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            desktop = QApplication.desktop()
            screen_width = desktop.screenGeometry().width()
            screen_height = desktop.screenGeometry().height()
            content_layout =QVBoxLayout()
            content_layout.setContentsMargins(0,0,0,0)
            gif_label = QLabel()
            movie = QMovie(GraphicsDirectoryPath('final.gif'))################################
            gif_label.setMovie(movie)
            max_gif_size_H = int (screen_width/ 12* 6)   #16*9  # CHANGE THE SIZE OF THE GIF ACCORDING TO SCRREN WIDTH 
            movie.setScaledSize(QSize(screen_width, max_gif_size_H))
            gif_label.setAlignment(Qt.AlignCenter)
            movie.start()
            gif_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.icon_label = QLabel()
            pixmap= QPixmap(GraphicsDirectoryPath('Mic_on.png'))
            new_pixmap= pixmap.scaled(60,60)
            self.icon_label.setPixmap(new_pixmap)
            self.icon_label.setFixedSize(150,150)
            self.icon_label.setAlignment(Qt.AlignCenter)
            self.toggled= True
            self.toggle_icon()
            self.icon_label_mousePressEvent = self.toggle_icon 
            self.toggled = True
            self.toggle_icon()
            self.icon_label.mousePressEvent = self.toggle_icon
            self.label= QLabel("")
            self.label.setStyleSheet("color: green; font-size:16px; margin-bottom:0;")
            content_layout.addWidget(gif_label,alignment = Qt.AlignCenter)
            content_layout.addWidget(self.icon_label, alignment= Qt.AlignCenter )
            content_layout.setContentsMargins(0,0,0,150)
            self.setLayout(content_layout)
            self.setFixedHeight(screen_height)
            self.setFixedWidth(screen_width)
            self.setStyleSheet("background-color: black;")  #mic colour 
            self.timer = QTimer (self)
            self.timer.timeout.connect(self.SpeechRecogText)
            self.timer.start(5)
        
        def SpeechRecogText(self):
            with open(TempDirectoryPath('Status.data'),"r",encoding='utf-8') as file :
                messages = file.read()
                self.label.setText(messages)
        def load_icon(self,path,width=60,height=60):
            pixmap = QPixmap(path)
            new_pixmap = pixmap.scaled(width,height)
            self.icon_label.setPixmap(new_pixmap)
        def toggle_icon(self, event= None ):
            if self.toggled:
                self.load_icon(GraphicsDirectoryPath('Mic_on.png'),60,60)
                MicButtonInitialed()
            else:
                self.load_icon(GraphicsDirectoryPath('Mic_off.png'),60,60)
                MicButtonClosed()
            self.toggled = not self.toggled
class MessageScreen(QWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            desktop = QApplication.desktop()
            screen_width = desktop.screenGeometry().width()
            screen_height = desktop.screenGeometry().height()
            layout = QVBoxLayout()
            label =QLabel("")
            layout.addWidget(label)
            chat_section =ChatSection()
            layout.addWidget(chat_section)
            self.setLayout(layout)
            self.setStyleSheet("background-color: black;") #CHAT KA BACKGROUND
            self.setFixedHeight(screen_height)
            self.setFixedWidth(screen_width)
        
class CustomTopBar(QWidget):
    
    def __init__(self,parent,stacked_widget):
        super().__init__(parent)
        self.initUI()
        self.current_screen =None
        self.stacked_widget = stacked_widget
        
    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignRight)
        home_button = QPushButton()
        home_icon =QIcon(GraphicsDirectoryPath("Home.png"))
        home_button.setIcon(home_icon)
        home_button.setText("HOME")
        home_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color:black; font:bold")
        message_button = QPushButton()
        message_icon = QIcon(GraphicsDirectoryPath("Chats.png"))
        message_button.setIcon(message_icon)
        message_button.setText("CHAT")
        message_button.setStyleSheet("height:40px; line-height:40px; background-color:white; color:black; font:bold;") #home vagrera ka color 
        minimize_button = QPushButton()
        minimize_icon = QIcon(GraphicsDirectoryPath("Minimize2.png"))
        minimize_button.setIcon(minimize_icon)
        minimize_button.setStyleSheet("background-color:white") #minimize ka color 
        minimize_button.clicked.connect(self.minimizeWindow)
        self.maximize_button = QPushButton()
        self.maximize_icon = QIcon(GraphicsDirectoryPath('Maximize.png'))
        self.restore_icon =QIcon(GraphicsDirectoryPath('Minimize.png'))
        self.maximize_button.setIcon(self.maximize_icon)
        self.maximize_button.setFlat(True)
        self.maximize_button.setStyleSheet("background-color:silver")
        self.maximize_button.clicked.connect(self.maximizeWindow)
        close_button =QPushButton()
        close_icon =QIcon(GraphicsDirectoryPath('Close.png'))
        close_button.setIcon(close_icon)
        close_button.setStyleSheet("background-color:black") #close icon ka backgrounf
        close_button.clicked.connect(self.closeWindow)
        line_frame =QFrame()
        line_frame.setFixedHeight(1)
        line_frame.setFrameShape(QFrame.HLine)
        line_frame.setStyleSheet("border-color:black;")
        title_label = QLabel(f"{str(Assistantname).capitalize()}.AI<3  ")
        title_label.setStyleSheet("color:black; font-size:18px; background-color:silver;") # Z>AI ka background
        home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))
        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(home_button)
        layout.addWidget(message_button)
        layout.addStretch(1)
        layout.addWidget(minimize_button)
        layout.addWidget(self.maximize_button)
        layout.addWidget(close_button)
        layout.addWidget(line_frame)
        self.draggable =True
        self.offset = None 
        
    def paintEvent(self, event ):
        painter =QPainter(self)
        painter.fillRect(self.rect(), Qt.white)  #change title bar ka color 
        super().paintEvent(event)
    def minimizeWindow(self):
        self.parent().showMinimized()
        
    def maximizeWindow(self):
        if self.parent().isMaximized():
            self.parent().showNormal()
            self.maximize_button.setIcon(self.restore_icon)
        else:
            self.parent().showMaximized()
            self.maximize_button.setIcon(self.restore_icon)
            
    def closeWindow(self):
        self.parent().close()
    
    def mousePressEvent(self, event):
        if self.draggable:
            self.offset = event.pos()
        
    def mouseMoveEvent(self, event):
        if self.draggable and self.offset:
            new_pos = event.globalPos() - self.offset 
            self.parent().move(new_pos)
    def showMessageScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        message_screen = MessageScreen(self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(message_screen)
        self.current_screen =message_screen 
    def showInitialScreen(self):
        if self.current_screen is not None:
            self.current_screen.hide()
        initial_screen =InitialScreen (self)
        layout = self.parent().layout()
        if layout is not None:
            layout.addWidget(initial_screen)
        self.current_screen = initial_screen
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()
    def initUI(self):
        desktop = QApplication.desktop()
        screen_width = desktop.screenGeometry().width()
        screen_height = desktop.screenGeometry().height()
        stacked_widget = QStackedWidget(self)
        initial_screen = InitialScreen (self)
        message_screen = MessageScreen(self)
        stacked_widget.addWidget(initial_screen)
        stacked_widget.addWidget(message_screen)
        self.setGeometry(0,0,screen_height,screen_width)
        self.setStyleSheet("background-color:black;")  #mic k yaha ka niche ka color 
        top_bar =CustomTopBar (self, stacked_widget)
        self.setCentralWidget(stacked_widget)
        self.setMenuWidget(top_bar)
        
def GraphicalUserInterface():
    app =QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    
if __name__ == "__main__":
    GraphicalUserInterface()
    
    

























# from PyQt5.QtWidgets import (
#     QHBoxLayout, QApplication, QMainWindow, QTextEdit, QStackedWidget, QWidget,
#     QLineEdit, QGridLayout, QVBoxLayout, QPushButton, QFrame, QLabel, QSizePolicy
# )
# from PyQt5.QtGui import QIcon, QPainter, QMovie, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat
# from PyQt5.QtCore import Qt, QSize, QTimer
# from dotenv import dotenv_values 
# import sys
# import os 

# # Load environment variables
# env_vars = dotenv_values(".env")
# Assistantname = env_vars.get("Assistantname", "Assistant")  # Default value if none
# current_dir = os.getcwd()

# # Directories
# TempDirPath = os.path.join(current_dir, "Frontend", "Files")
# GraphicsDirPath = os.path.join(current_dir, "Frontend", "Graphics")

# # Ensure directories exist
# if not os.path.exists(TempDirPath):
#     os.makedirs(TempDirPath)
# if not os.path.exists(GraphicsDirPath):
#     os.makedirs(GraphicsDirPath)

# def GraphicsDirectoryPath(Filename):
#     """Returns the full path of a graphic file."""
#     path = os.path.join(GraphicsDirPath, Filename)
#     if not os.path.exists(path):
#         print(f"Error: File not found -> {path}")
#     return path

# def TempDirectoryPath(Filename):
#     """Returns the full path of a temporary file."""
#     return os.path.join(TempDirPath, Filename)

# class ChatSection(QWidget):
#     def __init__(self):
#         super(ChatSection, self).__init__()
#         layout = QVBoxLayout(self)
#         self.chat_text_edit = QTextEdit()
#         self.chat_text_edit.setReadOnly(True)
#         self.chat_text_edit.setTextInteractionFlags(Qt.NoTextInteraction)
#         self.chat_text_edit.setFrameStyle(QFrame.NoFrame)
#         layout.addWidget(self.chat_text_edit)

#         # Apply styles properly
#         self.setStyleSheet("background-color: black; color: white;")
#         self.chat_text_edit.setStyleSheet("border: none; color: white;")

#         # Load GIF safely
#         self.gif_label = QLabel()
#         self.gif_label.setStyleSheet("border: none;")
#         gif_path = GraphicsDirectoryPath("Jarvis.gif")
#         if os.path.exists(gif_path):
#             movie = QMovie(gif_path)
#             movie.setScaledSize(QSize(480, 270))
#             self.gif_label.setMovie(movie)
#             movie.start()
#         else:
#             print("Warning: Jarvis.gif not found!")

#         layout.addWidget(self.gif_label)
#         self.timer = QTimer(self)
#         self.timer.timeout.connect(self.loadMessages)
#         self.timer.start(500)  # Adjusted timer interval

#     def loadMessages(self):
#         """Loads chat messages from a file."""
#         try:
#             with open(TempDirectoryPath("Responses.data"), "r", encoding="utf-8") as file:
#                 messages = file.read().strip()
#                 if messages:
#                     self.chat_text_edit.setPlainText(messages)
#         except FileNotFoundError:
#             pass  # File might not exist initially
# class InitialScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         content_layout = QVBoxLayout()
#         gif_label = QLabel()
        
#         # Load GIF safely
#         gif_path = GraphicsDirectoryPath("Jarvis.gif")
#         if os.path.exists(gif_path):
#             movie = QMovie(gif_path)
#             movie.setScaledSize(QSize(640, 360))  # Adjust size
#             gif_label.setMovie(movie)
#             movie.start()
#         else:
#             print("Warning: Jarvis.gif not found!")

#         content_layout.addWidget(gif_label, alignment=Qt.AlignCenter)
#         self.setLayout(content_layout)
#         self.setStyleSheet("background-color: black;")

# class MessageScreen(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         layout = QVBoxLayout()
#         chat_section = ChatSection()
#         layout.addWidget(chat_section)
#         self.setLayout(layout)
#         self.setStyleSheet("background-color: black;")

# class CustomTopBar(QWidget):
#     def __init__(self, parent, stacked_widget):
#         super().__init__(parent)
#         self.stacked_widget = stacked_widget
#         self.initUI()

#     def initUI(self):
#         self.setFixedHeight(50)
#         layout = QHBoxLayout(self)
#         layout.setAlignment(Qt.AlignRight)

#         home_button = QPushButton("HOME")
#         home_button.setIcon(QIcon(GraphicsDirectoryPath("Home.png")))
#         home_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))

#         message_button = QPushButton("Chat")
#         message_button.setIcon(QIcon(GraphicsDirectoryPath("Chats.png")))
#         message_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(1))

#         close_button = QPushButton()
#         close_button.setIcon(QIcon(GraphicsDirectoryPath("Close.png")))
#         close_button.clicked.connect(self.closeWindow)

#         layout.addWidget(home_button)
#         layout.addWidget(message_button)
#         layout.addWidget(close_button)
#         self.setLayout(layout)

#     def closeWindow(self):
#         """Closes the application."""
#         self.parent().close()

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowFlags(Qt.FramelessWindowHint)
#         self.initUI()

#     def initUI(self):
#         stacked_widget = QStackedWidget(self)
#         initial_screen = InitialScreen(self)
#         message_screen = MessageScreen(self)

#         stacked_widget.addWidget(initial_screen)
#         stacked_widget.addWidget(message_screen)

#         top_bar = CustomTopBar(self, stacked_widget)

#         # Apply a proper layout
#         central_widget = QWidget()
#         layout = QVBoxLayout(central_widget)
#         layout.addWidget(top_bar)
#         layout.addWidget(stacked_widget)
#         self.setCentralWidget(central_widget)

#         self.setStyleSheet("background-color: black;")

# def GraphicalUserInterface():
#     app = QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     GraphicalUserInterface()

