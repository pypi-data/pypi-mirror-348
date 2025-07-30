[![Test & Lint](https://github.com/ponomar/pgmini/actions/workflows/main.yml/badge.svg)](https://github.com/ponomar/pgmini/actions/workflows/main.yml)

## 🇺🇦 What is pgmini? 🇺🇦

It is the PostgreSQL query builder with next core principles:
- simple (predictable, without magic)
- fast

All object are immutable (thanks to [attrs](https://www.attrs.org) lib).
Python code as close to SQL structure as possible.
Library doesn't try to be everything.
It doesn't manage connections to postgres, doesn't escape params.
All this can and should be done with other tools: (asyncpg, psycopg2, postgresql itself etc.).

I've decided to use `PascalCase` methods naming to avoid collisions with python reserved words: 
`From`, `And`, `Or`, `Else`, `With`, `As` etc.

## Examples
```python
User = Table('user')  # dynamic columns

q = Select(User.id, User.name).From(User).Where(User.email == 'test@test.com')

build(q)
# (
#     'SELECT id, name FROM "user" WHERE email = $1', 
#     ['test@test.com'],
# )
```

Explicitly defined table schema allows to save filters and methods for further reusing 
and to use IDE code analyzers for smart completions, find usages, bulk refactors etc.  
```python
class RoleSchema(Table):
    id: int
    name: str
    status: str
    
    @property
    def status_active(self):  # can also be decorated with functools.cache
        return self.status == Literal('active')
    
    def name_startswith(self, value: str):
        return self.name.Like(f'{value}%')

Role = RoleSchema('role')
q = Select(Role.id).From(Role).Where(Role.status_active, Role.name_startswith('admin'))

RoleAlias = Role.As('role2')  # all columns/methods are visible for IDE live inspection as well
q = (
    Select(Role.STAR).From(Role)
    .Where(Not(Exists(
        Select(1).From(RoleAlias)
        .Where(RoleAlias.id < Role.id, RoleAlias.status_active)
    )))
)
```

#### WHERE
Where takes *args which work like AND operator.
```python
t = Table('tbl')
q = (
    Select(t.id).From(t)
    .Where(
        t.id.Between(10, 20), 
        Or(t.name > 'name', And(t.status == 'active', Not(t.id == 15))),
    )
)
# SELECT id FROM tbl WHERE id BETWEEN $1 AND $2 AND (name > $3 OR (status = $4 AND NOT (id = $5)))

# Add filters to existent query
q2 = q.Where(t.id != 14)
```

#### JOIN
```python
t, t2 = Table('tbl'), Table('tbl2')

sq = Select(t2.name).From(t2).Where(t2.id == t.id).Subquery('sq')
q = (
    Select(t.id).From(t)
    .Join(t2, t2.id == t.id)
    .LeftJoin(t2, And(t2.id == t.id, t2.status == 'active'))
    .JoinLateral(sq, True)
    .LeftJoinLateral(sq, sq.name != 'test')
)
```

#### PARAMETERS / LITERALS
By default, all values are considered as parameters. 
If you need to cast value or add alias use Param wrapper.
If you need to literally insert value into sql use special Literal wrapper, 
but be very careful - it won't be escaped and can lead to SQL injections. 
Use Literal only with data you can 100% trust.
```python
t = Table('tbl')
q = (
    Select(t.STAR, Param(10).Cast('int').As('added')).From(t)
    .Where(
        t.id1 == 1, 
        t.id2 != Param(2).Cast('float'), 
        t.id3 > Literal(3), 
        t.id4 < Literal(4).Cast('numeric'),
    )
)
build(q)
# (
#     'SELECT *, $1::int AS added FROM tbl WHERE id1 == $2 AND id2 != $3::float AND id3 > 3 AND id4 < 4::numeric',
#     [10, 1, 2],
# )
```

#### FUNCTIONS
There are `Func` and its `F` alias.
```python
t = Table('tbl')

q1 = (
    Select(
        F.count('*'), 
        F.count(t.id).Where(t.id > 10, t.id < 20),
        F.array_agg(t.id).OrderBy(t.id.Desc().NullsLast()).As('ids'),
    )
    .From(t)
)

q2 = Select(t.id, F.row_number().Over(partition_by=t.status, order_by=t.id)).From(t)

f = F.unnest(Literal([1, 2, 3])).As('idx')
q3 = Select(f.STAR).From(f)
# SELECT * FROM UNNEST(ARRAY[1, 2, 3]) AS idx

q4 = Select(Case((t.id == 1, 'first'), (t.id == 2, 'second'), Else='third').As('val')).From(t)

q5 = Select(Array([t.id, 5, 7])).From(t)
```

#### ORDER BY / GROUP BY / HAVING / DISTINCT / DISTINCT ON
```python
t = Table('tbl')

q1 = Select(t.id.Distinct()).From(t)
# SELECT DISTINCT id FROM tbl

q2 = Select(t.STAR).From(t).OrderBy(t.id.Desc(), t.name.NullsLast())

q3 = Select(F.count('*')).From(t).GroupBy(t.status).Having(F.count('*') > 10)

q4 = Select(t.id, t.status).From(t).DistinctOn(t.status)
# SELECT DISTINCT ON (status) id, status FROM tbl
```

#### OPERATIONS
Basic math operator are supported out of the box: 
`+`, `-`, `*`, `/`, `>`, `>=`, `<`, `<=`. 
Others are support as methods:
```python
t = Table('tbl')
q = (
    Select(
        t.id + t.id,
        t.id - 1,
        t.id * 10,
        t.id > 15,
        (t.id == 10).As('equals_ten'),
        (t.id != 11).As('not_equals_eleven'),
        Param(10) > 9,
        (Literal(5) * 3.5).Cast('int'),
        t.id.Between(1, 2),
        t.id.In([1, 2, 3]),
        t.id.NotIn(Select(t.id).From(t).Where(t.id < 10)),
        t.name.Is(None),
        t.active.IsNot(False),
        t.data.Op('->>', 'key').As('value1'),
        t.data.Op('#>>', ['key1', 'key2']).As('value2'),
        t.id.Any(list(range(1_000))),
        t.name.Like('%ABC%'),
        t.name.Ilike('%abc%'),
    )
    .From(t)
)
```

#### INSERT
```python
t = Table('tbl')
q = (
    Insert(t, columns=(t.name, t.status))
    .Values(
        (Param('some text').Cast('varchar(10)'), 'active'),
        ('other text', Literal('deleted')),
    )
    .Returning(t.STAR)
)

build(q)
# (
#     "INSERT INTO tbl (name, status) VALUES ($1::varchar(10), $2), ($3, 'deleted') RETURNING *",
#     ['some text', 'active', 'other text'],
# )

# From select
q = (
    Insert(t, columns=(t.name, t.status))
    .Select(
        Select(F.concat(t.name, F.random().Cast('text')), t.status)
        .From(t)
        .Where(t.id < 100)
        .Limit(10)
    )
    .Returning(t.STAR)
)

# CTE
sq = Select(t.STAR).From(t).Where(t.id < 100).Subquery('sq')
q = (
    With(sq)
    .Insert(t, ('name', 'status'))
    .From(Select(sq.name, sq.status).From(sq))
)

# Efficient bulk insert from the list of values
values = [(str(i), 'active') for i in range(1_000)]
q = (
    Insert(t, ('name', 'status'))
    .From(Select(
        F.unnest(Param([name for name, _ in values]).Cast('text[]')),
        F.unnest(Param([status for _, status in values]).Cast('enum_status[]')),
    ))
)
```

#### UPDATE / DELETE
```python
t = Table('stmh')
q1 = Update(t).Set({t.name: 'second'}).Where(t.name == 'first', t.status == 'active').Returning(t.id)
q2 = Delete(t).Where(t.id == 25).Returning(t.id)
```

#### Subquery / CTE
Any Select/Insert/Update/Delete has Subquery method.
```python
t = Table('tbl')
sq = Select(t.id).From(t).Where(t.id < 100).Subquery('sq')

# Subquery
q = Select(sq.id).From(sq).Where(sq.id > 50)
# SELECT id FROM (SELECT id FROM tbl WHERE id < $1) As sq WHERE id > $2

# CTE
q = With(sq).Select(sq.id).From(sq).Where(sq.id > 50).Limit(2)
# WITH sq AS (SELECT id FROM tbl WHERE id < $1) SELECT id FROM sq WHERE id > $2 LIMIT $3
```

***

### Why not sqlalchemy?
- too smart (tries to do everything: from connection/session management, to sql generating and params escaping)
- too complex
- too slow
- mutable (on its core)

It is good for simple projects with simple sql queries. 
But when your project grows up, your team grows up, sqlalchemy always leads to errors,
unnecessary complexity, extra time your team need to spend to learn it, find not obvious bugs etc.  


### Why not pypika?
While it is much simpler then sqlalchemy, it also requires you to learn their own "sql syntax" which is not always obvious.
And by default it uses parameters as literals, so it can lead to sql injections.


***

The library is inspired by Ukraine🇺🇦 (Kyiv is my home) and its brave and free people🔱.

Slava Ukraini, Heroyam slava!
