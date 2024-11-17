from flask import Flask, request, send_file
from rembg import remove
import io

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    # Vérifie si une image a été envoyée
    if 'image' not in request.files:
        return {"error": "Aucune image n'a été envoyée. Veuillez inclure une image dans le champ 'image'."}, 400

    file = request.files['image']

    try:
        # Lire le fichier image
        input_image = file.read()

        # Supprimer le fond
        output_image = remove(input_image)

        # Préparer l'image pour la réponse
        output_stream = io.BytesIO(output_image)
        output_stream.seek(0)

        # Retourner l'image sans fond
        return send_file(
            output_stream,
            mimetype='image/png',
            as_attachment=True,
            download_name='image_sans_fond.png'
        )

    except Exception as e:
        # Gérer les erreurs éventuelles
        return {"error": f"Une erreur est survenue : {str(e)}"}, 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Utilise le port de Render ou 5000 par défaut
    app.run(host='0.0.0.0', port=port)
