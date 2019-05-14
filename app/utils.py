from app.models import User

'''
    Das Paginator Objekt mit allen relevanten Variablen.
    list: SuperListe aller SubListen (Seiten)
    cur_page: aktuelle Seite (Index + 1 der list)
    max_page: Anzahl der Seiten
    items: list[cur_page-1], also return der aktuellen Seite; 
        Falls der Index out of Range ist -> Erste Seite; Falls die Liste Leer ist, Leere Liste returned
'''
class Paginator:
    def __init__(self, list:list, cur_page:int, max_page:int):
        self.list = list
        self.cur_page = cur_page
        self.max_page = max_page
        try:
            self.items = self.list[self.cur_page-1]
        except IndexError:
            try:
                self.items = self.list[0]
            except IndexError:
                self.items = []

    def __repr__(self):
        return f'List with {self.max_page} pages. Current page is {self.cur_page}.'
    '''
    Die folgenden Klassenfunktionen zeigen einfach an ob eine nächste Seite existiert, und welchen Index diese hat.
    Funktionen werden zur Link Generation verwendet
    '''
    def next_num(self):
        return self.cur_page + 1
    def prev_num(self):
        return self.cur_page - 1
    def has_next(self):
        return not self.cur_page >= self.max_page
    def has_prev(self):
        return not self.cur_page == 1

'''
Funktion zum Erstellen eines Pagination Objektes
Die Objekte der Liste werden in [max] Lange Sublisten gepackt, welche dann an die Superliste angehangen werden
'''
def paginate(list: list, page: int, max: int):
    list = reversed(list)   
    superlist = []
    sublist = []
    i = 0
    p_i = 0

    for entry in list:
        # Objekt wird an Sublist gehangen
        sublist.append(entry)
        i += 1
        # Sobald 5 Objekte in der Subliste sind wird diese an die Superlist appenden, die Subliste und der Iterator wird zurückgesetzt
        # Page_Index wird erhöht
        if i == max:
            superlist.append(sublist)
            sublist = []
            i = 0
            p_i += 1
    # Nach Abschluss des for Loops wird eine teils gefüllte Liste angehängt
    if len(sublist) > 0:
        superlist.append(sublist)
        p_i += 1
    # Paginator Objekt wird returnt
    return Paginator(superlist, page, p_i)

# FUnktion um jedem Post ein Autor Objekt hinzuzufügen; returnt eine Liste von (Post, Autor) Tupeln
def add_author(posts:list):
    matched_posts = []
    for post in posts:
        author = User.query.filter_by(id=post.user_id).first()
        matched_posts.append((post,author))
    return matched_posts
    