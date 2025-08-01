#test_data/dummy_users.py

from models.user import User

dummy_users = [
    User("Kristoffer", "Gillesberg", "kristoffer@example.com", "admin"),
    User("Anna", "Hansen", "anna@example.com", "tech_support"),
    User("Mikkel", "Jensen", "mikkel@example.com", "owner")
]

def dummy_users_as_dicts():
    return [user.__dict__ for user in dummy_users]
