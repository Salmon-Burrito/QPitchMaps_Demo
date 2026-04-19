#pyinstaller --onefile --windowed --add-data "Blank_Zone_H.png;." --add-data "Blank_Zone_P.png;." --add-data "ball.png;." --add-data "intended_zone.png;." --add-data "loggers_logo.png;." C:\Users\sbs_f\OneDrive\Desktop\QPitchMaps\QPitchMaps1.2.1.py
from turtle import width
from PyQt5.QtCore import Qt, QDate, QPoint, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,QLabel, QGraphicsOpacityEffect, QCheckBox, QInputDialog, QDialog
from PyQt5.QtWidgets import QMessageBox, QListWidget, QComboBox, QGroupBox, QStackedWidget, QStackedLayout, QTabWidget, QFormLayout, QFileDialog, QSpacerItem, QSlider
from PyQt5.QtWidgets import QSizePolicy, QTableWidget, QTableWidgetItem, QTableView, QListWidgetItem, QGridLayout, QAbstractItemView
from PyQt5.QtGui import QFont, QCursor, QPixmap
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.image as mpimg
import os
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
import sys
import numpy
import shutil
import csv
import sqlite3
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Image, PageBreak, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
import webbrowser



def get_base_path():
    """Return folder where the app/exe is located."""
    if getattr(sys, 'frozen', False):  # Running as PyInstaller EXE
        return os.path.dirname(sys.executable)
    else:  # Running as normal Python script
        return os.path.dirname(os.path.abspath(__file__))

class HomeScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.title = QLabel("Welcome to QPitchMaps (Demo)")
        self.title.setStyleSheet(" QLabel {color: #FFFFFF; font-size: 50pt; font: Optima;background-color: #000000;}")
        
        self.title.setAlignment(Qt.AlignCenter)

        self.player_data = QPushButton("Enter Player Data (Start Here!)")
        self.player_data.setFixedHeight(int(self.height()*0.3))
        self.game_btn = QPushButton("Enter Game Data")
        self.game_btn.setFixedHeight(int(self.height()*0.3))
        self.bullpen_btn = QPushButton("Enter Bullpen Data")
        self.bullpen_btn.setFixedHeight(int(self.height()*0.3))
        
    

        
       
        self.master_layout = QVBoxLayout()
        self.row1 = QHBoxLayout()
        self.row2 = QHBoxLayout()
        self.row3 = QHBoxLayout()

        self.row1.addWidget(self.player_data)
        self.row2.addWidget(self.game_btn)
        self.row2.addWidget(self.bullpen_btn)


        self.master_layout.addWidget(self.title, 50)
        self.master_layout.addLayout(self.row1, 25)
        self.master_layout.addLayout(self.row2, 25)
        self.master_layout.addLayout(self.row3)


        self.setLayout(self.master_layout)



