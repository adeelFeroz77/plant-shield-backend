import io
from flask import jsonify, send_file
from app import app
from app.models import *
from app.static import *

@app.route('/get-image/<int:image_id>',methods=['GET'])
def get_image(image_id):
    image = Image.query.filter_by(id=image_id).first()
    if not image:
        return jsonify({'error':'Image not found'}), 404
    return send_file(io.BytesIO(image.data),
                             mimetype=f'image/{image.image_extension}',
                             as_attachment=True,
                             download_name=f"{image.image_name}.{image.image_extension}")