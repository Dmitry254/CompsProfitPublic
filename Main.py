"""

A program for calculating the income from the sale of something (in this case, computers).

"""

import tkinter as tk
from tkinter import ttk
import sqlite3


class Main(tk.Frame):
    """
    Constructor of the main window
    """
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()
        self.results()

    def init_main(self):
        toolbar = tk.Frame(bg='#33ff33', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='.\images\\add.png')
        btn_open_dialog = tk.Button(toolbar, text='Добавить ПК',
                                    command=lambda: self.open_dialog(),
                                    bg='#33ff33', bd=0, compound=tk.TOP,
                                    image=self.add_img)
        btn_open_dialog.place(x=10, y=0)

        self.edit_img = tk.PhotoImage(file='.\images\\edit.png')
        btn_edit = tk.Button(toolbar, text='Изменить запись',
                             command=lambda: self.open_edit_dialog(),
                             bg='#33ff33', bd=0, compound=tk.TOP,
                             image=self.edit_img)
        btn_edit.place(x=130, y=0)

        self.delete_img = tk.PhotoImage(file='.\images\\delete.png')
        btn_delete = tk.Button(toolbar, text='Удалить запись',
                               command=lambda: self.delete_records(),
                               bg='#33ff33', bd=0, compound=tk.TOP,
                               image=self.delete_img)
        btn_delete.pack(side=tk.RIGHT)

        ttk.Style().configure('Treeview', rowheight=155)
        ttk.Style().configure('Treeview', font=('Arial 10'))
        self.tree = ttk.Treeview(self, columns=('ID', 'desc', 'spent',
                                                'earn', 'profit', 'days'),
                                 heigh=40, show='headings',)

        self.tree.column('ID', width=50, anchor=tk.CENTER)
        self.tree.column('desc', width=380, anchor=tk.W)
        self.tree.column('spent', width=150, anchor=tk.CENTER)
        self.tree.column('earn', width=150, anchor=tk.CENTER)
        self.tree.column('profit', width=100, anchor=tk.CENTER)
        self.tree.column('days', width=100, anchor=tk.CENTER)

        self.tree.heading('ID', text='№')
        self.tree.heading('desc', text='Комплектующие')
        self.tree.heading('spent', text='Куплен за')
        self.tree.heading('earn', text='Продан за')
        self.tree.heading('profit', text='Прибыль')
        self.tree.heading('days', text='Дней продажи')

        self.tree.pack()

    def records(self, desc, earn, days):
        text = desc.split('\n')  # Removing excess from desc to calculate profit and spent
        newlist = []
        for x in text:
            if x != '':
                start = x.find(' - ') + len(' - ')
                newlist.append(int(x[start:]))
        spent = sum(newlist)  # Считаются Profit и spent
        profit = int(earn) - spent
        self.db.insert_data(desc, spent, earn, profit, days)
        self.view_records()

    def update_records(self, desc, earn, days):
        text = desc.split('\n')  # Removing excess from desc to calculate profit and spent
        newlist = []
        for x in text:
            if x != '':
                start = x.find(' - ') + len(' - ')
                newlist.append(int(x[start:]))
        spent = sum(newlist)
        profit = int(earn) - spent  # Profit and spent are calculated
        self.db.c.execute('''UPDATE CompsProfit SET desc=?, spent=?, earn=?, profit=?, days=? WHERE ID=?''',
                          (desc, spent, earn, profit, days, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.comm.commit()
        self.view_records()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM CompsProfit WHERE ID=?''',
                              [self.tree.set(selection_item, '#1')])
            self.db.comm.commit()
            self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM CompsProfit''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def results(self):
        self.db.c.execute('''SELECT profit FROM CompsProfit''')
        self.base_total_profit = self.db.c.fetchall()
        self.total_profit = 0
        for profit_counter in self.base_total_profit:
            self.total_profit += profit_counter[0]

        self.db.c.execute('''SELECT days FROM CompsProfit''')
        self.base_total_days = self.db.c.fetchall()
        self.total_days = 0
        for days_counter in self.base_total_days:
            self.total_days += days_counter[0]

        self.results_string = 'Итого за %s дня заработано %s рублей.' % (
                                self.total_days, self.total_profit)

        self.label_results = tk.Label(root, text=self.results_string, font="Arial 11", bg="#33ff33")
        self.label_results.place(x=500, y=10)

    def open_dialog(self):
        edit_data = ('', '', '')
        Child(edit_data)  # Passes edit_data to add a record

    def open_edit_dialog(self):
        global edit_data
        for selection_item in self.tree.selection():
            self.db.c.execute('''SELECT desc, earn, days FROM CompsProfit WHERE ID=?''',
                              [self.tree.set(selection_item, '#1')])
            edit_data = self.db.c.fetchall()
            edit_data = edit_data[0]
        Update(edit_data)  # Passes edit_data to edit a record


class Child(tk.Toplevel):
    """
    Constructor of the add/edit windows
    """
    def __init__(self, edit_data):
        super().__init__(root)
        self.edit_data = edit_data
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Данные о ПК')
        self.geometry('500x340+400+300')
        self.resizable(False, False)

        label_desc = ttk.Label(self, text='Комплектующие:')
        label_desc.place(x=20, y=50)
        label_earn = ttk.Label(self, text='Продан за:')
        label_earn.place(x=20, y=240)
        label_days = ttk.Label(self, text='Дней продажи:')
        label_days.place(x=20, y=270)
        label_how_use = ttk.Label(self, text='Используйте синтаксис: "модель - цена"')
        label_how_use.place(x=150, y=20)

        self.entry_desc = tk.Text(self, width=42, height=10, font='Arial 11')
        self.entry_desc.place(x=140, y=50)
        self.entry_desc.insert(0.0, self.edit_data[0])
        self.entry_earn = tk.Text(self, width=42, height=1, font='Arial 11')
        self.entry_earn.place(x=140, y=240)
        self.entry_earn.insert(0.0, self.edit_data[1])
        self.entry_days = tk.Text(self, width=42, height=1, font='Arial 11')
        self.entry_days.place(x=140, y=270)
        self.entry_days.insert(0.0, self.edit_data[2])

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=400, y=300)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=315, y=300)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(
                                                self.entry_desc.get("1.0", "end-1c"),
                                                self.entry_earn.get("1.0", "end-1c"),
                                                self.entry_days.get("1.0", "end-1c")))


class Update(Child):
    """
    Constructor of the update window
    """
    def __init__(self, edit_data):
        super().__init__(edit_data)
        self.edit_data = edit_data
        self.init_edit()
        self.view = app

    def init_edit(self):
        self.title('Отредактировать данные')
        btn_edit = ttk.Button(self, text='Редактировать', command=self.destroy)
        btn_edit.place(x=300, y=300)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_records(
                                                self.entry_desc.get("1.0", "end-1c"),
                                                self.entry_earn.get("1.0", "end-1c"),
                                                self.entry_days.get("1.0", "end-1c")))


class DB:
    def __init__(self):
        self.comm = sqlite3.connect('CompsProfit.db')
        self.c = self.comm.cursor()
        self.c.execute(
            '''CREATE TABLE IF NOT EXISTS CompsProfit(id integer primary key, desc text,
            spent integer, earn integer, profit integer, days integer)''')
        self.comm.commit()

    def insert_data(self, desc, spent, earn, profit, days):
        self.c.execute('''INSERT INTO CompsProfit(desc, spent, earn, profit, days) 
        VALUES (?, ?, ?, ?, ?)''', (desc, spent, earn, profit, days))
        self.comm.commit()


if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('CompsProfit')
    root.geometry('940x600+200+100')
    root.resizable(False, False)
    root.mainloop()
