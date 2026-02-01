"""
Add demo users to Qdrant user_profiles collection.
These match the frontend demo users for testing purposes.
"""
import os
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# Generate consistent UUIDs from names (using namespace)
NAMESPACE = uuid.UUID('6ba7b810-9dad-11d1-80b4-00c04fd430c8')  # DNS namespace

def generate_uuid(name: str) -> str:
    """Generate a consistent UUID from a name."""
    return str(uuid.uuid5(NAMESPACE, name))

# Print UUIDs for frontend reference
print("Generated UUIDs for demo users:")
print(f"  demo_student_001:     {generate_uuid('demo_student_001')}")
print(f"  demo_professional_001: {generate_uuid('demo_professional_001')}")
print(f"  demo_parent_001:      {generate_uuid('demo_parent_001')}")
print(f"  demo-user-001:        {generate_uuid('demo-user-001')}")
print(f"  guest:                {generate_uuid('guest')}")
print()

# Demo users matching frontend auth.tsx
# Using predictable UUIDs so frontend can reference them
DEMO_USERS = [
    {
        "id": generate_uuid("demo_student_001"),  # Will be consistent UUID
        "original_id": "demo_student_001",
        "name": "Sarah Chen",
        "email": "sarah.chen@demo.edu",
        "persona_type": "college_student",
        "age_range": "18-24",
        "financial_context": {
            "monthly_income": 1500,
            "monthly_expenses": 1200,
            "savings_goal": 200,
            "credit_score_range": "650-700"
        },
        "payment_methods": ["debit_card", "credit_card"],
        "primary_payment_method": "debit_card",
        "preferences": {
            "categories": ["Electronics", "Books & Media", "Fashion"],
            "brands": ["Apple", "Samsung", "Nike"],
            "price_sensitivity": "high"
        },
        "financial_goals": ["save_for_emergency", "build_credit"],
        "purchase_history": [],
        "total_lifetime_value": 0,
        "purchase_count": 0,
        "avg_order_value": 0,
        "days_since_last_purchase": 0,
        "days_since_registration": 30,
        "session_count": 5,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
        "budget_min": 300,
        "budget_max": 800,
        "affordability_score": 0.5,
        "price_sensitivity": 0.7
    },
    {
        "id": generate_uuid("demo_professional_001"),
        "original_id": "demo_professional_001",
        "name": "Marcus Johnson",
        "email": "marcus.j@demo.tech",
        "persona_type": "software_engineer",
        "age_range": "25-34",
        "financial_context": {
            "monthly_income": 8000,
            "monthly_expenses": 4500,
            "savings_goal": 2000,
            "credit_score_range": "750-800"
        },
        "payment_methods": ["credit_card", "debit_card", "installments"],
        "primary_payment_method": "credit_card",
        "preferences": {
            "categories": ["Electronics", "Home & Kitchen", "Sports & Fitness"],
            "brands": ["Apple", "Sony", "Bose", "Nike"],
            "price_sensitivity": "low"
        },
        "financial_goals": ["invest", "home_purchase"],
        "purchase_history": [],
        "total_lifetime_value": 5000,
        "purchase_count": 15,
        "avg_order_value": 333.33,
        "days_since_last_purchase": 7,
        "days_since_registration": 365,
        "session_count": 50,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
        "budget_min": 1000,
        "budget_max": 2500,
        "affordability_score": 0.85,
        "price_sensitivity": 0.3
    },
    {
        "id": generate_uuid("demo_parent_001"),
        "original_id": "demo_parent_001",
        "name": "Jennifer Martinez",
        "email": "jen.martinez@demo.family",
        "persona_type": "budget_conscious_parent",
        "age_range": "35-44",
        "financial_context": {
            "monthly_income": 5000,
            "monthly_expenses": 4200,
            "savings_goal": 500,
            "credit_score_range": "700-750"
        },
        "payment_methods": ["debit_card", "credit_card"],
        "primary_payment_method": "debit_card",
        "preferences": {
            "categories": ["Home & Kitchen", "Beauty & Personal Care", "Books & Media"],
            "brands": ["Target", "Amazon Basics", "Instant Pot"],
            "price_sensitivity": "high"
        },
        "financial_goals": ["save_for_kids_education", "emergency_fund"],
        "purchase_history": [],
        "total_lifetime_value": 2000,
        "purchase_count": 25,
        "avg_order_value": 80,
        "days_since_last_purchase": 3,
        "days_since_registration": 180,
        "session_count": 40,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
        "budget_min": 200,
        "budget_max": 600,
        "affordability_score": 0.4,
        "price_sensitivity": 0.8
    },
    {
        "id": generate_uuid("demo-user-001"),
        "original_id": "demo-user-001",
        "name": "Demo User",
        "email": "demo@finfind.com",
        "persona_type": "general_shopper",
        "age_range": "25-34",
        "financial_context": {
            "monthly_income": 5000,
            "monthly_expenses": 3500,
            "savings_goal": 1000,
            "credit_score_range": "700-750"
        },
        "payment_methods": ["credit_card", "debit_card"],
        "primary_payment_method": "credit_card",
        "preferences": {
            "categories": ["Electronics", "Fashion", "Home & Kitchen"],
            "brands": ["Apple", "Samsung", "Nike", "Sony"],
            "price_sensitivity": "medium"
        },
        "financial_goals": ["save_money", "smart_shopping"],
        "purchase_history": [],
        "total_lifetime_value": 1500,
        "purchase_count": 10,
        "avg_order_value": 150,
        "days_since_last_purchase": 14,
        "days_since_registration": 60,
        "session_count": 20,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
        "budget_min": 500,
        "budget_max": 1500,
        "affordability_score": 0.65,
        "price_sensitivity": 0.5
    },
    {
        "id": generate_uuid("guest"),
        "original_id": "guest",
        "name": "Guest User",
        "email": "guest@finfind.demo",
        "persona_type": "guest",
        "age_range": "unknown",
        "financial_context": {
            "monthly_income": 0,
            "monthly_expenses": 0,
            "savings_goal": 0,
            "credit_score_range": "unknown"
        },
        "payment_methods": ["credit_card"],
        "primary_payment_method": "credit_card",
        "preferences": {
            "categories": [],
            "brands": [],
            "price_sensitivity": "medium"
        },
        "financial_goals": [],
        "purchase_history": [],
        "total_lifetime_value": 0,
        "purchase_count": 0,
        "avg_order_value": 0,
        "days_since_last_purchase": 0,
        "days_since_registration": 0,
        "session_count": 1,
        "created_at": datetime.now().isoformat(),
        "updated_at": None,
        "budget_min": 0,
        "budget_max": 1000,
        "affordability_score": 0.5,
        "price_sensitivity": 0.5
    }
]


