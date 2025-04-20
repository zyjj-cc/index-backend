# Import the Surreal class
from surrealdb import Surreal

# Using a context manger to automatically connect and disconnect
with Surreal("ws://localhost:8005/rpc") as db:
    db.signin({"username": 'xiaoyou', "password": 'xiaoyou'})
    db.use("namepace_test", "database_test")

    # Create a record in the person table
    db.create(
        "person",
        {
            "user": "me",
            "password": "safe",
            "marketing": True,
            "tags": ["python", "documentation"],
        },
    )

    # Read all the records in the table
    print(db.select("person"))

