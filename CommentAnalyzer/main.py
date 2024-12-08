from CommentSentimentScore import get_sentiment_for_comments, save_to_comment_sentiment_score, print_sentiment_results
from parse_words import load_processed_comments
import asyncio
from TikTokApi.TrendingComments.get_comments import (
    get_comments,
    get_hashtag_videos,
    get_comments_for_videos,
    get_related_videos,
    get_video_from_user,
    sound_videos
)

from TikTokApi.TrendingComments.get_trending_videos import (
    trending_videos,
    get_hashtag_videos,
    
)
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, QRadioButton,
    QPushButton, QButtonGroup, QMessageBox, QTextEdit
)
from PyQt5.QtWidgets import QInputDialog, QFileDialog
import json
class SentimentAnalysisApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TikTok Comment Sentiment Analysis")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("TikTok Comment Sentiment Analysis")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        layout.addWidget(title_label)

        # Instructions
        instructions = """Please select a letter for your desired mode of sentiment analysis:

A. Input video IDs for analysis on comments
B. Input hashtag for analysis on comments from hashtagged videos
C. Analyze trending videos' comments
D. Input sound ID for analysis on comments from videos under provided sound
E. Input username for analysis on comments from videos created by user
F. Input video URL for analysis on comments from related videos
G. Directly input comments to analyze
"""
        instructions_text = QTextEdit()
        instructions_text.setPlainText(instructions)
        instructions_text.setReadOnly(True)
        instructions_text.setStyleSheet("font-size: 14px;")
        layout.addWidget(instructions_text)

        # Radio Buttons
        self.button_group = QButtonGroup()
        modes = [
            ("A. Input video IDs for analysis on comments", "A"),
            ("B. Input hashtag for analysis on comments from hashtagged videos", "B"),
            ("C. Analyze trending videos' comments", "C"),
            ("D. Input sound ID for analysis on comments from videos under provided sound", "D"),
            ("E. Input username for analysis on comments from videos created by user", "E"),
            ("F. Input video URL for analysis on comments from related videos", "F"),
            ("G. Directly input comments to analyze", "G"),
        ]

        for text, value in modes:
            radio_button = QRadioButton(text)
            self.button_group.addButton(radio_button, id=ord(value))
            layout.addWidget(radio_button)

        # Submit Button
        submit_button = QPushButton("Submit")
        submit_button.setStyleSheet("font-size: 16px; padding: 10px;")
        submit_button.clicked.connect(self.handleSubmit)
        layout.addWidget(submit_button)

        # Set layout
        
        self.results_display = QTextEdit()
        self.results_display.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.results_display)
        central_widget.setLayout(layout)

    def handleSubmit(self):
        selected_button = self.button_group.checkedButton()
        if selected_button:
            selected_id = chr(self.button_group.id(selected_button))
            self.routeSelection(selected_id)
        else:
            QMessageBox.warning(self, "Warning", "Please select a mode.")

    def routeSelection(self, mode):
        """
        Route to the appropriate action based on the selected mode.
        """
        if mode == "A":
            self.handleVideoIDInput()
        elif mode == "B":
            self.handleHashtagInput()
        elif mode == "C":
            self.handleTrendingAnalysis()
        elif mode == "D":
            self.handleSoundIDInput()
        elif mode == "E":
            self.handleUsernameInput()
        elif mode == "F":
            self.handleRelatedVideoAnalysis()
        elif mode == "G":
            self.handleDirectCommentInput()
        else:
            QMessageBox.critical(self, "Error", "Invalid selection!")

    def handleVideoIDInput(self):
        """
        Ask the user to input video IDs for analysis.
        """
        video_ids, ok = QInputDialog.getText(
            self,
            "Input Video IDs",
            "Enter Video IDs separated by commas:"
        )
        if ok and video_ids.strip():
            video_ids_list = [vid.strip() for vid in video_ids.split(",") if vid.strip()]
            comments = asyncio.run(self.async_handleVideoIDInput(video_ids_list))
            results = get_sentiment_for_comments(comments)

            self.display_results(comments, results)
            
            
            # You can now process video_ids_list as needed
        else:
            QMessageBox.warning(self, "No Input", "No Video IDs were entered.")
        
    async def async_handleVideoIDInput(self, video_ids_list):
        comments = await get_comments_for_videos(video_ids_list)
        return comments
    
    def handleHashtagInput(self):
        """
        Ask the user to input a hashtag for analysis.
        """
        hashtag, ok = QInputDialog.getText(
            self,
            "Input Hashtag",
            "Enter a hashtag (without the # symbol):"
        )
        if ok and hashtag.strip():
            hashtag = hashtag.strip()
            comments = asyncio.run(self.async_handleHashtagInput(hashtag))
            results = get_sentiment_for_comments(comments)
            self.display_results(comments, results)
            
            # You can now process the hashtag as needed
        else:
            QMessageBox.warning(self, "No Input", "No hashtag was entered.")
           
           
    async def async_handleHashtagInput(self, hashtag):
        videos = await get_hashtag_videos(hashtag)
        comments = await get_comments_for_videos(videos)
        return comments
    
     
    def handleTrendingAnalysis(self):
        """
        Stub for analyzing trending videos' comments.
        """
        comments = asyncio.run(self.async_handleTrendingAnalysis())
        results = get_sentiment_for_comments(comments)
        self.display_results(comments, results)
        # video_ids = await trending_videos()
    
        # all_comments = await get_comments_for_videos(video_ids)
        
    async def async_handleTrendingAnalysis(self):
        videos = await trending_videos()
        comments = await get_comments_for_videos(videos)
        return comments

    def handleSoundIDInput(self):
        """
        Ask the user to input a Sound ID for analysis.
        """
        sound_id, ok = QInputDialog.getText(
            self,
            "Input Sound ID",
            "Enter the Sound ID:"
        )
        if ok and sound_id.strip():
            sound_id = sound_id.strip()
            comments = asyncio.run(self.async_handleSoundIDInput(sound_id))
            results = get_sentiment_for_comments(comments)
            self.display_results(comments, results)
            # You can now process the sound_id as needed
        else:
            QMessageBox.warning(self, "No Input", "No Sound ID was entered.")
            
    async def async_handleSoundIDInput(self, sound_id):
        videos = await sound_videos(sound_id)
        comments = await get_comments_for_videos(videos)
        return comments
            
    def handleUsernameInput(self):
        """
        Ask the user to input a username for analysis.
        """
        username, ok = QInputDialog.getText(
            self,
            "Input Username",
            "Enter the username (without @):"
        )
        if ok and username.strip():
            username = username.strip()
            comments = asyncio.run(self.async_handleUsernameInput(username))
            results = get_sentiment_for_comments(comments)
            self.display_results(comments, results)
            # You can now process the username as needed
        else:
            QMessageBox.warning(self, "No Input", "No username was entered.")
            
    async def async_handleUsernameInput(self, username):
        videos = await get_video_from_user(username)
        comments = await get_comments_for_videos(videos)
        return comments
            
    def handleRelatedVideoAnalysis(self):
        """
        Ask the user to input a video ID for analysis of related video comments.
        """
        video_id, ok = QInputDialog.getText(
            self,
            "Input Video URL",
            "Enter the video URL for related videos analysis:"
        )
        if ok and video_id.strip():
            URL = video_id.strip()
            comments = asyncio.run(self.async_handleRelatedVideoAnalysis(URL))
            results = get_sentiment_for_comments(comments)
            self.display_results(comments, results)
        
            # You can now process the video_id as needed
        else:
            QMessageBox.warning(self, "No Input", "No video ID was entered.")
            
    async def async_handleRelatedVideoAnalysis(self, URL):
        videos = await get_related_videos(URL)
        comments = await get_comments_for_videos(videos)
        return comments
            
    def handleDirectCommentInput(self):
        """
        Ask the user to select a file containing comments for direct analysis.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a JSON File",
            "",
            "JSON Files (*.json);;All Files (*)",
            options=options
        )
        if file_path.endswith(".json"):
            QMessageBox.information(
                self,
                "File Selected",
                f"The following file was selected for comment analysis:\n{file_path}"
            )
            # Process the selected JSON file
            self.processCommentsFile(file_path)
        else:
            QMessageBox.warning(self, "No File Selected", "No file was selected for analysis.")
            
    def processCommentsFile(self, file_path):
        """
        Process the selected JSON file containing comments.
        """
        comments = load_processed_comments(file_path)
        results = get_sentiment_for_comments(comments)
    
        save_to_comment_sentiment_score(comments, results)
        self.display_results(comments, results)
        
    def display_results(self, comments, results):
        """
        Display results in the text area.
        """
        self.results_display.clear()
        for comment, score in zip(comments, results):
            if score > 0:
                sentiment = "positive"
            elif score < 0:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            self.results_display.append(f"Comment: {' '.join(comment)}\nSentiment: {sentiment}\nScore: {score}\n")


def main():
    app = QApplication(sys.argv)
    main_window = SentimentAnalysisApp()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
