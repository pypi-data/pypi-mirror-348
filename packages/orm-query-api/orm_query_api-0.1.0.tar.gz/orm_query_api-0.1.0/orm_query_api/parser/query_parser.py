import datetime
import enum
import operator
from typing import Callable, Any

import lark
from lark import Transformer, Lark
from sqlalchemy.orm import InstrumentedAttribute

from ..exceptions.error import ValidationException


class SortOrder(str, enum.Enum):
    """
    Enumeration representing sort orders for sorting operations.

    Attributes:
        ASC (str): Sort in ascending order.
        DESC (str): Sort in descending order.

    Usage:
        To use this enumeration, simply access the attributes `ASC` and `DESC` for specifying
        the desired sort order in sorting operations.
    """

    ASC = "asc"
    DESC = "desc"


# ActionTree
#       |- select list[str]
#       |- filter col.eq=5 | relation.sub_relation.id=4
#       |- sort col.asc | relation.sub_relation.id.asc
#       |- limit: int > 0
#       |- offset: int >= 0
#       |- relations dict[str, ActionTree]


class ActionTree:
    """
    Represents a tree structure for defining actions such as selection, filtering, sorting,
    limiting, offsetting, and defining relations between entities.

    Attributes:
        name (str): The name of the action tree node.
        select (list[str]): List of attributes to select.
        filters (list[FilterAction]): List of filtering actions applied to the data.
        sort (SortAction or None): Sorting action applied to the data. None if not specified.
        limit (int): Maximum number of records to retrieve.
        offset (int): Offset for pagination.
        relations (dict[str, ActionTree]): Dictionary representing relations to other entities
            where keys are relation names and values are corresponding ActionTree instances.
    """

    def __init__(self):
        self.name = None
        self.select: list[str] = []
        self.filters: list[FilterAction] = []
        self.sort: SortAction | None = None
        self.limit: int = 20
        self.offset: int = 0
        self.relations: dict[str, ActionTree] = {}


class NestedField:
    """
    Represents a nested field within a data structure.

    Attributes:
        fields (list[str]): List of field names representing the nested structure.

    Methods:
        shift_down(): Returns a NestedField instance with the first field removed.
    """

    def __init__(self, fields: list[str]):
        self.fields = fields

    def shift_down(self):
        """
        Returns a NestedField instance with the first field removed.

        Returns:
            NestedField: A new NestedField instance.
        """
        _rest = self.fields[1:]
        return _rest[0] if len(_rest) == 1 else NestedField(_rest)


class FilterAction:
    """
    Represents a filter action to be applied on data.

    Attributes:
        field (str or NestedField): The field or nested field to filter on.
        operator (Callable): The filtering operation to be applied.
        value (Any): The value to filter against.
    """

    def __init__(self, field: str | NestedField, op: Callable, value: Any):
        self.field = field
        self.operator = op
        self.value = value

    def __eq__(self, other):
        """
        Checks if two FilterAction instances are equal.

        Parameters:
            other (FilterAction): Another FilterAction instance to compare.

        Returns:
            bool: True if the instances are equal, False otherwise.
        """
        return (
                self.field == other.field
                and self.operator == other.operator
                and self.value == other.value
        )


class SortAction:
    """
    Represents a sorting action to be applied on data.

    Attributes:
        order (SortOrder): The sorting order, either ascending or descending.
        field (NestedField): The nested field to sort on.

    """

    def __init__(self, order: SortOrder, field: NestedField):
        self.field = field
        self.order = order


class OffsetAction:
    def __init__(self, value: int):
        self.value = value


class LimitAction:
    """
    Represents an offset action for pagination.

    Attributes:
        value (int): The offset value.

    """

    def __init__(self, value: int):
        self.value = value


OPERATOR_SQLALCHEMY = {
    ">=": operator.ge,
    ">": operator.gt,
    "<": operator.lt,
    "<=>": operator.le,
    "=": operator.eq,
    "in": InstrumentedAttribute.in_,
    "!=": operator.ne,
    "is_null": InstrumentedAttribute.is_,
    "like": InstrumentedAttribute.like,
    "ilike": InstrumentedAttribute.ilike,
}

