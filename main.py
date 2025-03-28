"""
Console-Based Social App - Object-Oriented Version
Author: Nazmul Mustufa Farooquee
Date: 2025-03-28

Features:
1. Posting Messages
2. Reading Timelines
3. Following Users
4. Viewing Combined Wall
5. Input Validation
6. OOP Design with Class-Based Structure
"""

from typing import Dict, List, Tuple
from datetime import datetime
import json
import os


class SocialApp:
    """A console-based social networking app using OOP principles."""

    def __init__(self):
        self.user_messages: Dict[str, List[Tuple[datetime, str]]] = {}
        self.user_follows: Dict[str, List[str]] = {}

    def load_data(self) -> None:
        """Load all messages and follow data from JSON files."""
        if os.path.exists("messages.json"):
            with open("messages.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                for user, posts in data.items():
                    self.user_messages[user] = [
                        (datetime.fromisoformat(ts), msg) for ts, msg in posts
                    ]

        if os.path.exists("follows.json"):
            with open("follows.json", "r", encoding="utf-8") as f:
                self.user_follows = json.load(f)

    def save_data(self) -> None:
        """Save all user messages and follow data to JSON files."""
        with open("messages.json", "w", encoding="utf-8") as f:
            json.dump({
                user: [(ts.isoformat(), msg) for ts, msg in posts]
                for user, posts in self.user_messages.items()
            }, f)

        with open("follows.json", "w", encoding="utf-8") as f:
            json.dump(self.user_follows, f)

    def handle_posting(self, user: str, message: str) -> None:
        """Add a post for a user."""
        if not user.strip() or not message.strip():
            return

        self.user_messages.setdefault(user, [])
        self.user_messages[user].append((datetime.now(), message))
        print(f"✅ {user} posted: '{message}'")

    def handle_reading(self, user: str) -> None:
        """Display timeline of a specific user."""
        if user not in self.user_messages:
            print(f"ℹ️ No posts found for {user}.")
            return

        print(f"\n📜 {user}'s timeline:")
        for timestamp, message in reversed(self.user_messages[user]):
            elapsed = datetime.now() - timestamp
            minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
            date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{date_str}] {minutes}m {seconds}s ago ➜ {message}")

    def handle_following(self, follower: str, followee: str) -> None:
        """Allow one user to follow another."""
        if (
            not follower.strip() or
            not followee.strip() or
            follower == followee
        ):
            return

        self.user_follows.setdefault(follower, [])

        if followee not in self.user_follows[follower]:
            self.user_follows[follower].append(followee)
            print(f"🔗 {follower} now follows {followee}")
        else:
            print(f"ℹ️ {follower} already follows {followee}")

    def show_wall(self, user: str) -> None:
        """Display a combined wall of messages for
        the user and people they follow."""
        all_posts: List[Tuple[datetime, str, str]] = []

        followed_users = [user] + self.user_follows.get(user, [])
        for followed_user in followed_users:
            for ts, msg in self.user_messages.get(followed_user, []):
                all_posts.append((ts, msg, followed_user))

        if not all_posts:
            print(f"ℹ️ No posts found for {user}.")
            return

        all_posts.sort(reverse=True)
        print(f"\n🧱 {user}'s wall:")

        for timestamp, message, author in all_posts:
            elapsed = datetime.now() - timestamp
            minutes, seconds = divmod(int(elapsed.total_seconds()), 60)
            date_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            print(
                f"[{date_str}] {minutes}m {seconds}s ago "
                f"[{author}] ➜ {message}"
            )

    def run(self):
        """Main interactive loop."""
        self.load_data()

        print("\n📘 Welcome to the Console Social App!")
        print("Type messages like: Alice -> Hello")
        print("Type 'Alice' to read the timeline.")
        print("Type 'Alice follows Bob' to follow someone.")
        print("Type your own name to view your wall.")
        print("Type 'exit' to leave the app.\n")

        while True:
            command = input("💬 Your input: ").strip()

            if command.lower() == "exit":
                print("👋 Exiting. Goodbye!")
                self.save_data()
                break

            elif "->" in command:
                username, content = command.split("->")
                self.handle_posting(username.strip(), content.strip())

            elif "follows" in command:
                parts = command.split("follows")
                self.handle_following(parts[0].strip(), parts[1].strip())

            elif (
                command in self.user_messages or
                command in self.user_follows
            ):
                self.show_wall(command)

            else:
                self.handle_reading(command)


if __name__ == "__main__":
    app = SocialApp()
    app.run()
