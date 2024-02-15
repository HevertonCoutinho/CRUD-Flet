from flet import *
import sqlite3

#Conectando ao banco de dados
conexao = sqlite3.connect("dados.db", check_same_thread=False)
cursor = conexao.cursor()

#criar uma tabela no banco de dados
def tabela_base():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS clientes (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT)
    '''
    )

class App(UserControl):
    def __init__(self):
        super().__init__()
        
        self.todos_dados = Column(auto_scroll=True)
        self.adicionar_dados = TextField(label='Nome do dado')
        self.editar_dado = TextField(label='Editar')
        
    
    #deletar dados
    def deletar(self, x, y):
        cursor.execute("DELETE FROM clientes WHERE id = ?", [x])        
        y.open = False
        
        #chamando a função renderizar dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()
        
    def atualizar(self, x, y, z):
        cursor.execute("UPDATE clientes SET nome = ? WHERE id = ?", (y, x))
        conexao.commit()

        z.open = False
        
        #chamando a função renderizar dados
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()       
        
    #criando a função para abrir as ações
    def abrir_acoes(self, e):
        id_user = e.control.subtitle.value
        self.editar_dado.value = e.control.title.value
        self.update()
        
        alerta_dialogo = AlertDialog(
            title=Text(f"Editar ID {id_user}"),
            content=self.editar_dado,
            
            #botão de ação
            actions=[
                ElevatedButton(
                    'Deletar',
                    color='white', bgcolor='red',
                    on_click=lambda e:self.deletar(id_user, alerta_dialogo)
                ),
                ElevatedButton(
                    'Atualizar',
                    on_click=lambda e: self.atualizar(id_user, self.editar_dado.value, alerta_dialogo)    
                )
            ],
            actions_alignment='spaceBetween'
        )
        
        self.page.dialog = alerta_dialogo
        alerta_dialogo.open = True
        
        #atualizar a pagina
        self.page.update()

    
    #leitura dos dados    
    def renderizar_todos(self):
        cursor.execute("SELECT * FROM clientes")
        conexao.commit()
        
        meus_dados = cursor.fetchall()
        
        for dado in meus_dados:
            self.todos_dados.controls.append(
                ListTile(
                    subtitle=Text(dado[0]),
                    title=Text(dado[1]),
                    on_click=self.abrir_acoes
                )
            )
        self.update()
        
    def ciclo(self):
        self.renderizar_todos()    
    
    #inserindo dados dentro do banco    
    def adicionar_novo_dado(self, e):
        cursor.execute("INSERT INTO clientes (nome) VALUES (?)", [self.adicionar_dados.value])
        conexao.commit()
        
        self.todos_dados.controls.clear()
        self.renderizar_todos()
        self.page.update()
        
        
    def build(self):
        return Column([
            Text("CRUD COM SQLITE", size=20, weight='bold'),
            self.adicionar_dados,
            ElevatedButton(
            'Adicionar dado',
            on_click=self.adicionar_novo_dado
            ),
            self.todos_dados
        ])        

def main(page:Page):
    page.update()
    tabela_base()
    minha_aplicacao = App()   
    page.add(
        minha_aplicacao,
    )
      
app(target=main)