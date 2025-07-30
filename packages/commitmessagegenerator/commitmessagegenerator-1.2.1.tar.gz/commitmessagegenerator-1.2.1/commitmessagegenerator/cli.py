import argparse
import subprocess
from .generator import gerar_mensagem_commit
from .configure import api_key

def main():
    parser = argparse.ArgumentParser(description="Gerador de mensagens de commit com IA")
    parser.add_argument("-c", "--commit", action="store_true", help="Commits with the generated message")
    parser.add_argument("-cp", "--commitpush",  action="store_true", help="Commits and pushes with the generated message")
    parser.add_argument("-cf","--configure", action="store_true", help="Configures the GEMINI_API_KEY environment variable")
    args = parser.parse_args()

    if not args.cf:
        mensagem = gerar_mensagem_commit()

        if "No changes detected" in mensagem:
            print(mensagem)
            return

        print("\nGenerated commit message:\n" + mensagem)

    if args.c or args.cp:
        print("\nCommitting changes...")
        subprocess.run(["git", "commit", "-m", mensagem])

    if args.cp:
        print("\nPushing changes...")
        subprocess.run(["git", "push"])
    
    if args.cf:
        print("\nPlease input your API KEY\nThis is directly set in the .env file\n")
        key = input()
        api_key(key)
        print("\nAPI KEY saved in .env file\n")
    
    if not args.c or not args.cp:
        print("\nRemoving staged changes (git reset)...")
        subprocess.run(["git", "reset"])
