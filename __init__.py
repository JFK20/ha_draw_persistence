from homeassistant.helpers.http import HomeAssistantView
from homeassistant.helpers.typing import ConfigType
from homeassistant.core import HomeAssistant

DOMAIN = "ha_draw_persistence"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up File Upload."""
    hass.http.register_view(FileUploadView)
    return True


def allowed_file(filename):
    """
    Check if the file extension is allowed.

    :param filename: Name of the file to check
    :return: Boolean indicating if file is allowed
    """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class FileUploadView(HomeAssistantView):
    """HTTP View to upload files."""

    url = "/api/file_upload"
    name = "api:file_upload"

    print("FileUploadView")

    print(allowed_file("tldraw.json"))