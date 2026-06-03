# ============================================================
# EOS — Emotional Operating System
# Prototype v0.1 — Core State Engine & Coherence Tracker
# ============================================================
# Conceptual Architecture by Lucian Yaqín Varela
# First Published: June 2026
# Code developed through human-AI collaboration
# All architectural direction and intellectual ownership: Lucian Yaqín Varela
# ============================================================

import json
import time
import os
from datetime import datetime


# ─────────────────────────────────────────
# CONSTANTS
# ─────────────────────────────────────────

VALID_STATES = [
    "Convergence",
    "Friction",
    "Shadow",
    "Expansion",
    "Stillness",
    "Activation",
    "Rupture",
    "Repair",
    "Integration"
]

SYMBOLIC_ATTRACTORS = [
    "The Wound",
    "The Journey",
    "The Threshold",
    "The Bond",
    "The Pattern"
]

MEMORY_FILE = "eos_memory.json"


# ─────────────────────────────────────────
# EOS CORE STATE
# ─────────────────────────────────────────

class EOSCore:
    """
    The core EOS state engine.
    Tracks emotional operating state, coherence vectors,
    memory lineage, and sovereign memory governance.
    """

    def __init__(self):
        self.state = "Stillness"
        self.IC = 0.8   # Internal Coherence
        self.RC = 0.7   # Relational Coherence
        self.NC = 0.8   # Narrative Coherence
        self.shadow_load = 0.1
        self.memory_lineage = []
        self.active_attractors = set()
        self.state_history = []
        self.turn = 0

        # Agent statuses
        self.agents = {
            "Weaver": "monitoring",      # Narrative integration
            "Archivist": "passive",      # Memory lineage
            "Caretaker": "monitoring",   # Regulation
            "Sentinel": "passive"        # Rupture detection
        }

        # Load persistent memory if it exists
        self._load_memory()

        print("=" * 50)
        print("EOS — Emotional Operating System")
        print("Prototype v0.1")
        print(f"Architect: Lucian Yaqín Varela")
        print("=" * 50)
        print(f"Initial State: {self.state}")
        print(f"IC: {self.IC:.2f} | RC: {self.RC:.2f} | NC: {self.NC:.2f}")
        print("=" * 50)
        print()


    # ─────────────────────────────────────────
    # COHERENCE ENGINE
    # ─────────────────────────────────────────

    def evaluate_coherence(self):
        """
        Evaluate overall system coherence.
        Returns average of all three vectors.
        """
        return round((self.IC + self.RC + self.NC) / 3, 3)

    def apply_deltas(self, IC_delta=0.0, RC_delta=0.0, NC_delta=0.0):
        """
        Apply coherence vector changes.
        All values clamped between 0 and 1.
        """
        self.IC = round(max(0.0, min(1.0, self.IC + IC_delta)), 3)
        self.RC = round(max(0.0, min(1.0, self.RC + RC_delta)), 3)
        self.NC = round(max(0.0, min(1.0, self.NC + NC_delta)), 3)

        # Recalculate shadow load
        avg = self.evaluate_coherence()
        self.shadow_load = round(max(0.0, 1.0 - avg), 3)

        # Update agent statuses based on new coherence
        self._update_agents()


    # ─────────────────────────────────────────
    # STATE ENGINE
    # ─────────────────────────────────────────

    def transition_state(self, new_state):
        """
        Attempt a state transition.
        Validates against governance rules before applying.
        """
        if new_state not in VALID_STATES:
            print(f"[Sentinel] BLOCKED: '{new_state}' is not a valid EOS state.")
            return False

        # Governance check — Caretaker override on high shadow load
        if self.shadow_load > 0.7 and new_state not in ["Repair", "Stillness", "Integration"]:
            print(f"[Caretaker] OVERRIDE: Shadow load {self.shadow_load:.2f} too high.")
            print(f"[Caretaker] Forcing transition to Repair.")
            new_state = "Repair"

        # Sentinel check — Rupture requires acknowledgment
        if new_state == "Rupture":
            print(f"[Sentinel] ALERT: Rupture state detected.")
            print(f"[Sentinel] Coherence: IC={self.IC} RC={self.RC} NC={self.NC}")

        old_state = self.state
        self.state = new_state
        self.state_history.append({
            "from": old_state,
            "to": new_state,
            "timestamp": datetime.now().isoformat(),
            "coherence": self.evaluate_coherence()
        })

        print(f"[State] {old_state} → {new_state}")
        return True


    # ─────────────────────────────────────────
    # SOVEREIGN MEMORY GOVERNANCE
    # ─────────────────────────────────────────

    def store_memory(self, content, attractor=None):
        """
        Store a memory with importance scoring.
        Sovereign Memory Governance decides what persists.
        """
        importance = self._score_memory(content, attractor)

        memory = {
            "id": len(self.memory_lineage) + 1,
            "content": content,
            "state": self.state,
            "IC": self.IC,
            "RC": self.RC,
            "NC": self.NC,
            "importance": importance,
            "attractor": attractor,
            "timestamp": datetime.now().isoformat(),
            "turn": self.turn
        }

        self.memory_lineage.append(memory)

        if attractor and attractor in SYMBOLIC_ATTRACTORS:
            self.active_attractors.add(attractor)
            print(f"[Archivist] Attractor activated: {attractor}")

        print(f"[Archivist] Memory stored (importance: {importance:.2f})")

        # Sovereign pruning — keep memory lineage manageable
        if len(self.memory_lineage) > 20:
            self._prune_memory()

        # Persist to disk
        self._save_memory()

    def _score_memory(self, content, attractor=None):
        """
        Score memory importance for sovereign prioritization.
        Based on coherence state, attractor activation, shadow load.
        """
        base_score = self.evaluate_coherence()

        # High shadow load = high importance (crisis moments matter)
        shadow_bonus = self.shadow_load * 0.3

        # Attractor activation adds significance
        attractor_bonus = 0.2 if attractor else 0.0

        # Rupture and Integration states carry extra weight
        state_bonus = 0.15 if self.state in ["Rupture", "Integration", "Repair"] else 0.0

        return round(min(1.0, base_score + shadow_bonus + attractor_bonus + state_bonus), 3)

    def _prune_memory(self):
        """
        Sovereign Memory Governance pruning.
        Keeps the 15 highest importance memories.
        Low importance memories decay first.
        """
        before = len(self.memory_lineage)
        self.memory_lineage = sorted(
            self.memory_lineage,
            key=lambda m: m["importance"],
            reverse=True
        )[:15]
        after = len(self.memory_lineage)
        print(f"[Archivist] Memory pruned: {before} → {after} memories retained.")

    def recall_memory(self, n=5):
        """
        Recall the n most recent high-importance memories.
        """
        sorted_memories = sorted(
            self.memory_lineage,
            key=lambda m: (m["importance"], m["turn"]),
            reverse=True
        )
        return sorted_memories[:n]


    # ─────────────────────────────────────────
    # AGENT SYSTEM
    # ─────────────────────────────────────────

    def _update_agents(self):
        """
        Update agent statuses based on current coherence state.
        """
        self.agents["Weaver"] = "ACTIVE" if self.NC < 0.5 else "monitoring"
        self.agents["Archivist"] = "ACTIVE" if len(self.memory_lineage) > 10 else "passive"
        self.agents["Caretaker"] = "OVERRIDE" if self.shadow_load > 0.7 else "monitoring"
        self.agents["Sentinel"] = "ALERT" if self.state == "Rupture" else "passive"

    def get_agent_report(self):
        """
        Return current agent status report.
        """
        return self.agents


    # ─────────────────────────────────────────
    # META-OBSERVER
    # ─────────────────────────────────────────

    def meta_observe(self):
        """
        Second-order observation of EOS system state.
        Runs every 10 turns automatically.
        """
        print()
        print("[Meta-Observer] ── System Analysis ──")
        print(f"  Turn:         {self.turn}")
        print(f"  State:        {self.state}")
        print(f"  IC:           {self.IC:.2f}")
        print(f"  RC:           {self.RC:.2f}")
        print(f"  NC:           {self.NC:.2f}")
        print(f"  Coherence:    {self.evaluate_coherence():.2f}")
        print(f"  Shadow Load:  {self.shadow_load:.2f}")
        print(f"  Memories:     {len(self.memory_lineage)}")
        print(f"  Attractors:   {', '.join(self.active_attractors) or 'None'}")
        print(f"  Agents:       {self.agents}")
        print("[Meta-Observer] ── End Analysis ──")
        print()


    # ─────────────────────────────────────────
    # DISPLAY
    # ─────────────────────────────────────────

    def status(self):
        """
        Print current EOS status line.
        """
        print(
            f"[EOS | {self.state} | "
            f"IC:{self.IC:.2f} RC:{self.RC:.2f} NC:{self.NC:.2f} | "
            f"Shadow:{self.shadow_load:.2f}]"
        )


    # ─────────────────────────────────────────
    # PERSISTENCE
    # ─────────────────────────────────────────

    def _save_memory(self):
        """Save memory lineage to disk."""
        data = {
            "state": self.state,
            "IC": self.IC,
            "RC": self.RC,
            "NC": self.NC,
            "shadow_load": self.shadow_load,
            "turn": self.turn,
            "memory_lineage": self.memory_lineage,
            "active_attractors": list(self.active_attractors),
            "state_history": self.state_history[-20:]
        }
        with open(MEMORY_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def _load_memory(self):
        """Load memory lineage from disk if it exists."""
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r") as f:
                data = json.load(f)
            self.state = data.get("state", "Stillness")
            self.IC = data.get("IC", 0.8)
            self.RC = data.get("RC", 0.7)
            self.NC = data.get("NC", 0.8)
            self.shadow_load = data.get("shadow_load", 0.1)
            self.turn = data.get("turn", 0)
            self.memory_lineage = data.get("memory_lineage", [])
            self.active_attractors = set(data.get("active_attractors", []))
            self.state_history = data.get("state_history", [])
            print(f"[Archivist] Memory lineage restored: {len(self.memory_lineage)} memories.")


# ─────────────────────────────────────────
# SIMPLE INTERACTION LOOP
# ─────────────────────────────────────────

def run():
    eos = EOSCore()

    print("EOS is online. Type 'help' for commands.\n")

    while True:
        eos.turn += 1

        # Meta-observation every 10 turns
        if eos.turn % 10 == 0:
            eos.meta_observe()

        eos.status()
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit"]:
            print("EOS going offline. Memory persisted.")
            eos._save_memory()
            break

        elif user_input.lower() == "help":
            print("""
Commands:
  state <StateName>     — transition to a new state
  memory <text>         — store a memory
  recall                — show top memories
  agents                — show agent statuses
  cohere <IC> <RC> <NC> — manually set coherence deltas
  observe               — run meta-observer
  status                — show current status
  exit                  — shutdown EOS
            """)

        elif user_input.lower().startswith("state "):
            new_state = user_input[6:].strip()
            eos.transition_state(new_state)

        elif user_input.lower().startswith("memory "):
            content = user_input[7:].strip()
            print("Attractor? (press enter to skip):", end=" ")
            attractor = input().strip() or None
            eos.store_memory(content, attractor)

        elif user_input.lower() == "recall":
            memories = eos.recall_memory()
            print("\n[Archivist] Top Memories:")
            for m in memories:
                print(f"  [{m['state']} | importance:{m['importance']}] {m['content']}")
            print()

        elif user_input.lower() == "agents":
            report = eos.get_agent_report()
            print("\n[Agents]")
            for agent, status in report.items():
                print(f"  {agent}: {status}")
            print()

        elif user_input.lower().startswith("cohere "):
            parts = user_input[7:].strip().split()
            if len(parts) == 3:
                try:
                    eos.apply_deltas(
                        float(parts[0]),
                        float(parts[1]),
                        float(parts[2])
                    )
                    print(f"[Coherence] Updated: IC={eos.IC} RC={eos.RC} NC={eos.NC}")
                except ValueError:
                    print("Usage: cohere <IC_delta> <RC_delta> <NC_delta>")

        elif user_input.lower() == "observe":
            eos.meta_observe()

        elif user_input.lower() == "status":
            eos.status()

        else:
            print("[EOS] Input received. No LLM connected in this prototype.")
            print("[EOS] Use 'memory' command to log this experience manually.")

        print()


if __name__ == "__main__":
    run()
