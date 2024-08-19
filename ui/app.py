"""Módulo principal para a interface do usuário com Flet."""

import flet as ft

def main(page: ft.Page):
    """Função principal para o aplicativo Flet."""
    page.title = "OCB - Organizador de Contas Brasileiro"

    # TODO: Implementar a interface do usuário com Flet.
    page.add(ft.Text("Em construção..."))

if __name__ == "__main__":
    ft.app(target=main)