# CRUD_REPO
Proyecto MVC ABM
1.Create app.py witch it is the controller.
2. Define in app.py de entrsance pont app=Flask(__name__)
3.Configure datebase conection
4.Configure routings.:
 "/" In the index I expect to have the registers of the database sdo I'll define index function
5. Create a folder called templates/table_name in the root of the project. In this folder it will be allocate the view.
6.Create 3 html files : index, create, edit.
7.Index is empty for now, create should have a form to insert a register in the database so I`ll we create a field for each column I need, except ID.
8.Method of the form should be Post, and action  /store
