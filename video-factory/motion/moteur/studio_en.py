"""Version anglaise (marché US) du corps commun de studio.py : textes affichés + prix en dollars.
Appeler anglais() en tête de scenes.py, après `from studio import *`."""
import studio

TR_EN = {
    "AUJOURD'HUI,": "TODAY,", "Un produit": "A product", "Un service": "A service", "Ton message": "Your message",
    "À LA PAGE": "KEEP UP", "CAPTIVÉ": "HOOKED", "Il regarde": "Watches", "Il comprend": "Gets it", "Il agit": "Acts",
    "Réserver": "Book now", "Ton activité": "Your business", "En direct": "Live", "Demandes": "Inquiries",
    "Clients": "Customers", "Nouvelle demande": "New inquiry", "Nouveau client": "New customer", "à l'instant": "just now",
    "Devis": "Quote", "Conception": "Design", "Pose": "Install", "Sur ton site": "On your website", "· cuisines": "· kitchens",
    "Votre cuisine,": "Your kitchen,", "sur mesure.": "made to measure.", "cuisines-morel.fr": "morelkitchens.com",
    "Clair": "Clear", "3 OU 4": "3 OR 4", "ACCROCHES": "HOOKS", "À tester": "Test them", "3–4 accroches": "3–4 hooks",
    "Script inclus": "Script included", "Ton offre, en mouvement.": "Your offer, in motion.",
    "Demander mon devis": "Get my quote", "dès 290 € TTC": "from $299", "À PARTIR DE": "FROM",
    "Titre": "Title", "Formes": "Shapes", "Texte": "Text", "Son": "Sound",
    "Le problème": "The problem", "Tes clients ne comprennent pas ?": "Customers don't get it?",
    "Le bénéfice": "The benefit", "Compris en quelques secondes.": "Clear in seconds.",
    "La curiosité": "Curiosity", "Ton meilleur vendeur ?": "Your best salesperson?",
    "La solution": "The solution", "Montre. Donne envie.": "Show it. Make them want it.",
}


def anglais(prix=True):
    studio.TR.update(TR_EN)
    studio.PRIX.update(chiffres="299", devise="$", avant=True, mention=None)
    if not prix:
        studio.TR["dès 290 € TTC"] = "2nd format free"
