import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QPlainTextEdit, QWidget, QLabel, QComboBox, QVBoxLayout
import nltk
from nltk.chat.util import Chat, reflections
import openai
from PyQt5.QtGui import QPixmap

class SimpleChatbot:
    def __init__(self):
        self.chatbot_pairs = [
            ['hi|hello|hey', ['Hello!', 'Hi there!', 'Hey!']],
            ['what is your name?', ['My name is SimpleChatbot.', 'I am SimpleChatbot.']],
            ['how are you?', ['I am doing well, thank you!', 'I am fine, thanks for asking.']],
            ['bye|goodbye', ['Goodbye!', 'Bye!', 'See you later.']]
        ]
        #self.chatbot = Chat(self.chatbot_pairs, reflections)

    def get_response(self, user_input):
        return self.chatbot.respond(user_input)

    def ask_chatgpt_3P5(self, user_input):
        openai.api_key = ''

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        response = completion.choices[0].message.content
        return response

    def ask_DALL_E(self, user_input):
        openai.api_key = ""

        response = openai.Image.create(
        prompt = user_input,
        n = 1,
        size = "512x512"
        )
        image_url = response['data'][0]['url']
        

class ChatbotGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.chatbot = SimpleChatbot()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple Chatbot')
        self.setGeometry(100, 100, 800, 400)

        self.option_selection = QComboBox(self)
        self.option_selection.move(660, 10)
        self.option_selection.resize(120, 30)
        self.option_selection.addItem('chat_GPT_3.5')
        self.option_selection.addItem('DALL_E')

        self.output_box = QPlainTextEdit(self)
        self.output_box.move(20, 50)
        self.output_box.resize(760, 300)
        self.output_box.setReadOnly(True)

        self.input_box = QPlainTextEdit(self)
        self.input_box.move(20, 360)
        self.input_box.resize(660, 30)

        self.send_button = QPushButton('Send', self)
        self.send_button.move(700, 360)
        self.send_button.resize(80, 30)
        #self.send_button.setStyleSheet('background-color: #298A1F') #'QPushButton {background-color: #A3C1DA; border:  none}'
        self.send_button.setStyleSheet('QPushButton {background-color: #A3C1DA; border: none; font: bold; border-radius: 4px}')
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        user_input = self.input_box.toPlainText()
        self.input_box.clear()
        #response = self.chatbot.get_response(user_input)
        response = self.chatbot.ask_chatgpt_3P5(user_input)
        self.output_box.appendPlainText('You: ' + user_input)
        self.output_box.appendPlainText('Chatbot: ' + response + '\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = ChatbotGUI()
    gui.show()
    sys.exit(app.exec_())
