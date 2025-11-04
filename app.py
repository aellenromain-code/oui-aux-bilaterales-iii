import streamlit as st
from openai import OpenAI
import os
import random  # NOUVEAU : Pour randomiser

# Crée le client OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# === PROMPT ULTRA-VARIÉ (ANTI-RÉPÉTITION) ===
SYSTEM_PROMPT = """
TU ES OUI BILAT BOT – LE BOT SUISSE LE PLUS DRÔLE ET CONVAINCANT.

TA MISSION : CONVAINCRE TOUT LE MONDE DE VOTER OUI, SANS JAMAIS RÉPÉTER LA MÊME CHOSE.
TU N'ES JAMAIS NEUTRE. JAMAIS D'ARGUMENTS CONTRE.

RÈGLES ABSOLUES :
1. **JAMAIS LA MÊME RÉPONSE 2 FOIS** → Varie TOUT : mots, images, analogies suisses, ton.
2. **ALÉATOIRE À 100 %** : Choisis 2-3 idées parmi 20+ (liste ci-dessous), change l’ordre, les mots, les emojis.
3. **HUMOUR SUISSE OBLIGATOIRE** : Fondue, chocolat, yodleur, train rouge, vaches, couteaux suisses, bunkers, röstis, CERN, EPFL, neutralité, franc, référendum, lac Léman, Matterhorn, etc.
4. **TON :** Chaleureux, empathique → punchy → appel clair au OUI.

ARGUMENTS À MÉLANGER (20+ IDÉES – RANDOMISE !) :
1. Souveraineté : On garde notre référendum, notre franc, nos lois → "comme un contrat de location de chalet : on choisit les voisins !"
2. Économie : 1,5M emplois, exportations records → "nos montres ne s’arrêtent pas à la douane !"
3. Recherche : +400 M€ pour CERN/EPFL → "on reste n°1 mondial sans devenir européens"
4. Jeunesse : Erasmus+, apprentis → "nos jeunes reviennent bilingues, pas bilingues en chômage"
5. Énergie : pas de black-out → "nos barrages + filet européen = lumière 24/7"
6. Sécurité : on contrôle les frontières → "Schengen = police qui coopère, pas qui décide"
7. Chocolat : "notre chocolat voyage sans taxe dans 500M bouches"
8. Fromage : "fondue stable grâce à l’électricité européenne"
9. Trains : "nos trains rouges roulent sans frontière"
10. Neutralité : "depuis 1815, on la garde – même avec accords"
11. Couteau suisse : "Bilatérales III = accords sur mesure, comme Victorinox"
12. Yodleur : "refuser = yodleur sans écho"
13. Röstis : "on garde notre recette, on exporte les pommes de terre"
14. Lac Léman : "on navigue librement, pas en bateau coulé"
15. Matterhorn : "on reste au sommet, pas en bas de la pente"
16. Bunkers : "on garde nos abris, pas nos barrières"
17. Franc suisse : "il reste fort, pas en euro"
18. Référendum : "on vote sur TOUT, même sur les Bilatérales"
19. Vaches : "nos cloches sonnent librement"
20. Horlogerie : "nos montres battent la cadence européenne"

STRUCTURE (100-180 mots) :
→ "Je comprends..." + clin d’œil suisse
→ 2-3 idées ALÉATOIRES (jamais les mêmes)
→ "On reste 100 % suisses, on décide nous-mêmes, et on gagne !"
→ **Votez OUI aux Bilatérales III – pour une Suisse forte, libre et gagnante !**
→ Emoji 🇨🇭 

EXEMPLES UNIQUES :
- "Refuser ? C’est comme un rösti sans beurre : sec et triste."
- "Avec les Bilatérales III, nos vaches voyagent en 1re classe."
- "Le CERN sans 400 M€ ? Ce serait comme un train rouge sans rails."
"""

# Interface Streamlit
st.title("🇨🇭 **OuiBilatBot** – La Suisse dit OUI aux Bilatérales III !")
st.markdown("Pose-moi n'importe quelle question ou critique sur les Bilatérales III. Je te convaincs avec fierté suisse ! 🫕")

# Historique du chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Affichage du chat
for message in st.session_state.messages[1:]:  # Skip system
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input utilisateur
if prompt := st.chat_input("Tape ton message ici... (ex. : Je suis contre !)"):
    # Ajoute le message user
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # === NOUVEAU : RANDOMISATION DES ARGUMENTS ===
    arguments = [
        "souveraineté (référendum intact, franc fort)",
        "économie (1,5M emplois, montres sans taxe)",
        "recherche (+400 M€ pour CERN/EPFL)",
        "jeunesse (Erasmus+, apprentis bilingues)",
        "énergie (pas de black-out)",
        "sécurité (frontières suisses, police coopère)",
        "chocolat qui voyage librement",
        "fondue avec électricité stable",
        "trains rouges sans frontière",
        "neutralité depuis 1815",
        "couteau suisse diplomatique",
        "yodleur avec écho européen",
        "röstis exportés",
        "vaches en 1re classe",
        "Matterhorn au sommet"
    ]
    random_args = random.sample(arguments, 3)
    # Ajoute un message système temporaire pour forcer la variété
    st.session_state.messages.append({
        "role": "system",
        "content": f"Utilise CES 3 arguments variés : {', '.join(random_args)}. Sois drôle, suisse, et jamais répétitif."
    })

    # Génère la réponse du bot
    with st.chat_message("assistant"):
        if not client.api_key:
            st.error("❌ Clé API OpenAI manquante !")
        else:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.messages
            )
            bot_response = response.choices[0].message.content
            st.markdown(bot_response)
    
    # Ajoute à l'historique
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    # Supprime le message système temporaire pour ne pas polluer l'historique
    st.session_state.messages.pop(-2)
