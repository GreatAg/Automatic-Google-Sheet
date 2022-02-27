from gspread import Cell


class Cells:

    def __init__(self, list_of_cells):
        self.cells = list()
        self.partitioned_by_row = dict()
        self.partitioned_by_column = dict()

        self.is_partitioned = False
        for cell in list_of_cells:
            if type(cell) != Cell:
                raise TypeError()
            self.cells.append(cell)

        self.partition_cells()

    def append(self, cell):
        self + cell

    def add_cell_to_partitions(self, cell):
        if cell.col not in self.partitioned_by_column:
            self.partitioned_by_column[cell.col] = []
        if cell.row not in self.partitioned_by_row:
            self.partitioned_by_row[cell.row] = []
        self.partitioned_by_row[cell.row].append(cell)
        self.partitioned_by_column[cell.col].append(cell)

    def partition_cells(self):
        for cell in self.cells:
            self.add_cell_to_partitions(cell)
        self.is_partitioned = True

    def __add__(self, cell: Cell):
        if type(cell) != Cell:
            raise TypeError()
        self.cells.append(cell)
        self.add_cell_to_partitions(cell)

    def __sub__(self, cells):
        if type(cells) != Cells:
            raise TypeError()
        new_cells = self
        for cell in cells.cells:
            new_cells.delete(cell)
        return new_cells

    def delete(self, cell: Cell):
        if cell in self.cells:
            try:
                del self.cells[self.cells.index(cell)]
            finally:
                self.delete_from_partitions(cell)

    def delete_from_partitions(self, cell):
        try:
            del self.partitioned_by_row[cell.row][self.partitioned_by_row[cell.row].index(cell)]
        except:
            pass
        try:
            del self.partitioned_by_column[cell.col][self.partitioned_by_column[cell.col].index(cell)]
        except:
            pass

    def get_row_values_by_index(self, sheet_index):
        # return [cell for cell in self.cells if cell.row == sheet_index]
        return self.partitioned_by_row.get(sheet_index, [])

    def get_column_by_index(self, sheet_index):
        # return [cell for cell in self.cells if cell.col == sheet_index]
        return self.partitioned_by_column.get(sheet_index, [])

    def find(self, value):
        r = None
        for cell in self.cells:
            if cell.value == value:
                r = cell
                break
        return r

    def find_all(self, value):
        r = []
        for cell in self.cells:
            if cell.value == value:
                r.append(cell)
        return r

    def iter_rows(self):
        for row, row_cells in self.partitioned_by_row.items():
            yield row_cells

    def iter_columns(self):
        for columns, columns_cells in self.partitioned_by_column.items():
            yield columns_cells

    def export_for_batch_update(self):
        all_ = []
        for row in self.partitioned_by_row.values():
            for cell in row:
                all_.append({'range': cell.address, 'values': [[cell.value]]})
        return all_
# for row in self.partitioned_by_row.values():
#     for cell in row:
#         all_.append({'range': cell.address, 'values': [[cell.value]]})