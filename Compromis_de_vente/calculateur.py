# Calcul de risque


def calculer_risque(
    situation_pro,
    achat_immobilier,
    revenu_mensuel,
    revenus_supplementaires,
    montant_revenus_supplementaires,
    deja_proprietaire,
    antecedents_credit,
    dettes_en_cours,
    capital_disponible,
    montant_pret,
    duree_remboursement,
    budget_mensuel,
    epargne_mensuelle,
    prix_achat,
    type_bien,
    frais_copropriete,
    couts_renovation,
    taxes_foncieres,
    rester_longtemps,
    projets_revente,
    utilisation_bien,
):
    # Exemple simplifié de calcul de risque basé sur des règles
    risque = 0

    # Nettoyer et valider les entrées
    try:
        revenu_mensuel = int(revenu_mensuel)
        montant_pret = int(montant_pret)
        epargne_mensuelle = int(epargne_mensuelle)
        capital_disponible = int(capital_disponible)
        prix_achat = int(prix_achat)
        couts_renovation = int(couts_renovation)
        taxes_foncieres = int(taxes_foncieres)
    except ValueError:
        return "Erreur: Veuillez entrer des valeurs numériques valides pour les montants financiers."

    # Extraire la durée en années
    try:
        duree_remboursement_annees = int(
            "".join(filter(str.isdigit, duree_remboursement))
        )
    except ValueError:
        return "Erreur: Durée de remboursement non valide."

    # Facteurs de risque basés sur les revenus et les dettes
    if revenu_mensuel < 2000:
        risque += 10
    if dettes_en_cours == "***Oui***":
        risque += 10
    if revenus_supplementaires == "***Non***":
        risque += 5

    # Facteurs de risque basés sur le prêt et la capacité de remboursement
    if montant_pret > (revenu_mensuel * 12 * duree_remboursement_annees):
        risque += 15

    # Facteurs de risque basés sur l'expérience et l'historique
    if deja_proprietaire == "***Non***":
        risque += 5
    if antecedents_credit == "***Oui***":
        risque += 5

    # Facteurs de risque basés sur le type de bien et sa localisation
    if type_bien == "***Ancien***":
        risque += 5

    # Facteurs de risque basés sur la capacité d'épargne et l'apport initial
    if epargne_mensuelle < 500:
        risque += 5
    if capital_disponible < (0.2 * prix_achat):
        risque += 10

    # Facteurs de risque basés sur les coûts supplémentaires
    if couts_renovation > 0:
        risque += 5
    if taxes_foncieres > 1000:
        risque += 5

    # Ajuster le risque selon la durée de séjour prévue
    if rester_longtemps == "***Non***" or projets_revente == "***Oui***":
        risque += 5

    return risque


def classer_risque(score):
    if score <= 20:
        return "Parfait"
    elif 21 <= score <= 40:
        return "Peu risqué"
    else:
        return "Risqué"
