from PyQt5.QtWidgets import QMainWindow, QFileDialog
from PyQt5.QtCore import pyqtSlot, QUrl, QFileInfo
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
import logging
from tts import TTS
import threading
from ui.mainwindow import Ui_MainWindow


class App(QMainWindow):
    def __init__(self):
        super(App, self).__init__()
        self.ui = Ui_MainWindow()
        self.filename = "./output/out.wav"
        self.ui.setupUi(self)
        self.ui.file_toolButton.clicked.connect(self.__on_chose_file_clicked)
        self.ui.run_pushButton.clicked.connect(self.__on_run_clicled)
        self.ui.listen_pushButton.clicked.connect(self.__on_listen_clicked)
        self.ui.progressBar.setValue(0)
        self.ui.progressBar.hide()
        self.ui.wait_label.hide()
        self.ui.img_label.hide()
        self.ui.file_res_label.hide()
        self.ui.listen_pushButton.hide()
        self.ui.radioButton_allosyl.setChecked(True)
        self.text = ""
        self.tts = TTS(self.filename, "wav")
        self.tts.eventSignal.connect(self.progress_signal)
        self.tts.workDone.connect(self.thread_finished_signal)
        self.player = QMediaPlayer()

        self.mucis_pixmap = QPixmap("./res/music.png")
        self.play_pixmap = QPixmap("./res/play.png")
        self.ui.img_label.setPixmap(self.mucis_pixmap)
        self.ui.listen_pushButton.setIcon(QIcon(self.play_pixmap))

    @pyqtSlot()
    def thread_finished_signal(self):
        self.ui.run_pushButton.setEnabled(True)
        self.ui.listen_pushButton.setEnabled(True)
        self.ui.progressBar.show()
        self.ui.wait_label.show()
        self.ui.img_label.show()
        self.ui.listen_pushButton.show()
        self.ui.file_res_label.setText(os.path.join(os.getcwd(), self.filename))
        self.ui.file_res_label.show()

    @pyqtSlot(str, int)
    def progress_signal(self, str, num):
        self.ui.wait_label.setText(str)
        self.ui.progressBar.setValue(num)
        self.ui.wait_label.update()
        self.ui.progressBar.update()

    def __on_run_clicled(self):
        self.ui.run_pushButton.setEnabled(False)
        self.ui.listen_pushButton.setEnabled(False)
        self.text = self.ui.plainTextEdit.toPlainText()
        self.ui.progressBar.show()
        self.ui.wait_label.show()
        logging.warning("Thread started")
        mode = self.__get_mode()
        thread = threading.Thread(target=self.__thread_function, args=(self.tts, mode))
        thread.start()
        logging.warning("Thread joined")

    def __get_mode(self):
        mode = 0
        if self.ui.radioButton_allosyl.isChecked():
            mode = 4
        return mode

    def __on_listen_clicked(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        else:
            abs_path = QFileInfo(self.filename).absoluteFilePath()
            print(abs_path)
            media_content = QMediaContent(QUrl.fromLocalFile(abs_path))

            self.player.setMedia(media_content)
            self.player.play()

    def __thread_function(self, tts, mode):
        tts.process(self.text, mode)

    def __on_chose_file_clicked(self):
        fname = QFileDialog.getOpenFileName(self, "Open file")[0]
        if fname != "":
            file = open(fname, "r")
            self.text = file.read()
            self.ui.plainTextEdit.setPlainText(self.text)
            self.ui.fname_label.setText(fname)
