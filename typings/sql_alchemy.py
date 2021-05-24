from typing import Any
from flask_sqlalchemy import SQLAlchemy as SQLAlchemyBase, Model as ModelBase


class QueryModel:
    add_column: Any = ...
    add_columns: Any = ...
    add_entity: Any = ...
    all: Any = ...
    apply_labels: Any = ...
    as_scalar: Any = ...
    autoflush: Any = ...
    correlate: Any = ...
    count: Any = ...
    cte: Any = ...
    delete: Any = ...
    distinct: Any = ...
    enable_assertions: Any = ...
    enable_eagerloads: Any = ...
    except_: Any = ...
    except_all: Any = ...
    execute: Any = ...
    execution_options: Any = ...
    exists: Any = ...
    filter: Any = ...
    filter_by: Any = ...
    first: Any = ...
    first_or_404: Any = ...
    from_self: Any = ...
    from_statement: Any = ...
    get: Any = ...
    get_execution_options: Any = ...
    get_or_404: Any = ...
    group_by: Any = ...
    having: Any = ...
    instances: Any = ...
    intersect: Any = ...
    intersect_all: Any = ...
    join: Any = ...
    label: Any = ...
    limit: Any = ...
    load_options: Any = ...
    memoized_attribute: Any = ...
    memoized_instancemethod: Any = ...
    merge_result: Any = ...
    offset: Any = ...
    one: Any = ...
    one_or_none: Any = ...
    only_return_tuples: Any = ...
    options: Any = ...
    order_by: Any = ...
    outerjoin: Any = ...
    paginate: Any = ...
    params: Any = ...
    populate_existing: Any = ...
    prefix_with: Any = ...
    reset_joinpoint: Any = ...
    scalar: Any = ...
    scalar_subquery: Any = ...
    select_entity_from: Any = ...
    select_from: Any = ...
    set_label_style: Any = ...
    slice: Any = ...
    subquery: Any = ...
    suffix_with: Any = ...
    union: Any = ...
    union_all: Any = ...
    update: Any = ...
    value: Any = ...
    values: Any = ...
    where: Any = ...
    with_entities: Any = ...
    with_for_update: Any = ...
    with_hint: Any = ...
    with_labels: Any = ...
    with_parent: Any = ...
    with_polymorphic: Any = ...
    with_session: Any = ...
    with_statement_hint: Any = ...
    with_transformation: Any = ...
    yield_per: Any = ...


class SQLAlchemy(SQLAlchemyBase):
    class Model(ModelBase):
        query: QueryModel

    Column: Any = ...
    ForeignKey: Any = ...
    relationship: Any = ...
    backref: Any = ...

    BigInteger: Any = ...
    Boolean: Any = ...
    Date: Any = ...
    DateTime: Any = ...
    Enum: Any = ...
    Float: Any = ...
    Integer: Any = ...
    Interval: Any = ...
    LargeBinary: Any = ...
    MatchType: Any = ...
    Numeric: Any = ...
    PickleType: Any = ...
    SchemaType: Any = ...
    SmallInteger: Any = ...
    String: Any = ...
    Text: Any = ...
    Time: Any = ...
    Unicode: Any = ...
    UnicodeText: Any = ...
