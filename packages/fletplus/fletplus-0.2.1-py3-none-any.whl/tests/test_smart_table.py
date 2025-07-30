import flet as ft
from fletplus.components.smart_table import SmartTable

class DummyPage:
    def update(self): pass

class DummyControl:
    page = DummyPage()

class DummyEvent:
    def __init__(self, column_index):
        self.column_index = column_index
        self.control = DummyControl()

def test_smart_table_full_behavior():
    columns = ["ID", "Nombre"]
    rows = [
        ft.DataRow(cells=[ft.DataCell(ft.Text("2")), ft.DataCell(ft.Text("Bob"))]),
        ft.DataRow(cells=[ft.DataCell(ft.Text("1")), ft.DataCell(ft.Text("Alice"))]),
        ft.DataRow(cells=[ft.DataCell(ft.Text("3")), ft.DataCell(ft.Text("Charlie"))]),
    ]

    table = SmartTable(columns, rows, page_size=2)

    assert table.current_page == 0
    assert table.page_size == 2
    assert table.sort_ascending is True
    assert table.sorted_column is None

    built = table.build()
    assert isinstance(built, ft.Column)
    assert any(isinstance(c, ft.DataTable) for c in built.controls)

    sort_handler = table._on_sort(0)
    sort_handler(DummyEvent(0))
    assert table.sorted_column == 0
    assert table.sort_ascending is True
    assert table.rows[0].cells[0].content.value == "1"

    sort_handler(DummyEvent(0))
    assert table.sort_ascending is False
    assert table.rows[0].cells[0].content.value == "3"

    table._next_page(DummyEvent(0))
    assert table.current_page == 1

    table._previous_page(DummyEvent(0))
    assert table.current_page == 0
