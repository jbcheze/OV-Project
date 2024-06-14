import streamlit as st


st.set_page_config(page_title="OV-simulateur", page_icon=":house:")

st.title("Bienvenue !")


with st.sidebar:

    img_path = "images/logo_ov2.png"
    st.image(img_path, use_column_width=True)

    if st.button("Home"):
        st.switch_page("main.py")


with st.container(border=True):
    st.header(
        "Les questions à potentiellement mettre plus tard dans notre simulateur : "
    )
    st.write(
        """
             
             Informations Personnelles et Financières
Situation professionnelle et revenus

Quelle est votre situation professionnelle actuelle ? (CDI, CDD, indépendant, etc.)
Quel est votre revenu mensuel net ?
Avez-vous des revenus supplémentaires ? Si oui, de quel montant ?
Historique financier

Avez-vous déjà été propriétaire d'un bien immobilier ?
Avez-vous des antécédents de crédit (prêts remboursés ou en cours) ?
Avez-vous des dettes en cours ? Si oui, de quel montant ?
Capacité d'emprunt et apport personnel

Combien de capital avez-vous disponible pour l'apport initial ?
Quel est le montant du prêt que vous envisagez de demander ?
Quelle est la durée de remboursement souhaitée pour votre prêt immobilier ?
Dépenses et épargne

Quel est votre budget mensuel actuel (loyer, dépenses courantes, etc.) ?
Combien épargnez-vous en moyenne par mois ?
Informations sur le Bien Immobilier
Caractéristiques du bien

Où se situe le bien immobilier (ville, quartier) ?
Quelle est la superficie du bien ?
Quel est le prix d'achat du bien immobilier ?
Le bien est-il neuf ou ancien ?
Charges et frais supplémentaires

Quels sont les frais de notaire associés à cet achat ?
Quels sont les frais de copropriété (le cas échéant) ?
Quels sont les coûts estimés de rénovation ou de réparation du bien (si nécessaire) ?
Quels sont les coûts annuels de taxes foncières ?
Potentiel de valorisation

Quelle est la tendance actuelle du marché immobilier dans la région ?
Y a-t-il des projets de développement ou d'infrastructure à proximité qui pourraient affecter la valeur du bien ?
Risques liés à l'achat
Stabilité de l'emploi

Votre emploi est-il stable ? Y a-t-il des risques de perte d'emploi ou de baisse de revenu ?
Taux d'intérêt

Quel est le taux d'intérêt actuel pour les prêts immobiliers ?
Êtes-vous préparé à une possible augmentation des taux d'intérêt ?
Impact financier

Quelle part de vos revenus mensuels sera consacrée au remboursement du prêt immobilier ?
Avez-vous une marge financière suffisante pour faire face à des imprévus ?
Risques du marché immobilier

Le marché immobilier local est-il sujet à des fluctuations importantes ?
Y a-t-il des signes de surévaluation du marché immobilier dans la région choisie ?
Questions sur les Préférences Personnelles
Projet de vie

Envisagez-vous de rester longtemps dans cette propriété ?
Avez-vous des projets de revente à court ou moyen terme ?
Souhaitez-vous utiliser ce bien comme résidence principale, secondaire, ou pour un investissement locatif ?
Critères personnels

Quelles sont les caractéristiques essentielles pour vous dans un bien immobilier (nombre de chambres, jardin, proximité des commodités, etc.) ?
Êtes-vous prêt à faire des compromis sur certains critères pour rester dans votre budget ?
             
             """
    )
