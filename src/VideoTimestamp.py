import datetime

class VideoTimestamp:
    def __init__(self, frame_rate):
        self.frame_rate = frame_rate
        self.frame_count = 0

    def update_frame_count(self):
        self.frame_count += 1

    def get_elapsed_time(self):
        elapsed_time_sec = self.frame_count / self.frame_rate
        return datetime.timedelta(seconds=elapsed_time_sec)

    def get_formatted_time(self):
        elapsed_time = self.get_elapsed_time()
        return str(elapsed_time)
