import click
import json
import os


@click.group()
def mycommands():
    pass


PRIORITIES = {
    "1": "High priority",
    "2": "Medium priority",
    "3": "Low priority"
}


def load_todo_list(todofile):
    try:
        with open(todofile, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_todo_list(todofile, todo_list):
    with open(todofile, "w") as f:
        json.dump(todo_list, f, indent=4)


def print_todo(idx, todo):
    print(f"({idx}) - {todo['name']}: {todo['desc']} [Priority: {todo['priority']}]")


@click.command()
@click.argument("priority", type=click.Choice(PRIORITIES.keys()), default="2")
@click.argument("todofile", type=click.Path(exists=False), required=0)
@click.option("-n", "--name", prompt="Enter the todo name", help="The name of the todo item")
@click.option("-d", "--desc", prompt="Describe the todo", help="The description of the todo item")
def add_todo(name, desc, priority, todofile):
    if not todofile:
        todofile = "mytodos.json"
        if not os.path.exists(todofile):
            with open(todofile, "w") as f:
                f.write("[]")
    todo_list = load_todo_list(todofile)
    todo_list.append({"name": name, "desc": desc, "priority": PRIORITIES[priority]})
    save_todo_list(todofile, todo_list)
    click.echo(f"Task added successfully")


@click.command()
@click.argument("idx", type=int, required=1)
@click.argument("todofile", type=click.Path(exists=True), required=0)
def delete_todo(idx, todofile):
    if not todofile:
        todofile = "mytodos.json"
    todo_list = load_todo_list(todofile)
    if idx < len(todo_list):
        del todo_list[idx]
        save_todo_list(todofile, todo_list)
        click.echo(f"Task deleted successfully")
    else:
        click.echo(f"Invalid index")


@click.command()
@click.option("-p", "--priority", type=click.Choice(PRIORITIES.keys()), help="Filter todos by priority")
@click.argument("todofile", type=click.Path(exists=True), required=0)
def list_todos(priority, todofile):
    if not todofile:
        todofile = "mytodos.json"
    todo_list = load_todo_list(todofile)
    if priority is None:
        for idx, todo in enumerate(todo_list):
            print_todo(idx, todo)
    else:
        for idx, todo in enumerate(todo_list):
            if todo["priority"] == PRIORITIES[priority]:
                print_todo(idx, todo)


@click.command()
@click.argument("idx", type=int, required=1)
@click.argument("todofile", type=click.Path(exists=True), required=0)
@click.option("-n", "--name", help="The name of the todo item")
@click.option("-d", "--desc", help="The description of the todo item")
@click.option("-p", "--priority", help="Enter the new priority of the todo item")
def edit_todo(idx, todofile, name, desc, priority):
    if not todofile:
        todofile = "mytodos.json"
    todo_list = load_todo_list(todofile)
    if idx < len(todo_list):
        if name:
            todo_list[idx]["name"] = name
        if desc:
            todo_list[idx]["desc"] = desc
        if priority:
            todo_list[idx]["priority"] = PRIORITIES[priority]
        save_todo_list(todofile, todo_list)
        click.echo(f"Todo at index {idx} updated successfully")
    else:
        click.echo(f"Invalid index")


mycommands.add_command(add_todo)
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)
mycommands.add_command(edit_todo)


if __name__ == "__main__":
    mycommands()
