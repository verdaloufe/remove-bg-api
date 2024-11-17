from flask import Flask, request, send_file
from rembg import remove
from PIL import Image
import io

app = Flask(__name__)

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    # Vérifier si un fichier a été envoyé
    if 'image' not in request.files:
        return {"error": "Aucune image n'a été envoyée"}, 400

    # Récupérer le fichier envoyé
    file = request.files['image']

    try:
        # Lire l'image et supprimer le fond
        input_image = file.read()
        output_image = remove(input_image)

        # Convertir en format compatible pour envoi
        output_stream = io.BytesIO(output_image)
        output_stream.seek(0)

        return send_file(
            output_stream,
            mimetype='image/png',
            as_attachment=True,
            download_name='image_sans_fond.png'
        )

    except Exception as e:
        return {"error": f"Une erreur est survenue : {str(e)}"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
