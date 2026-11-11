"""Core Thought Rollback Coordinator implementation."""
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

@dataclass
class ActionRecord:
    name: str
    forward_desc: str
    inverse_fn: Callable[[], bool]
    executed: bool = True

class ThoughtRollbackCoordinator:
    """Provides transactional undo capabilities for multi-step agent scratchpad actions."""
    
    def __init__(self):
        self.transactions: Dict[str, List[ActionRecord]] = {}
        self.active_tx: Optional[str] = None

    def begin_transaction(self, tx_name: str) -> None:
        self.transactions[tx_name] = []
        self.active_tx = tx_name

    def record_action(self, forward_desc: str, inverse_fn: Callable[[], bool]) -> None:
        if not self.active_tx:
            raise RuntimeError("No active transaction to record action in")
        record = ActionRecord(name=forward_desc, forward_desc=forward_desc, inverse_fn=inverse_fn)
        self.transactions[self.active_tx].append(record)

    def rollback(self, tx_name: Optional[str] = None) -> List[str]:
        target = tx_name or self.active_tx
        if not target or target not in self.transactions:
            return []

        actions = self.transactions[target]
        reverted = []
        # Revert in reverse order (LIFO)
        for act in reversed(actions):
            try:
                success = act.inverse_fn()
                if success:
                    reverted.append(act.name)
            except Exception:
                pass

        del self.transactions[target]
        if self.active_tx == target:
            self.active_tx = None
        return reverted

    def commit(self, tx_name: Optional[str] = None) -> None:
        target = tx_name or self.active_tx
        if target and target in self.transactions:
            del self.transactions[target]
        if self.active_tx == target:
            self.active_tx = None
