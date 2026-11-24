---
name: codebase-design
description: Design deep module interfaces and seams. Use when shaping a module interface, collapsing thin layers, deciding where a seam goes, or comparing candidate interfaces.
---

# Codebase Design

Design module boundaries that concentrate complexity behind small interfaces, keep caller-owned costs explicit, and serve real production callers.

## Vocabulary

- **Module**: a cohesive code boundary with a public interface (a file, subsystem, or cross-layer slice).
- **Interface**: everything a caller must know to use a module correctly: types and signatures, invariants, ordering constraints, error modes, resource lifetimes, and performance characteristics.
- **Depth**: combining **leverage** (callers learn little to accomplish much, regardless of call-site count) and **locality** (related logic, state transitions, and changes stay in one place instead of scattering across files), distinguishing a **deep** module from a **shallow** pass-through.
- **Seam**: a cut point where behavior can vary (swapping implementations or adapters) without editing callers.
- **Adapter**: a concrete implementation that satisfies an interface at a seam.

## Boundary and depth rules

- **Weigh depth against net gain.** Weigh depth alongside correctness, runtime cost, and explicit resource control. Keep costs that callers must govern (memory allocation, synchronization, ownership, resource lifetimes, hardware or protocol state) explicit in the interface.
- **Keep cross-module boundaries strict and internals linear.** Public interfaces carry durable contracts and cross-file navigation cost. Inside a module, prefer self-contained linear flow over single-use helper fragments; extract a private helper only for real reuse or to isolate a distinct complex sub-stage.
- **Apply the deletion test to thin layers.** Imagine removing the module or wrapper. Collapse or delete it when complexity disappears or consolidates, unless it prevents duplication across callers or provides one of two single-call-site guarantees:
  1. **Type or invariant wrappers** that encode a validated or normalized guarantee in the type system so invalid states cannot pass downstream.
  2. **External isolation layers** that quarantine volatile third-party libraries or external protocols.

## Seam placement

Introduce a public seam (an abstract interface or port) only when multiple production implementations genuinely vary across it, or at a genuine remote or external I/O or ownership boundary. Keep internal seams private.

Place seams by dependency category:

- **In-process** (pure logic, in-memory state, no I/O): merge directly behind the module's interface with no port or adapter.
- **Local-substitutable** (dependencies with faithful local instances such as an embedded database or temp directory): use the concrete dependency directly inside the module via normal production configuration, with no abstract port on the public interface.
- **Remote but owned** (your own services across a network or process boundary): place a port at the transport seam so domain logic stays deep while production transport and local stand-in adapters swap cleanly.
- **True external** (third-party services or hardware APIs you do not control): isolate behind a narrow injected port and adapter at the external boundary.

## Comparing candidate interfaces

When the user asks to compare interface options, or when designing a cross-module boundary with multiple callers or high rework cost, read [DESIGN-IT-TWICE.md](DESIGN-IT-TWICE.md).
