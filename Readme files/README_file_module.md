# 📁 Module de Chiffrement de Fichiers – Membre 3  

Ce module gère le chiffrement et le déchiffrement des fichiers dans le projet.
Il utilise **AES-GCM** (module du Membre 2) pour sécuriser les données.

---

## 🎯 Objectif du module

Le rôle du Membre 3 est :

- Lire un fichier en entrée  
- Le découper en morceaux (chunks)  
- Chiffrer chaque morceau avec AES-GCM  
- Encoder les valeurs en Base64  
- Stocker le contenu chiffré dans un fichier JSON  
- Recharger ensuite ce JSON et déchiffrer tout le fichier  

Ce module permet donc l’envoi sécurisé de fichiers dans la Phase suivante.

---

# 🔐 Fonctions principales

### ✔️ encrypt_file(aes_key, infile_path, chunk_size)
- Lit le fichier en blocs de 1 Mo
- Chiffre chaque bloc via `encrypt_message`
- Retourne une structure :

```json
{
  "filename": "nom du fichier",
  "total_chunks": 1,
  "chunks": [
    {
      "nonce": "...",
      "ciphertext": "...",
      "tag": "..."
    }
  ]
}
