"""IT Helpdesk Ticket Allocator.

Manage helpdesk tickets, assign technicians, add notes, and save tickets.
"""

import ipaddress
from itertools import count
import json
import os
import re
import subprocess
from datetime import datetime

# Global state
tickets = {}
TICKET_COUNTER = count(101)
ADMIN_PASSWORD = os.getenv("HELPDESK_ADMIN_PASSWORD")


def raise_ticket(user, issue_type, urgency="3", audit_trail=None):
    """Create a ticket after validating its urgency."""

    try:
        priority = int(urgency)
    except (TypeError, ValueError) as exc:
        raise ValueError("Urgency must be an integer from 1 to 5.") from exc

    if not 1 <= priority <= 5:
        raise ValueError("Urgency must be between 1 and 5.")

    if audit_trail is None:
        audit_trail = []

    ticket_id = next(TICKET_COUNTER)

    tickets[ticket_id] = {
        "user": user,
        "issue": issue_type,
        "priority": priority,
        "tech": None,
        "notes": [],
    }

    audit_trail.append(
        f"{user} raised #{ticket_id} at {datetime.now().isoformat()}"
    )
    return ticket_id


def assign_ticket(ticket_id, technician):
    """Assign an existing ticket to a technician."""
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")

    tickets[ticket_id]["tech"] = technician


def add_note(ticket_id, note):
    """Add a note to an existing ticket."""
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")

    tickets[ticket_id]["notes"].append(note)


def close_ticket(ticket_id, password):
    """Close an existing ticket after administrator authentication."""
    if ticket_id not in tickets:
        raise KeyError(f"Ticket {ticket_id} does not exist.")

    if not ADMIN_PASSWORD:
        raise RuntimeError(
            "Administrator password is not configured. "
            "Set HELPDESK_ADMIN_PASSWORD before closing tickets."
        )

    if password != ADMIN_PASSWORD:
        raise PermissionError("Incorrect administrator password.")

    del tickets[ticket_id]


def unresolved_high_priority():
    """Return IDs of unassigned tickets with priority 4 or 5."""
    return [
        ticket_id
        for ticket_id, ticket in tickets.items()
        if ticket["priority"] >= 4 and ticket["tech"] is None
    ]


def ping_user_machine(hostname):
    """Ping a valid hostname or IP address without invoking a shell."""
    if not isinstance(hostname, str) or not hostname:
        raise ValueError("A valid hostname or IP address is required.")

    try:
        ipaddress.ip_address(hostname)
    except ValueError as exc:
        if (
            len(hostname) > 253
            or not re.fullmatch(
                r"[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?",
                hostname,
            )
            or ".." in hostname
        ):
            raise ValueError(
                "Invalid hostname or IP address."
            ) from exc

    return subprocess.run(
        ["ping", "-n", "1", hostname],
        check=False,
        shell=False,
        capture_output=True,
        text=True,
        timeout=5,
    ).returncode


def save_tickets(file="tickets.json"):
    """Save all tickets as JSON using UTF-8 encoding."""
    with open(file, "w", encoding="utf-8") as ticket_file:
        json.dump(tickets, ticket_file, indent=4)


def main():
    """Run a demonstration of the helpdesk ticket allocator."""
    audit_trail = []

    ticket_one = raise_ticket("anil", "printer", "5", audit_trail)
    ticket_two = raise_ticket("meera", "wifi", "4", audit_trail)
    ticket_three = raise_ticket("joe", "vpn", "3", audit_trail)

    assign_ticket(ticket_one, "Tech-Kiran")
    add_note(ticket_one, "Called user")

    print("Unassigned high priority:", unresolved_high_priority())

    urgency = input(
        "Urgency for a new laptop ticket (1-5, Enter for 3): "
    ).strip() or "3"

    try:
        raise_ticket("sana", "laptop", urgency, audit_trail)
    except ValueError as exc:
        print(f"Ticket not created: {exc}")

    if ADMIN_PASSWORD:
        try:
            close_ticket(ticket_three, ADMIN_PASSWORD)
        except (KeyError, PermissionError, RuntimeError) as exc:
            print(f"Could not close ticket: {exc}")
    else:
        print(
            "Ticket not closed: configure HELPDESK_ADMIN_PASSWORD "
            "to enable administrator authentication."
        )

    save_tickets()
    print("Open tickets:", list(tickets.keys()))
    print("Audit entries:", len(audit_trail))
    print("Second ticket ID:", ticket_two)


if __name__ == "__main__":
    main()
