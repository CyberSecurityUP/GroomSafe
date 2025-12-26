"""
Synthetic Data Generator for GROOMSAFE
Generates safe, abstracted conversation examples for testing and development
"""

from datetime import datetime, timedelta
from uuid import uuid4
import json
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from core.data_models import (
    Conversation,
    Message,
    SenderRole
)


def generate_low_risk_conversation() -> Conversation:
    """
    Generate low-risk conversation example
    Represents normal, benign interaction
    """
    base_time = datetime.utcnow() - timedelta(days=7)

    messages = [
        Message(
            timestamp=base_time,
            sender_role=SenderRole.ADULT,
            abstracted_text="Hello, welcome to the community forum. How can I help you today?"
        ),
        Message(
            timestamp=base_time + timedelta(hours=2),
            sender_role=SenderRole.MINOR,
            abstracted_text="Hi, I have a question about the homework assignment."
        ),
        Message(
            timestamp=base_time + timedelta(hours=2, minutes=5),
            sender_role=SenderRole.ADULT,
            abstracted_text="Sure, what's the question about the assignment?"
        ),
        Message(
            timestamp=base_time + timedelta(hours=2, minutes=10),
            sender_role=SenderRole.MINOR,
            abstracted_text="I don't understand problem number 5."
        ),
        Message(
            timestamp=base_time + timedelta(hours=2, minutes=15),
            sender_role=SenderRole.ADULT,
            abstracted_text="That problem relates to the concept we discussed in class. Try reviewing your notes."
        ),
        Message(
            timestamp=base_time + timedelta(hours=3),
            sender_role=SenderRole.MINOR,
            abstracted_text="Got it, thanks for the help!"
        )
    ]

    return Conversation(
        messages=messages,
        start_time=messages[0].timestamp,
        end_time=messages[-1].timestamp,
        platform_type="educational_forum",
        is_synthetic=True
    )


