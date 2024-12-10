from homeassistant.helpers.typing import ConfigType
from homeassistant.core import HomeAssistant
import logging

import os
from flask import Flask, jsonify
from flask_cors import CORS

app = None
DOMAIN = "ha_draw_persistence"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
UPLOAD_FOLDER = '/homeassistant/www'

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up File Upload."""
    _LOGGER = logging.getLogger("ha_draw_persistence")
    _LOGGER.info("File Upload view registered")
    _LOGGER.critical(allowed_file("tldraw.json"))
    app = Flask(__name__)
    CORS(app)
    app.run(host='0.0.0.0', port=5000, debug=False)
    return True


def allowed_file(filename):
    """
    Check if the file extension is allowed.

    :param filename: Name of the file to check
    :return: Boolean indicating if file is allowed
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/list-files', methods=['GET'])
def list_files():
    """
    List all uploaded files.

    :return: JSON response with list of files
    """
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