class GameInput(QWidget):
    playersSet = pyqtSignal(str, str, int, int)
    gameSet = pyqtSignal(int)
    def __init__(self):
        super().__init__()


        self.add_team_btn = QPushButton("Add Team")
        self.add_team_btn.clicked.connect(self.addTeam)


        self.game_select = QComboBox()
        self.loadGames()
        self.add_game_btn = QPushButton("Add Game")
        self.add_game_btn.clicked.connect(self.addGame)
        self.set_game_btn =  QPushButton("Set Game")
        self.set_game_btn.clicked.connect(self.getSelectedGameId)



        self.pitcher_input = QComboBox()
        self.pitcher_input.setEditable(True)
        self.pitcher_input.setInsertPolicy(QComboBox.NoInsert)
        self.pitcher_name = self.pitcher_input.currentText()
        self.add_pitcher_btn = QPushButton("Add Pitcher")
        self.hitter_input = QComboBox()
        self.hitter_input.setEditable(True)
        self.hitter_input.setInsertPolicy(QComboBox.NoInsert)
        self.hitter_name = self.hitter_input.currentText()
        self.add_hitter_btn = QPushButton("Add Hitter")

        


        self.set_players_btn = QPushButton("Set Players")

        self.setStyleSheet("QComboBox {font-size: 15pt;} QPushButton {font-size: 15pt;}")


        self.pitcher_id, self.hitter_id = None,None


       


        self.master_layout = QHBoxLayout()

        self.game_group = QGroupBox("Game")
        self.game_group_layout = QFormLayout()

        self.player_group = QGroupBox("Players")
        self.player_group_layout = QFormLayout()


        self.game_group_layout.addRow(self.add_team_btn)
        self.game_group_layout.addRow("Select Game: ", self.game_select)
        self.game_group_layout.addRow(self.add_game_btn, self.set_game_btn)
        self.player_group_layout.addRow("Pitcher Name: ", self.pitcher_input)
        self.player_group_layout.addRow(self.add_pitcher_btn)
        self.player_group_layout.addRow("Hitter Name: ", self.hitter_input)
        self.player_group_layout.addRow(self.add_hitter_btn)
        self.player_group_layout.addRow(self.set_players_btn)

        self.game_group.setLayout(self.game_group_layout)
        self.player_group.setLayout(self.player_group_layout)

        self.master_layout.addWidget(self.game_group)
        self.master_layout.addWidget(self.player_group)

        self.setLayout(self.master_layout)
        self.load_players()


        self.set_players_btn.clicked.connect(self.updateLabels)
        self.add_pitcher_btn.clicked.connect(self.addPitcher)
        self.add_hitter_btn.clicked.connect(self.addHitter)
        


    def load_players(self):
        pitcher_list = []
        hitter_list = []
        query = QSqlQuery("SELECT first_name, last_name, team FROM pitchers")
        while query.next():
            first_name = query.value(0)
            last_name = query.value(1)
            team = query.value(2)
            full_name = f"{first_name} {last_name}, {team}"
            pitcher_list.append(full_name)
       


       
        query = QSqlQuery("SELECT first_name, last_name, team FROM hitters")
        while query.next():
            first_name = query.value(0)
            last_name = query.value(1)
            team = query.value(2)
            full_name = f"{first_name} {last_name}, {team}"
            hitter_list.append(full_name)
           
        self.pitcher_input.addItems(pitcher_list)
        self.hitter_input.addItems(hitter_list)


    def addPitcher(self):
            first_name, ok1 = QInputDialog.getText(self, "Add Pitcher", "First Name:")
            last_name, ok2 = QInputDialog.getText(self, "Add Pitcher", "Last Name:")
            handedness, ok4 = QInputDialog.getItem(self, "Add Pitcher", "Select Handedness: ", ["Right", "Left", "Switch", "hold"], 0, False)
            teams = self.pullTeams()
            team_names = [team[1] for team in teams]
            team, ok3 = QInputDialog.getItem(self, "Add Pitcher", "Select Team:", team_names, 0, False)
            team_id = self.pull_team_id(team)
            if ok1 and ok2 and ok3 and ok4:
                insert_query = QSqlQuery()
                insert_query.prepare("INSERT INTO pitchers (first_name, last_name, handedness, team, team_id) VALUES (?, ?, ?, ?, ?)")
                insert_query.addBindValue(first_name)
                insert_query.addBindValue(last_name)
                insert_query.addBindValue(handedness)
                insert_query.addBindValue(team)
                insert_query.addBindValue(team_id)
                insert_query.exec_()
                self.pitcher_input.addItem(f"{first_name} {last_name}, {team}")
                self.pitcher_input.setCurrentIndex(self.pitcher_input.count() - 1)


    def addHitter(self):
            first_name, ok1 = QInputDialog.getText(self, "Add Hitter", "First Name:")
            last_name, ok2 = QInputDialog.getText(self, "Add Hitter", "Last Name:")
            handedness, ok4 = QInputDialog.getItem(self, "Add Hitter", "Select Handedness:", ["Right", "Left", "Switch", "hold"], 0, False)
            teams = self.pullTeams()
            team_names = [team[1] for team in teams]
            team, ok3 = QInputDialog.getItem(self, "Add Pitcher", "Select Team:", team_names, 0, False)
            team_id = self.pull_team_id(team)
            if ok1 and ok2 and ok3 and ok4:
                insert_query = QSqlQuery()
                insert_query.prepare("INSERT INTO hitters (first_name, last_name, handedness, team, team_id) VALUES (?, ?, ?, ?,?)")
                insert_query.addBindValue(first_name)
                insert_query.addBindValue(last_name)
                insert_query.addBindValue(handedness)
                insert_query.addBindValue(team)
                insert_query.addBindValue(team_id)
                insert_query.exec_()
                self.hitter_input.addItem(f"{first_name} {last_name}, {team}")
                self.hitter_input.setCurrentIndex(self.hitter_input.count() - 1)
       
    def updateLabels(self):
        self.pitcher_name = self.pitcher_input.currentText()
        self.pitcher_name = self.pitcher_name.split(",")[0]
        self.hitter_name = self.hitter_input.currentText()
        self.hitter_name = self.hitter_name.split(",")[0]
        self.pitcher_id,self.hitter_id = self.pullIds()
        self.playersSet.emit(self.pitcher_name, self.hitter_name, self.pitcher_id, self.hitter_id)
       
    def pullIds(self):
        pitcher_id = None
        hitter_id = None
        if self.pitcher_name is not None:
            query = QSqlQuery()
            query.prepare("SELECT id FROM pitchers WHERE first_name || ' ' || last_name = ?")
            query.addBindValue(self.pitcher_name)
            query.exec_()
            if query.next():
                pitcher_id = query.value(0)

        if self.hitter_name is not None:
            query.prepare("SELECT id FROM hitters WHERE first_name || ' ' || last_name = ?")
            query.addBindValue(self.hitter_name)
            query.exec_()
            if query.next():
                hitter_id = query.value(0)


        return pitcher_id, hitter_id


    def loadGames(self):
        game_list = []
        query = QSqlQuery("SELECT id, game_date, opponent FROM games")
        while query.next():
            game_id = query.value(0)
            game_date = query.value(1)
            opponent = query.value(2)
            display_text = f"{game_date} vs {opponent}"
            game_list.append((game_id, display_text))
       
        for game_id, display_text in game_list:
            self.game_select.addItem(display_text, game_id)
   
    def addGame(self):
        game_date, ok1 = QInputDialog.getText(self, "Add Game", "Game Date (YYYYMMDD):")
        team_input = QComboBox()
        teams = self.pullTeams()
        team_names = [team[1] for team in teams]
        team_input.addItems(team_names)
        opponent, ok2 = QInputDialog.getItem(self, "Add Game", "Select Opponent:", team_names, 0, False)
        opponent_id = self.pull_team_id(opponent)
        away, ok3 = QInputDialog.getItem(self, "Add Game", "Is it an away game?", ["No", "Yes"], 0, False)
        away = 1 if away == "Yes" else 0
        if ok1 and ok2 and ok3:
            insert_query = QSqlQuery()
            insert_query.prepare("INSERT INTO games (game_date, opponent, opponent_id, away) VALUES (?, ?, ?, ?)")
            insert_query.addBindValue(game_date)
            insert_query.addBindValue(opponent)
            insert_query.addBindValue(int(opponent_id))
            insert_query.addBindValue(away)
            insert_query.exec_()
        self.loadGames()
   
    def pullTeams(self):
        teams = []
        query = QSqlQuery("SELECT id, team_name FROM teams")
        while query.next():
            team_id = query.value(0)
            team_name = query.value(1)
            teams.append((team_id, team_name))
        return teams


    def pull_team_id(self, team_name):
        if team_name is None:
            return None
        query = QSqlQuery()
        query.prepare("SELECT id FROM teams WHERE team_name = ?")
        query.addBindValue(team_name)
        query.exec_()
        if query.next():
            return query.value(0)
        return None
   
    def addTeam(self):
        team_name, ok = QInputDialog.getText(self, "Add Team", "Team Name:")
        if ok:
            insert_query = QSqlQuery()
            insert_query.prepare("INSERT INTO teams (team_name) VALUES (?)")
            insert_query.addBindValue(team_name)
            insert_query.exec_()
   
    def getSelectedGameId(self):
        if self.game_select.currentData() is not (None or "" or " "):
            self.gameSet.emit(self.game_select.currentData())
        else:
            self.gameSet.emit(None)
    
    def bulkLoadTeam(self):
        players = []
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Player List",
            "",
            "CSV Files (*.csv)"
        )
        if file_path:
            with open(file_path, 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                for row in csv_reader:
                    first = row[0]
                    last = row[1]
                    pos = row[2]
                    pitcher = (True if (('P') in pos) else False)
                    hit = row [4]
                    throw = row[5]
                    handedness = {
                        'L' : 'Left',
                        'R' : 'Right',
                        'S' : 'Switch'
                    }
                    if hit == 'L':
                        handedness = 'Left'
                    elif handedness == 'R':
                        handedness = 'Right'
                    elif handedness == 'S':
                        handedness = 'Switch'
                    else:
                        handedness = 'Hold'

                    team = row[7]
                    players.append((first,last,pitcher,handedness, team))
        return players

    def bulkInputTeam(self):
        players = self.bulkLoadTeam()
        print(players)

    



#Create Zone
class ClickableLabel(QLabel):
    clicked = pyqtSignal(int, int)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            self.clicked.emit(x, y)



class QPitchMapsInput (QWidget):
    def __init__(self):
        super().__init__()


        #
        self.velo_input = QLineEdit()
        self.velo_input.setStyleSheet("QLineEdit {font-size: 15pt;}")
        self.pitchtype_input = QComboBox()
        self.setStyleSheet("QComboBox {font-size: 15pt;}")
        self.pitchtype_input.addItems(["","4FB","SI","CUT", "CH", "SL" ,"CU","SW", "SPL", "KN", "OTHER" ])


        self.result_box = QComboBox()
        self.result_box.addItems(["","BALL","QM","STRIKE","WHIFF","FOUL","INPLAY"])


        self.submit_btn = QPushButton("Submit Pitch")
        self.submit_btn.setStyleSheet("QPushButton {font-size: 15pt; background-color: #000000; color: #FFFFFF; padding: 10px; border-radius: 5px;} QPushButton:hover {background-color: #990000;}")

        self.make_opposing_lineup_btn = QPushButton("Create Opposing Lineup")

        self.opposing_lineup_list = QListWidget()
        self.opposing_pitcher_list = QListWidget()

        self.make_lineup_btn = QPushButton("Create Lineup")
        self.select_players_btn = QPushButton("Select Players")
        self.select_players_btn.setStyleSheet("QPushButton {font-size: 15pt; background-color: #000000; color: #FFFFFF; padding: 10px; border-radius: 5px;} QPushButton:hover {background-color: #990000;}")
        self.lineup_list = QListWidget()
        self.pitcher_list = QListWidget()

        #Toggle pitcher or hitter view
        self.mode_toggle_label = QLabel("Pitcher View:")
        self.mode_toggle = QCheckBox()


        #Player Labels
       
        self.player_info = QLabel("Pitcher: \nHitter: \n")
        self.team_info = QLabel("Opponent: \n")
        self.balls_count = 0
        self.strikes_count = 0
        self.count_label = QLabel(f"Ball: {self.balls_count} Strikes: {self.strikes_count}")
        self.reset_count_btn = QPushButton("Reset Count")
        self.strike_up_button = QPushButton("Strike +1")
        self.ball_up_button = QPushButton("Ball +1")
        self.strike_up_button.setStyleSheet("QPushButton {font-size: 10pt; background-color: #000000; color: #FFFFFF; padding: 10px; border-radius: 5px;} QPushButton:hover {background-color: #990000;}")
        self.ball_up_button.setStyleSheet("QPushButton {font-size: 10pt; background-color: #000000; color: #FFFFFF; padding: 10px; border-radius: 5px;} QPushButton:hover {background-color: #990000;}")


        #Working on getting a clickable image in the strike zone
        def resource_path(relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
       

        self.scale =  int(self.width()*2)
        self.zone_clickable = ClickableLabel()
        self.pixmap_h = QPixmap(resource_path("Blank_Zone_H.png"))
        self.pixmap_p = QPixmap(resource_path("Blank_Zone_P.png"))
        #self.image_dir_h = os.path.join(__file__.replace("QPitchMapsBeta0.2.py","Blank_Zone_H.png"))
        #self.pixmap_h = QPixmap(self.image_dir_h)
        #self.pixmap_p = QPixmap(os.path.join(__file__.replace("QPitchMapsBeta0.2.py","Blank_Zone_P.png")))
        self.scaled_pixmap_h = self.pixmap_h.scaled(
                        self.scale,
                        self.scale,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
        self.scaled_pixmap_p = self.pixmap_p.scaled(
                        self.scale,
                        self.scale,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
        self.zone_clickable.setPixmap(self.scaled_pixmap_h)
        self.zone_clickable.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.zone_clickable.setFixedSize(self.scaled_pixmap_h.size())
        self.isP = False


        #Initializes the pointer object (Ball)
        self.ball = QLabel(self)

        ball_pixmap = QPixmap(resource_path("ball.png"))
        #ball_pixmap = QPixmap(os.path.join(__file__.replace("QPitchMapsBeta0.2.py","ball.png")))
        ball_scaled = ball_pixmap.scaled(int(0.02667 * self.zone_clickable.width()),int(0.02667 * self.zone_clickable.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ball.setPixmap(ball_scaled)
        self.ball.setFixedSize(ball_scaled.size())
        self.ball.hide()
        self.ball.raise_()
       


        #Initializes the coordinate lists and player ids
        self.mouse_x_list = []
        self.mouse_y_list = []
        self.working_pitcher_id = None
        self.working_hitter_id = None
        self.team_id = None
        self.team_name = None
        self.game_id = None
        self.pa_result = None
        self.temp_x = None
        self.temp_y = None
        #retrives the x and y location of the mouse click
        def get_location(x, y):
            self.temp_x = x/self.zone_clickable.width()
            self.temp_y = y/self.zone_clickable.height()
            #Moves the ball to the clicked location
            self.ball.move(self.zone_clickable.x() + x + self.location_group.x() - self.ball.width() // 2,
                           self.zone_clickable.y() + y + self.location_group.y() - self.ball.height() // 2)
            self.ball.raise_()
            self.ball.show()


            #print(self.mouse_x_list,self.mouse_y_list)


        #
        self.master_layout = QHBoxLayout()

        #
        self.pitchinfo_group = QGroupBox("Pitch Info")
        self.pitchinfo_layout = QFormLayout()
        self.view_layout = QFormLayout()

        self.opposing_btns = QHBoxLayout()
        self.opposing_capsule = QWidget()
        self.lineup_btns = QHBoxLayout()
        self.lineup_capsule = QWidget()

        self.opposing_btns.addWidget(self.make_opposing_lineup_btn)
        self.opposing_capsule.setLayout(self.opposing_btns)

        self.lineup_btns.addWidget(self.make_lineup_btn)
        self.lineup_capsule.setLayout(self.lineup_btns)



        self.pitchinfo_layout.addRow("Pitch Velocity: ",self.velo_input)
        self.pitchinfo_layout.addRow("Pitch Type: ",self.pitchtype_input)
        self.pitchinfo_layout.addRow("Pitch Result: ",self.result_box)
        self.pitchinfo_layout.addRow(self.submit_btn)
        self.pitchinfo_layout.addRow(self.opposing_capsule)
        self.pitchinfo_layout.addRow(self.opposing_lineup_list)
        self.pitchinfo_layout.addRow(self.opposing_pitcher_list)
        self.pitchinfo_layout.addRow(self.lineup_capsule)
        self.pitchinfo_layout.addRow(self.lineup_list)
        self.pitchinfo_layout.addRow(self.pitcher_list)
        self.pitchinfo_layout.addRow(self.select_players_btn)


        self.pitchinfo_group.setLayout(self.pitchinfo_layout)




        self.master_layout.addWidget(self.pitchinfo_group,35)


        #
        self.location_group = QGroupBox("Pitch Location")
        self.location_layout = QHBoxLayout()


        self.view_layout.addWidget(self.mode_toggle_label)
        self.view_layout.addWidget(self.mode_toggle)
        self.view_layout.addWidget(self.player_info)
        self.view_layout.addWidget(self.team_info)
        self.view_layout.addWidget(self.count_label)
        self.view_layout.addWidget(self.reset_count_btn)
        self.view_layout.addWidget(self.strike_up_button)
        self.view_layout.addWidget(self.ball_up_button)

        self.location_layout.addWidget(self.zone_clickable)
        self.location_group.setLayout(self.location_layout)




        self.master_layout.addWidget(self.location_group, 70)
        self.master_layout.addLayout(self.view_layout)




        self.setLayout(self.master_layout)




        self.zone_clickable.clicked.connect(get_location)
        self.mode_toggle.stateChanged.connect(self.toggle_mode)
        self.submit_btn.clicked.connect(lambda: self.submit_pitch(self.temp_x, self.temp_y))
        self.reset_count_btn.clicked.connect(self.resetCount)
        self.strike_up_button.clicked.connect(self.strikeUp)
        self.ball_up_button.clicked.connect(self.ballUp)
        self.make_opposing_lineup_btn.clicked.connect(self.createOpposingLineup)
        self.make_lineup_btn.clicked.connect(self.createLineup)
        self.select_players_btn.clicked.connect(self.selectPlayers)

        self.opposing_lineup_list.itemSelectionChanged.connect(lambda: self.deselect(self.lineup_list))
        self.lineup_list.itemSelectionChanged.connect(lambda: self.deselect(self.opposing_lineup_list))
        self.opposing_pitcher_list.itemSelectionChanged.connect(lambda: self.deselect(self.pitcher_list))
        self.pitcher_list.itemSelectionChanged.connect(lambda: self.deselect(self.opposing_pitcher_list))
       
    def submit_pitch(self,x,y):
        if x is None or y is None:
            QMessageBox.warning(self, "Input Error", "Please click on the strike zone to input pitch location.")
            return
        else:
            if self.result_box.currentText() == "INPLAY":
                self.select_pa_result()
            self.mouse_x_list.append(x)
            self.mouse_y_list.append(y)
            self.storeValues()
            self.ball.hide()
           


    def select_pa_result(self):
        pa_results = ["Single", "Double", "Triple", "Home Run", "Ground Out", "Fly Out", "Line Out"]
        result, ok = QInputDialog.getItem(self, "Select PA Result", "Result:", pa_results, 0, False)
        if result and ok:
            self.pa_result = result
           


    def storeValues(self):
        x = self.mouse_x_list[-1]
        y = self.mouse_y_list[-1]
        if self.isP:
            x = 1 - x
        velo_text = self.velo_input.text()
        pitcher = self.getPitcher()
        hitter = self.getHitter()
        game = self.getGame()
        print(pitcher, hitter, game)
        ok1 = QMessageBox.question(self, "Confirm Submission", f"Pitch at ({x}, {y}) ({self.balls_count}-{self.strikes_count})\nPitchType: {self.pitchtype_input.currentText() or None} \nPAResult {self.pa_result} \nVelo: {float(velo_text) if velo_text else None}\nPitcher: {pitcher}\nHitter: {hitter}\nGame: {game}", QMessageBox.Yes | QMessageBox.No)
        if ok1 == QMessageBox.Yes:
            query = QSqlQuery()


            query.prepare("""
                INSERT INTO pitchinput (
                    pitch_x,
                    pitch_y,
                    balls,
                    strikes,
                    pitch_type,
                    pitch_velocity,
                    pitch_result,
                    pa_result,
                    pitcher_id,
                    hitter_id,
                    game_id
                
                ) VALUES (
                    :x,
                    :y,
                    :b,
                    :s,
                    :ptype,
                    :velo,
                    :result,
                    :pa,
                    :pid,
                    :hid,
                    :game_id
                )
            """)


            


            query.bindValue(":x", x)
            query.bindValue(":y", y)
            query.bindValue(":b", self.balls_count)
            query.bindValue(":s", self.strikes_count)
            query.bindValue(":ptype", self.pitchtype_input.currentText() or None)
            query.bindValue(":result", self.result_box.currentText())
            query.bindValue(":pa", self.pa_result)
            
            query.bindValue(":velo", float(velo_text) if velo_text else None)


            query.bindValue(":pid", self.working_pitcher_id)
            query.bindValue(":hid", self.working_hitter_id)
            query.bindValue(":game_id", self.game_id)

            


            QMessageBox.information(self, "Pitch Submitted", f"Pitch at ({x}, {y}) ({self.balls_count}-{self.strikes_count})\nPitchType: {self.pitchtype_input.currentText() or None} \nPAResult {self.pa_result} \nVelo: {float(velo_text) if velo_text else None}\nPitcher: {pitcher}\nHitter: {hitter}\nGame: {game}")
            if not query.exec_():
                print("QUERY:", query.lastQuery())
                print("VALUES:", query.boundValues())
                print("SQL ERROR:", query.lastError().text())

            if self.result_box.currentText() == "INPLAY":
                self.balls_count = 0
                self.strikes_count = 0
            elif self.result_box.currentText() == "BALL" or self.result_box.currentText() == "QM":
                self.balls_count += 1
                if self.balls_count >= 4:
                    self.balls_count = 0
                    self.strikes_count = 0
            elif self.result_box.currentText() == "STRIKE" or self.result_box.currentText() == "WHIFF":
                self.strikes_count += 1
                if self.strikes_count >= 3:
                    self.strikes_count = 0
                    self.balls_count = 0
            elif self.result_box.currentText() == "FOUL":
                if self.strikes_count < 2:
                    self.strikes_count +=1
            self.count_label.setText(f"Ball: {self.balls_count} Strikes: {self.strikes_count}")

            self.pa_result = None

    def resetCount(self):
        self.strikes_count = 0
        self.balls_count = 0
        self.count_label.setText(f"Ball: {self.balls_count} Strikes: {self.strikes_count}")

    def getPitcher(self):
        pitcher = None
        query = QSqlQuery()
        query.prepare("""SELECT first_name, last_name FROM pitchers WHERE id = ?""")
        query.addBindValue(self.working_pitcher_id)
        query.exec_()
        if query.next():
            pitcher = f"{query.value(0)} {query.value(1)}"
        return pitcher
    
    def getHitter(self):
        hitter = None
        query = QSqlQuery()
        query.prepare("""SELECT first_name, last_name FROM hitters WHERE id = ?""")
        query.addBindValue(self.working_hitter_id)
        query.exec_()
        if query.next():
            hitter = f"{query.value(0)} {query.value(1)}"
        return hitter
    
    def getGame(self):
        game = None
        query = QSqlQuery()
        query.prepare("""SELECT game_date, opponent, away FROM games WHERE id = ?""")
        query.addBindValue(self.game_id)
        query.exec_()
        if query.next():
            game = f"{query.value(0)} vs {query.value(1)} {query.value(2)}"
        return game

    def toggle_mode(self):
        if self.mode_toggle.isChecked():
            self.zone_clickable.setPixmap(self.scaled_pixmap_p)
            self.zone_clickable.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.zone_clickable.setFixedSize(self.scaled_pixmap_p.size())
            self.isP = True
        else:
            self.zone_clickable.setPixmap(self.scaled_pixmap_h)
            self.zone_clickable.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.zone_clickable.setFixedSize(self.scaled_pixmap_h.size())
            self.isP = False


    def updateLabels(self,pitcher, hitter, pitcher_id, hitter_id):
        self.working_pitcher_id = pitcher_id
        self.working_hitter_id = hitter_id
        self.player_info.setText(f"Pitcher: {pitcher} \nHitter: {hitter}")


    def retriveGame(self, game_id):
        self.game_id = game_id
        if game_id is not None:
            #print(self.game_id)
            query = QSqlQuery()
            query.prepare("SELECT game_date, away, opponent FROM games WHERE id = ?")
            query.addBindValue(game_id)
            query.exec_()
            while query.next():
                self.team_name = query.value(2)
                game_date = query.value(0)
                away = query.value(1)
                self.team_info.setText(f"Opponent: {self.team_name} on {game_date} {'(Away)' if away else '(Home)'}")
        else:
            self.team_info.setText("No game selected")

    def strikeUp(self):
        self.strikes_count += 1
        if self.strikes_count >= 3:
            self.strikes_count = 0
            self.balls_count = 0
        self.count_label.setText(f"Ball: {self.balls_count} Strikes: {self.strikes_count}")

    def ballUp(self):
        self.balls_count += 1
        if self.balls_count >= 4:
            self.balls_count = 0
            self.strikes_count = 0
        self.count_label.setText(f"Ball: {self.balls_count} Strikes: {self.strikes_count}")
       
    def createOpposingLineup(self):
        hitter_names_away = QDialog()
        hitter_names_away.setWindowTitle("Select Hitters For Opposing Team")
        hitter_names_away.resize(800,600)
        main_layout = QVBoxLayout()

        row1 = QHBoxLayout()

        opposing_full_list = QListWidget()
        opposing_lineup_list = QListWidget()

        opposing_lineup_list.setDragDropMode(QAbstractItemView.DragDrop)
        opposing_lineup_list.setDefaultDropAction(Qt.MoveAction)
        opposing_lineup_list.setDragEnabled(True)
        opposing_lineup_list.setAcceptDrops(True)
        opposing_full_list.setDragDropMode(QAbstractItemView.DragDrop)
        opposing_full_list.setDefaultDropAction(Qt.MoveAction)
        opposing_full_list.setDragEnabled(True)
        opposing_full_list.setAcceptDrops(True)

        query = QSqlQuery("SELECT id, first_name, last_name, team, handedness FROM hitters ORDER BY team")
        while query.next():
            hitter_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            hand = query.value(4)
            full_name = f"{first_name} {last_name} ({team}) - {hand}"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, hitter_id)
            opposing_full_list.addItem(item)

        row1.addWidget(opposing_full_list)
        row1.addWidget(opposing_lineup_list)

        submit_btn = QPushButton("Submit")

        main_layout.addWidget(QLabel("Select OPPOSING Lineup"))
        main_layout.addLayout(row1)
        main_layout.addWidget(submit_btn)

        hitter_names_away.setLayout(main_layout)

        submit_btn.clicked.connect(hitter_names_away.accept)

        opposing_lineup_list.setStyleSheet("QListWidget {font-size: 15pt;}")
        opposing_full_list.setStyleSheet("QListWidget {font-size: 15pt;}")

        hitter_names_away.exec()

        self.opposing_lineup_list.clear()
        if hitter_names_away.result() == QDialog.DialogCode.Accepted:
            for i in range(opposing_lineup_list.count()):
                self.opposing_lineup_list.addItem(opposing_lineup_list.item(i).clone())
        self.createOpposingLineupPitcher()

    def createOpposingLineupPitcher(self):
        pitcher_name_away = QDialog()
        pitcher_name_away.setWindowTitle("Select Pitcher for Opposing Team")
        pitcher_name_away.resize(800,600)
        main_layout = QVBoxLayout()

        row1 = QHBoxLayout()

        opposing_full_list = QListWidget()
        opposing_lineup_list = QListWidget()

        opposing_lineup_list.setDragDropMode(QAbstractItemView.DragDrop)
        opposing_lineup_list.setDefaultDropAction(Qt.MoveAction)
        opposing_lineup_list.setDragEnabled(True)
        opposing_lineup_list.setAcceptDrops(True)
        opposing_full_list.setDragDropMode(QAbstractItemView.DragDrop)
        opposing_full_list.setDefaultDropAction(Qt.MoveAction)
        opposing_full_list.setDragEnabled(True)
        opposing_full_list.setAcceptDrops(True)

        query = QSqlQuery("SELECT id, first_name, last_name, team, handedness FROM pitchers ORDER BY team")
        while query.next():
            pitcher_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            hand = query.value(4)
            full_name = f"{first_name} {last_name} ({team}) - {hand}"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, pitcher_id)
            opposing_full_list.addItem(item)

        row1.addWidget(opposing_full_list)
        row1.addWidget(opposing_lineup_list)

        submit_btn = QPushButton("Submit")

        main_layout.addWidget(QLabel("Select OPPOSING Pitcher"))
        main_layout.addLayout(row1)
        main_layout.addWidget(submit_btn)

        pitcher_name_away.setLayout(main_layout)

        submit_btn.clicked.connect(pitcher_name_away.accept)

        opposing_lineup_list.setStyleSheet("QListWidget {font-size: 15pt;}")
        opposing_full_list.setStyleSheet("QListWidget {font-size: 15pt;}")

        pitcher_name_away.exec()

        self.opposing_pitcher_list.clear()
        if pitcher_name_away.result() == QDialog.DialogCode.Accepted:
            for i in range(opposing_lineup_list.count()):
                self.opposing_pitcher_list.addItem(opposing_lineup_list.item(i).clone())
        
    def createLineup(self):
        hitter_names = QDialog()
        hitter_names.setWindowTitle("Select Hitters For Your Team")
        hitter_names.resize(800,600)
        main_layout = QVBoxLayout()

        row1 = QHBoxLayout()

        full_list = QListWidget()
        lineup_list = QListWidget()

        lineup_list.setDragDropMode(QAbstractItemView.DragDrop)
        lineup_list.setDefaultDropAction(Qt.MoveAction)
        lineup_list.setDragEnabled(True)
        lineup_list.setAcceptDrops(True)
        full_list.setDragDropMode(QAbstractItemView.DragDrop)
        full_list.setDefaultDropAction(Qt.MoveAction)
        full_list.setDragEnabled(True)
        full_list.setAcceptDrops(True)

        query = QSqlQuery("SELECT id, first_name, last_name, team, handedness FROM hitters ORDER BY team")
        while query.next():
            hitter_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            hand = query.value(4)
            full_name = f"{first_name} {last_name} ({team}) - {hand}"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, hitter_id)
            full_list.addItem(item)

        row1.addWidget(full_list)
        row1.addWidget(lineup_list)

        submit_btn = QPushButton("Submit")

        main_layout.addWidget(QLabel("Select OPPOSING Lineup"))
        main_layout.addLayout(row1)
        main_layout.addWidget(submit_btn)

        hitter_names.setLayout(main_layout)

        submit_btn.clicked.connect(hitter_names.accept)

        lineup_list.setStyleSheet("QListWidget {font-size: 15pt;}")
        full_list.setStyleSheet("QListWidget {font-size: 15pt;}")

        hitter_names.exec()

        self.lineup_list.clear()
        if hitter_names.result() == QDialog.DialogCode.Accepted:
            for i in range(lineup_list.count()):
                self.lineup_list.addItem(lineup_list.item(i).clone())
        self.createLineupPitcher()

    def createLineupPitcher(self):
        pitcher_name = QDialog()
        pitcher_name.setWindowTitle("Select Pitcher For Your Team")
        pitcher_name.resize(800,600)
        main_layout = QVBoxLayout()

        row1 = QHBoxLayout()

        full_list = QListWidget()
        lineup_list = QListWidget()

        lineup_list.setDragDropMode(QAbstractItemView.DragDrop)
        lineup_list.setDefaultDropAction(Qt.MoveAction)
        lineup_list.setDragEnabled(True)
        lineup_list.setAcceptDrops(True)
        full_list.setDragDropMode(QAbstractItemView.DragDrop)
        full_list.setDefaultDropAction(Qt.MoveAction)
        full_list.setDragEnabled(True)
        full_list.setAcceptDrops(True)

        query = QSqlQuery("SELECT id, first_name, last_name, team, handedness FROM pitchers ORDER BY team")
        while query.next():
            pitcher_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            hand = query.value(4)
            full_name = f"{first_name} {last_name} ({team}) - {hand}"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, pitcher_id)
            full_list.addItem(item)

        row1.addWidget(full_list)
        row1.addWidget(lineup_list)

        submit_btn = QPushButton("Submit")

        main_layout.addWidget(QLabel("Select Pitcher"))
        main_layout.addLayout(row1)
        main_layout.addWidget(submit_btn)

        pitcher_name.setLayout(main_layout)

        submit_btn.clicked.connect(pitcher_name.accept)

        lineup_list.setStyleSheet("QListWidget {font-size: 15pt;}")
        full_list.setStyleSheet("QListWidget {font-size: 15pt;}")

        pitcher_name.exec()

        self.pitcher_list.clear()
        if pitcher_name.result() == QDialog.DialogCode.Accepted:
            for i in range(lineup_list.count()):
                self.pitcher_list.addItem(lineup_list.item(i).clone())
    
    def selectPlayers(self):
        opposing_hitter = self.opposing_lineup_list.selectedItems()
        opposing_pitcher = self.opposing_pitcher_list.selectedItems()

        hitter = self.lineup_list.selectedItems()
        pitcher = self.pitcher_list.selectedItems()
        
        pitcher_name = ""
        hitter_name = ""

        if pitcher:
            self.working_pitcher_id = pitcher[0].data(Qt.UserRole)
            pitcher_name = pitcher[0].text()
        elif opposing_pitcher:
            self.working_pitcher_id = opposing_pitcher[0].data(Qt.UserRole)
            pitcher_name = opposing_pitcher[0].text()
        
        if hitter:
            self.working_hitter_id = hitter[0].data(Qt.UserRole)
            hitter_name = hitter[0].text()
        elif opposing_hitter:
            self.working_hitter_id = opposing_hitter[0].data(Qt.UserRole)
            hitter_name = opposing_hitter[0].text()

        self.updateLabels(pitcher_name, hitter_name, self.working_pitcher_id, self.working_hitter_id)
    
    def deselect(self, list):
        list.clearSelection()

        
        

       
#Create SQL Database
def resource_path():
    """
    Get absolute path to resource, works for dev and for PyInstaller --onefile
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except AttributeError:
        base_path = os.path.abspath(".")
    return base_path

db_path = os.path.join(get_base_path(), "pitchinput.db")


database = QSqlDatabase.addDatabase("QSQLITE")
database.setDatabaseName(db_path)
if not database.open():
    QMessageBox.critical(None, "Error", "Could not open Database")
    sys.exit(1)



query = QSqlQuery()
query.exec_("""
            CREATE TABLE IF NOT EXISTS pitchinput (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                pitch_x REAL,
                pitch_y REAL,
                balls INTEGER,
                strikes INTEGER,
                pitch_type TEXT,
                pitch_result TEXT,
                pa_result TEXT,
                pitch_velocity REAL,
                pitcher_id INTEGER,
                hitter_id INTEGER,
                game_id INTEGER,
                FOREIGN KEY (pitcher_id) REFERENCES pitchers(id),
                FOREIGN KEY (hitter_id) REFERENCES hitters(id),
                FOREIGN KEY (game_id) REFERENCES games(id)
               
            )""")

query.exec_("""
            CREATE TABLE IF NOT EXISTS bullpeninput (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                intended_x REAL,
                intended_y REAL,
                pitch_x REAL,
                pitch_y REAL,
                pitch_type TEXT,
                pitch_velocity REAL,
                pitcher_id INTEGER,
                FOREIGN KEY (pitcher_id) REFERENCES pitchers(id)
            )""")

query.exec_("""
            CREATE TABLE IF NOT EXISTS pitchers (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                handedness TEXT,
                team TEXT,
                team_id INTEGER,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
        """)
query.exec_("""
            CREATE TABLE IF NOT EXISTS hitters (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT,
                last_name TEXT,
                handedness TEXT,
                team TEXT,
                team_id INTEGER,
                FOREIGN KEY (team_id) REFERENCES teams(id)
            )
    """)
query.exec_("""
            CREATE TABLE IF NOT EXISTS games (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                game_date INTEGER,
                opponent TEXT,
                opponent_id INTEGER,
                away INTEGER,
                bullpen_mode INTEGER,
                FOREIGN KEY (opponent_id) REFERENCES teams(id))
            """)
query.exec_("""
            CREATE TABLE IF NOT EXISTS teams (
                id  INTEGER PRIMARY KEY AUTOINCREMENT,
                team_name TEXT
            )
            """)

class BullpenClickableLabel(QLabel):
    clicked = pyqtSignal(int, int)
    x = None
    y = None
    #Intended x and y coordinates
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            self.clicked.emit(x, y)
                

    


class BullpenInput(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("QPushButton {font-size: 15pt; background-color: #000000; color: #FFFFFF; padding: 10px; border-radius: 5px;} QPushButton:hover {background-color: #990000;}")
        self.velo_input = QLineEdit()
        self.velo_input.setStyleSheet("QLineEdit {font-size: 15pt;}")
        self.pitchtype_input = QComboBox()
        self.pitchtype_input.setStyleSheet("QComboBox {font-size: 15pt;}")
        self.pitchtype_input.addItems(["","4FB","SI","CUT", "CH", "SL" ,"CU","SW", "SPL", "KN", "OTHER" ])
        self.submit_btn = QPushButton("Submit Pitch")

        self.mode_toggle_label = QLabel("Pitcher View:")
        self.mode_toggle = QCheckBox()


        #Player Labels
       
        self.player_info = QLabel("Pitcher: ")
        self.bullpen_label = QLabel("Bullpen Mode")


        #Working on getting a clickable image in the strike zone
        def resource_path(relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
       

        self.scale =  int(self.width()*2)
        self.zone_clickable = ClickableLabel()
        self.pixmap_h = QPixmap(resource_path("Blank_Zone_H.png"))
        self.pixmap_p = QPixmap(resource_path("Blank_Zone_P.png"))
        #self.image_dir_h = os.path.join(__file__.replace("QPitchMapsBeta0.2.py","Blank_Zone_H.png"))
        #self.pixmap_h = QPixmap(self.image_dir_h)
        #self.pixmap_p = QPixmap(os.path.join(__file__.replace("QPitchMapsBeta0.2.py","Blank_Zone_P.png")))
        self.scaled_pixmap_h = self.pixmap_h.scaled(
                        self.scale,
                        self.scale,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
        self.scaled_pixmap_p = self.pixmap_p.scaled(
                        self.scale,
                        self.scale,
                        Qt.KeepAspectRatioByExpanding,
                        Qt.SmoothTransformation
                    )
        self.zone_clickable.setPixmap(self.scaled_pixmap_h)
        self.zone_clickable.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.zone_clickable.setFixedSize(self.scaled_pixmap_h.size())
        self.isP = False

        self.intended_zone = QLabel(self)
        intended_pixmap = QPixmap(resource_path("intended_zone.png"))
        #intended_pixmap = QPixmap(os.path.join((__file__.replace("QPitchMapsBeta0.2.py","")),"intended_zone.png"))
        intended_scaled = intended_pixmap.scaled(int(0.023 * self.zone_clickable.width()),int(0.023 * self.zone_clickable.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.intended_zone.setPixmap(intended_scaled)
        self.intended_zone.setFixedSize(intended_scaled.size())
        self.intended_zone.hide()
        self.intended_zone.raise_()

        #Initializes the pointer object (Ball)
        self.ball = QLabel(self)

        ball_pixmap = QPixmap(resource_path("ball.png"))
        #ball_pixmap = QPixmap(os.path.join(__file__.replace("QPitchMapsBeta0.2.py","ball.png")))
        ball_scaled = ball_pixmap.scaled(int(0.02667 * self.zone_clickable.width()),int(0.02667 * self.zone_clickable.height()), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.ball.setPixmap(ball_scaled)
        self.ball.setFixedSize(ball_scaled.size())
        self.ball.hide()
        self.ball.raise_()

        self.mouse_x_list = []
        self.mouse_y_list = []
        self.intended_x_list = []
        self.intended_y_list = []
        self.working_pitcher_id = None
        self.intended_x = None
        self.intended_y = None
        self.temp_x = None
        self.temp_y = None
        self.intended = True
        #retrives the x and y location of the mouse click
        def get_location(x, y):
            if self.intended:
                self.intended_x = x/self.zone_clickable.width()
                self.intended_y = y/self.zone_clickable.height()
                #Moves the intended zone to the clicked location
                self.intended_zone.move(self.zone_clickable.x() + x + self.location_group.x() - self.intended_zone.width() // 2,
                               self.zone_clickable.y() + y + self.location_group.y() - self.intended_zone.height() // 2)
                self.intended_zone.raise_()
                self.intended_zone.show()
                self.intended = False
            elif not self.intended:
                self.temp_x = x/self.zone_clickable.width()
                self.temp_y = y/self.zone_clickable.height()
                #Moves the ball to the clicked location
                self.ball.move(self.zone_clickable.x() + x + self.location_group.x() - self.ball.width() // 2,
                            self.zone_clickable.y() + y + self.location_group.y() - self.ball.height() // 2)
                self.ball.raise_()
                self.ball.show()
                self.intended = True
            


        self.main_layout = QHBoxLayout()

        self.pitchinfo_group = QGroupBox("Pitch Info")
        self.pitchinfo_layout = QFormLayout()

        self.pitchinfo_layout.addRow("Pitch Velocity: ",self.velo_input)
        self.pitchinfo_layout.addRow("Pitch Type: ",self.pitchtype_input)
        self.pitchinfo_layout.addRow(self.submit_btn)
        self.pitchinfo_group.setLayout(self.pitchinfo_layout)
        self.main_layout.addWidget(self.pitchinfo_group,35)

        self.location_group = QGroupBox("Pitch Location")
        self.location_layout = QHBoxLayout()
        self.location_layout.addWidget(self.zone_clickable)
        self.location_group.setLayout(self.location_layout)
        self.main_layout.addWidget(self.location_group, 70)

        self.view_layout = QFormLayout()

        self.view_layout.addRow(self.mode_toggle_label)
        self.view_layout.addRow(self.mode_toggle)
        self.view_layout.addRow(self.player_info)

        self.main_layout.addLayout(self.view_layout)

        self.setLayout(self.main_layout)

        self.zone_clickable.clicked.connect(get_location)
        self.submit_btn.clicked.connect(self.submit_pitch)
        self.mode_toggle.stateChanged.connect(self.toggle_mode)


    def submit_pitch(self):
        x = self.temp_x
        y = self.temp_y
        intended_x = self.intended_x
        intended_y = self.intended_y
        self.intended = True
        if x is None or y is None or intended_x is None or intended_y is None:
            QMessageBox.warning(self, "Input Error", "Please click on the strike zone to input pitch location.")
            return
        else:
            print(intended_x,intended_y,x,y)
            self.intended_x_list.append(intended_x)
            self.intended_y_list.append(intended_y)
            self.mouse_x_list.append(x)
            self.mouse_y_list.append(y)
            self.storeValues()
            self.ball.hide()
            self.intended_zone.hide()
    
    def storeValues(self):
        query = QSqlQuery()


        query.prepare("""
            INSERT INTO bullpeninput (
                intended_x,
                intended_y,
                pitch_x,
                pitch_y,
                pitch_type,
                pitch_velocity,
                pitcher_id
               
            ) VALUES (
                :intx,
                :inty,
                :x,
                :y,
                :ptype,
                :velo,
                :pid
            )
        """)

        ix = self.intended_x_list[-1]
        iy = self.intended_y_list[-1]

        x = self.mouse_x_list[-1]
        y = self.mouse_y_list[-1]

        
        if self.isP:
            ix = 1-ix
            x = 1 - x
        

        query.bindValue(":intx", ix)
        query.bindValue(":inty", iy)
        query.bindValue(":x", x)
        query.bindValue(":y", y)
        query.bindValue(":ptype", self.pitchtype_input.currentText() or None)
        velo_text = self.velo_input.text()
        query.bindValue(":velo", float(velo_text) if velo_text else None)
        pitcher = self.getPitcher()
        print(self.working_pitcher_id)
        query.bindValue(":pid", self.working_pitcher_id)
        #query.bindValue(":pid", self.working_pitcher_id)

        
        if not query.exec_():
            print("QUERY:", query.lastQuery())
            print("VALUES:", query.boundValues())
            print("SQL ERROR:", query.lastError().text())
        else:
            QMessageBox.information(self, "Pitch Submitted", f"Pitch intended at: ({x}, {y}) Pitch at ({x}, {y})\nPitchType: {self.pitchtype_input.currentText() or None} \nVelo: {float(velo_text) if velo_text else None}\nPitcher: {pitcher}")

    def getPitcher(self):
        pitcher = None
        query = QSqlQuery()
        query.prepare("""SELECT first_name, last_name FROM pitchers WHERE id = ?""")
        query.addBindValue(self.working_pitcher_id)
        query.exec_()
        if query.next():
            pitcher = f"{query.value(0)} {query.value(1)}"
        return pitcher

    
    def updateLabels(self,pitcher, hitter, pitcher_id, hitter_id):
        print(pitcher,hitter,pitcher_id,hitter_id)
        self.working_pitcher_id = pitcher_id
        self.player_info.setText(f"Pitcher: {pitcher}")

    def toggle_mode(self):
        if self.mode_toggle.isChecked():
            self.zone_clickable.setPixmap(self.scaled_pixmap_p)
            self.zone_clickable.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.zone_clickable.setFixedSize(self.scaled_pixmap_p.size())
            self.isP = True
        else:
            self.zone_clickable.setPixmap(self.scaled_pixmap_h)
            self.zone_clickable.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.zone_clickable.setFixedSize(self.scaled_pixmap_h.size())
            self.isP = False
        
        


 






class AnyliticsScreen(QWidget):
    def __init__(self):
        super().__init__()

        

        #All buttons
        self.plot_button = QPushButton("Plot")
        self.save_button = QPushButton("Save")
        self.testbtn = QPushButton("test")
        self.mode_toggle_label = QLabel("Pitcher View:")
        self.mode_toggle = QCheckBox()
        self.isP = False
        self.bins_slider = QSlider(Qt.Orientation.Horizontal)
        self.bins_slider.setRange(1,100)
        self.bins_slider.setValue(30)
        self.bins_label = QLabel(str(self.bins_slider.value()))
        self.auto_bins_button = QPushButton("Auto Set Bins")

        self.custom_query_label = QLabel("Enter a custom query (SQLITE)")
        self.custom_query_input = QLineEdit()
        self.submit_query_btn = QPushButton("Submit Query")
        self.setStyleSheet("QLineEdit {font-size: 15pt;}")
        self.custom = False

        self.count_pitches_btn = QPushButton("Filter Count Pitches")

        self.select_pitcher = QComboBox()
        self.submit_pitcher_btn = QPushButton("Filter by Pitcher")
        self.setStyleSheet("QComboBox {font-size: 15pt;} QLineEdit {font-size: 15pt;}")
        self.load_players()



        #Creating the overlay for the histogram
        def resource_path(relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)
        
        screen = QApplication.primaryScreen()
        screen_size = screen.availableGeometry()

        width = int(screen_size.width() * 0.6)
        self.scale =  int(width * 0.6)
        self.zone_overlay = QLabel()
        #self.image_dir_h = os.path.join((__file__.replace("QPitchMapsBeta0.2.py","")),"Blank_Zone_H.png")
        #self.pixmap_h = QPixmap(self.image_dir_h)
        self.pixmap_h = QPixmap(resource_path("Blank_Zone_H.png"))
        self.pixmap_p = QPixmap(resource_path("Blank_Zone_P.png"))
        self.scaled_pixmap_h = self.pixmap_h.scaled(
                        self.scale,
                        self.scale,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )
        #self.image_dir_p = os.path.join((__file__.replace("QPitchMapsBeta0.2.py","")),"Blank_Zone_P.png")
        #self.pixmap_p = QPixmap(self.image_dir_p)
        self.scaled_pixmap_p = self.pixmap_p.scaled(
                        self.scale,
                        self.scale,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
        )
        self.zone_overlay.setPixmap(self.scaled_pixmap_h)
        self.zone_overlay.setFixedSize(self.scaled_pixmap_h.size())
        opacity_effect = QGraphicsOpacityEffect(self.zone_overlay)
        opacity_effect.setOpacity(0.4)
        self.zone_overlay.setGraphicsEffect(opacity_effect)


        

       
        

        #Creating the histogram plot
        self.figscale =  int(width*.6)
        self.figure = plt.figure(figsize=(self.figscale/100, self.figscale/100), dpi=100, frameon=False)
        ax = self.figure.add_axes([0, 0, 1, 1])  # FULL canvas
        ax.set_aspect('equal')
        ax.axis("off")
        
        #Figure Canvas Class
        self.canvas = FigureCanvas(self.figure)

        self.canvas.setFixedSize(self.figscale, self.figscale)
        self.canvas.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.canvas.setStyleSheet("background: transparent;")
        self.figure.patch.set_alpha(0)
        

        self.pitch_x_list = []
        self.pitch_y_list = []
        self.pullLists()

        ax = self.figure.subplots()
        self.figure.subplots_adjust(
            left=0,
            right=1,
            bottom=0,
            top=1
        )
        ax.set_aspect('equal', adjustable='box')

        H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
        H_flipped = numpy.fliplr(H.T)
        ax.imshow(H.T)
        #


        self.canvas.draw()
        #ax.set_xlim(-0.5,16.5)
        #ax.set_ylim(-5,5)


        def update():
            if self.mode_toggle.isChecked():
                if self.custom == False:
                    self.pullLists()
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H_flipped)
                    self.canvas.draw()
                elif self.custom == True:
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H_flipped)
                    self.canvas.draw()
                    self.custom = False
                
            else:
                if self.custom == False:
                    self.pullLists()
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H.T)
                    self.canvas.draw()
                elif self.custom == True:
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H.T)
                    self.canvas.draw()
                    self.custom = False
                
        self.overlay_container = QWidget()
        self.overlay_layout = QHBoxLayout(self.overlay_container)
        self.overlay_layout.setContentsMargins(0, 0,(int(.1*width)),0)
        self.overlay_layout.addWidget(self.zone_overlay)
        self.overlay_layout.addStretch()
        #self.overlay_container.setFixedSize(690, 690)
        self.overlay_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  


        def toggle_mode():
            ## Toggles between hitter and pitcher views (overlay and data)
            if self.mode_toggle.isChecked():
                self.isP = True
                self.zone_overlay.setPixmap(self.scaled_pixmap_p)
                self.overlay_layout.setContentsMargins(0, 0,(int(.1*width)),0)
                update()
               
            else:
                self.isP = False
                self.zone_overlay.setPixmap(self.scaled_pixmap_h)
                self.overlay_layout.setContentsMargins(0, 0,(int(.1*width)),0)
                update()
               


        self.toggle_group = QFormLayout()
        self.toggle_group.addWidget(self.mode_toggle_label)
        self.toggle_group.addWidget(self.mode_toggle)

        self.stack = QStackedLayout()
        self.stack.addWidget(self.canvas)
        self.stack.addWidget(self.overlay_container)
        self.stack.layout().setStackingMode(QStackedLayout.StackAll)

        self.hm_container = QWidget()
        self.hm_container.setLayout(self.stack)
       
        self.master_layout = QHBoxLayout()

        self.col1 = QFormLayout()
        self.col2 = QVBoxLayout()
        self.col3 = QVBoxLayout()


        self.col1.addRow(self.plot_button)
        self.col1.addRow(self.bins_label, self.bins_slider)
        self.col1.addRow(self.auto_bins_button)
        self.col1.addRow("Enter a custom query (SQLITE)", self.custom_query_input)
        self.col1.addRow(self.submit_query_btn)
        self.col1.addRow(self.save_button)
        


        self.col2.addStretch()
        self.col2.addWidget(self.hm_container)
        self.col2.addStretch()


        self.col3.addLayout(self.toggle_group)


        self.master_layout.addLayout(self.col1,20)
        self.master_layout.addLayout(self.col2,75)
        self.master_layout.addLayout(self.col3,5)


        self.setLayout(self.master_layout)


        self.testbtn.clicked.connect(self.pullLists)
        self.plot_button.clicked.connect(update)
        self.mode_toggle.stateChanged.connect(toggle_mode)
        self.bins_slider.valueChanged.connect(self.updateBinsLabel)
        self.save_button.clicked.connect(self.savePlot)
        self.submit_query_btn.clicked.connect(self.submitCustomQuery)
        self.submit_query_btn.clicked.connect(update)
        self.submit_pitcher_btn.clicked.connect(self.filterByPitcher)
        self.submit_pitcher_btn.clicked.connect(update)
        self.auto_bins_button.clicked.connect(self.autoSetBins)
        self.auto_bins_button.clicked.connect(update)
        self.count_pitches_btn.clicked.connect(self.findCount)
        
       
    def updateBinsLabel(self):
        self.bins_label.setText(str(self.bins_slider.value()))


    def pullLists(self):
        self.pitch_x_list = []
        self.pitch_y_list = []
        query = QSqlQuery("SELECT pitch_x, pitch_y FROM pitchinput")
        while query.next():
            self.pitch_x_list.append(query.value(0))
            self.pitch_y_list.append(query.value(1))
           
        #ax.imshow(H.T)
        #print(self.pitch_x_list,self.pitch_y_list)
        self.canvas.draw()

    def savePlot(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            pixmap = self.hm_container.grab()
            pixmap.save(file_path)            

    def submitCustomQuery(self):
        self.custom = True
        query_text = str(f"SELECT pitch_x, pitch_y FROM pitchinput WHERE {self.custom_query_input.text()}")
        query = QSqlQuery(query_text)
        print(query_text)
        self.pitch_x_list = []
        self.pitch_y_list = []
        while query.next():
            self.pitch_x_list.append(query.value(0))
            self.pitch_y_list.append(query.value(1))

    def filterByPitcher(self):
        name = self.select_pitcher.currentText()
        first_name, last_name, team = name.split(", ")
        self.custom = True
        query_text = f'SELECT pitch_x, pitch_y FROM pitchinput INNER JOIN pitchers ON pitchinput.pitcher_id = pitchers.id WHERE pitchers.first_name LIKE UPPER("{first_name.upper()}") AND pitchers.last_name LIKE UPPER("{last_name.upper()}")'
        query = QSqlQuery(str(query_text))
        self.pitch_x_list = []
        self.pitch_y_list = []
        print(query_text)
        while query.next():
            self.pitch_x_list.append(query.value(0))
            self.pitch_y_list.append(query.value(1))

    def load_players(self):
        pitcher_list = []
        self.select_pitcher.clear()
        query = QSqlQuery("SELECT first_name, last_name, team FROM pitchers")
        while query.next():
            first_name = query.value(0)
            last_name = query.value(1)
            team = query.value(2)
            full_name = f"{first_name}, {last_name}, {team}"
            pitcher_list.append(full_name)
        self.select_pitcher.addItems(pitcher_list)

    def autoSetBins(self):
        n = len(self.pitch_x_list)
        if n > 10:
            optimal_bins = n**(1/2)+5
            self.bins_slider.setValue(int(optimal_bins))

    def generateVisualReport(self,name):
        self.plot_button.click()
        self.savePlotAs(f"{name}all")

    def savePlotAs(self, filename):
        if not filename:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
            if file_path:
                self.figure.savefig(file_path)
                self.overlay_strike_zone(file_path, resource_path("intended_zone.png"))
        else:
            self.figure.savefig(filename)
            self.overlay_strike_zone(filename, resource_path("intended_zone.png"))
    
    def overlay_strike_zone(self, heatmap_path, zone_image_path):
        """
        Overlays a transparent strike zone PNG on top of a saved heatmap image.
        """

        base_img = Image.open(heatmap_path).convert("RGBA")
        zone_img = Image.open(zone_image_path).convert("RGBA")

        # Resize zone to match heatmap dimensions
        zone_img = zone_img.resize(base_img.size, Image.LANCZOS)

        # Combine images
        combined = Image.alpha_composite(base_img, zone_img)

        combined.save(heatmap_path)  # overwrite original

    def findCount(self):
        window = QDialog()
        window.setWindowTitle("Select the region that you would like to count")
        window.resize(int(self.scale * 1.2), int(self.scale * 1.2))

        x1_slider = QSlider()
        y1_slider = QSlider()

        x2_slider = QSlider()
        y2_slider = QSlider()

        main_layout = QVBoxLayout()

        top = QHBoxLayout()
        middle = QHBoxLayout()
        left = QVBoxLayout()

        top.addWidget(x1_slider)
        top.addWidget(y1_slider)

        left.addWidget(x2_slider)
        left.addWidget(y2_slider)

        #middle.addWidget(self.scaled_pixmap_h)
        middle.addWidget(QLabel("Add Pixmap"))
        middle.addLayout(left)

        main_layout.addLayout(top)
        main_layout.addLayout(middle)

        window.setLayout(main_layout)

        window.exec()


class BullpenAnyliticsScreen(QWidget):
    def __init__(self):
        super().__init__()

        

        #All buttons
        self.plot_button = QPushButton("Plot")
        self.save_button = QPushButton("Save")
        self.mode_toggle_label = QLabel("Pitcher View:")
        self.mode_toggle = QCheckBox()
        self.isP = False
        self.bins_slider = QSlider(Qt.Orientation.Horizontal)
        self.bins_slider.setRange(1,100)
        self.bins_slider.setValue(30)
        self.bins_label = QLabel(str(self.bins_slider.value()))

        self.custom_query_label = QLabel("Enter a custom query (SQLITE)")
        self.custom_query_input = QLineEdit()
        self.submit_query_btn = QPushButton("Submit Query")
        
        self.custom = False

        self.select_pitcher = QComboBox()
        self.submit_pitcher_btn = QPushButton("Filter by Pitcher")
        self.setStyleSheet("QComboBox {font-size: 15pt;} QLineEdit {font-size: 15pt;}")
        self.load_players()

        #self.select_ptype = QComboBox()
        #self.select_ptype_btn = QPushButton("Filter by Pitch Type")

        self.easy_query_btn = QPushButton("Easy Query")






        #Creating the overlay for the histogram
        def resource_path(relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")

            return os.path.join(base_path, relative_path)
        
        screen = QApplication.primaryScreen()
        screen_size = screen.availableGeometry()

        width = int(screen_size.width() * 0.6)
        self.scale =  int(width * 0.15)
        self.zone_overlay = QLabel()
        #self.image_dir_h = os.path.join((__file__.replace("QPitchMapsBeta0.2.py","")),"Blank_Zone_H.png")
        #self.pixmap_h = QPixmap(self.image_dir_h)
        self.pixmap = QPixmap(resource_path("intended_zone.png"))
        self.scaled_pixmap = self.pixmap.scaled(
                        self.scale,
                        self.scale,
                        Qt.KeepAspectRatio,
                        Qt.SmoothTransformation
                    )

        self.zone_overlay.setPixmap(self.scaled_pixmap)
        self.zone_overlay.setFixedSize(self.scaled_pixmap.size())
        opacity_effect = QGraphicsOpacityEffect(self.zone_overlay)
        opacity_effect.setOpacity(0.4)
        self.zone_overlay.setGraphicsEffect(opacity_effect)


        

       
        

        #Creating the histogram plot
        self.figscale =  int(width*.6)
        self.figure = plt.figure(figsize=(self.figscale/100, self.figscale/100), dpi=100, frameon=False)
        ax = self.figure.add_axes([0, 0, 1, 1])  # FULL canvas
        ax.set_aspect('equal')
        ax.axis("off")
        
        #Figure Canvas Class
        self.canvas = FigureCanvas(self.figure)

        self.canvas.setFixedSize(self.figscale, self.figscale)
        self.canvas.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.canvas.setStyleSheet("background: transparent;")
        self.figure.patch.set_alpha(0)
        

        self.pitch_x_list = []
        self.pitch_y_list = []
        self.pullLists()

        ax = self.figure.subplots()
        self.figure.subplots_adjust(
            left=0,
            right=1,
            bottom=0,
            top=1
        )
        ax.set_aspect('equal', adjustable='box')

        H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
        H_flipped = numpy.fliplr(H.T)
        ax.imshow(H.T)
        #


        self.canvas.draw()
        #ax.set_xlim(-0.5,16.5)
        #ax.set_ylim(-5,5)


        def update():
            
            if self.mode_toggle.isChecked():
                if self.custom == False:
                    self.pullLists()
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H_flipped)
                    self.canvas.draw()
                elif self.custom == True:
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H_flipped)
                    self.canvas.draw()
                    self.custom = False
                
            else:
                if self.custom == False:
                    self.pullLists()
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H.T)
                    self.canvas.draw()
                elif self.custom == True:
                    H,xe,ye = numpy.histogram2d(self.pitch_x_list, self.pitch_y_list, bins = self.bins_slider.value(), range = [[0,1],[0,1]])
                    H_flipped = numpy.fliplr(H.T)
                    ax.imshow(H.T)
                    self.canvas.draw()
                    self.custom = False
                
        self.overlay_container = QWidget()
        self.overlay_layout = QHBoxLayout(self.overlay_container)
        self.overlay_layout.setContentsMargins(int(self.figscale*0.375), (int(self.scale*.025)),0,0)
        self.overlay_layout.addWidget(self.zone_overlay)
        self.overlay_layout.addStretch()
        #self.overlay_container.setFixedSize(690, 690)
        self.overlay_container.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)  


        def toggle_mode():
            ## Toggles between hitter and pitcher views (overlay and data)
            if self.mode_toggle.isChecked():
                self.isP = True
                update()
               
            else:
                self.isP = False
                update()
               


        self.toggle_group = QFormLayout()
        self.toggle_group.addWidget(self.mode_toggle_label)
        self.toggle_group.addWidget(self.mode_toggle)

        self.stack = QStackedLayout()
        self.stack.addWidget(self.canvas)
        self.stack.addWidget(self.overlay_container)
        self.stack.layout().setStackingMode(QStackedLayout.StackAll)

        self.hm_container = QWidget()
        self.hm_container.setLayout(self.stack)
       
        self.master_layout = QHBoxLayout()

        self.col1 = QFormLayout()
        self.col2 = QVBoxLayout()
        self.col3 = QVBoxLayout()


        self.col1.addRow(self.plot_button)
        self.col1.addRow(self.bins_label, self.bins_slider)
        self.col1.addRow("Enter a custom query (SQLITE)", self.custom_query_input)
        self.col1.addRow(self.submit_query_btn)
        self.col1.addRow("Filter by Pitcher:", self.select_pitcher)
        self.col1.addRow(self.submit_pitcher_btn)
        self.col1.addRow(self.save_button)


        self.col2.addStretch()
        self.col2.addWidget(self.hm_container)
        self.col2.addStretch()


        self.col3.addLayout(self.toggle_group)


        self.master_layout.addLayout(self.col1,20)
        self.master_layout.addLayout(self.col2,75)
        self.master_layout.addLayout(self.col3,5)


        self.setLayout(self.master_layout)


        self.plot_button.clicked.connect(update)
        self.mode_toggle.stateChanged.connect(toggle_mode)
        self.bins_slider.valueChanged.connect(self.updateBinsLabel)
        self.save_button.clicked.connect(self.savePlot)
        self.submit_query_btn.clicked.connect(self.submitCustomQuery)
        self.submit_query_btn.clicked.connect(update)
        self.submit_pitcher_btn.clicked.connect(self.filterByPitcher)
        self.submit_pitcher_btn.clicked.connect(update)
        self.easy_query_btn.clicked.connect(self.easyQuery)
        self.easy_query_btn.clicked.connect(update)
       
    def updateBinsLabel(self):
        self.bins_label.setText(str(self.bins_slider.value()))


    def pullLists(self):
        self.pitch_x_list = []
        self.pitch_y_list = []
        query = QSqlQuery("SELECT intended_x, intended_y, pitch_x, pitch_y FROM bullpeninput")
        while query.next():
            intended_x, intended_y = query.value(0), query.value(1)
            x, y = query.value(2), query.value(3)
            diff_x = x - intended_x
            diff_y = y - intended_y
            diff_x = 0.5 + diff_x
            diff_y = 0.5 + diff_y
            self.pitch_x_list.append(diff_x)
            self.pitch_y_list.append(diff_y)
           
        self.canvas.draw()


    def savePlot(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "PNG Files (*.png);;JPEG Files (*.jpg);;All Files (*)")
        if file_path:
            pixmap = self.hm_container.grab()
            pixmap.save(file_path)

    def submitCustomQuery(self):
        self.custom = True
        query_text = str(f"SELECT intended_x, intended_y, pitch_x, pitch_y FROM bullpeninput WHERE {self.custom_query_input.text()}")
        query = QSqlQuery(query_text)
        print(query_text)
        self.pitch_x_list = []
        self.pitch_y_list = []
        while query.next():
            intended_x, intended_y = query.value(0), query.value(1)
            x, y = query.value(2), query.value(3)
            diff_x = x - intended_x
            diff_y = y - intended_y
            diff_x = 0.5 + diff_x
            diff_y = 0.5 + diff_y
            self.pitch_x_list.append(diff_x)
            self.pitch_y_list.append(diff_y)
    
    def filterByPitcher(self):
        name = self.select_pitcher.currentText()
        first_name, last_name, team = name.split(", ")
        self.custom = True
        query_text = f'SELECT bullpeninput.intended_x, bullpeninput.intended_y, bullpeninput.pitch_x, bullpeninput.pitch_y FROM bullpeninput INNER JOIN pitchers ON bullpeninput.pitcher_id = pitchers.id WHERE pitchers.first_name LIKE UPPER("{first_name.upper()}") AND pitchers.last_name LIKE UPPER("{last_name.upper()}")'
        query = QSqlQuery(str(query_text))
        self.pitch_x_list = []
        self.pitch_y_list = []
        print(query_text)
        while query.next():
            intended_x, intended_y = query.value(0), query.value(1)
            x, y = query.value(2), query.value(3)
            diff_x = x - intended_x
            diff_y = y - intended_y
            diff_x = 0.5 + diff_x
            diff_y = 0.5 + diff_y
            self.pitch_x_list.append(diff_x)
            self.pitch_y_list.append(diff_y)

    def load_players(self):
        pitcher_list = []
        self.select_pitcher.clear()
        query = QSqlQuery("SELECT first_name, last_name, team FROM pitchers")
        while query.next():
            first_name = query.value(0)
            last_name = query.value(1)
            team = query.value(2)
            full_name = f"{first_name}, {last_name}, {team}"
            pitcher_list.append(full_name)
        self.select_pitcher.addItems(pitcher_list)

    def easyQuery(self):
        self.custom = True
        self.pitch_x_list = []
        self.pitch_y_list = []

class SelectPlayerDialog(QWidget):
    def __init__(self, player_type):
        super().__init__()
        self.setWindowTitle("Select Player")
        self.setFixedSize(300, 400)
        self.player_list = QListWidget()
        self.submit_btn = QPushButton("Generate Report")
        self.pull_players(player_type)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.player_list)
        self.main_layout.addWidget(self.submit_btn)
        self.setLayout(self.main_layout)

        

    def pull_players(self, player_type):
        if player_type == "Pitcher":
            query = QSqlQuery("SELECT id, first_name, last_name, team FROM pitchers")
        else:
            query = QSqlQuery("SELECT id, first_name, last_name, team  FROM hitters")

        while query.next():
            player_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            full_name = f"{first_name} {last_name} ({team})"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, player_id)
            self.player_list.addItem(item)
            
            
        

class HeatmapWidget(QWidget):
    def __init__(self, scale, bins, printable):
        super().__init__()

        self.bins = bins
        self.isP = False
        self.printable = printable

        # --- Matplotlib Figure ---
        
        #plt.style.use('')
        self.figure = plt.figure(figsize=(scale/100, scale/100), dpi=100, frameon=False)
        if self.printable:
            plt.rcParams['image.cmap'] = 'gray_r'
        else:
            plt.rcParams['image.cmap'] = 'viridis'
        self.ax = self.figure.add_axes([0, 0, 1, 1])
        self.ax.set_aspect('equal')
        
        self.ax.axis("off")

        self.canvas = FigureCanvas(self.figure)
        self.canvas.setFixedSize(scale, scale)

        # --- Overlay ---
        self.zone_overlay = QLabel()

        self.pixmap_h = QPixmap(self.resource_path("Blank_Zone_H.png"))
        self.pixmap_p = QPixmap(self.resource_path("Blank_Zone_P.png"))

        self.scaled_pixmap_h = self.pixmap_h.scaled(scale, scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.scaled_pixmap_p = self.pixmap_p.scaled(scale, scale, Qt.KeepAspectRatio, Qt.SmoothTransformation)

        self.zone_overlay.setPixmap(self.scaled_pixmap_h)
        self.zone_overlay.setFixedSize(scale, scale)

        opacity = QGraphicsOpacityEffect()
        opacity.setOpacity(0.4)
        self.zone_overlay.setGraphicsEffect(opacity)

        # --- Layout stack ---
        self.stack = QStackedLayout()
        self.stack.addWidget(self.canvas)
        self.stack.addWidget(self.zone_overlay)
        self.stack.setStackingMode(QStackedLayout.StackAll)

        self.setLayout(self.stack)

    def resource_path(self, relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

    def update_data(self, x_list, y_list, bins_input):
        self.ax.clear()
        self.ax.set_aspect('equal')
        self.ax.axis("off")

        if len(x_list) > 0:
            H, xe, ye = numpy.histogram2d(
                x_list,
                y_list,
                bins=bins_input,
                range=[[0, 1], [0, 1]]
            )

            if self.isP:
                H = numpy.fliplr(H.T)
            else:
                H = H.T

            self.ax.imshow(H)

        self.canvas.draw()

    def toggle_view(self, pitcher_view):
        self.isP = pitcher_view
        if pitcher_view:
            self.zone_overlay.setPixmap(self.scaled_pixmap_p)
        else:
            self.zone_overlay.setPixmap(self.scaled_pixmap_h)
        # Refresh with current data

    def makePrintable(self, printable):
        self.printable = printable
        if printable:
            plt.rcParams['image.cmap'] = 'gray_r'
        else:
            plt.rcParams['image.cmap'] = 'viridis'
        
class PitcherProfiles(QWidget):
    def __init__(self):
        super().__init__()

        screen = QApplication.primaryScreen()
        screen_size = screen.availableGeometry()

        width = int(screen_size.width() * 0.6)
        self.scale =  int(width * 0.6*.3)

        self.pitcher_list = QListWidget()
        self.profile_display = QLabel("Select a pitcher to view their profile.")
        self.profile_display.setWordWrap(True)
        self.select_pitcher_btn = QPushButton("Select Pitcher")
        self.loadPitchers()

        self.bins_slider = QSlider(Qt.Orientation.Horizontal)
        self.bins_slider.setRange(1,100)
        self.bins_slider.setValue(30)
        self.bins_value_label = QLabel(f"Bins: {str(self.bins_slider.value())}")

        self.toggle_overlay = QCheckBox("Pitcher View")
        self.toggle_overlay.setChecked(True)
        self.toggle_overlay.stateChanged.connect(self.toggle_all)

        self.printable = QCheckBox("Printable Mode")

        self.view_mode = QLabel("Pitcher View")
        self.whiff_rate = 0.00
        self.whiff_rate_label = QLabel(f"Whiff rate: {self.whiff_rate}%")
        
        
        self.report_btn = QPushButton("Generate Report")

        self.stats_container = QWidget()
        self.stats_container_layout = QVBoxLayout()
        self.stats_container_layout.addWidget(self.view_mode)
        self.stats_container_layout.addWidget(self.whiff_rate_label)
        self.stats_container.setLayout(self.stats_container_layout)

        self.filter_by_handedness_input = QComboBox()
        self.filter_by_handedness_input.addItems(["All", "Right", "Left", "Switch", "Hold"])

        self.filter_container = QWidget()
        self.filter_layout = QFormLayout()
        self.filter_layout.addRow("Opp. Handedness: ", self.filter_by_handedness_input)
        self.filter_container.setLayout(self.filter_layout)

        self.grid = QGridLayout()
        self.player_label = QLabel("All Pitchers")
        self.player_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        self.player_label.setWordWrap(True)
        self.num_pitches = 0
        self.num_pitches_label = QLabel(f"n = {self.num_pitches}")

        self.pitcher_names = []

        self.pitcher_id = None  # To be set when a pitcher is selected
        self.handedness = ("Right", "Left", "Switch", "Hold","")
        self.heatmaps = []

        self.grid.addWidget(QLabel("All Pitches"), 0, 1)
        self.grid.addWidget(QLabel("Whiffs"), 0, 2)
        self.grid.addWidget(QLabel("Hard Hits"), 0, 3)

        self.grid.addWidget(QLabel("All Pitches"), 1, 0)
        self.grid.addWidget(QLabel("Fastball"), 2, 0)
        self.grid.addWidget(QLabel("Breaking Balls"), 3, 0)
        self.grid.addWidget(QLabel("Offspeed"), 4, 0)

        self.grid.addWidget(self.player_label, 0, 5)
        self.grid.addWidget(self.num_pitches_label, 1, 5)
        self.grid.addWidget(self.stats_container, 2, 5)
        self.grid.addWidget(self.filter_container, 3, 5)

        for i in range(12):
            hm = HeatmapWidget(self.scale, bins= self.bins_slider.value(), printable = self.printable.isChecked())
            self.heatmaps.append(hm)
            row = i // 3 + 1
            col = i % 3 + 1
            self.grid.addWidget(hm, row, col)

        self.main_layout = QHBoxLayout()
        self.pitcher_select_layout = QVBoxLayout()
        self.pitcher_select_layout.addWidget(self.toggle_overlay)
        
        self.pitcher_select_layout.addWidget(self.bins_value_label)
        self.pitcher_select_layout.addWidget(self.bins_slider)
        self.pitcher_select_layout.addWidget(self.profile_display)
        self.pitcher_select_layout.addWidget(self.pitcher_list)
        self.pitcher_select_layout.addWidget(self.select_pitcher_btn)

        self.container = QWidget()
        self.container.setLayout(self.grid)

        self.main_layout.addLayout(self.pitcher_select_layout,30)


        self.main_layout.addWidget(self.container,70)

        self.setLayout(self.main_layout)


        self.select_pitcher_btn.clicked.connect(self.select_pitcher)
        self.bins_slider.valueChanged.connect(self.update_bins)
        self.report_btn.clicked.connect(self.generate_report)
        self.printable.stateChanged.connect(self.update_printable)
        self.toggle_all()

    def load_data(self):
        filter_clause = None
        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE hitters.handedness IN {self.handedness} ")
        if self.pitcher_id is not None:
            filter_clause = f"AND pitcher_id = {self.pitcher_id} AND hitters.handedness IN {self.handedness}"
            query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE pitcher_id = {self.pitcher_id} AND hitters.handedness IN {self.handedness}")

        

        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []

        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)

        self.heatmaps[0].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[1].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[2].update_data(hard_x, hard_y, self.bins_slider.value())

        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE pitch_type IN ('4FB','SI','CUT') {filter_clause if filter_clause else f"AND hitters.handedness IN {self.handedness}"}")
        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []
        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)
        self.heatmaps[3].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[4].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[5].update_data(hard_x, hard_y, self.bins_slider.value())
        
        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE pitch_type IN ('CU','SL','SW') {filter_clause if filter_clause else f"AND hitters.handedness IN {self.handedness}"}")
        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []
        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)

        self.heatmaps[6].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[7].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[8].update_data(hard_x, hard_y, self.bins_slider.value())

        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE pitch_type IN ('CH','SPL','KN', 'OTHER') {filter_clause if filter_clause else f"AND hitters.handedness IN {self.handedness}"}")
        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []
        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)
        self.heatmaps[9].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[10].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[11].update_data(hard_x, hard_y, self.bins_slider.value())

        if filter_clause:
            query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE pitcher_id = {self.pitcher_id} AND hitters.handedness IN {self.handedness}")
            if query.next():
                self.num_pitches = query.value(0)
                self.num_pitches_label.setText(f"n = {self.num_pitches}")
        else:
            query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE hitters.handedness IN {self.handedness}")
            if query.next():
                self.num_pitches = query.value(0)
                self.num_pitches_label.setText(f"n = {self.num_pitches}")

        query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE pitch_result IN ('WHIFF','INPLAY', 'FOUL') {filter_clause if filter_clause else f"AND hitters.handedness IN {self.handedness}"}")
        query.next()
        temp = query.value(0)

        query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN hitters ON hitter_id = hitters.id WHERE pitch_result = 'WHIFF' {filter_clause if filter_clause else f"AND hitters.handedness IN {self.handedness}"}")
        query.next()
        if (temp > 0):
            self.whiff_rate = round(((query.value(0) / temp)*100),2)       
        else:
            self.whiff_rate = 0
        self.whiff_rate_label.setText(f"Whiff rate: {self.whiff_rate}%")

    def toggle_all(self):
        pitcher_view = self.toggle_overlay.isChecked()
        if pitcher_view:
            self.view_mode.setText("Pitcher View")
        else:            
            self.view_mode.setText("Hitter View")
        for hm in self.heatmaps:
            hm.toggle_view(pitcher_view)
        self.load_data()  # redraw existing data if stored

    def update_printable(self):
        printable = self.printable.isChecked()
        if printable:
            self.setStyleSheet("background-color: #FFFFFFFF;")
        else:
            self.setStyleSheet("")
        for hm in self.heatmaps:
            hm.makePrintable(printable)
        self.load_data()  # redraw existing data with new color scheme

    def loadPitchers(self):
        query = QSqlQuery("SELECT id, first_name, last_name, team FROM pitchers")
        self.pitcher_list.clear()
        while query.next():
            pitcher_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            full_name = f"{first_name} {last_name} ({team})"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, pitcher_id)
            self.pitcher_list.addItem(item)

    def select_pitcher(self):
        selected_item = self.pitcher_list.currentItem()
        if selected_item:
            self.pitcher_id = selected_item.data(Qt.UserRole)
            self.player_label.setText(selected_item.text())

        hand = self.filter_by_handedness_input.currentText()
        if hand == "All":
            self.handedness = ("Right", "Left", "Switch", "Hold", "")
        else:
            self.handedness = (hand, "")
        self.load_data()

    def update_bins(self):
        self.bins_value_label.setText(f"Bins: {str(self.bins_slider.value())}")
    
    def resource_path(self, relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

    def generate_report(self):
        player_names = QDialog()
        player_names.setWindowTitle("Select Players")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select pitcher(s) for the report:"))
        select_pitcher = QListWidget()

        query = QSqlQuery("SELECT id, first_name, last_name, team, handedness FROM pitchers")
        while query.next():
            pitcher_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            hand = query.value(4)
            full_name = f"{first_name} {last_name} ({team}) - {hand}"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, pitcher_id)
            select_pitcher.addItem(item)

        select_pitcher.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        layout.addWidget(select_pitcher)
        submit_btn = QPushButton("Submit")
        layout.addWidget(submit_btn)
        player_names.setLayout(layout)
        submit_btn.clicked.connect(player_names.accept)

        player_names.exec()
        if player_names.result() == QDialog.DialogCode.Accepted:
            for item in select_pitcher.selectedItems():
                self.pitcher_names.append([item.data(Qt.UserRole), item.text()])

        self.grab_report_data(self.pitcher_names)


        
    
    def grab_report_data(self, pitcher_names):
        save_path = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf);;All Files (*)")[0]
        if save_path:
            report_list = []
            for pitcher in pitcher_names:
                self.player_label.setText(pitcher[1])
                self.pitcher_id = pitcher[0]
                self.load_data()
                pixmap = self.container.grab()
                report_list.append((pitcher[1], pixmap))

            self.create_pdf(report_list, save_path)
        else:
            QMessageBox.warning(self, "No Save Path", "Please select a valid save path for the report.")
            
    def create_pdf(self, pixmap_list, save_path):

        temp_paths = []

        doc = SimpleDocTemplate(
            save_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        elements = []

        # Available frame size (after margins)
        frame_width = doc.width
        frame_height = doc.height

        for i, pixmap in enumerate(pixmap_list):

            temp_path = self.resource_path(f"temp_{i}.png")
            pixmap[1].save(temp_path, "PNG")

            img = Image(temp_path)

            img_width, img_height = img.wrap(0, 0)

            scale = min(
                frame_width / img_width,
                frame_height / img_height
            )

            img.drawWidth = img_width * scale
            img.drawHeight = img_height * scale

            elements.append(img)
            elements.append(Paragraph(pixmap[0], getSampleStyleSheet()['Heading2']))

            if i < len(pixmap_list) - 1:
                elements.append(PageBreak())

        doc.build(elements)
        for temps in temp_paths:
            if os.path.exists(temps):
                os.remove(temps)

    


class HitterProfiles(QWidget):
    def __init__(self):
        super().__init__()

        screen = QApplication.primaryScreen()
        screen_size = screen.availableGeometry()

        width = int(screen_size.width() * 0.6)
        self.scale =  int(width * 0.6*.3)

        self.hitter_list = QListWidget()
        self.profile_display = QLabel("Select a hitter to view their profile.")
        self.profile_display.setWordWrap(True)
        self.select_hitter_btn = QPushButton("Select Hitter")
        self.loadHitters()

        self.bins_slider = QSlider(Qt.Orientation.Horizontal)
        self.bins_slider.setRange(1,100)
        self.bins_slider.setValue(30)
        self.bins_value_label = QLabel(f"Bins: {str(self.bins_slider.value())}")

        self.toggle_overlay = QCheckBox("Pitcher View")
        self.toggle_overlay.setChecked(False)
        self.toggle_overlay.stateChanged.connect(self.toggle_all)

        self.printable = QCheckBox("Printable Mode")

        self.view_mode = QLabel("Hitter View")
        self.whiff_rate = 0.00
        self.whiff_rate_label = QLabel(f"Whiff rate: {self.whiff_rate}%")

        self.report_btn = QPushButton("Generate Report")

        self.stats_container = QWidget()
        self.stats_container_layout = QVBoxLayout()
        self.stats_container_layout.addWidget(self.view_mode)
        self.stats_container_layout.addWidget(self.whiff_rate_label)
        self.stats_container.setLayout(self.stats_container_layout)

        self.filter_by_handedness_input = QComboBox()
        self.filter_by_handedness_input.addItems(["All","Right","Left","Switch","Hold"])
        


        self.filter_container = QWidget()
        self.filter_layout = QFormLayout()
        self.filter_layout.addRow("Opp. Handedness:", self.filter_by_handedness_input)
        self.filter_container.setLayout(self.filter_layout)
        

        self.grid = QGridLayout()
        self.player_label = QLabel("All Hitters")
        self.player_label.setStyleSheet("font-size: 12pt; font-weight: bold;")
        self.player_label.setWordWrap(True)
        self.num_pitches = 0
        self.num_pitches_label = QLabel(f"n = {self.num_pitches}")

        self.hitter_names = []

        self.hitter_id = None  # To be set when a hitter is selected
        self.handedness = ("Right", "Left", "Switch", "Hold", "")

        self.heatmaps = []

        self.grid.addWidget(QLabel("All Pitches"), 0, 1)
        self.grid.addWidget(QLabel("Whiffs"), 0, 2)
        self.grid.addWidget(QLabel("Hard Hits"), 0, 3)

        self.grid.addWidget(QLabel("All Pitches"), 1, 0)
        self.grid.addWidget(QLabel("Fastball"), 2, 0)
        self.grid.addWidget(QLabel("Breaking Balls"), 3, 0)
        self.grid.addWidget(QLabel("Offspeed"), 4, 0)

        self.grid.addWidget(self.player_label, 0, 5)
        self.grid.addWidget(self.num_pitches_label, 1, 5)
        self.grid.addWidget(self.stats_container, 2,5)
        self.grid.addWidget(self.filter_container, 3,5)

        

        for i in range(12):
            hm = HeatmapWidget(self.scale, bins= self.bins_slider.value(), printable = self.printable.isChecked())
            self.heatmaps.append(hm)
            row = i // 3 + 1
            col = i % 3 + 1
            self.grid.addWidget(hm, row, col)

        self.main_layout = QHBoxLayout()
        self.hitter_select_layout = QVBoxLayout()
        self.hitter_select_layout.addWidget(self.toggle_overlay)
        self.hitter_select_layout.addWidget(self.bins_value_label)
        self.hitter_select_layout.addWidget(self.bins_slider)
        self.hitter_select_layout.addWidget(self.profile_display)
        self.hitter_select_layout.addWidget(self.hitter_list)
        self.hitter_select_layout.addWidget(self.select_hitter_btn)

        self.container = QWidget()
        self.container.setLayout(self.grid)
        

        self.main_layout.addLayout(self.hitter_select_layout,30)

        self.main_layout.addWidget(self.container,70)

        self.setLayout(self.main_layout)


        self.select_hitter_btn.clicked.connect(self.select_hitter)
        self.bins_slider.valueChanged.connect(self.update_bins)
        self.report_btn.clicked.connect(self.generate_report)
        self.printable.stateChanged.connect(self.update_printable)
        self.toggle_all()

    def load_data(self):
        filter_clause = None
        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE pitchers.handedness IN {self.handedness} ")
        if self.hitter_id is not None:
            filter_clause = f"AND hitter_id = {self.hitter_id} AND pitchers.handedness IN {self.handedness}"
            query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE hitter_id = {self.hitter_id} AND pitchers.handedness IN {self.handedness}")

        

        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []

        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)
            
            

        self.heatmaps[0].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[1].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[2].update_data(hard_x, hard_y, self.bins_slider.value())

        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE pitch_type IN ('4FB','SI','CUT') {filter_clause if filter_clause else f"AND pitchers.handedness IN {self.handedness}"}")
        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []
        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)
        self.heatmaps[3].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[4].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[5].update_data(hard_x, hard_y, self.bins_slider.value())
        
        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE pitch_type IN ('CU','SL','SW') {filter_clause if filter_clause else f"AND pitchers.handedness IN {self.handedness}"}")
        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []
        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)

        self.heatmaps[6].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[7].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[8].update_data(hard_x, hard_y, self.bins_slider.value())

        query = QSqlQuery(f"SELECT pitch_x, pitch_y, pitch_result, pa_result FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE pitch_type IN ('CH','SPL','KN', 'OTHER') {filter_clause if filter_clause else f"AND pitchers.handedness IN {self.handedness}"}")
        all_x, all_y = [], []
        whiff_x, whiff_y = [], []
        hard_x, hard_y = [], []
        while query.next():
            x = query.value(0)
            y = query.value(1)
            result = query.value(2)

            all_x.append(x)
            all_y.append(y)

            if result == "WHIFF":
                whiff_x.append(x)
                whiff_y.append(y)

            if result == "INPLAY" and query.value(3) in ["Single", "Double", "Triple", "Home Run"]:
                hard_x.append(x)
                hard_y.append(y)
        self.heatmaps[9].update_data(all_x, all_y, self.bins_slider.value())
        self.heatmaps[10].update_data(whiff_x, whiff_y, self.bins_slider.value())
        self.heatmaps[11].update_data(hard_x, hard_y, self.bins_slider.value())

        

        if filter_clause:
            query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE hitter_id = {self.hitter_id} AND pitchers.handedness IN {self.handedness}")
            if query.next():
                self.num_pitches = query.value(0)
                self.num_pitches_label.setText(f"n = {self.num_pitches}")
        else:
            query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE pitchers.handedness IN {self.handedness}")
            if query.next():
                self.num_pitches = query.value(0)
                self.num_pitches_label.setText(f"n = {self.num_pitches}")

        
        query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE pitch_result IN ('WHIFF','INPLAY', 'FOUL') {filter_clause if filter_clause else f"AND pitchers.handedness IN {self.handedness}"}")
        query.next()
        temp = query.value(0)
        
        query = QSqlQuery(f"SELECT COUNT(*) FROM pitchinput INNER JOIN pitchers ON pitcher_id = pitchers.id WHERE pitch_result IN ('WHIFF') {filter_clause if filter_clause else f"AND pitchers.handedness IN {self.handedness}"}")
        query.next()
        if (temp > 0):
            self.whiff_rate = round(((query.value(0) / temp)*100),2)
        else:
            self.whiff_rate = 0
        self.whiff_rate_label.setText(f"Whiff rate: {self.whiff_rate}%")

    def toggle_all(self):
        hitter_view = self.toggle_overlay.isChecked()
        if hitter_view:
            self.view_mode.setText("Pitcher View")
        else:            
            self.view_mode.setText("Hitter View")
        for hm in self.heatmaps:
            hm.toggle_view(hitter_view)
        self.load_data()  # redraw existing data if stored


    def update_printable(self):
        printable = self.printable.isChecked()
        if printable:
            self.setStyleSheet("background-color: #FFFFFFFF;")
        else:
            self.setStyleSheet("")
        for hm in self.heatmaps:
            hm.makePrintable(printable)
        self.load_data()  # redraw existing data with new color scheme

    def loadHitters(self):
        self.hitter_list.clear()
        query = QSqlQuery("SELECT id, first_name, last_name, team FROM hitters")
        while query.next():
            hitter_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            full_name = f"{first_name} {last_name} ({team})"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, hitter_id)
            self.hitter_list.addItem(item)

    def select_hitter(self):
        selected_item = self.hitter_list.currentItem()
        if selected_item:
            self.hitter_id = selected_item.data(Qt.UserRole)
            self.player_label.setText(selected_item.text())

        hand = self.filter_by_handedness_input.currentText()
        if hand == "All":
            self.handedness = ("Right", "Left", "Switch", "Hold", "")
        else:
            self.handedness = (hand, "")
            
        self.load_data()
        

    def update_bins(self):
        self.bins_value_label.setText(f"Bins: {str(self.bins_slider.value())}")
    
    def generate_report(self):
        player_names = QDialog()
        player_names.setWindowTitle("Select Players")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Select hitter(s) for the report:"))
        select_hitter = QListWidget()

        query = QSqlQuery("SELECT id, first_name, last_name, team, handedness FROM hitters")
        while query.next():
            hitter_id = query.value(0)
            first_name = query.value(1)
            last_name = query.value(2)
            team = query.value(3)
            handedness = query.value(4)
            full_name = f"{first_name} {last_name} ({team}) - {handedness}"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, hitter_id)
            select_hitter.addItem(item)

        select_hitter.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        layout.addWidget(select_hitter)
        submit_btn = QPushButton("Submit")
        layout.addWidget(submit_btn)
        player_names.setLayout(layout)
        submit_btn.clicked.connect(player_names.accept)

        player_names.exec()
        if player_names.result() == QDialog.DialogCode.Accepted:
            for item in select_hitter.selectedItems():
                self.hitter_names.append([item.data(Qt.UserRole), item.text()])

        self.grab_report_data(self.hitter_names)


    def resource_path(self, relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)
    
    def grab_report_data(self, hitter_names):
        save_path = QFileDialog.getSaveFileName(self, "Save Report", "", "PDF Files (*.pdf);;All Files (*)")[0]
        if save_path:
            report_list = []
            for hitter in hitter_names:
                self.player_label.setText(hitter[1])
                self.hitter_id = hitter[0]
                self.load_data()
                pixmap = self.container.grab()
                report_list.append((hitter[1], pixmap))

            self.create_pdf(report_list, save_path)
        else:
            QMessageBox.warning(self, "No Save Path", "Please select a valid save path for the report.")
                
    def create_pdf(self, pixmap_list, save_path):

        temp_paths = []

        doc = SimpleDocTemplate(
            save_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        elements = []

        # Available frame size (after margins)
        frame_width = doc.width
        frame_height = doc.height

        for i, pixmap in enumerate(pixmap_list):

            temp_path = self.resource_path(f"temp_{i}.png")
            pixmap[1].save(temp_path, "PNG")

            img = Image(temp_path)
            temp_paths.append(temp_path)

            img_width, img_height = img.wrap(0, 0)

            scale = min(
                frame_width / img_width,
                frame_height / img_height
            )

            img.drawWidth = img_width * scale
            img.drawHeight = img_height * scale

            elements.append(img)
            elements.append(Paragraph(pixmap[0], getSampleStyleSheet()['Heading2']))

            if i < len(pixmap_list) - 1:
                elements.append(PageBreak())

        doc.build(elements)
        for temps in temp_paths:
            os.remove(temps)




class ViewTables(QWidget):
    def __init__(self):
        super().__init__()

        self.model = QSqlTableModel()
        self.model.setTable("pitchinput")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "pitch_x")
        self.model.setHeaderData(2, Qt.Horizontal, "pitch_y")
        self.model.setHeaderData(3, Qt.Horizontal, "balls")
        self.model.setHeaderData(4, Qt.Horizontal, "strikes")
        self.model.setHeaderData(5, Qt.Horizontal, "pitch_type")
        self.model.setHeaderData(6, Qt.Horizontal, "pitch_result")
        self.model.setHeaderData(7, Qt.Horizontal, "pa_result")
        self.model.setHeaderData(8, Qt.Horizontal, "pitch_velocity")
        self.model.setHeaderData(9, Qt.Horizontal, "pitcher_id")
        self.model.setHeaderData(10, Qt.Horizontal, "hitter_id")
        self.model.setHeaderData(11, Qt.Horizontal, "game_id")

        self.table = QTableView()
        self.table.setModel(self.model)

        self.edit_button = QPushButton("Edit")
        self.delete_button = QPushButton("Delete")
        self.save_button = QPushButton("Save As")
        self.save_report_button = QPushButton("Save Report")


        self.pitchinput_btn = QPushButton("pitchinput")
        self.bullpeninput_btn = QPushButton("bullpeninput")
        self.teams_btn = QPushButton("teams")
        self.games_btn = QPushButton("games")
        self.pitchers_btn = QPushButton("pitchers")
        self.hitters_btn = QPushButton("hitters")


        self.main_layout = QVBoxLayout()

        self.top_row = QHBoxLayout()
        self.table_row = QHBoxLayout()
        self.bottom_row = QHBoxLayout()

        self.top_row.addWidget(self.pitchinput_btn)
        self.top_row.addWidget(self.bullpeninput_btn)
        self.top_row.addWidget(self.teams_btn)
        self.top_row.addWidget(self.games_btn)
        self.top_row.addWidget(self.pitchers_btn)
        self.top_row.addWidget(self.hitters_btn)

        self.table_row.addWidget(self.table)

        
        self.bottom_row.addWidget(self.save_button)
        self.bottom_row.addWidget(self.save_report_button)
        self.bottom_row.addWidget(self.edit_button)
        self.bottom_row.addWidget(self.delete_button)
        


        self.main_layout.addLayout(self.top_row)
        self.main_layout.addLayout(self.table_row)
        self.main_layout.addLayout(self.bottom_row)

        self.setLayout(self.main_layout)

        self.pitchinput_btn.clicked.connect(self.loadPitchInput)
        self.bullpeninput_btn.clicked.connect(self.loadBullpenInput)
        self.teams_btn.clicked.connect(self.loadTeams)
        self.games_btn.clicked.connect(self.loadGames)
        self.pitchers_btn.clicked.connect(self.loadPitchers)
        self.hitters_btn.clicked.connect(self.loadHitters)
        self.delete_button.clicked.connect(self.deleteRow)
        self.edit_button.clicked.connect(self.editCell)
        self.save_button.clicked.connect(self.saveAs)
        self.save_report_button.clicked.connect(self.makeGameReport)
        

        self.current_table = "pitchinput"

    def loadPitchInput(self):
        self.current_table = "pitchinput"
        self.model.setTable("pitchinput")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "pitch_x")
        self.model.setHeaderData(2, Qt.Horizontal, "pitch_y")
        self.model.setHeaderData(3, Qt.Horizontal, "balls")
        self.model.setHeaderData(4, Qt.Horizontal, "strikes")
        self.model.setHeaderData(5, Qt.Horizontal, "pitch_type")
        self.model.setHeaderData(6, Qt.Horizontal, "pitch_result")
        self.model.setHeaderData(7, Qt.Horizontal, "pa_result")
        self.model.setHeaderData(8, Qt.Horizontal, "pitch_velocity")
        self.model.setHeaderData(9, Qt.Horizontal, "pitcher_id")
        self.model.setHeaderData(10, Qt.Horizontal, "hitter_id")
        self.model.setHeaderData(11, Qt.Horizontal, "game_id")

        #self.pullStats()
    
    def loadBullpenInput(self):
        self.current_table = "bullpeninput"
        self.model.setTable("bullpeninput")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "intended_x")
        self.model.setHeaderData(2, Qt.Horizontal, "intended_y")
        self.model.setHeaderData(3, Qt.Horizontal, "pitch_x")
        self.model.setHeaderData(4, Qt.Horizontal, "pitch_y")
        self.model.setHeaderData(5, Qt.Horizontal, "pitch_type")
        self.model.setHeaderData(6, Qt.Horizontal, "pitch_velocity")
        self.model.setHeaderData(7, Qt.Horizontal, "pitcher_id")

    def loadTeams(self):
        self.current_table = "teams"
        self.model.setTable("teams")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "team_name")
    
    def loadGames(self):
        self.current_table = "games"
        self.model.setTable("games")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "game_date")
        self.model.setHeaderData(2, Qt.Horizontal, "opponent")
        self.model.setHeaderData(3, Qt.Horizontal, "opponent_id")
        self.model.setHeaderData(4, Qt.Horizontal, "away")
    
    def loadPitchers(self):
        self.current_table = "pitchers"
        self.model.setTable("pitchers")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "first_name")
        self.model.setHeaderData(2, Qt.Horizontal, "last_name")
        self.model.setHeaderData(3, Qt.Horizontal, "handedness")
        self.model.setHeaderData(4, Qt.Horizontal, "team")
        self.model.setHeaderData(5, Qt.Horizontal, "team_id")
    
    def loadHitters(self):
        self.current_table = "hitters"
        self.model.setTable("hitters")
        self.model.select()

        self.model.setHeaderData(0, Qt.Horizontal, "id")
        self.model.setHeaderData(1, Qt.Horizontal, "first_name")
        self.model.setHeaderData(2, Qt.Horizontal, "last_name")
        self.model.setHeaderData(3, Qt.Horizontal, "handedness")
        self.model.setHeaderData(4, Qt.Horizontal, "team")
        self.model.setHeaderData(5, Qt.Horizontal, "team_id")
    
    def deleteRow(self):
        index = self.table.currentIndex()
        confirm = QMessageBox.critical(self, "Delete row", "Are you sure you want to delete selected row?", QMessageBox.Yes, QMessageBox.No)
        if confirm == QMessageBox.Yes:
            row = index.row()
            self.model.removeRow(row)
        self.model.select()
        QMessageBox.information(self, "Deleted", "The selected row has been deleted.")

    def editCell(self):
        self.model.submitAll();
    
    def resource_path(self, relative_path):
            """
            Get absolute path to resource, works for dev and for PyInstaller --onefile
            """
            try:
                base_path = sys._MEIPASS  # PyInstaller temp folder
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

    
    def get_base_path(self):
        """Return folder where the app/exe is located."""
        if getattr(sys, 'frozen', False):  # Running as PyInstaller EXE
            return os.path.dirname(sys.executable)
        else:  # Running as normal Python script
            return os.path.dirname(os.path.abspath(__file__))

    def saveAs(self):
        source_path = self.get_base_path() + "/" + "pitchinput.db"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Plot", "", "DB Files (*.db);;CSV Files (*.csv);;All Files (*)")
        if file_path:
            if file_path.endswith(".db"):
                shutil.copy2(source_path,file_path)
            elif file_path.endswith(".csv"):
                conn = sqlite3.connect(source_path)
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {self.current_table}")

                headers = [i[0] for i in cursor.description]

                with open(file_path, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(headers) # Write headers
                    csv_writer.writerows(cursor) # Write all data rows

                conn.close()

    def makeGameReport (self):
        source_path = self.get_base_path() + "/" + "pitchinput.db"
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Game Data", "", "CSV Files (*.csv);;All Files (*)")

        pitch_types = ["4FB","SI","CUT","CH","SL", "CU","SW" ,"SPL","KN", "OTHER"]
        results = ["All","WHIFF", "STRIKE", "QM"]
        combined = [f"{pt} {res}" for pt in pitch_types for res in results]
        pitchers = self.pullStats()
        if file_path:
            with open(file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                
                csv_writer.writerow(["first", "last", "team","id", "total pitches", "first pitch strikes", "1-0>1-1", "1-1>1-2", "strike%", "lead outs"] + combined)
                csv_writer.writerows(pitchers)
                csv_writer.writerows(["",""])

                conn = sqlite3.connect(source_path)
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM pitchinput")
                
                headers = [i[0] for i in cursor.description]
                csv_writer.writerow(headers) # Write headers
                csv_writer.writerows(cursor) # Write all data rows
                conn.close()



                

                
            

    def pullStats(self):
        stats = []
        pitchers = []
        total_pitches = 0
        strikes = 0
        first_pitch_strikes = 0
        ones_count = 0
        twos_count = 0
        first_out = 0
        innings = 0
        outs = 0
        kperc = 0
        result = ""
        pitch_counts = []
        id = -1
        game_id = self.getGame()
        query = QSqlQuery(f"SELECT DISTINCT pitchers.first_name, pitchers.last_name, pitchers.team, pitchinput.pitcher_id FROM pitchinput INNER JOIN pitchers ON pitchinput.pitcher_id = pitchers.id WHERE game_id = {game_id} GROUP BY pitchers.team, pitchers.last_name, pitchers.first_name")
        while query.next():

            print(query.value(0),query.value(1), query.value(2))
            pitchers.append((query.value(0),query.value(1),query.value(2),query.value(3)))
            
        for pitcher in pitchers:
            query = QSqlQuery(f"SELECT COUNT(id) FROM pitchinput WHERE pitcher_id = {pitcher[3]}")
            while query.next():
                total_pitches = query.value(0)
            query = QSqlQuery(f'SELECT COUNT(id) FROM pitchinput WHERE (pitch_result = "STRIKE" OR pitch_result = "WHIFF" OR pitch_result = "QM" OR pitch_result = "INPLAY") AND pitcher_id = {pitcher[3]}')
            while query.next():
                strikes = query.value(0)
            query = QSqlQuery(f'SELECT COUNT(id) FROM pitchinput WHERE (balls = 0 AND strikes = 0 AND (pitch_result = "STRIKE" OR pitch_result = "WHIFF")) AND pitcher_id = {pitcher[3]}')
            while query.next():
                first_pitch_strikes = query.value(0)
            query = QSqlQuery(f'SELECT COUNT(id) FROM pitchinput WHERE (balls = 1 AND strikes = 0 AND (pitch_result = "STRIKE" OR pitch_result = "WHIFF")) AND pitcher_id = {pitcher[3]}')
            while query.next():
                ones_count = query.value(0)
            query = QSqlQuery(f'SELECT COUNT(id) FROM pitchinput WHERE (balls = 1 AND strikes = 1 AND (pitch_result = "STRIKE" OR pitch_result = "WHIFF")) AND pitcher_id = {pitcher[3]}')
            while query.next():
                twos_count = query.value(0)
            query = QSqlQuery(f'SELECT pa_result, id FROM pitchinput WHERE pitcher_id = {pitcher[3]} LIMIT 1')
            while query.next():
                result = query.value(0)
                id = query.value(1)
        
            ALL = []
            WHIFFS = []
            K = []
            QM = []

            for pitch_type in ['4FB','SI','CUT','CH','SL','CU','SW','SPL','KN', 'OTHER']:
                query = QSqlQuery(f"SELECT count(*) FROM pitchinput WHERE (pitcher_id = {pitcher[3]} AND game_id = {game_id}) AND pitch_type = '{pitch_type}'")
                query.next()
                count = query.value(0)
                ALL.append(count)
                query = QSqlQuery(f"SELECT count(*) FROM pitchinput WHERE (pitcher_id = {pitcher[3]} AND game_id = {game_id}) AND pitch_type = '{pitch_type}' AND (pitch_result = 'WHIFF')")
                query.next()
                count = query.value(0)
                WHIFFS.append(count)
                query = QSqlQuery(f"SELECT count(*) FROM pitchinput WHERE (pitcher_id = {pitcher[3]} AND game_id = {game_id}) AND pitch_type = '{pitch_type}' AND (pitch_result = 'WHIFF' OR pitch_result = 'STRIKE' OR pitch_result = 'QM' OR pitch_result = 'INPLAY')")
                query.next()
                count = query.value(0)
                K.append(count)
                query = QSqlQuery(f"SELECT count(*) FROM pitchinput WHERE (pitcher_id = {pitcher[3]} AND game_id = {game_id}) AND pitch_type = '{pitch_type}' AND (pitch_result = 'QM')")
                query.next()
                count = query.value(0)
                QM.append(count)
            temp = []

            for i in range(len(['4FB','SI','CUT','CH','SL','CU','SW','SPL','KN', 'OTHER'])):
                temp.append(ALL[i])
                temp.append(WHIFFS[i])
                temp.append(K[i])
                temp.append(QM[i])

            
        

                
            

            first_out, innings = self.count_first_outs(pitcher[3], id)

            kperc = (strikes/total_pitches)*100
            print([pitcher[0], pitcher[1], pitcher[2], pitcher[3], total_pitches, first_pitch_strikes, ones_count, twos_count, kperc, 0]+temp)
            stats.append([pitcher[0], pitcher[1], pitcher[2],pitcher[3], total_pitches, first_pitch_strikes, ones_count, twos_count, kperc, 0]+temp)
        return stats
    

    def getGame(self):
        game_id_dialog = QDialog()
        game_id_dialog.setWindowTitle("Select Game")
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Enter Game ID:"))
        game_id_input = QListWidget()
        query = QSqlQuery("SELECT id, game_date, opponent FROM games")
        while query.next():
            game_id = query.value(0)
            game_date = query.value(1)
            opponent = query.value(2)
            full_name = f"{game_date} vs {opponent}"
            item = QListWidgetItem(full_name)
            item.setData(Qt.UserRole, game_id)
            game_id_input.addItem(item)
        game_id_input.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        layout.addWidget(game_id_input)
        submit_btn = QPushButton("Submit")  
        layout.addWidget(submit_btn)
        game_id_dialog.setLayout(layout)
        submit_btn.clicked.connect(game_id_dialog.accept)
        game_id_dialog.exec()
        if game_id_dialog.result() == QDialog.DialogCode.Accepted:
            selected_items = game_id_input.selectedItems()
            if selected_items:
                return selected_items[0].data(Qt.UserRole)
            
    def count_first_outs(self, pitcher_id, game_id):
        innings = 0
        outs = 0
        first_outs = 0
        source_path = self.get_base_path() + "/" + "pitchinput.db"
        conn = sqlite3.connect(source_path)
        cursor = conn.cursor()
        cursor.execute(f'SELECT balls, strikes, pitch_result, pa_result FROM pitchinput WHERE pitcher_id = {pitcher_id} AND game_id = {game_id}')

        for row in cursor.fetchall():
            balls = row[0]
            strikes = row[1]
            pitch_result = row[2]
            pa_result = row[3]

            if strikes == 2 and (pitch_result == "STRIKE" or pitch_result == "WHIFF"):
                if pa_result == None:
                    outs += 1
                    if outs == 0:
                        first_outs += 1
            elif pa_result in ["Ground Out", "Fly Out", "Line Out"]:
                outs += 1
                if outs == 1:
                    first_outs += 1
            if outs == 3:
                innings += 1
                outs = 0
        conn.close()
        return first_outs, innings
    


            
        #dir_path = QFileDialog.getExistingDirectory(self,"Select Directory")







class Main(QWidget):

    def __init__(self):
        super().__init__()



        screen = QApplication.primaryScreen()
        
        screen_size = screen.availableGeometry()

        print(screen_size.width(), screen_size.height())

        width = int(screen_size.width() * 0.6)
        height = int(screen_size.height() * 0.6)

        self.resize(width, height)

        self.setWindowTitle("QPitchMaps")



        main_layout = QVBoxLayout()



        self.stack = QStackedWidget()


        self.home_screen = HomeScreen()
        self.game_input = GameInput()
        self.pitch_input = QPitchMapsInput()
        self.bullpen_input = BullpenInput()
        self.analyitics = AnyliticsScreen()
        self.pen_analytics = BullpenAnyliticsScreen()
        self.pitcher_profiles = PitcherProfiles()
        self.hitter_profiles = HitterProfiles()
        self.table_screen = ViewTables()


        self.game_input.playersSet.connect(self.pitch_input.updateLabels)
        self.game_input.playersSet.connect(self.bullpen_input.updateLabels)
        self.game_input.gameSet.connect(self.pitch_input.retriveGame)

        self.home_screen.setFixedHeight(int(height*0.7))
        self.stack.addWidget(self.home_screen)
        self.stack.addWidget(self.game_input)
        self.stack.addWidget(self.pitch_input)
        self.stack.addWidget(self.analyitics)
        self.stack.addWidget(self.bullpen_input)
        self.stack.addWidget(self.pen_analytics)
        self.stack.addWidget(self.pitcher_profiles)
        self.stack.addWidget(self.hitter_profiles)
        self.stack.addWidget(self.table_screen)
       




        home_screen_btn = QPushButton("Home Screen")
        game_data_input_btn = QPushButton("Game Data")
        pitch_input_btn = QPushButton("Input Game")
        analyze_btn = QPushButton("Analyze Game")
        bullpen_input_btn = QPushButton("Input Bullpen")
        pen_analyze_btn = QPushButton("Analyze Bullpen")
        pitcher_profiles_btn = QPushButton("Pitcher Profiles")
        hitter_profiles_btn = QPushButton("Hitter Profiles")
        view_database_btn = QPushButton("View Database")



        self.setStyleSheet("QPushButton {border-radius: 8px; background-color: lightgray; border: 1px solid black; padding: 5px;} QPushButton:hover {background-color: lightblue;}")
        self.setStyleSheet("QWidget {font: Optima;  }  ")


        buttonrow = QHBoxLayout()
        buttonrow.addWidget(home_screen_btn)
        buttonrow.addWidget(game_data_input_btn)
        buttonrow.addWidget(pitch_input_btn)
        buttonrow.addWidget(analyze_btn)
        buttonrow.addWidget(bullpen_input_btn)
        buttonrow.addWidget(pen_analyze_btn)
        buttonrow.addWidget(pitcher_profiles_btn)
        buttonrow.addWidget(hitter_profiles_btn)
        buttonrow.addWidget(view_database_btn)


        home_screen_btn.clicked.connect(self.one)
        game_data_input_btn.clicked.connect(self.two)
        pitch_input_btn.clicked.connect(self.three)
        analyze_btn.clicked.connect(self.four)   
        bullpen_input_btn.clicked.connect(self.five)
        pen_analyze_btn.clicked.connect(self.six)
        pitcher_profiles_btn.clicked.connect(self.seven)
        hitter_profiles_btn.clicked.connect(self.eight)
        view_database_btn.clicked.connect(self.nine)
        




        main_layout.addWidget(self.stack)
        main_layout.addLayout(buttonrow)



        self.stack.setCurrentIndex(0)
        self.setLayout(main_layout)

        self.home_screen.bullpen_btn.clicked.connect(self.five)
        self.home_screen.game_btn.clicked.connect(self.three)
        self.home_screen.player_data.clicked.connect(self.two)



    def one(self):
        self.stack.setCurrentIndex(0)
    def two(self):  
        self.stack.setCurrentIndex(1)
    def three(self):  
        self.stack.setCurrentIndex(2)
    def four(self):  
        self.stack.setCurrentIndex(3)
        self.analyitics.load_players()
    def five(self):
        self.stack.setCurrentIndex(4)
    def six(self):  
        self.stack.setCurrentIndex(5)
        self.pen_analytics.load_players()
    def seven(self):
        self.stack.setCurrentIndex(6)
        self.pitcher_profiles.loadPitchers()
    def eight(self):
        self.stack.setCurrentIndex(7)
        self.hitter_profiles.loadHitters()
    def nine(self):
        self.stack.setCurrentIndex(8)
    def ten (self):
        self.stack.setCurrentIndex(9)

    def loadDatabase(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Database",
            "",
            "SQLite Database (*.db)"
        )

        if not file_path:
            return

        global database

        if database.isOpen():
            database.close()

        database.setDatabaseName(file_path)

        if not database.open():
            QMessageBox.critical(self, "Database Error", "Could not open selected database.")
            return

        QMessageBox.information(self, "Database Loaded", f"Now using:\n{file_path}")

        self.analyitics.load_players()
        self.game_input.load_players()

if __name__ == "__main__":
    app = QApplication([])
    my_app = Main()
    my_app.show()
    app.exec_()