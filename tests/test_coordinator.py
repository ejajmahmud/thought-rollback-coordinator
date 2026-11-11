"""Unit tests for thought-rollback-coordinator."""
import unittest
from thought_rollback_coordinator.coordinator import ThoughtRollbackCoordinator

class TestThoughtRollbackCoordinator(unittest.TestCase):
    def setUp(self):
        self.coord = ThoughtRollbackCoordinator()

    def test_lifo_rollback(self):
        log = []
        self.coord.begin_transaction("tx1")
        self.coord.record_action("act1", lambda: log.append("undo_1") or True)
        self.coord.record_action("act2", lambda: log.append("undo_2") or True)

        reverted = self.coord.rollback()
        self.assertEqual(reverted, ["act2", "act1"])
        self.assertEqual(log, ["undo_2", "undo_1"])

    def test_commit_clears_transaction(self):
        self.coord.begin_transaction("tx2")
        self.coord.record_action("act", lambda: True)
        self.coord.commit()
        reverted = self.coord.rollback("tx2")
        self.assertEqual(reverted, [])
