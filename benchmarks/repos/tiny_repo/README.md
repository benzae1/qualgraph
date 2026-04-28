# tiny_repo

Small benchmark repository for qualgraph. It is intentionally ordinary rather
than clever: a tiny order-processing package with enough modules, call edges,
branches, and tests to exercise graph construction, metrics, and future
annotators.

The code contains a few realistic rough edges on purpose:

- policy-heavy pricing logic
- service classes that call across modules
- low-level utility functions used from several places
- partial test coverage
- enough branching to give complexity annotators something to see
