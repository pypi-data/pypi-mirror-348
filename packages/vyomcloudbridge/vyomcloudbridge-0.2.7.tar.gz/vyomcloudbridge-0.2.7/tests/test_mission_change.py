# mission_start_example.py

import sys
import signal
import threading

from vyomcloudbridge.services.mission_stats import MissionStats


def setup_signal_handlers(obj):
    """Setup signal handlers for graceful shutdown (must be called from main thread)."""
    if threading.current_thread() is not threading.main_thread():
        print("Signal handlers must be set in the main thread. Skipping setup.")
        return

    def signal_handler(sig, frame):
        print(f"Received signal {sig}. Shutting down {obj.__class__.__name__}...")
        obj.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


def main():
    # Initialize MissionStats in main thread
    mission_stats = MissionStats()

    # Set up signal handlers in main thread
    setup_signal_handlers(mission_stats)
    
    success, error = mission_stats.end_current_mission()

    # Start a new mission
    mission_detail, error = mission_stats.start_mission(
        id=287463824444,                         # Optional: Unique mission ID
        name="optional_human_readable_name",     # Optional: Defaults to timestamp-based name
        description="Description of mission",    # Optional
        creator_id=1,                             # Recommended: user_id of the initiator
        owner_id=101                              # Optional: Defaults to creator_id
    )

    if error:
        print("Failed to start mission:", error)
    else:
        print("Mission started successfully:", mission_detail)


if __name__ == "__main__":
    main()
