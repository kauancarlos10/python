from models import Jogador, db


def popular_dados():
    if Jogador.query.count() > 0:
        return

    jogadores = [
        # Goleiros
        Jogador(nome="Alisson", posicao="Goleiro", clube="Liverpool", cabeceio=5, forca=7),
        Jogador(nome="Ederson", posicao="Goleiro", clube="Fenerbahçe", cabeceio=5, forca=7),
        Jogador(nome="Weverton", posicao="Goleiro", clube="Grêmio", cabeceio=5, forca=6),
        # Defensores
        Jogador(nome="Alex Sandro", posicao="Defensor", clube="Flamengo", cabeceio=7, forca=7),
        Jogador(nome="Bremer", posicao="Defensor", clube="Juventus", cabeceio=9, forca=9),
        Jogador(nome="Danilo", posicao="Defensor", clube="Flamengo", cabeceio=7, forca=8),
        Jogador(nome="Douglas Santos", posicao="Defensor", clube="Zenit", cabeceio=6, forca=7),
        Jogador(nome="Gabriel Magalhães", posicao="Defensor", clube="Arsenal", cabeceio=9, forca=8),
        Jogador(nome="Ibañez", posicao="Defensor", clube="Al-Ahli", cabeceio=8, forca=8),
        Jogador(nome="Léo Pereira", posicao="Defensor", clube="Flamengo", cabeceio=8, forca=8),
        Jogador(nome="Marquinhos", posicao="Defensor", clube="PSG", cabeceio=9, forca=9),
        # Meio-campistas
        Jogador(nome="Bruno Guimarães", posicao="Meio-campista", clube="Newcastle", cabeceio=7, forca=8),
        Jogador(nome="Casemiro", posicao="Meio-campista", clube="Manchester United", cabeceio=8, forca=10),
        Jogador(nome="Danilo Santos", posicao="Meio-campista", clube="Botafogo", cabeceio=7, forca=7),
        Jogador(nome="Éderson", posicao="Meio-campista", clube="Atalanta", cabeceio=6, forca=8),
        Jogador(nome="Fabinho", posicao="Meio-campista", clube="Al-Ittihad", cabeceio=7, forca=9),
        Jogador(nome="Lucas Paquetá", posicao="Meio-campista", clube="Flamengo", cabeceio=6, forca=7),
        # Atacantes
        Jogador(nome="Endrick", posicao="Atacante", clube="Lyon", cabeceio=7, forca=8),
        Jogador(nome="Gabriel Martinelli", posicao="Atacante", clube="Arsenal", cabeceio=7, forca=8),
        Jogador(nome="Igor Thiago", posicao="Atacante", clube="Brentford", cabeceio=8, forca=8),
        Jogador(nome="Luiz Henrique", posicao="Atacante", clube="Zenit", cabeceio=6, forca=7),
        Jogador(nome="Matheus Cunha", posicao="Atacante", clube="Manchester United", cabeceio=7, forca=8),
        Jogador(nome="Neymar", posicao="Atacante", clube="Santos", cabeceio=7, forca=9),
        Jogador(nome="Raphinha", posicao="Atacante", clube="Barcelona", cabeceio=8, forca=9),
        Jogador(nome="Rayan", posicao="Atacante", clube="Bournemouth", cabeceio=6, forca=7),
        Jogador(nome="Vinícius Júnior", posicao="Atacante", clube="Real Madrid", cabeceio=6, forca=9),
    ]

    db.session.add_all(jogadores)
    db.session.commit()
