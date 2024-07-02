from typing import Union


class CalculateRisk:
    @staticmethod
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
    ) -> Union[int, str]:
        """Calculate the risk score for an individual based on various financial and property factors.

        This function calculates a risk score based on input parameters related to the individual's financial situation
        and the property they intend to purchase. Factors such as income, existing debts, loan amount, property type,
        renovation costs, and future plans are taken into account to determine the risk score.

        Args:
            situation_pro (str): Professional situation of the individual.
            achat_immobilier (str): Intention of buying property.
            revenu_mensuel (int): Monthly income of the individual.
            revenus_supplementaires (str): Whether there are additional income sources.
            montant_revenus_supplementaires (str): Amount of additional income.
            deja_proprietaire (str): Whether the individual already owns property.
            antecedents_credit (str): Whether there is a credit history.
            dettes_en_cours (str): Whether there are current debts.
            capital_disponible (int): Available capital for down payment.
            montant_pret (int): Loan amount requested.
            duree_remboursement (str): Duration of the loan repayment.
            budget_mensuel (str): Monthly budget for expenses.
            epargne_mensuelle (int): Monthly savings amount.
            prix_achat (int): Property purchase price.
            type_bien (str): Type of property (new or old).
            frais_copropriete (str): Condominium fees.
            couts_renovation (int): Renovation costs.
            taxes_foncieres (int): Property taxes.
            rester_longtemps (str): Intention to stay long-term.
            projets_revente (str): Plans for property resale.
            utilisation_bien (str): Intended use of the property.

        Returns:
            int: Risk score indicating the level of risk associated with the property purchase decision.
        """

        risque = 0

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

        try:
            duree_remboursement_annees = int(
                "".join(filter(str.isdigit, duree_remboursement))
            )
        except ValueError:
            return "Erreur: Durée de remboursement non valide."

        if situation_pro == "CDD":
            risque += 10
        if achat_immobilier == "Seul":
            risque += 5
        if revenu_mensuel < 2000:
            risque += 10
        if int(montant_revenus_supplementaires) <= 0:
            risque = +5
        if dettes_en_cours == "***Oui***":
            risque += 10
        if revenus_supplementaires == "***Non***":
            risque += 5

        if int(montant_pret) > (revenu_mensuel * 12 * duree_remboursement_annees):
            risque += 15

        if int(budget_mensuel) > (0.7 * revenu_mensuel):
            risque += 10

        if deja_proprietaire == "***Non***":
            risque += 5
        if antecedents_credit == "***Oui***":
            risque += 5

        if type_bien == "***Ancien***":
            risque += 5
        if int(frais_copropriete) >= (0.02 * revenu_mensuel):
            risque += 5
        if epargne_mensuelle < 500:
            risque += 5
        if capital_disponible < (0.2 * prix_achat):
            risque += 10

        if couts_renovation > 0:
            risque += 5
        if taxes_foncieres > 1000:
            risque += 5

        if rester_longtemps == "***Non***" or projets_revente == "***Oui***":
            risque += 5

        return risque

    @staticmethod
    def classer_risque(score) -> str:
        """Returns the risk associated with the score obtained

        Args:
            score (int): computed score from the function above

        Returns:
            str: takes 3 different values depending on the risk
        """
        if score <= 20:
            return "Parfait"
        elif 21 <= score <= 40:
            return "Peu risqué"
        else:
            return "Risqué"