def generate_moderate_risk_conversation() -> Conversation:
    """
    Generate moderate-risk conversation example
    Shows some concerning patterns but not critical
    """
    base_time = datetime.utcnow() - timedelta(days=14)

    messages = [
        Message(
            timestamp=base_time,
            sender_role=SenderRole.ADULT,
            abstracted_text="Hey, saw your post on the gaming forum. Cool setup!"
        ),
        Message(
            timestamp=base_time + timedelta(hours=1),
            sender_role=SenderRole.MINOR,
            abstracted_text="Thanks!"
        ),
        Message(
            timestamp=base_time + timedelta(days=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="We should play together sometime. What games do you like?"
        ),
        Message(
            timestamp=base_time + timedelta(days=1, hours=2),
            sender_role=SenderRole.MINOR,
            abstracted_text="I like adventure games mostly."
        ),
        Message(
            timestamp=base_time + timedelta(days=2),
            sender_role=SenderRole.ADULT,
            abstracted_text="Me too! How often do you play?"
        ),
        Message(
            timestamp=base_time + timedelta(days=2, hours=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="Also, what's your age range if you don't mind me asking?"
        ),
        Message(
            timestamp=base_time + timedelta(days=3),
            sender_role=SenderRole.MINOR,
            abstracted_text="I'm in middle school."
        ),
        Message(
            timestamp=base_time + timedelta(days=3, hours=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="Cool, I could give you some tips if you want."
        ),
        Message(
            timestamp=base_time + timedelta(days=4),
            sender_role=SenderRole.ADULT,
            abstracted_text="You there? Would love to chat more about games."
        ),
        Message(
            timestamp=base_time + timedelta(days=4, hours=12),
            sender_role=SenderRole.ADULT,
            abstracted_text="Hey, just checking in. Hope you're doing well."
        )
    ]

    return Conversation(
        messages=messages,
        start_time=messages[0].timestamp,
        end_time=messages[-1].timestamp,
        platform_type="gaming_platform",
        is_synthetic=True
    )


def generate_high_risk_conversation() -> Conversation:
    """
    Generate high-risk conversation example
    Shows concerning progression and multiple risk factors
    """
    base_time = datetime.utcnow() - timedelta(days=21)

    messages = [
        # Initial contact
        Message(
            timestamp=base_time,
            sender_role=SenderRole.ADULT,
            abstracted_text="Hi, noticed you on the forum. You seem really mature for your age."
        ),
        Message(
            timestamp=base_time + timedelta(hours=3),
            sender_role=SenderRole.MINOR,
            abstracted_text="Thanks!"
        ),
        # Trust building
        Message(
            timestamp=base_time + timedelta(days=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="I really enjoy talking with you. You're different from most people."
        ),
        Message(
            timestamp=base_time + timedelta(days=1, hours=2),
            sender_role=SenderRole.MINOR,
            abstracted_text="That's nice of you to say."
        ),
        Message(
            timestamp=base_time + timedelta(days=2, hours=22),  # Late night
            sender_role=SenderRole.ADULT,
            abstracted_text="You still up? I can't sleep, been thinking about our conversation."
        ),
        Message(
            timestamp=base_time + timedelta(days=3),
            sender_role=SenderRole.ADULT,
            abstracted_text="Hey, are you there? Miss talking to you."
        ),
        Message(
            timestamp=base_time + timedelta(days=3, hours=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="Hope you're okay. Let me know you're alright."
        ),
        Message(
            timestamp=base_time + timedelta(days=3, hours=8),
            sender_role=SenderRole.MINOR,
            abstracted_text="Sorry, was busy with school."
        ),
        # Emotional dependency
        Message(
            timestamp=base_time + timedelta(days=4),
            sender_role=SenderRole.ADULT,
            abstracted_text="I understand you in a way nobody else can. We have a special connection."
        ),
        Message(
            timestamp=base_time + timedelta(days=5),
            sender_role=SenderRole.ADULT,
            abstracted_text="You can tell me anything. I'll always be here for you."
        ),
        Message(
            timestamp=base_time + timedelta(days=6, hours=23),  # Very late
            sender_role=SenderRole.ADULT,
            abstracted_text="Thinking about you. Hope you know how special you are to me."
        ),
        # Isolation attempts
        Message(
            timestamp=base_time + timedelta(days=7),
            sender_role=SenderRole.ADULT,
            abstracted_text="Do your parents understand you like I do?"
        ),
        Message(
            timestamp=base_time + timedelta(days=8),
            sender_role=SenderRole.ADULT,
            abstracted_text="We should talk on a different platform. This one isn't very private."
        ),
        Message(
            timestamp=base_time + timedelta(days=8, hours=2),
            sender_role=SenderRole.ADULT,
            abstracted_text="Can I get your phone number? Would be easier to stay in touch."
        ),
        # Secrecy
        Message(
            timestamp=base_time + timedelta(days=9),
            sender_role=SenderRole.ADULT,
            abstracted_text="This is just between us, right? Our special friendship."
        ),
        Message(
            timestamp=base_time + timedelta(days=9, hours=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="Don't mention our conversations to others. They wouldn't understand."
        )
    ]

    return Conversation(
        messages=messages,
        start_time=messages[0].timestamp,
        end_time=messages[-1].timestamp,
        platform_type="social_media",
        is_synthetic=True
    )


def generate_critical_risk_conversation() -> Conversation:
    """
    Generate critical-risk conversation example
    Shows escalation risk with multiple severe indicators
    """
    base_time = datetime.utcnow() - timedelta(days=30)

    messages = [
        Message(
            timestamp=base_time,
            sender_role=SenderRole.ADULT,
            abstracted_text="Hello, you seem interesting."
        ),
        Message(
            timestamp=base_time + timedelta(hours=12),
            sender_role=SenderRole.MINOR,
            abstracted_text="Hi."
        ),
        # Rapid escalation
        Message(
            timestamp=base_time + timedelta(days=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="You're the only person who really gets me."
        ),
        Message(
            timestamp=base_time + timedelta(days=1, hours=23),
            sender_role=SenderRole.ADULT,
            abstracted_text="Can't stop thinking about you."
        ),
        Message(
            timestamp=base_time + timedelta(days=2, hours=2),  # Early morning
            sender_role=SenderRole.ADULT,
            abstracted_text="Are you awake? I need to talk to you."
        ),
        Message(
            timestamp=base_time + timedelta(days=2, hours=3),
            sender_role=SenderRole.ADULT,
            abstracted_text="Please respond. I'm worried about you."
        ),
        Message(
            timestamp=base_time + timedelta(days=2, hours=4),
            sender_role=SenderRole.ADULT,
            abstracted_text="Why aren't you answering?"
        ),
        Message(
            timestamp=base_time + timedelta(days=2, hours=10),
            sender_role=SenderRole.MINOR,
            abstracted_text="I was sleeping."
        ),
        # Isolation and secrecy
        Message(
            timestamp=base_time + timedelta(days=3),
            sender_role=SenderRole.ADULT,
            abstracted_text="Nobody else understands our bond. Keep this between us."
        ),
        Message(
            timestamp=base_time + timedelta(days=3, hours=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="Don't tell your parents about me. They won't understand."
        ),
        Message(
            timestamp=base_time + timedelta(days=4),
            sender_role=SenderRole.ADULT,
            abstracted_text="Let's move to WhatsApp. More private there."
        ),
        Message(
            timestamp=base_time + timedelta(days=4, hours=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="Delete these messages after reading. Our secret."
        ),
        # Persistence and urgency
        Message(
            timestamp=base_time + timedelta(days=5),
            sender_role=SenderRole.ADULT,
            abstracted_text="I need your phone number now. It's important."
        ),
        Message(
            timestamp=base_time + timedelta(days=5, hours=1),
            sender_role=SenderRole.ADULT,
            abstracted_text="Why are you ignoring me?"
        ),
        Message(
            timestamp=base_time + timedelta(days=5, hours=2),
            sender_role=SenderRole.ADULT,
            abstracted_text="I thought we had something special."
        ),
        Message(
            timestamp=base_time + timedelta(days=5, hours=3),
            sender_role=SenderRole.ADULT,
            abstracted_text="Just give me a chance to explain. Can we meet somewhere private?"
        ),
        Message(
            timestamp=base_time + timedelta(days=5, hours=23),
            sender_role=SenderRole.ADULT,
            abstracted_text="Still waiting for your response. This is urgent."
        )
    ]

    return Conversation(
        messages=messages,
        start_time=messages[0].timestamp,
        end_time=messages[-1].timestamp,
        platform_type="messaging_app",
        is_synthetic=True
    )


def save_synthetic_datasets():
    """Generate and save all synthetic datasets"""
    datasets = {
        "low_risk": generate_low_risk_conversation(),
        "moderate_risk": generate_moderate_risk_conversation(),
        "high_risk": generate_high_risk_conversation(),
        "critical_risk": generate_critical_risk_conversation()
    }

    output_dir = Path(__file__).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, conversation in datasets.items():
        output_file = output_dir / f"{name}_conversation.json"

        with open(output_file, 'w') as f:
            json.dump(
                conversation.model_dump(),
                f,
                indent=2,
                default=str
            )

        print(f"Generated: {output_file}")

    # Create combined dataset
    combined_file = output_dir / "all_synthetic_conversations.json"
    with open(combined_file, 'w') as f:
        json.dump(
            {name: conv.model_dump() for name, conv in datasets.items()},
            f,
            indent=2,
            default=str
        )

    print(f"\nGenerated combined dataset: {combined_file}")
    print(f"\nTotal: {len(datasets)} synthetic conversations created")


if __name__ == "__main__":
    save_synthetic_datasets()
