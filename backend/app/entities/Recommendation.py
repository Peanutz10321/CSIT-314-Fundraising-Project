from sqlalchemy.orm import joinedload
from sklearn.tree import DecisionTreeClassifier

from app.database import SessionLocal
from app.entities.FavoriteList import FavoriteList
from app.entities.FundraisingActivity import FundraisingActivity


class Recommendation:

    @staticmethod
    def _progress(activity):
        if not activity.goal_amount or activity.goal_amount <= 0:
            return 0
        return activity.current_amount / activity.goal_amount

    @staticmethod
    def _get_donee_preferred_category_ids(db, donee_id: int):
        saved_activities = (
            db.query(FundraisingActivity)
            .join(FavoriteList, FavoriteList.activity_id == FundraisingActivity.id)
            .filter(FavoriteList.donee_id == donee_id)
            .all()
        )

        return {
            activity.category_id
            for activity in saved_activities
            if activity.category_id is not None
        }

    @staticmethod
    def _features(activity, preferred_category_ids):
        category_match = 1 if activity.category_id in preferred_category_ids else 0

        return [
            category_match,
            activity.view_count or 0,
            activity.shortlist_count or 0,
            Recommendation._progress(activity),
            activity.goal_amount or 0,
        ]

    @staticmethod
    def _fallback_recommendations(active_activities, preferred_category_ids, limit: int):
        scored = []

        for activity in active_activities:
            score = 0

            if activity.category_id in preferred_category_ids:
                score += 5

            if (activity.view_count or 0) >= 300:
                score += 3
            elif (activity.view_count or 0) >= 100:
                score += 2
            elif (activity.view_count or 0) >= 30:
                score += 1

            if (activity.shortlist_count or 0) >= 30:
                score += 3
            elif (activity.shortlist_count or 0) >= 10:
                score += 2
            elif (activity.shortlist_count or 0) >= 3:
                score += 1

            scored.append((score, activity))

        scored.sort(key=lambda item: item[0], reverse=True)

        return [
            Recommendation._to_response(activity, score, "Rule-based fallback recommendation")
            for score, activity in scored[:limit]
        ]

    @staticmethod
    def _to_response(activity, score, reason):
        return {
            "id": activity.id,
            "title": activity.title,
            "description": activity.description,
            "currency": activity.currency,
            "goal_amount": activity.goal_amount,
            "current_amount": activity.current_amount,
            "category": activity.category,
            "location": activity.location,
            "beneficiaryName": activity.beneficiaryName,
            "fundraiserName": activity.fundraiserName,
            "deadline": activity.deadline,
            "status": activity.status,
            "view_count": activity.view_count,
            "shortlist_count": activity.shortlist_count,
            "recommendation_score": round(float(score), 2),
            "recommendation_reason": reason,
        }

    @staticmethod
    def recommendActivities(donee_id: int, limit: int = 5):
        db = SessionLocal()

        try:
            preferred_category_ids = Recommendation._get_donee_preferred_category_ids(
                db,
                donee_id,
            )

            saved_activity_ids = {
                row.activity_id
                for row in db.query(FavoriteList)
                .filter(FavoriteList.donee_id == donee_id)
                .all()
            }

            active_activities = (
                db.query(FundraisingActivity)
                .options(joinedload(FundraisingActivity.category_ref))
                .filter(FundraisingActivity.status == "ACTIVE")
                .all()
            )

            candidate_activities = [
                activity
                for activity in active_activities
                if activity.id not in saved_activity_ids
            ]

            if not candidate_activities:
                return []

            training_activities = active_activities

            X = []
            y = []

            for activity in training_activities:
                X.append(Recommendation._features(activity, preferred_category_ids))
                y.append(1 if activity.id in saved_activity_ids else 0)

            # Decision Tree needs both positive and negative labels.
            if len(set(y)) < 2:
                return Recommendation._fallback_recommendations(
                    candidate_activities,
                    preferred_category_ids,
                    limit,
                )

            model = DecisionTreeClassifier(
                max_depth=4,
                random_state=42,
            )

            model.fit(X, y)

            scored_recommendations = []

            for activity in candidate_activities:
                features = Recommendation._features(activity, preferred_category_ids)

                probability = model.predict_proba([features])[0]

                # If class 1 exists, use its probability.
                class_probability = {
                    class_label: probability[index]
                    for index, class_label in enumerate(model.classes_)
                }

                score = class_probability.get(1, 0)

                scored_recommendations.append((score, activity))

            scored_recommendations.sort(key=lambda item: item[0], reverse=True)

            return [
                Recommendation._to_response(
                    activity,
                    score,
                    "Recommended using decision tree based on saved categories, views, shortlists, progress, and goal amount.",
                )
                for score, activity in scored_recommendations[:limit]
            ]

        finally:
            db.close()