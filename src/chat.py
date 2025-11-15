from search import search_prompt

def main():
    # Apresentação e instruções do chat
    print("=" * 60)
    print("🤖 BEM-VINDO AO CHAT INTERATIVO")
    print("=" * 60)
    print("\nInstruções:")
    print("• Digite sua pergunta e pressione Enter")
    print("• O sistema buscará informações na base de dados vetorial")
    print("• Para encerrar, digite: 'sair', 'exit' ou 'quit'\n")
    print("=" * 60)
    print()
    
    # Loop principal do chat para interação contínua até o usuário decidir sair
    while True:
        try:
            # Solicitando pergunta ao usuário
            pergunta = input("💬 Você: ").strip()
            
            # Verificando se o usuário quer sair
            if pergunta.lower() in ['sair', 'exit', 'quit', '']:
                print("\n👋 Encerrando chat. Até logo!")
                break

            # Processando a pergunta e obtendo a resposta
            print("\n🔍 Buscando informações...\n")
            resposta = search_prompt(pergunta)
            print(f"🤖 Assistente: {resposta}")
            
            print("\n" + "-" * 60 + "\n")            
        except KeyboardInterrupt:
            print("\n\n👋 Chat interrompido. Até logo!")
            break
        except Exception as e:
            print(f"\n❌ Erro ao processar a sua pergunta: {str(e)}")
            print("Tente novamente.\n")

if __name__ == "__main__":
    main()