"""CLI for thought-rollback-coordinator."""
import sys
import argparse
from .coordinator import ThoughtRollbackCoordinator

def main():
    parser = argparse.ArgumentParser(description="Thought Rollback Coordinator CLI")
    parser.add_argument("--demo", action="store_true", help="Simulate action recording and rollback")
    args = parser.parse_args()

    if args.demo:
        coord = ThoughtRollbackCoordinator()
        state = {"files": []}
        coord.begin_transaction("tx_build")
        state["files"].append("step1.py")
        coord.record_action("create_step1", lambda: state["files"].remove("step1.py") is None)
        print(f"State before rollback: {state}")
        reverted = coord.rollback()
        print(f"Reverted actions: {reverted}")
        print(f"State after rollback: {state}")
    else:
        parser.print_help()
    sys.exit(0)

if __name__ == "__main__":
    main()
