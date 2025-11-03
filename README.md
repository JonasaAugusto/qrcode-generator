# Gerador de QR Code com Interface Gráfica (qrcodeOpen.py)

## 💻 Descrição
Este é um aplicativo de desktop robusto e multifuncional para geração de QR Codes, desenvolvido em Python utilizando a biblioteca `tkinter` para a interface gráfica e `qrcode` para a geração das imagens.

O aplicativo oferece uma ampla gama de tipos de QR Codes e funcionalidades avançadas, como personalização de cores, histórico de geração, e até mesmo a criação em lote de vCards a partir de um arquivo CSV.

## ✨ Funcionalidades
*   **Interface Gráfica (GUI):** Desenvolvida com `tkinter` e `ttk` para uma experiência de usuário moderna.
*   **Múltiplos Tipos de QR Code:**
    *   Link (URL)
    *   Texto Simples
    *   Telefone
    *   Wi-Fi (com opções de segurança)
    *   E-mail (mailto)
    *   Contato (vCard) - com opção de geração manual ou **em lote via CSV**.
    *   Localização (geo) - via link do Google Maps ou coordenadas manuais.
*   **Personalização de Cores:** Permite escolher a cor do QR Code e a cor de fundo, com histórico de cores salvas.
*   **Histórico de Geração:** Armazena os QR Codes gerados para fácil regeneração.
*   **Ações Pós-Geração:**
    *   Salvar o QR Code como arquivo PNG.
    *   Enviar o QR Code por e-mail (requer Senha de App do Gmail).
*   **Suporte a Idiomas:** Inclui uma estrutura de tradução (Português e Inglês) no código.

## ⚙️ Requisitos
Para executar este script, você precisará:
1.  **Python 3.x** instalado.
2.  As bibliotecas `qrcode`, `Pillow` (para `ImageTk` e `Image`), e `email.message`, `smtplib`, `ssl`, `os`, `re`, `json`, `sys`, `csv`, `threading`, `webbrowser`, `tkinter` (geralmente inclusa).

### Instalação das Dependências
```bash
pip install qrcode Pillow
```

## 🚀 Como Usar

1.  **Execute o script:**
    ```bash
    python qrcodeOpen.py
    ```

2.  **Selecione o Tipo:**
    *   Na tela inicial, escolha o tipo de QR Code que deseja gerar (Link, Texto, Telefone, ou "Mais Opções" para Wi-Fi, E-mail, Contato, Localização).

3.  **Insira os Dados:**
    *   Preencha os campos de dados solicitados. O aplicativo possui validações para garantir o formato correto.

4.  **Personalize (Opcional):**
    *   Clique em "Personalizar Cores" para alterar as cores padrão (preto e branco).

5.  **Gere e Visualize:**
    *   Clique em **"Gerar e Visualizar"**. O QR Code será exibido em uma nova janela.

6.  **Ações:**
    *   Na janela de visualização, você pode **Salvar Arquivo** (PNG) ou **Enviar por E-mail**.

## ⚠️ Observações
*   **Geração em Lote (vCard):** Para usar a função de geração em lote, o arquivo CSV deve seguir o formato de cabeçalho: `Nome,Telefone,Email,Empresa,TipoTelefone`.
*   **Envio de E-mail:** O envio de e-mail utiliza o servidor SMTP do Gmail e requer uma **Senha de App** (não a sua senha de conta normal) para autenticação.
*   **Tamanho do Código:** O limite de caracteres para o QR Code de Texto Simples é de aproximadamente 2953 bytes (UTF-8).
