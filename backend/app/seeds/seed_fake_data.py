import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.entities.UserAccount import UserAccount
from app.entities.UserProfile import UserProfile
from app.entities.FundraisingCategory import FundraisingCategory
from app.entities.FundraisingActivity import FundraisingActivity
from app.middleware.auth import hash_password

_FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
    "Iris", "Jack", "Karen", "Liam", "Mia", "Noah", "Olivia", "Paul",
    "Quinn", "Rachel", "Samuel", "Tina", "Uma", "Victor", "Wendy", "Xander",
    "Yvonne", "Zachary", "Aria", "Ben", "Clara", "Dylan", "Emma", "Finn",
    "Gina", "Hugo", "Isla", "James", "Kira", "Leo", "Maya", "Nate",
]

_LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
    "Davis", "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson",
    "White", "Harris", "Martin", "Thompson", "Young", "Allen", "King",
    "Wright", "Scott", "Green", "Baker", "Adams", "Nelson", "Carter",
    "Mitchell", "Perez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee",
    "Walker", "Hall", "Turner", "Hill", "Parker",
]

_CATEGORY_NAMES = [
    "Youth Sports", "Senior Care", "Environmental Conservation", "Mental Health Support",
    "Food Security", "Clean Water Access", "Refugee Support", "Indigenous Communities",
    "LGBTQ+ Rights", "Disability Access", "Rural Development", "Urban Renewal",
    "Arts & Culture", "Music Education", "Film & Media", "Theater Arts",
    "Science Research", "Technology Access", "Digital Literacy", "Cybersecurity Awareness",
    "Climate Action", "Renewable Energy", "Ocean Conservation", "Wildlife Protection",
    "Rainforest Preservation", "Coral Reef Restoration", "Polar Conservation", "Wetlands Protection",
    "Organic Farming", "Sustainable Agriculture", "Beekeeping Support", "Aquaculture Development",
    "Literacy Programs", "Early Childhood Education", "STEM Education", "Vocational Training",
    "University Scholarships", "Teacher Development", "Library Support", "Language Preservation",
    "Cancer Research", "Diabetes Awareness", "Heart Disease Prevention", "HIV/AIDS Support",
    "Mental Wellness", "Addiction Recovery", "Maternal Health", "Child Nutrition",
    "Elderly Care", "Hospice Support", "Vision Impairment Aid", "Hearing Impairment Aid",
    "Emergency Relief", "Flood Recovery", "Earthquake Aid", "Wildfire Recovery",
    "Hurricane Relief", "Drought Relief", "Pandemic Response", "War Zone Aid",
    "Homeless Support", "Affordable Housing", "Domestic Violence Shelter", "Prison Reform",
    "Youth Employment", "Microfinance", "Women Entrepreneurship", "Small Business Support",
    "Veterans Support", "Military Families", "War Veteran Rehabilitation", "PTSD Support",
    "Children's Hospitals", "Orphan Care", "Foster Care", "Child Labor Prevention",
    "Human Trafficking Prevention", "Migrant Worker Support", "Immigration Aid", "Asylum Seeker Support",
    "Community Kitchen", "Food Bank Operations", "Community Sports", "Para-athletics",
    "Special Olympics", "Adaptive Sports", "Public Health Awareness", "Vaccination Campaigns",
    "Disease Prevention", "Water Sanitation", "Cycling Infrastructure", "Pedestrian Safety",
    "Road Safety", "Space Exploration Education", "Marine Biology Research", "Genetics Research",
    "Social Justice", "Equal Pay Initiative", "Childcare Support", "Youth Mentorship",
]

_LOCATIONS = [
    "New York, USA", "London, UK", "Tokyo, Japan", "Sydney, Australia",
    "Toronto, Canada", "Berlin, Germany", "Paris, France", "Mumbai, India",
    "São Paulo, Brazil", "Lagos, Nigeria", "Nairobi, Kenya", "Cairo, Egypt",
    "Bangkok, Thailand", "Seoul, South Korea", "Mexico City, Mexico", "Kuala Lumpur, Malaysia",
    "Singapore", "Jakarta, Indonesia", "Manila, Philippines", "Cape Town, South Africa",
]

_CURRENCIES = ["USD", "EUR", "GBP", "AUD", "CAD", "MYR", "SGD"]

_BENEFICIARIES = [
    "Children", "Families", "Seniors", "Veterans", "Students", "Refugees",
    "Communities", "Local Farmers", "Young Women", "Disabled Individuals",
    "Homeless People", "Orphans", "Elderly", "Youth", "Animals",
]

_ACTIVITY_WORDS = [
    "Hope", "Future", "Change", "Impact", "Together", "Rising", "Unity",
    "Bright", "New Dawn", "Light", "Path", "Journey", "Bridge", "Spark",
    "Wave", "Force", "Power", "Voice", "Dream", "Vision",
]


def _random_deadline(rng: random.Random) -> str:
    return (datetime.now() + timedelta(days=rng.randint(30, 365))).strftime("%Y-%m-%d")


