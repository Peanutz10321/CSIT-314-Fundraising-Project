from app.entities.Recommendation import Recommendation


class recommendActivitiesController:
    def recommendActivities(self, donee_id: int, limit: int = 5):
        return Recommendation.recommendActivities(donee_id, limit)