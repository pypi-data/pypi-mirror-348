from typing import Type

from sqlalchemy import asc, desc, and_, select, func, case
from sqlalchemy.orm import RelationshipDirection

from ..exceptions.error import SQLGenerationException
from .query_parser import (
    SortOrder,
    ActionTree,
    NestedField,
    FilterAction,
    SortAction,
)
from ..services.serialization import BaseSerializer, get_prop_serializer, get_serializer

EXCLUDE_COLUMN_PREFIX = "!"

WILDCARD = "*"


def _debug_query(q):
    """
    This function compiles the given SQLAlchemy query object 'q' using the SQLite dialect
    and prints the resulting SQL query with bound parameters as literals, helpful for debugging
    purposes. It utilizes SQLAlchemy`s 'compile' method with specific compile kwargs to ensure
    the query is compiled with bound parameter values rendered as literals.

    Parameters:
        q (sqlalchemy.sql.expression.Selectable): The SQLAlchemy query object to be debugged.

    Returns:
        None
    """
    from sqlalchemy.dialects import sqlite

    print(q.compile(dialect=sqlite.dialect(), compile_kwargs={"literal_binds": True}))


def _resolve_relationships(
        action: ActionTree, serializer: Type[BaseSerializer], id_field
):
    """
    The _resolve_relationships function is responsible for resolving relationships within an ActionTree,
    retrieving necessary information from the provided serializer, and generating the required SQL expressions
    to handle these relationships.

    Parameters:
        action (type: ActionTree): An instance of the ActionTree class representing the current action and its relations

        serializer (type: Type[BaseSerializer]): A subclass of BaseSerializer representing the serializer associated
        with the model for which relationships are being resolved.

        id_field: The field used as an identifier for the model.

    Returns:
        Tuple: The function returns a tuple containing the following elements:

            _fields: A list of fields to be selected in the SQL query.

            _joins: A list of tuples representing the relationships and associated join conditions.

            sort_field_cte_alias: An optional alias for the sort field's common table expression (CTE).
    """
    _model_inspect = serializer.get_model_inspection()
    _fields = []
    _joins = []
    sort_field_cte_alias = None
    for relation_name, relation_action_tree in action.relations.items():
        relation_src_name = serializer.get_serializer_field(relation_name)
        sql_relation = _model_inspect.relationships[relation_src_name.field]
        rel_serializer = get_prop_serializer(serializer.model, relation_src_name.field)
        _rel_cte = _relation_select(
            relation_action_tree, rel_serializer, serializer.model, sql_relation, action
        )
        if relation_action_tree.select is not None:
            _fields.append(relation_name)
            else_case = None
            match sql_relation.direction:
                case RelationshipDirection.ONETOMANY:
                    else_case = func.json("[]")
                    agg_fn = func.json(_rel_cte.c.obj)
                case RelationshipDirection.MANYTOONE:
                    agg_fn = func.json_extract(_rel_cte.c.obj, "$[0]")
                case RelationshipDirection.MANYTOMANY:
                    else_case = func.json("[]")
                    agg_fn = func.json(_rel_cte.c.obj)
                case _:
                    raise SQLGenerationException(
                        f"Unsupported relation type: {sql_relation.direction}"
                    )
            _fields.append(
                case(
                    (_rel_cte.c.id.is_not(None), agg_fn),
                    else_=else_case,
                )
            )

        # if relation_name == action.sort.field.fields[0]:
        #     sort_field_cte_alias = _rel_cte.alias()
        _joins.append((relation_name, _rel_cte, id_field == _rel_cte.c.id))
    return (
        _fields,
        _joins,
        sort_field_cte_alias,
    )


