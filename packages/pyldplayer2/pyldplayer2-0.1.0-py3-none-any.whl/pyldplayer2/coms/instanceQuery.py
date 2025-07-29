import functools
import re
import typing

from pyldplayer2.base.models.list2meta import list2alias, List2Meta
from pyldplayer2.base.objects.appattr import UseAppAttr

ALL_STRING_OPS = [
    "startswith",
    "endswith",
    "contains",
    "find",
    "index",
    "rfind",
    "rindex",
]

ALL_QUERY_TYPES = typing.Union[
    str, int, typing.List[int], typing.List[str], typing.List[typing.Union[int, str]]
]


def op_index_parse(string: str):
    """
    parse strng such as
    id[3:] -> id > 3
    id[:3] -> id < 3
    id[3:5] -> id > 3 and id < 5
    """
    # Extract the variable name and slice parts
    match = re.match(r"(\w+)\[([^:]*):([^:]*)\]", string)
    if not match:
        return string

    var_name, start, end = match.groups()

    # Handle different slice cases
    if start and end:  # id[3:5]
        return f"{var_name} > {start} and {var_name} < {end}"
    elif start:  # id[3:]
        return f"{var_name} > {start}"
    elif end:  # id[:3]
        return f"{var_name} < {end}"

    return string


def query_str(string: str):
    if "*" in string and " " not in string:
        string = f"name({string})"

    # split by parts
    parts = string.split()

    for i in range(len(parts)):
        stringpart = parts[i]

        # if quotation marks not following string operations, append them
        # ex: x.startswith(xxx) -> x.startswith("xxx")
        for op in ALL_STRING_OPS:
            if f"{op}(" in stringpart:
                stringpart = stringpart.replace(f"{op}(", f'{op}("')
                stringpart = stringpart.replace(")", '")')

        # parse as regex
        if any(part in stringpart for part in ["*", "?", "+"]):
            # name(xxx) -> xxx
            deshell = stringpart.split("(")[1].split(")")[0]
            outer = stringpart.split("(")[0]
            stringpart = f'_ld_re_search("{deshell}", {outer})'

        if "[" in stringpart:
            stringpart = op_index_parse(stringpart)

        parts[i] = stringpart.strip()

    return " ".join(parts)


class Query(UseAppAttr):
    params: dict = {}
    query_str = functools.partial(query_str)

    def __other_type_query(
        self,
        query: typing.Union[
            int, typing.List[int], typing.List[str], typing.List[typing.Union[int, str]]
        ],
    ):
        from pyldplayer2.coms.console import Console

        if isinstance(query, str) and query == "all":
            return Console(self.attr).list2()

        if isinstance(query, str) and query == "running":
            c = Console(self.attr)
            ret = []
            for i in c.list2():
                if i["android_started_int"] != 0:
                    ret.append(i)
            return ret

        if not isinstance(query, list):
            query = [query]

        query = [int(i) if isinstance(i, str) and i.isdigit() else i for i in query]

        list2s = Console(self.attr).list2()

        ret = []
        for s in list2s:
            if s["id"] in query:
                ret.append(s)
            elif s["name"] in query:
                ret.append(s)
        return ret

    def query(
        self,
        query: ALL_QUERY_TYPES,
        retType: typing.Literal["first", "all"] = "all",
        limit: int = -1,
    ) -> list[List2Meta]:
        """Query LDPlayer instances with flexible query syntax.

        Args:
            query: Query can be one of:
                - str: Query string with conditions
                - int: Instance ID
                - list[int]: List of instance IDs
                - list[str]: List of instance names
                - "all": All instances
                - "running": All running instances
            retType: "first" or "all" results
            limit: Maximum number of results (-1 for unlimited)

        Examples:
            # String queries
            query("name.startswith(test)")  # Names starting with 'test'
            query("id[1:5]")  # IDs between 1 and 5
            query("name.contains('dev')")  # Names containing 'dev'
            query("name(*dev*)")  # Names matching regex pattern

            # Direct ID/name queries
            query(1)  # Instance with ID 1
            query([1, 2, 3])  # Instances with IDs 1, 2, 3
            query(["test1", "test2"])  # Instances named 'test1', 'test2'

            # Special queries
            query("all")  # All instances
            query("running")  # All running instances

            # With options
            query("name.startswith('test')", retType="first")  # First matching instance
            query("id[1:5]", limit=2)  # Maximum 2 results
        """
        if isinstance(query, list) and all(isinstance(i, dict) for i in query):
            # assert this is a list of results
            if retType == "first":
                return query[:1]
            if limit > 0:
                return query[:limit]
            return query

        if not isinstance(query, str) or (
            " " not in query and re.match(r"^[A-Za-z0-9_-]+$", query)
        ):
            ret = self.__other_type_query(query)
            if retType == "first":
                return ret[:1]
            if limit > 0:
                return ret[:limit]
            return ret

        qstring = query_str(query)

        from pyldplayer2.coms.console import Console

        list2s = Console(self.attr).list2()
        ret = []
        for i in list2s:
            eval_params = list2alias(i)
            eval_params.update(self.params)
            eval_params["_ld_re_search"] = re.search

            if eval(qstring, eval_params):
                ret.append(i)
                if retType == "first":
                    return ret
                if limit > 0 and len(ret) >= limit:
                    return ret
        return ret

    def queryInts(
        self,
        string: str,
        retType: typing.Literal["first", "all"] = "all",
        limit: int = -1,
    ) -> list[int]:
        return [i["id"] for i in self.query(string, retType, limit)]

    def queryNames(
        self,
        string: str,
        retType: typing.Literal["first", "all"] = "all",
        limit: int = -1,
    ) -> list[str]:
        return [i["name"] for i in self.query(string, retType, limit)]
