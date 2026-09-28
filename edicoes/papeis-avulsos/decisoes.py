"""Papéis Avulsos — decisões editoriais sobre o texto estabelecido.

EMENDAS: (tipo, busca, troca) na grafia do texto-base.
  'erro' — erro evidente do impresso de 1882 (conferido no fac-símile) ou das transcrições;
  'ocr'  — erro só da transcrição do Gutenberg (o impresso traz a forma certa).
As lições de 1882 que fazem sentido ficam, ainda que as edições modernas as emendem.
"""

EMENDAS = [
    ('erro', 'chronistas de tempo', 'chronistas do tempo'),
    ('erro', 'anterior; o D. Evarista', 'anterior; e D. Evarista'),
    ('erro', 'no dia em Simão Bacamarte', 'no dia em que Simão Bacamarte'),
    ('erro', 'um pouco a effeito', 'um pouco o effeito'),
    ('erro', 'mandaria declarar Sua', 'mandaria declarar a Sua'),
    ('erro', 'boca, cheio do', 'boca, cheio de'),
    ('erro', 'estala com uma palmada', 'estala como uma palmada'),
    ('erro', 'para os olhos, mais muito', 'para os olhos, mas muito'),
    ('erro', 'pela jardim', 'pelo jardim'),
    ('erro', 'uma uma noute', 'uma noute'),
    ('erro', 'repetiu que a almoço', 'repetiu que o almoço'),
    ('erro', 'subia es escadas', 'subia as escadas'),
    ('erro', 'redarguiu a mão', 'redarguiu a mãe'),
    ('erro', 'nomeada de grande', 'nomeada de grandes'),
    ("erro", "fructo d'esse experiencia", "fructo d'essa experiencia"),
    ('erro', 'foi sempre mesma coisa', 'foi sempre a mesma coisa'),
    ('erro', 'O ultimo foi primeiro', 'O ultimo foi o primeiro'),
    ('erro', 'Cá voou', 'Cá vou'),
    ('erro', 'sentiu toda força', 'sentiu toda a força'),
    ('erro', 'continuo do eternidade', 'continuo da eternidade'),
    ('erro', 'todos as santos', 'todos os santos'),
    ('erro', 'Não venha restaurá-la', 'Não venho restaurá-la'),
    ('erro', 'acariciva-as', 'acariciava-as'),
    ('erro', 'peitaram-se as vistas', 'peitaram-se as visitas'),
    ('erro', 'todos os do capital', 'todos os da capital'),
    ('erro', 'secreção do braço', 'secreção do baço'),
    ('erro', 'cuja filho era', 'cujo filho era'),
    # só do Gutenberg
    ('ocr', 'Okam', 'Cham'),
    ('ocr', 'triumpliante', 'triumphante'),
    ('ocr', 'salvação da Itaguahy', 'salvação de Itaguahy'),
    ('ocr', 'quinze. ¶ V ¶ Quero', 'quinze. ¶ A ¶ Quero'),
]

AJUSTES = []

MANUAL = {
    'Japhet': 'Jafé',
    'Cham': 'Cam',
    'cincoenta': 'cinquenta',
    'escripto': 'escrito',
    'Noticias': 'Notícias',
    'emphasis': 'ênfase',
}

