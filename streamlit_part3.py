import streamlit as st
import pandas as pd
import os

# Charger les données des utilisateurs
def load_user_data():
    return pd.read_csv("users.csv")

# Mettre à jour les données des utilisateurs
def save_user_data(df):
    df.to_csv("users.csv", index=False)

# Page d'authentification
def login_page(users):
    st.title("Page de Connexion")
    st.sidebar.info("Veuillez vous connecter pour accéder à l'application.")

    # Formulaire de connexion
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")
    if st.button("Se connecter"):
        if username in users['name'].values:
            user_row = users[users['name'] == username]
            if user_row['password'].values[0] == password:
                # Succès de connexion
                users.loc[users['name'] == username, 'logged_in'] = True
                save_user_data(users)
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.success(f"Bienvenue, {username} !")
            else:
                st.warning("Mot de passe incorrect.")
        else:
            st.warning("Nom d'utilisateur introuvable.")

# Page d'accueil
def home_page():
    st.title("Accueil")
    st.write("Bienvenue sur mon application Streamlit !")

# Page album de photos
def photo_album_page():
    st.title("Album de Photos")
    st.write("Voici mes chèvres.")

    # Charger les images
    image_folder = "images"
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]

    # Afficher les images par lignes de 3
    cols = st.columns(3)
    for i, image_file in enumerate(image_files):
        with cols[i % 3]:
            st.image(os.path.join(image_folder, image_file), use_container_width=True)

# Application principale
def main():
    st.sidebar.title("Menu")
    users = load_user_data()

    # Vérifier si l'utilisateur est connecté
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if st.session_state['logged_in']:
        username = st.session_state['username']
        st.sidebar.success(f"Bienvenue {username}!")
        page = st.sidebar.radio("Navigation", ["Accueil", "Album de Photos"])

        if page == "Accueil":
            home_page()
        elif page == "Album de Photos":
            photo_album_page()

        if st.sidebar.button("Déconnexion"):
            users.loc[users['name'] == username, 'logged_in'] = False
            save_user_data(users)
            st.session_state['logged_in'] = False
            st.session_state['username'] = ""
            st.experimental_rerun()
    else:
        login_page(users)

if __name__ == "__main__":
    main()