def _json_query(qo: ActionTree, serializer: Type[BaseSerializer]):
    """
    The _json_query function generates a SQL query for retrieving entities based on the provided ActionTree and
    serializer. It constructs a JSON representation of the selected fields, handles filtering, sorting, and
    relationships, and returns a subquery representing the queried data.

    Parameters:
        qo (ActionTree): An instance of the ActionTree class representing the query options, filters, sorting,
        and relationships for the entities to be retrieved.

        serializer (Type[BaseSerializer]): A subclass of BaseSerializer representing the serializer associated
        with the model for which entities are being queried.

    Returns:
        Subquery: A subquery representing the SQL query for retrieving entities based on the provided qo and serializer.
    """
    _fields = []
    _joins = []
    _hidden_fields_to_select = []
    _exclude_fields = []
    _model_inspect = serializer.get_model_inspection()
    _wild_select = any((_field == "*" for _field in qo.select))
    _field_to_select = []
    if _wild_select:
        _field_to_select = [
            _field
            for _field in serializer.fields
            if _field.field not in _model_inspect.relationships
        ]
    else:
        _field_to_select = [
            serializer.get_serializer_field(field_alias)
            for field_alias in qo.select
            if not field_alias.startswith("!")
        ]

    for _field in qo.select:
        if _field.startswith(EXCLUDE_COLUMN_PREFIX):
            _field_to_select = [
                _field
                for _field in serializer.fields
                if _field.field not in _model_inspect.relationships
            ]
            _field_to_select.remove(serializer.get_serializer_field(_field[1:]))

    for field in _field_to_select:
        _fields.append(field.alias)
        _fields.append(serializer.get_db_field(field.field))
    if "id" not in qo.select:
        _hidden_fields_to_select.append(serializer.get_db_field("id"))
    _filters = []
    _inner_cte: list[str] = []
    for flt_item in qo.filters:
        if isinstance(flt_item.field, NestedField):
            if flt_item.field.fields[0] in qo.relations:
                rel_action = qo.relations[flt_item.field.fields[0]]
            else:
                rel_action = ActionTree()
                rel_action.select = None
                qo.relations[flt_item.field.fields[0]] = rel_action

            rel_action.filters.append(
                FilterAction(
                    field=flt_item.field.shift_down(),
                    op=flt_item.operator,
                    value=flt_item.value,
                )
            )
            _inner_cte.append(flt_item.field.fields[0])
            continue
        _filters.append(
            flt_item.operator(
                serializer.get_db_field(
                    serializer.get_serializer_field(flt_item.field).field
                ),
                flt_item.value,
            )
        )
    rel_fields, _joins, field_order_by = _resolve_relationships(
        qo, serializer, serializer.model.id
    )
    _fields.extend(rel_fields)

    for relation_name, relation_action_tree in qo.relations.items():
        sql_relation = _model_inspect.relationships[relation_name]

        if sql_relation.primaryjoin.left in _model_inspect.columns.values():
            this_id_col = sql_relation.primaryjoin.left
        else:
            this_id_col = sql_relation.primaryjoin.right
        has_child_id_col = this_id_col != serializer.model.id

        if has_child_id_col:
            _hidden_fields_to_select.append(this_id_col)
    obj = func.json_object(*_fields)

    q = select(obj.label("sql_rest"), *_hidden_fields_to_select)

    # In debug, I can get certain anon(dictionary by [] iteration)
    for join in _joins:
        match join:
            case (relation_name, cte, on_clause):
                q = q.join(
                    cte,
                    onclause=on_clause,
                    isouter=relation_name
                            not in _inner_cte,
                )

    if _filters:
        q = q.filter(*_filters)

    if qo.sort is not None:
        field_stack = []
        field_stack.extend(reversed(qo.sort.field.fields))
        model = None
        if len(field_stack) == 1:
            q = q.order_by(
                asc(
                    serializer.get_db_field(
                        serializer.get_serializer_field(qo.sort.field.fields[0]).field
                    )
                )
                if qo.sort.order is not SortOrder.DESC
                else desc(
                    serializer.get_db_field(
                        serializer.get_serializer_field(qo.sort.field.fields[0]).field
                    )
                )
            )
        else:
            while field_stack:
                current_field = field_stack.pop()
                if current_field in qo.relations:
                    if (
                            _model_inspect.relationships[current_field].direction
                            == RelationshipDirection.MANYTOMANY
                    ):
                        field_order = None
                        for join in _joins:
                            match join:
                                case (relation_name, cte, on_clause):
                                    if relation_name == current_field:
                                        field_order = cte.c["field_sort_by"]
                        order_by_clause = (
                            asc(field_order)
                            if qo.sort.order is not SortOrder.DESC
                            else desc(field_order)
                        )
                        q = q.order_by(order_by_clause)
                        break
                    else:
                        serializer_entity = get_serializer(
                            _model_inspect.relationships[
                                qo.sort.field.fields[0]
                            ].entity.entity
                        )

                        db_field = serializer_entity.get_db_field(
                            serializer_entity.get_serializer_field(
                                qo.sort.field.fields[1]
                            ).field
                        )

                        order_by_clause = (
                            asc(db_field)
                            if qo.sort.order is not SortOrder.DESC
                            else desc(db_field)
                        )

                        if serializer_entity.get_serializer_field(
                                qo.sort.field.fields[-1]
                        ).entity:
                            nested_field_stack = qo.sort.field.fields[:-1]
                            for nested_field in nested_field_stack:
                                serializer_entity = get_serializer(
                                    serializer_entity.get_serializer_field(
                                        nested_field
                                    ).entity.entity
                                )
                                db_field = serializer_entity.get_db_field(nested_field)

                            q = q.join(db_field)
                            q = q.order_by(order_by_clause)
                        else:
                            q = q.select()
                            q = q.order_by(order_by_clause)

    if qo.offset:
        q = q.offset(qo.offset)
    if qo.limit:
        q = q.limit(qo.limit)
    q = q.group_by(serializer.get_db_field("id"))
    q = q.subquery()

    return q


