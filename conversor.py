import flet as ft
import re

def main(page: ft.Page):
    page.title = "Conversor de bases"
    lbl_conversao=ft.Text(size=22)
    
    base_conversao_regex={
        "Binario": [2,bin,r"^[0-1]*$"],
        "Decimal": [10,lambda x: "00" + str(x),r"^[0-9]*$"],
        "Octal": [8,oct,r"^[0-7]*$"],
        "Hexadecimal":[16,hex,r"^[0-9a-f]*$"]
    }

    def alterar(e):
        input_numero.input_filter.regex_string=base_conversao_regex[select_numero.value][2]
        #verifica se o valor no input, ao mudar o select, bate com o regex
        input_numero.value=input_numero.value if re.search(f"{str(input_numero.input_filter.regex_string)}", input_numero.value) else "" 
        input_numero.update()
        if input_numero.value != '':
            #converte o valor no input para um valor decimal, antes de converte-lo para a base requerida
            num=int(input_numero.value,base_conversao_regex[select_numero.value][0])
            lbl_conversao.value=f"{select_converte.value}: {base_conversao_regex[select_converte.value][1](num)[2::]}"
            lbl_conversao.update()
    
    opcoes_select=[ft.dropdown.Option(item) for item in base_conversao_regex.keys()]
    select_numero=ft.Dropdown(
        width=200,
        on_change=alterar,
        options=opcoes_select,
        value="Decimal"
    )
    select_converte = ft.Dropdown(
        width=200,
        on_change=alterar,
        options=opcoes_select,
        value="Binario",
        autofocus=True
    )

    input_numero = ft.TextField(
        label="Numero", 
        hint_text="Numero para conversão", 
        on_change=alterar, 
        input_filter=ft.InputFilter(allow=True,regex_string=r"^[0-9]*$")
    )
    
    page.add(select_numero, input_numero, select_converte, lbl_conversao)

ft.app(target=main)