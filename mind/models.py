from dataclasses import dataclass, field


@dataclass(frozen=True)
class Belief:
    topic: str
    summary: str
    opinion: str


@dataclass(frozen=True)
class Thought:
    topic: str
    reason: str
    opinion: str


@dataclass(frozen=True)
class CurrentState:
    focus: str | None
    beliefs: tuple[Belief, ...] = ()
    thoughts: tuple[Thought, ...] = ()