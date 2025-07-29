from datetime import datetime
import requests

def layout_msg_teams(titulo, mensagem):
    """
    Gera o corpo de um Adaptive Card para ser enviado ao Microsoft Teams.
 
    Args:
        titulo (str): O título principal da mensagem.
        mensagem (str): A mensagem principal.
        detalhes (str): Detalhes adicionais (opcional).
 
    Returns:
        dict: Estrutura JSON do Adaptive Card.
    """
    agora = datetime.now()
 
    return {
        "type": "message",
        "attachments": [
            {
                "contentType": "application/vnd.microsoft.card.adaptive",
                "content": {
                    "$schema": "http://adaptivecards.io/schemas/adaptive-card.json",
                    "version": "1.4",
                    "type": "AdaptiveCard",
                    "body": [
                        {
                            "type": "TextBlock",
                            "text": titulo,
                            "weight": "Bolder",
                            "size": "Large",
                            "color": "Attention"
                        },
                        {
                            "type": "TextBlock",
                            "text": f"{mensagem}\n\n**Enviado em:** {agora.strftime('%d/%m/%Y %H:%M:%S')}",
                            "wrap": True
                        }
                    ]
                }
            }
        ]
    }
 
 
def enviar_msg_teams(webhook_url, titulo, mensagem):
    """
    Envia uma mensagem para o Microsoft Teams usando um webhook.
 
    Args:
        webhook_url (str): URL do webhook do Teams.
        titulo (str): O título principal da mensagem.
        mensagem (str): A mensagem principal.
        detalhes (str): Detalhes adicionais (opcional).
    """
    # Gerar o corpo da mensagem usando a função
    corpo_mensagem = layout_msg_teams(titulo, mensagem)
 
    response = requests.post(webhook_url, json=corpo_mensagem)
    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem: {response.status_code}, {response.text}")