def main():
    print("Connecting to Qdrant...")
    client = QdrantClient(
        url=os.getenv('QDRANT_URL'),
        api_key=os.getenv('QDRANT_API_KEY')
    )
    
    print("Loading embedding model...")
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    print("Creating demo user points...")
    points = []
    
    for user in DEMO_USERS:
        # Generate embedding from user profile
        text = f"""
        User persona: {user['persona_type']}
        Age range: {user['age_range']}
        Budget range: ${user['budget_min']} - ${user['budget_max']}
        Categories: {', '.join(user['preferences']['categories'])}
        Brands: {', '.join(user['preferences']['brands'])}
        Price sensitivity: {user['preferences']['price_sensitivity']}
        """
        
        vector = model.encode(text).tolist()
        
        # Create payload (exclude 'id' as it's separate)
        payload = {k: v for k, v in user.items() if k != 'id'}
        
        points.append(PointStruct(
            id=user['id'],
            vector=vector,
            payload=payload
        ))
        print(f"  Created point for: {user['name']} ({user['id']})")
    
    print(f"\nUpserting {len(points)} demo users to Qdrant...")
    client.upsert(
        collection_name='user_profiles',
        points=points
    )
    
    print("Done! Demo users added to user_profiles collection.")
    
    # Verify
    count = client.count(collection_name='user_profiles').count
    print(f"Total user profiles now: {count}")


if __name__ == "__main__":
    main()
