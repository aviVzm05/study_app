from models.models import Progress
from datetime import datetime

class ProgressService:
    def __init__(self):
        pass

    def get_progress_for_topic(self, topic_id):
        """Retrieves progress for a specific topic."""
        return next((p for p in Progress.find_all() if p.topic_id == topic_id), None)

    def update_progress(self, topic_id, score, completed):
        """Updates or creates progress for a topic."""
        progress = self.get_progress_for_topic(topic_id)
        if progress:
            # Update existing progress
            progress.score = max(progress.score, score) # Keep highest score
            progress.completed = completed
            progress.last_attempted = datetime.now().isoformat()
            progress.save()
        else:
            # Create new progress entry
            progress = Progress(topic_id=topic_id, score=score, completed=completed, last_attempted=datetime.now().isoformat())
            progress.save()
        return progress

    def is_topic_completed(self, topic_id):
        """Checks if a topic has been marked as completed."""
        progress = self.get_progress_for_topic(topic_id)
        return progress and progress.completed