def _relation_select(
        action: ActionTree,
        serializer: Type[BaseSerializer],
        parent_model,
        sql_relation,
        full_action: ActionTree,
):
    """
    The _relation_select function is responsible for generating a Common Table Expression (CTE)
    that represents a SQL query for retrieving related entities based on the provided ActionTree,
    serializer, parent model, and SQL relationship information.

    Parameters:
        action (ActionTree): An instance of the ActionTree class representing the current action
        and its associated relationships.

        serializer (Type[BaseSerializer]): A subclass of BaseSerializer representing the serializer associated
        with the model for which relationships are being resolved.

        parent_model: The model of the parent entity.

        sql_relation: An object representing the SQL relationship between the parent model and the related entity.

    Returns:
        CTE: A Common Table Expression representing the SQL query for retrieving related entities based on
        the provided parameters.
    """
    primaryjoin = sql_relation.primaryjoin
    fields_into_json = []  # fields that we want to select
    _joins = []  # for linked entities
    _cte = None  # Common Table Expression

    # Get model from serializer(mapper[Model])
    _model_inspect = serializer.get_model_inspection()

    if primaryjoin.left in _model_inspect.columns.values():
        parent_id_col = primaryjoin.left
        other_id_col = primaryjoin.right
    else:
        parent_id_col = primaryjoin.right
        other_id_col = primaryjoin.left

    # Check if in linked entity is foreign key for this entity
    has_parent_id_col = parent_id_col != serializer.model.id

    if action.select:  # In action tree check if there are any select for parent entity
        _exclude_fields = []  # If we use "!" we store fields that we want to exclude

        # True if "*" in select fields
        _wild_select = any((_field == WILDCARD for _field in action.select))

        _field_to_select = []
        if _wild_select:  # Get all fields that are in this serializer if "*"
            _field_to_select = [
                _field
                for _field in serializer.fields
                if _field.field
                   not in _model_inspect.relationships  # We don`t add it to list if it is relation(navigation property)
            ]
        else:  # if something else than all fields *
            # Take fields that entered by user
            _field_to_select = [
                serializer.get_serializer_field(_field) for _field in action.select
            ]
        for _field in action.select:  # for each field do
            if _field.startswith(EXCLUDE_COLUMN_PREFIX):  # if "!" before field
                _field_to_select = [
                    _field
                    for _field in serializer.fields
                    if _field.field not in _model_inspect.relationships
                ]

                # Take all fields, but remove with !
                _field_to_select.remove(serializer.get_serializer_field(_field[1:]))

        # Get fields such as in DB and provide unique
        fld = set(serializer.get_db_field(field.field) for field in _field_to_select)

        if has_parent_id_col:
            if sql_relation.direction != RelationshipDirection.MANYTOMANY:
                fld.add(parent_id_col)  # add to set foreign key

        for flt in action.filters:
            # If filter to linked entity, then we don`t anything
            if isinstance(flt.field, NestedField):
                continue
            fld.add(
                serializer.get_db_field(
                    serializer.get_serializer_field(flt.field).field
                )
            )
        fld.add(serializer.get_db_field("id"))  # add id
        q = select(*fld)  # Create query
    else:  # if fields to select are not defined
        q = select(serializer.model)  # query for select certain model
        _field_to_select = [
            _field
            for _field in serializer.fields
            if _field.field not in _model_inspect.relationships
        ]  # There all fields are selected

    if action.sort is not None:  # if order is defined
        # field that we want rows to sort by
        col = serializer.get_db_field(action.sort.field)

        # set order ascending or descending
        col = desc(col) if action.sort.order == SortOrder.DESC else asc(col)
        q = q.order_by(col)  # Add it to query
    q = q.subquery()  # Make from query subquery to manipulate in future

    for field_def in _field_to_select or []:
        fields_into_json.append(field_def.alias)

        # Add to list elements that we want to select
        fields_into_json.append(q.c[field_def.field])

    filter_items = []
    _inner_cte: list[str] = []
    for flt_item in action.filters:
        if isinstance(flt_item.field, NestedField):
            # In [0] we have relation and in [1] certain field
            if flt_item.field.fields[0] in action.relations:
                rel_action = action.relations[flt_item.field.fields[0]]
            else:
                rel_action = ActionTree()  # For linked in 2 and more depth filtering
                rel_action.select = ["id"]
                action.relations[flt_item.field.fields[0]] = rel_action

            rel_action.filters.append(
                FilterAction(
                    field=flt_item.field.shift_down(),
                    op=flt_item.operator,
                    value=flt_item.value,
                )  # add filterAction for related entities
            )

            # add relation to common table expression
            _inner_cte.append(flt_item.field.fields[0])
            continue  # while nested we do it again and again

        # add operator that we use to filter
        filter_items.append(
            flt_item.operator(
                q.c[serializer.get_serializer_field(flt_item.field).field],
                flt_item.value,
            )
        )

    relation_fields_into_json, _joins, field_order_by = _resolve_relationships(
        action,
        serializer,
        q.c.id,
    )
    # get lists that define requests parameters properly(According to relation type, etc.)
    fields_into_json.extend(relation_fields_into_json)  # fields that we want to select
    if (
            full_action.sort is not None
            and sql_relation.direction == RelationshipDirection.MANYTOMANY
            and full_action.sort.field.fields[0] == sql_relation.key
    ):
        field_stack = []
        field_stack.extend(reversed(full_action.sort.field.fields))
        if len(field_stack) != 1:
            while field_stack:
                current_field = field_stack.pop()

                if current_field != sql_relation.key:
                    _field_to_sort_by = q.c[
                        serializer.get_serializer_field(current_field).field
                    ]
                    _cte = select(
                        func.json_group_array(
                            func.json_object(*fields_into_json)
                        ).label(
                            "obj"
                        ),  # JSON array comprised of all values in the aggregation
                        _field_to_sort_by.label("field_sort_by"),
                        parent_model.id.label(
                            "id"
                        )  # Take id from model if linked model doesn`t have foreign key
                        if not has_parent_id_col
                           or sql_relation.direction == RelationshipDirection.MANYTOMANY
                        else q.c[parent_id_col.name].label("id"),
                    ).select_from(
                        q
                    )
    else:

        # JSON array comprised of all values in the aggregation
        _cte = select(
            func.json_group_array(func.json_object(*fields_into_json)).label("obj"),
            parent_model.id.label("id")
            if not has_parent_id_col
               or sql_relation.direction == RelationshipDirection.MANYTOMANY
            else q.c[parent_id_col.name].label("id"),
        ).select_from(q)

        # many to many check
    if sql_relation.direction == RelationshipDirection.MANYTOMANY:
        relation_model_table = primaryjoin.right.table
        # First by id cte right table (user_id), second join by second table from right table
        _cte = _cte.join(
            relation_model_table,
            onclause=sql_relation.secondaryjoin.right == q.c.id,
            isouter=False,
        )
        _cte = _cte.join(
            parent_model,
            onclause=other_id_col == sql_relation.primaryjoin.right,
            isouter=False,
        )

    else:
        if not has_parent_id_col:
            _cte = _cte.join(
                parent_model,
                onclause=other_id_col == q.c[parent_id_col.name],
                isouter=True,
            )  # Make join by other_id_col == q.c[parent_id_col.name] if linked model doesn`t have foreign key

    for relation_name, rel_cte, onclause in _joins:
        _cte = _cte.join(
            rel_cte,
            onclause=onclause,
            isouter=relation_name not in _inner_cte,
        )  # Make join in cte,is outer needed if true - left outer join
    if filter_items:
        _cte = _cte.filter(and_(*filter_items))  # Add to CTE filters if there are

    _cte = _cte.group_by(
        parent_model.id
        if not has_parent_id_col
           or sql_relation.direction == RelationshipDirection.MANYTOMANY
        else q.c[parent_id_col.name]
    )  # We group by id if there are FK else by parent_id_col.name

    return _cte.cte().prefix_with("NOT MATERIALIZED")
    # create CTE object, and we want to first compute CTE, then use it


def get_all(query_options: ActionTree, serializer: Type[BaseSerializer]):
    """
    The get_all function generates a SQL query to retrieve a list of entities based on the provided ActionTree and
    serializer. It utilizes the _json_query function to construct the necessary SQL expressions for the given query
    options.

    Parameters:
        query_options (ActionTree): An instance of the ActionTree class representing the query options, filters
        and relationships for the entities to be retrieved.

        serializer (Type[BaseSerializer]): A subclass of BaseSerializer representing the serializer associated
        with the model for which entities are being retrieved.

    Returns:
        Query: A SQL query that retrieves a list of entities based on the provided query_options and serializer.
    """
    query = select(
        "["
        + func.coalesce(
            func.group_concat(_json_query(query_options, serializer).c.sql_rest), ""
        )
        + "]"
    )
    return query