# versos citados na nota a «O Anel de Polícrates», em quadras
VERSOS = {
    '«Sabes tu de um poeta enorme, Que andar não usa No chão, e cuja estranha musa, Que nunca dorme,':
        ['«Sabes tu de um poeta enorme,', 'Que andar não usa', 'No chão, e cuja estranha musa,', 'Que nunca dorme,'],
    '«Calça o pé melindroso e leve, Como uma pluma, De folha e flor, de sol e neve, Cristal e espuma;':
        ['«Calça o pé melindroso e leve,', 'Como uma pluma,', 'De folha e flor, de sol e neve,', 'Cristal e espuma;'],
    '«E mergulha, como Leandro, A forma rara No Pó, no Sena, em Guanabara, E no Escamandro;':
        ['«E mergulha, como Leandro,', 'A forma rara', 'No Pó, no Sena, em Guanabara,', 'E no Escamandro;'],
    '«Ouve a Tupã e escuta a Momo, Sem controvérsia, E tanto adora o estudo, como Adora a inércia;':
        ['«Ouve a Tupã e escuta a Momo,', 'Sem controvérsia,', 'E tanto adora o estudo, como', 'Adora a inércia;'],
    '«Ora do fuste, ora da ogiva Sair parece; Ora o Deus do ocidente esquece Pelo deus Siva;':
        ['«Ora do fuste, ora da ogiva', 'Sair parece;', 'Ora o Deus do ocidente esquece', 'Pelo deus Siva;'],
    '«Gosta do estrépito infinito, Gosta das longas Solidões em que se ouve o grito Das arapongas;':
        ['«Gosta do estrépito infinito,', 'Gosta das longas', 'Solidões em que se ouve o grito', 'Das arapongas;'],
    '«E se ama o rápido besouro, Que zumbe, zumbe, E a mariposa que sucumbe Na flama de ouro,':
        ['«E se ama o rápido besouro,', 'Que zumbe, zumbe,', 'E a mariposa que sucumbe', 'Na flama de ouro,'],
    '«Vaga-lumes e borboletas Da cor da chama, Roxas, brancas, rajadas, pretas, Não menos ama':
        ['«Vaga-lumes e borboletas', 'Da cor da chama,', 'Roxas, brancas, rajadas, pretas,', 'Não menos ama'],
    '«Os hipopótamos tranquilos, E os elefantes, E mais os búfalos nadantes, E os crocodilos,':
        ['«Os hipopótamos tranquilos,', 'E os elefantes,', 'E mais os búfalos nadantes,', 'E os crocodilos,'],
    '«Como as girafas e as panteras, Onças, condores, Toda a casta de bestas-feras E voadores.':
        ['«Como as girafas e as panteras,', 'Onças, condores,', 'Toda a casta de bestas-feras', 'E voadores.'],
    '«Se não sabes quem ele seja, Trepa de um salto, Azul acima, onde mais alto A águia negreja;':
        ['«Se não sabes quem ele seja,', 'Trepa de um salto,', 'Azul acima, onde mais alto', 'A águia negreja;'],
    '«Onde morre o clamor iníquo Dos violentos; Onde não chega o riso oblíquo Dos fraudulentos.':
        ['«Onde morre o clamor iníquo', 'Dos violentos;', 'Onde não chega o riso oblíquo', 'Dos fraudulentos.'],
    '«Então olha, de cima posto, Para o oceano; Verás num longo rosto humano Teu mesmo rosto;':
        ['«Então olha, de cima posto,', 'Para o oceano;', 'Verás num longo rosto humano', 'Teu mesmo rosto;'],
    '«E hás de rir, não do riso antigo, Potente e largo, Riso de eterno moço amigo; Mas de outro amargo,':
        ['«E hás de rir, não do riso antigo,', 'Potente e largo,', 'Riso de eterno moço amigo;', 'Mas de outro amargo,'],
    '«Como o riso de um deus enfermo, Que se aborrece Da divindade, e que apetece Também um termo...':
        ['«Como o riso de um deus enfermo,', 'Que se aborrece', 'Da divindade, e que apetece', 'Também um termo...'],
}
# títulos de capítulo em caixa-alta no impresso: forma de frase
TITULOS = {
    'De Como Itaguaí Ganhou Uma Casa De Orates': 'De como Itaguaí ganhou uma casa de orates',
    'TORRENTE De Loucos': 'Torrente de loucos',
    'Deus Sabe O Que Faz!': 'Deus sabe o que faz!',
    'Uma Teoria Nova': 'Uma teoria nova',
    'O Terror': 'O terror',
    'A Rebelião': 'A rebelião',
    'O Inesperado': 'O inesperado',
    'As Angústias Do Boticário': 'As angústias do boticário',
    'Dois Lindos Casos': 'Dois lindos casos',
    'A Restauração': 'A restauração',
    'O Assombro De Itaguaí': 'O assombro de Itaguaí',
    'O Final Do § 4.º': 'O final do § 4.º',
    'Plus Ultra!': 'Plus ultra!',
}
