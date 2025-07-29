"""Connectives features.
"""
from cohmetrixBR.utils import ModelPool

pool = ModelPool()


def CNCAll(text: str):
    """
    Incidência de conjunções (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções no text)
    """
    doc = pool.nlp(text)

    conj_count = 0
    for token in doc:
        if token.pos_ == "CCONJ":
            conj_count += 1

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCCaus(text: str):
    """
    Incidência de conjunções causais (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_causal_count -> inteiro (quantidade de conjunções conectivas no text)
    """

    text = text.lower()
    conj_causal_list = [" porque ", " pois ", " porquanto ", " pois que ", " que ",
                        " pois que ", " por isso que ", " a que ", " uma vez que ",
                        " visto que ", " visto como "]

    conj_count = 0
    for conj_causal in conj_causal_list:
        count = text.count(conj_causal)
        conj_count += count
        # print(conj_causal,count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCADC(text: str):
    """
    Incidência de conjunções adversativas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_adversa_count -> inteiro (quantidade de conjunções adversativas no text)
    """

    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" contudo ", " entretanto ", " mas ", " embora ",
                 " nao obstante ", " no entanto ", " porem ", " todavia "]

    conj_count = 0
    for conj in conj_list:
        conj_count += text.count(conj)
        # print(conj,conj_count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCTemp(text: str):
    """
    Incidência de conjunções temporais (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_temp_count -> inteiro (quantidade de conjunções temporais no text)
    """

    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" quando ", " antes que ", " depois que ", " ate que ",
                 " logo que ", " sempre que ", " assim que ", " desde que ",
                 " todas as vezes que ", " cada vez que "]

    conj_count = 0
    for conj in conj_list:
        conj_count += text.count(conj)
        # print(conj,conj_count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCAdd(text: str):
    """
    Incidência de conjunções aditivas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_aditiva_count -> inteiro (quantidade de conjunções aditivas no text)
    """

    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" e ", " mas ainda ", " mas tambem ", " nem ", " tambem "]

    conj_count = 0
    for conj in conj_list:
        conj_count += text.count(conj)
        # print(conj,conj_count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCAlter(text: str):
    """
    Incidência de conjunções alternativas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """

    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" ja ", " ou ", " ora ", " quer "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count
        # print(conj_,count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCConclu(text: str):
    """
    Incidência de conjunções conclusivas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" assim ", " entao ", " logo ", " pois ",
                 " por conseguinte ", " por isso ", " portanto "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCExpli(text: str):
    """
    Incidência de conjunções explicativas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" pois ", " porquanto ", " porque ", " que "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count
        # print(conj_,count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCConce(text: str):
    """
    Incidência de conjunções concessiva (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" embora ", " conquanto ", " contanto ", " ainda que ",
                 " mesmo que ", " posto que ", " bem que ", " se bem que ",
                 " apesar de que ", " nem que ", " que "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count
        # print(conj_,count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCCondi(text: str):
    """
    Incidência de conjunções condicional (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """

    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" se ", " caso ", " quando ", " conquanto ", " contanto ",
                 " salvo se ", " sem que ", " dado que ", " desde que ",
                 " a menos que ", " a nao ser que "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count
        # print(conj_,count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCLogic(text: str):
    """
    Incidência de conjunções lógicas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """

    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" se ", " e ", " ou ", " implica ",
                 " entao ", " nao ", " somente "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count
        # print(conj_,count)

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCPos(text: str):
    """
    Incidência de conjunções positivas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """

    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" consequentemente ", " que ", " dado ", " de ", " por ",
                 " consequencia ", " conseguinte ", " resultado ", " isso ",
                 " por ", " causa ", " virtude ", " asim ", " fato ", " efeito ", " tao ",
                 " porque ", " porquanto ", " pois ", " visto ", " portanto ", " logo ",
                 " sorte ", " forma ", " haja ", " vista ", " entao ", " enfim ",
                 " logo ", " depois ", " principio ", " anteriormente ", " posteriormente ",
                 " seguida ", " final ", " finalmente ", " atualmente ", " fequentemente ",
                 " constantemente ", " eventualmente ", " ocasionalmente ", " sempre ",
                 " simultanemanete ", " interim ", " hiato ", " enquanto ", " quando ",
                 " antes ", " depois ", " logo ", " sempre ", " assim ", " desde ",
                 " todas ", " cada ", " ja ", " bem ", " ate ", " e ", " ou ", " se ", " entao ",
                 " somente ", " modo ", " alem ", " disso ", " demais ", " ademais ", " outrossim ", " ainda ",
                 " mais ", "tambem ", " so ", " como ", " bem ", " como ", " com ", " e/ou "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCNeg(text: str):
    """
    Incidência de conjunções negativas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" ja ", " raramente ", " raro ", " nao ", " apenas ", " mal ", " entretanto ", " todavia ",
                 " contudo ",
                 " entanto ", " nem ", " mas ", " apenas ", " porem "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCConfor(text: str):
    """
    Incidência de conjunções conformativas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" conforme ", " como ", " segundo ",
                 " consoante ", " tendo em vista "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCFinal(text: str):
    """
    Incidência de conjunções finais (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" para que ", " a fim de que ", " porque ", " que "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCProp(text: str):
    """
    Incidência de conjunções proporcionais (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" a medida que ", " ao passo que ", " a proporcao que ",
                 " enquanto ", " quanto mais ", " quanto menos "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCComp(text: str):
    """
    Incidência de conjunções comparativas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" que ", " do que ", " qual "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCConse(text: str):
    """
    Incidência de conjunções consecutivas (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" de modo que ", " de maneira que ", " que "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


def CNCInte(text: str):
    """
    Incidência de conjunções integrantes (conectivos).
    @:parameter: text -> text em português
    @:returns: conj_count -> inteiro (quantidade de conjunções conectivas no text)
    """
    text = pool.pre_processing_keep_stopword_token(text.lower())
    conj_list = [" se ", " que "]

    conj_count = 0
    for conj_ in conj_list:
        count = text.count(conj_)
        conj_count += count

    size = len(text.split())
    quociente = size // 1000
    resto = size % 1000

    if resto == 0:
        return conj_count / quociente
    else:
        return conj_count / (1 + quociente)


FEATURES = [
    CNCADC,
    CNCAdd,
    CNCAll,
    CNCAlter,
    CNCCaus,
    CNCComp,
    CNCConce,
    CNCConclu,
    CNCCondi,
    CNCConfor,
    CNCConse,
    CNCExpli,
    CNCFinal,
    CNCInte,
    CNCLogic,
    CNCNeg,
    CNCPos,
    CNCProp,
    CNCTemp
]
