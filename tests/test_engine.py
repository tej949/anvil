from adapters.mine import Engine

from benchmark.generator import (
    generate,
    GenConfig
)


def test_engine_ingestion():

    cfg = GenConfig(
        seed=42,
        n_services=4,
        days=2
    )

    dataset = generate(cfg)

    engine = Engine()

    engine.ingest(
        dataset.train_events
    )

    engine.ingest(
        dataset.eval_events
    )

    assert len(engine.events) > 0


def test_reconstruct_context():

    cfg = GenConfig(
        seed=42,
        n_services=4,
        days=2
    )

    dataset = generate(cfg)

    engine = Engine()

    engine.ingest(
        dataset.train_events
    )

    engine.ingest(
        dataset.eval_events
    )

    signal = dataset.eval_signals[0]

    context = engine.reconstruct_context(
        signal,
        mode="fast"
    )

    assert isinstance(context, dict)

    assert "related_events" in context

    assert "confidence" in context


def test_topology_resolution():

    cfg = GenConfig(
        seed=101,
        n_services=6,
        days=4
    )

    dataset = generate(cfg)

    engine = Engine()

    engine.ingest(
        dataset.train_events
    )

    topology_events = [
        e for e in dataset.train_events
        if e.get("kind") == "topology"
    ]

    assert len(topology_events) > 0