grammar = """
    DATE.10: DIGIT+ "-" DIGIT+ "-" DIGIT+
    ?rvalue: DATE | NUMBER | ESCAPED_STRING

    start: _root_query

    _root_query: "q" "=" action_tree

    action_tree: "(" field ("," field) * ")" ("." filter_fn)? ("." offset_fn)? ("." limit_fn)? ("." order_fn)? 

    filter_fn: "filter" "(" nested_field FILTER_OP rvalue ")"
    FILTER_OP: "=" | ">" | "<" | ">=" | "<=" | "in" | "!=" | "is_null" | "like" | "ilike"

    order_fn: "order" "(" (nested_field) "," SORT_ORDER ")"
    SORT_ORDER: "asc" | "desc"

    limit_fn: "limit" "(" NUMBER ")"
    offset_fn: "offset" "(" NUMBER ")"    

    !field: "!" CNAME | CNAME | "*" | relation

    nested_field: CNAME ("." CNAME)*

    relation: CNAME action_tree


    %import common.CNAME
    %import common.NUMBER
    %import common.DIGIT
    %import common.WS
    %import common.ESCAPED_STRING
    %ignore WS
"""


class SelectQueryTransformer(Transformer):
    def start(self, items):
        return items[0]

    def action_tree(self, items):
        opts = ActionTree()
        for item in items:
            match item:
                case SortAction(field=_, order=_):
                    opts.sort = item
                case FilterAction(field=_, operator=_, value=_):
                    if item not in opts.filters:
                        opts.filters.append(item)
                case OffsetAction(value=offset_value):
                    opts.offset = offset_value
                case LimitAction(value=limit_value):
                    opts.limit = limit_value
                case ActionTree(
                    relations=_, select=_, sort=_, filters=_, limit=_, offset=_
                ):
                    opts.relations[item.name] = item
                case _:
                    if opts.select is None:
                        opts.select = []
                    opts.select.append(item)
        return opts

    def FILTER_OP(self, items):
        return OPERATOR_SQLALCHEMY[items]

    def ESCAPED_STRING(self, items):
        return str(items[1:-1])

    def filter_fn(self, items):
        return FilterAction(items[0], items[1], items[2])

    def order_fn(self, items):
        return SortAction(items[1], items[0])

    def offset_fn(self, items):
        return OffsetAction(items[0])

    def limit_fn(self, items):
        return LimitAction(items[0])

    def SORT_ORDER(self, items):
        return SortOrder(items)

    def rvalue(self, items):
        return items[0]

    def NUMBER(self, items):
        if "." in items:
            return float(items)
        return int(items)

    def DATE(self, items):
        try:
            return datetime.datetime.strptime(items, "%Y-%m-%d").date()
        except ValueError:
            raise ValidationException(f"Invalid date format: {items}")

    def field(self, items):
        match items[0]:
            case ActionTree(
                relations=_, select=_, sort=_, filters=_, limit=_, offset=_
            ):
                return items[0]
            case "!":
                return "!" + str(items[1])
            case _:
                return str(items[0])

    def relation(self, items):
        action_tree = items[1]
        action_tree.name = str(items[0])
        return action_tree

    def nested_field(self, items):
        return NestedField(list(map(str, items)))


parser = Lark(grammar, parser="lalr", transformer=SelectQueryTransformer())


def parse_query(q: str):
    try:
        return parser.parse(q)
    except lark.UnexpectedToken as e:
        raise ValidationException(str(e))
    except lark.UnexpectedCharacters as e:
        raise ValidationException(str(e))
    except lark.UnexpectedEOF as e:
        raise ValidationException(str(e))
    except lark.UnexpectedInput as e:
        raise ValidationException(str(e))


if __name__ == "__main__":
    s = parser.parse("q=(id, created_at, todo(id)).filter(todo.id=2)")
    i = 0
