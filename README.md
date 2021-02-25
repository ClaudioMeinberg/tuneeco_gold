# tuneeco Feed Server

Gerenciador de feed e download de vídeos do youtube desenvolvido para integração com o Terra.


## Instalação
Vide INSTALL.md


### SSO

Inserir chave e secret oAuth2 no arquivo de configurações .env

Acessar o site e tentar login, o usuário não terá permissões.

Acessar o admin do django e definir como membro da equipe.
http://127.0.0.1:8000/admin/authenticator/user/


## URLs

- Django Admin: http://127.0.0.1:8000/admin

- Gerenciador de Feed: http://127.0.0.1:8000/videos

- Feed: http://127.0.0.1:8000/terra/marcioatalla/feed/video


## Produção
O documento SERVER.md contém informações para publicação de ambiente em produção em servidores debian-based