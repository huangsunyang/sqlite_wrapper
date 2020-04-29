# -*- coding=utf-8 -*-
import sqlite3


python_type_to_sqlite = {
    int: 'INTEGER',
    str: 'TEXT',
    float: 'REAL',
}

create_table_command = "create table if not exists {0} (\n\t{1}\n)"

drop_table_command = "drop table {};"

insert_table_command = "insert into {0} ({1}) values ({2});"

update_table_command = 'update {}\nset {} where {};'


def get_type_text(member):
    name, python_type = member
    type_text = python_type_to_sqlite[python_type]
    return '{} {}'.format(name, type_text)


def get_value_text(value):
    if isinstance(value, str):
        return "'{}'".format(value)
    return str(value)


class SqliteWrapper(object):
    def __init__(self, db_name=None):
        self.connection = None
        if db_name is not None:
            self.open(db_name)

    def open(self, db_name):
        if self.connection:
            self.connection.close()
        self.connection = sqlite3.connect(db_name)

    def create_table(self, table_name, **kwargs):
        members = ', '.join(map(get_type_text, kwargs.items()))
        return self._run_command(create_table_command.format(table_name, members))

    def drop_table(self, table_name):
        return self._run_command(drop_table_command.format(table_name))

    def show_table(self, table_name):
        cursor = self._run_command('select * from {}'.format(table_name))
        for x in cursor:
            print x

    def insert(self, table_name, **kwargs):
        columns = ','.join(kwargs.keys())
        values = ','.join(map(get_value_text, kwargs.values()))
        return self._run_command(insert_table_command.format(table_name, columns, values))

    def update(self, table_name, **kwargs):
        members = ','.join(['{}={}'.format(x, get_value_text(y)) for x, y in kwargs.items()])
        condition = 'id = 1'
        return self._run_command(update_table_command.format(table_name, members, condition))

    def _run_command(self, command):
        print command
        ret = self.connection.execute(command)
        self.connection.commit()
        return ret


if __name__ == '__main__':
    s = SqliteWrapper('test.db')
    name = 'test1'
    s.create_table(name, id=int, cost=float, name=str)
    for i in range(3):
        import random
        r_cost = random.random()
        r_len = random.randint(3, 8)
        r_name = ''
        for _ in range(r_len):
            r_name += chr(random.randint(70, 100))
        s.insert(name, id=i, cost=r_cost, name=r_name)
    cursor = s.show_table(name)
    # s.create_table(name, id=int, cost=float, name=str)
    while True:
        command = raw_input('> ')
        try:
            print eval(command)
        except:
            try:
                exec command in globals(), globals()
            except:
                import traceback
                traceback.print_stack()