def _seed_fake_users(db: Session, count: int = 100):
    if db.query(UserAccount).filter(UserAccount.email == "seed_user_001@example.com").first():
        return db.query(UserAccount).filter(
            UserAccount.email.like("seed_user_%@example.com")
        ).all()

    rng = random.Random(42)
    fundraiser_profile = db.query(UserProfile).filter(UserProfile.name_of_role == "FUNDRAISER").first()
    donee_profile = db.query(UserProfile).filter(UserProfile.name_of_role == "DONEE").first()
    if not fundraiser_profile or not donee_profile:
        return []

    created = []
    for i in range(1, count + 1):
        profile = fundraiser_profile if i <= count // 2 else donee_profile
        user = UserAccount(
            name=f"{rng.choice(_FIRST_NAMES)} {rng.choice(_LAST_NAMES)}",
            email=f"seed_user_{i:03d}@example.com",
            password_hash=hash_password("password123"),
            user_profile_id=profile.id,
            status="ACTIVE",
            phone_no=f"+1{rng.randint(20000000, 99999999)}",
            address=rng.choice(_LOCATIONS),
            dob=f"{rng.randint(1970, 2000)}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
        )
        db.add(user)
        created.append(user)

    db.commit()
    for u in created:
        db.refresh(u)
    return created


def _seed_fake_categories(db: Session, count: int = 100):
    existing_names = {c.name for c in db.query(FundraisingCategory).all()}
    names_to_add = [n for n in _CATEGORY_NAMES[:count] if n not in existing_names]

    created = []
    for name in names_to_add:
        category = FundraisingCategory(
            name=name,
            description=f"Fundraising activities related to {name.lower()}.",
            status="ACTIVE",
            date_created=datetime.now(),
        )
        db.add(category)
        created.append(category)

    if created:
        db.commit()
        for c in created:
            db.refresh(c)

    return db.query(FundraisingCategory).filter(
        FundraisingCategory.name.in_(_CATEGORY_NAMES[:count])
    ).all()


def _seed_fake_activities(db: Session, fundraisers, categories, count: int = 100) -> None:
    if not fundraisers or not categories:
        return

    fundraiser_ids = [u.id for u in fundraisers]
    existing_count = db.query(FundraisingActivity).filter(
        FundraisingActivity.fundraiser_id.in_(fundraiser_ids)
    ).count()
    missing_count = count - existing_count
    if missing_count <= 0:
        return

    rng = random.Random(42)
    statuses = ["ACTIVE", "ACTIVE", "ACTIVE", "SUSPENDED", "COMPLETED"]

    for i in range(1, missing_count + 1):
        fundraiser = rng.choice(fundraisers)
        category = rng.choice(categories)
        beneficiary = rng.choice(_BENEFICIARIES)
        location = rng.choice(_LOCATIONS)
        word = rng.choice(_ACTIVITY_WORDS)

        status = rng.choice(statuses)

        goal = round(rng.uniform(500, 50000), 2)

        if status == "COMPLETED":
            current = round(rng.uniform(goal, goal * 1.2), 2)
        else:
            current = round(rng.uniform(0, goal * 0.85), 2)

        if status == "COMPLETED":
            deadline = (datetime.now() - timedelta(days=rng.randint(1, 180))).strftime("%Y-%m-%d")
        else:
            deadline = _random_deadline(rng)

        activity = FundraisingActivity(
            fundraiser_id=fundraiser.id,
            title=f"{word} for {beneficiary} #{i}",
            description=f"A fundraising campaign to support {beneficiary.lower()} in {location}.",
            currency=rng.choice(_CURRENCIES),
            goal_amount=goal,
            current_amount=current,
            category_id=category.id,
            location=location,
            beneficiaryName=beneficiary,
            fundraiserName=fundraiser.name,
            deadline=deadline,
            status=status,
            view_count=rng.randint(0, 500),
            shortlist_count=0,
            date_created=datetime.now() - timedelta(days=rng.randint(0, 365)),
        )
        db.add(activity)

    db.commit()

def _seed_fake_favorites(db: Session, donees, activities, count: int = 100):
    from app.entities.FavoriteList import FavoriteList

    if not donees or not activities:
        return

    existing_count = db.query(FavoriteList).count()
    if existing_count >= count:
        return

    rng = random.Random(42)
    pairs = set()

    while len(pairs) < count:
        donee = rng.choice(donees)
        activity = rng.choice(activities)

        pair = (donee.id, activity.id)
        if pair in pairs:
            continue

        pairs.add(pair)

        favorite = FavoriteList(
            donee_id=donee.id,
            activity_id=activity.id,
            date_saved=datetime.now() - timedelta(days=rng.randint(0, 90)),
        )

        activity.shortlist_count = (activity.shortlist_count or 0) + 1
        db.add(favorite)

    db.commit()


def seed_fake_data(db: Session) -> None:
    all_users = _seed_fake_users(db)

    fundraiser_profile_ids = {
        p.id for p in db.query(UserProfile).filter(UserProfile.name_of_role == "FUNDRAISER").all()
    }
    fundraisers = [u for u in all_users if u.user_profile_id in fundraiser_profile_ids]

    categories = _seed_fake_categories(db)
    _seed_fake_activities(db, fundraisers, categories)

    donee_profile_ids = {
        p.id for p in db.query(UserProfile).filter(
            UserProfile.name_of_role == "DONEE"
        ).all()
    }

    donees = [u for u in all_users if u.user_profile_id in donee_profile_ids]

    activities = db.query(FundraisingActivity).all()
    _seed_fake_favorites(db, donees, activities)
