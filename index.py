from tkinter import ttk
from tkinter import *
import sqlite3


class Product:
    db_name='database.db'
    def __init__(self,window):
        self.wind = window
        self.wind.title('Product Application') 
        #creamos un contenedor en un frame
        frame= LabelFrame(self.wind,text='register a new product') 
        frame.grid(row=0, column=0, columnspan= 3, pady=20)
        # name input
        Label(frame, text='name: ').grid(row=1,column=0)
        self.name= Entry(frame)
        self.name.focus()                    # ubicacion del cursor
        self.name.grid(row=1,column=1)
        # price input
        Label(frame, text='Price: ').grid(row=2,column=0)
        self.price= Entry(frame)
        self.price.grid(row=2,column=1)
        # button add product
        ttk.Button(frame,text='Save product',command=self.add_product).grid(row=3,columnspan=2, sticky= W+E)
        # output messages
        self.message= Label(text='',fg='red')
        self.message.grid(row=3, column=0,columnspan=2,sticky=W+E)
        # table
        self.tree= ttk.Treeview(height=10,column=2)
        self.tree.grid(row=4,column=0,columnspan=2)
        self.tree.heading('#0',text='Name', anchor=CENTER)
        self.tree.heading('#1',text='Price', anchor=CENTER)

        # buttons

        ttk.Button(text="Delete",command= self.delete_product).grid(row=5,column=0,sticky=W+E)
        ttk.Button(text="Edit", command= self.edit_product).grid(row=5,column=1,sticky=W+E)

        self.get_products()
        # db
    def run_query(self,query,parameters=()):
        with sqlite3.connect(self.db_name) as conn:
                cursor= conn.cursor()
                result= cursor.execute(query,parameters)
                conn.commit()
        return result
    
    def get_products(self):
        # limpiando la tabla    
        records= self.tree.get_children() 
        for record in records:
                self.tree.delete(record)
        #consulta de datos

        query='SELECT * FROM Products ORDER BY name DESC'
        db_rows=self.run_query(query)
        for row in db_rows:
                self.tree.insert('',0,text= row[1],values=row[2])
                

    def validation(self):
           return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def add_product(self):
            if self.validation():
                query= 'INSERT INTO Products VALUES(NULL,?,?)'
                parameters=(self.name.get(),self.price.get())
                self.run_query(query,parameters)
                self.message['text']= 'producto {} agregado satisfactoriamente'.format(self.name.get())
                self.name.delete(0,END)
                self.price.delete(0,END)
            else:
                self.message['text'] ='todos los campos son requeridos'    
            self.get_products()

    def delete_product(self):
        self.message['text']=''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
             self.message['text']= 'seleccione un registro'
             return
        self.message['text']=''

        name=  self.tree.item(self.tree.selection())['text']
        query= 'DELETE FROM Products WHERE name= ?'
        self.run_query(query,(name, ))
        self.message['text']='el producto {} ha sido eliminado'.format(name)
        self.get_products()

    def edit_product(self):
        self.message['text']=''
        try:
           self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
             self.message['text']= 'seleccione un registro'
             return
        name= self.tree.item(self.tree.selection())['text']
        old_price=self.tree.item(self.tree.selection())['values'][0]
        self.edit_wind= Toplevel()
        self.edit_wind.title='edit product'

        # old name
        Label(self.edit_wind, text='old name: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=name),state='readonly').grid(row=0,column=2)
        
        # new name
        Label(self.edit_wind, text='new name: ').grid(row=1, column=1)
        new_name=Entry(self.edit_wind)
        new_name.grid(row=1,column=2)

        #old price
        Label(self.edit_wind, text='old price: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable= StringVar(self.edit_wind, value=old_price),state='readonly').grid(row=2,column=2)

        
        #new price
        Label(self.edit_wind, text='new price: ').grid(row=3, column=1)
        new_price=Entry(self.edit_wind)
        new_price.grid(row=3,column=2)

        boton=Button(self.edit_wind,text='Update', command= lambda: self.edit_record(new_name.get(),name,new_price.get(),old_price))
        boton.grid(row=4,columnspan=2, sticky=W+E)

    def edit_record(self,new_name, name, new_price,old_price):
        query='UPDATE Products SET name=?, price=? WHERE name=? AND price=?'
        parameters= (new_name, new_price, name,old_price)
        self.run_query(query,parameters)
        self.edit_wind.destroy()
        self.message['text']= 'el record {} se ha actualizado correctamente'.format(new_name)
        self.get_products()

              

if __name__=='__main__':
    window= Tk()
    application=Product(window)
    window.mainloop()