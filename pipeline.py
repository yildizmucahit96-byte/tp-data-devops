"""Pipeline de données : extraire -> transformer -> charger."""

from pathlib import Path

import pandas as pd

ENTREE = Path("data/ventes.csv")
SORTIE = Path("output")


def extraire(chemin):
    """Lit le fichier CSV brut."""
    return pd.read_csv(chemin)


def transformer(df):
    """Nettoie les données et calcule le montant de chaque vente."""
    df = df.drop_duplicates()
    df = df.dropna(subset=["quantite", "prix_unitaire"])
    df = df[df["quantite"] > 0].copy()
    df["ville"] = df["ville"].str.strip().str.title()
    df["montant"] = df["quantite"] * df["prix_unitaire"]
    return df


def agreger_par_ville(df):
    """Calcule le chiffre d'affaires total par ville."""
    resultat = df.groupby("ville", as_index=False)["montant"].sum()
    return resultat.sort_values("montant", ascending=False)


def agreger_par_categorie(df):
    """Calcule le chiffre d'affaires total par catégorie."""
    resultat = df.groupby("categorie", as_index=False)["montant"].sum()
    return resultat.sort_values("montant", ascending=False)


def charger(df, chemin):
    """Écrit un DataFrame dans un fichier CSV."""
    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(chemin, index=False)


def main():
    brut = extraire(ENTREE)
    propre = transformer(brut)
    par_ville = agreger_par_ville(propre)
    par_categorie = agreger_par_categorie(propre)

    charger(propre, SORTIE / "ventes_propres.csv")
    charger(par_ville, SORTIE / "ca_par_ville.csv")
    charger(par_categorie, SORTIE / "ca_par_categorie.csv")

    print(f"{len(brut)} lignes lues, {len(propre)} lignes gardées.")
    print(par_ville.to_string(index=False))
    print(par_categorie.to_string(index=False))


if __name__ == "__main__":
    main()